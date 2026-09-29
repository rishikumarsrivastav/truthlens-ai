import pickle
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Works from the project root (recommended) and also if this file sits inside App/
BASE_DIR = Path(__file__).resolve().parent
if BASE_DIR.name == "App":
    BASE_DIR = BASE_DIR.parent
sys.path.insert(0, str(BASE_DIR))

from App.text_utils import normalize_text  # same cleaning the app uses at prediction time

DATA_CSV = BASE_DIR / "Data" / "fake_news_cleaned.csv"
if not DATA_CSV.exists():
    DATA_CSV = BASE_DIR / "fake_news_cleaned.csv"
if not DATA_CSV.exists():
    raise SystemExit("fake_news_cleaned.csv not found. Put it inside the Data folder.")

MODEL_DIR = BASE_DIR / "Model"
MODEL_DIR.mkdir(exist_ok=True)

MAX_CHARS = 2000
MAX_FEATURES = 100000

print(f"Loading {DATA_CSV.name} ...")
df = pd.read_csv(DATA_CSV)
df = df.dropna(subset=["text", "label", "split"]).copy()
df["label"] = df["label"].astype(int)          # 1 = fake, 0 = real
df["title"] = df["title"].fillna("").map(normalize_text)
df["content"] = (df["title"] + " " + df["text"].map(normalize_text)).str.strip()
print(f"Dataset shape: {df.shape}")
print("Label counts (0 = real, 1 = fake):", df["label"].value_counts().to_dict())

# The split column in the CSV is already stratified 80/10/10 with no duplicate leakage
train_df = df[df["split"] == "train"]
val_df = df[df["split"] == "val"]
test_df = df[df["split"] == "test"]
print(f"Train: {train_df.shape}, Val: {val_df.shape}, Test: {test_df.shape}")

rng = np.random.default_rng(42)


def random_snippet(text):
    words = str(text).split()
    return " ".join(words[:int(rng.integers(15, 120))])


has_title = train_df["title"].str.split().str.len().fillna(0) >= 4

full_articles = pd.DataFrame({
    "text": train_df["content"].str[:MAX_CHARS],
    "label": train_df["label"],
})
titles = pd.DataFrame({
    "text": train_df.loc[has_title, "title"],
    "label": train_df.loc[has_title, "label"],
})
snippets = pd.DataFrame({
    "text": train_df["content"].map(random_snippet),
    "label": train_df["label"],
})

train_all = pd.concat([full_articles, titles, snippets], ignore_index=True)
print(f"Training rows after adding short text: {len(train_all)}")

print("Vectorizing text data...")
tfidf = TfidfVectorizer(
    stop_words="english",
    min_df=5,
    max_df=0.9,
    max_features=MAX_FEATURES,
    sublinear_tf=True,
)
X_train = tfidf.fit_transform(train_all["text"])
print(f"Vocabulary size: {len(tfidf.vocabulary_)}")

print("Training Logistic Regression...")
clf = LogisticRegression(C=2.0, max_iter=1000)
clf.fit(X_train, train_all["label"])

val_pred = clf.predict(tfidf.transform(val_df["content"].str[:MAX_CHARS]))
print(f"\nValidation accuracy: {accuracy_score(val_df['label'], val_pred)*100:.2f}%")

X_test = tfidf.transform(test_df["content"].str[:MAX_CHARS])
y_pred = clf.predict(X_test)
accuracy = accuracy_score(test_df["label"], y_pred)
print(f"Test accuracy: {accuracy*100:.2f}%")

print("\nClassification Report:")
print(classification_report(test_df["label"], y_pred, target_names=["Real", "Fake"]))

print("Confusion Matrix:")
print(confusion_matrix(test_df["label"], y_pred))

mask = test_df["title"].str.split().str.len().fillna(0) >= 4
title_pred = clf.predict(tfidf.transform(test_df.loc[mask, "title"]))
print(f"\nHeadline only accuracy: {accuracy_score(test_df.loc[mask, 'label'], title_pred)*100:.2f}%")

short_text = test_df["content"].map(lambda t: " ".join(str(t).split()[:40]))
short_pred = clf.predict(tfidf.transform(short_text))
print(f"First 40 words accuracy: {accuracy_score(test_df['label'], short_pred)*100:.2f}%")

names = np.array(tfidf.get_feature_names_out())
order = np.argsort(clf.coef_[0])
print("\nTop words for REAL:", ", ".join(names[order[:20]]))
print("Top words for FAKE:", ", ".join(names[order[-20:][::-1]]))

print("\nSaving model and vectorizer...")
with open(MODEL_DIR / "lr_model.pkl", "wb") as f:
    pickle.dump(clf, f)

with open(MODEL_DIR / "tfidf_vectorizer.pkl", "wb") as f:
    pickle.dump(tfidf, f)

print("Model saved:", MODEL_DIR / "lr_model.pkl")
print("Vectorizer saved:", MODEL_DIR / "tfidf_vectorizer.pkl")