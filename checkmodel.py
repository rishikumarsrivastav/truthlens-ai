import pickle
from pathlib import Path

from App.text_utils import normalize_text

BASE_DIR = Path(__file__).resolve().parent

with open(BASE_DIR / "Model" / "lr_model.pkl", "rb") as f:
    clf = pickle.load(f)

with open(BASE_DIR / "Model" / "tfidf_vectorizer.pkl", "rb") as f:
    tfidf = pickle.load(f)

samples = [
    ("fake", "BREAKING: Deep state elites caught hiding the truth about vaccines, share before they delete this!"),
    ("fake", "Shocking secret the mainstream media does not want you to know, Hillary and Obama exposed"),
    ("fake", "Modi government will give free petrol to every citizen, forward this to 10 people to claim"),
    ("real", "The Reserve Bank of India kept the repo rate unchanged on Friday, citing inflation and global uncertainty, the central bank said in a statement."),
    ("real", "The Senate voted 62 to 38 on Tuesday to approve the budget bill after weeks of negotiation between the two parties."),
    ("real", "Health ministry officials said the vaccination drive will cover 12 districts next month, according to a government statement."),
    ("short", "Free petrol"),
]

fake_index = list(clf.classes_).index(1)
results = []

print(f"{'type':<7}{'words':>6}{'p_fake':>9}  message")
for kind, msg in samples:
    vec = tfidf.transform([normalize_text(msg)])
    p_fake = float(clf.predict_proba(vec)[0][fake_index])
    results.append(round(p_fake, 2))
    print(f"{kind:<7}{vec.nnz:>6}{p_fake:>9.2f}  {msg[:70]}")

if len(set(results)) <= 2:
    print("\nSame answer for almost every message, something is wrong with the model")
else:
    print("\nModel gives different answers for different messages")
print("fake lines should be high and real lines should be low")