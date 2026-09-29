import pandas as pd
from pathlib import Path

from App.text_utils import normalize_text

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "Data"
OUTPUT_CSV = DATA_DIR / "Combined_Cleaned.csv"

WELFAKE_CSV = DATA_DIR / "WELFake_Dataset.csv"
WELFAKE_1_IS_FAKE = True

NEW_FAKE_CSV = DATA_DIR / "Fake.csv"
NEW_TRUE_CSV = DATA_DIR / "True.csv"

NEW_SINGLE_CSV = None
NEW_LABEL_COLUMN = "label"
NEW_FAKE_VALUES = ["fake"]

TITLE_COLUMNS = ["title", "headline", "heading"]
TEXT_COLUMNS = ["text", "content", "article", "body", "news", "statement"]

MIN_WORDS = 8


def find_column(df, names, required=True):
    lookup = {c.lower().strip(): c for c in df.columns}
    for name in names:
        if name in lookup:
            return lookup[name]
    if required:
        raise KeyError(f"No matching column found. Columns in file: {list(df.columns)}")
    return None


def make_frame(df, labels, source):
    title_col = find_column(df, TITLE_COLUMNS, required=False)
    text_col = find_column(df, TEXT_COLUMNS)

    if title_col:
        title = df[title_col].map(normalize_text)
    else:
        title = pd.Series("", index=df.index)
    body = df[text_col].map(normalize_text)

    return pd.DataFrame({
        "title": title,
        "content": (title + " " + body).str.strip(),
        "label": labels.astype(int),
        "source": source,
    })


def load_welfake():
    print("Loading WELFake...")
    df = pd.read_csv(WELFAKE_CSV)
    print(f"Original shape: {df.shape}")

    df = df.dropna(subset=["text", "label"]).copy()
    print("Label counts in the file:")
    print(df["label"].value_counts().to_string())

    labels = df["label"].astype(int)
    if not WELFAKE_1_IS_FAKE:
        labels = 1 - labels

    print("\nSample headlines marked FAKE:")
    for t in df.loc[labels == 1, "title"].fillna("").sample(4, random_state=1):
        print("  -", t[:90])
    print("Sample headlines marked REAL:")
    for t in df.loc[labels == 0, "title"].fillna("").sample(4, random_state=1):
        print("  -", t[:90])

    return make_frame(df, labels, "welfake")


def load_new_dataset():
    print("\nLoading new dataset...")

    if NEW_SINGLE_CSV:
        df = pd.read_csv(NEW_SINGLE_CSV)
        print(f"Shape: {df.shape}, columns: {list(df.columns)}")
        label_col = find_column(df, [NEW_LABEL_COLUMN.lower()])
        df = df.dropna(subset=[label_col]).copy()
        values = df[label_col].astype(str).str.strip().str.lower()
        labels = values.isin(NEW_FAKE_VALUES).astype(int)
        print("Label counts (1 = fake):", labels.value_counts().to_dict())
        return make_frame(df, labels, "new_kaggle")

    fake_df = pd.read_csv(NEW_FAKE_CSV)
    true_df = pd.read_csv(NEW_TRUE_CSV)
    print(f"Fake file: {fake_df.shape}, True file: {true_df.shape}")
    print(f"Columns: {list(fake_df.columns)}")

    fake_part = make_frame(fake_df, pd.Series(1, index=fake_df.index), "new_kaggle")
    true_part = make_frame(true_df, pd.Series(0, index=true_df.index), "new_kaggle")
    return pd.concat([fake_part, true_part], ignore_index=True)


welfake = load_welfake()
new_data = load_new_dataset()

df = pd.concat([welfake, new_data], ignore_index=True)
print(f"\nCombined shape: {df.shape}")

df = df[df["content"].str.split().str.len() >= MIN_WORDS]
print(f"After removing very short rows: {df.shape}")

before = len(df)
df = df[df.groupby("content")["label"].transform("nunique") == 1]
print(f"Removed {before - len(df)} rows with conflicting labels")

before = len(df)
df = df.drop_duplicates(subset="content")
print(f"Removed {before - len(df)} duplicates: {df.shape}")

df = df.sample(frac=1, random_state=42).reset_index(drop=True)
df.to_csv(OUTPUT_CSV, index=False)

print(f"\nSaved to {OUTPUT_CSV}")
print("Label counts (0 = real, 1 = fake):")
print(df["label"].value_counts().to_string())
print("Rows per source:")
print(df["source"].value_counts().to_string())