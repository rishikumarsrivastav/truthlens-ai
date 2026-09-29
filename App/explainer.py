from lime.lime_text import LimeTextExplainer

explainer = LimeTextExplainer(class_names=["Real", "Fake"], random_state=42)


def get_lime_highlights(text, clf, tfidf, num_samples=500):
    def predict_proba(texts):
        return clf.predict_proba(tfidf.transform(texts))

    try:
        exp = explainer.explain_instance(
            text, predict_proba, labels=(1,), num_features=10, num_samples=num_samples
        )
        weights = exp.as_list(label=1)
    except Exception as e:
        print("LIME failed:", e)
        return {"fake_words": [], "real_words": []}

    weights = [w for w in weights if w[0].lower() in tfidf.vocabulary_]

    fake_words = sorted([w for w in weights if w[1] > 0], key=lambda x: -x[1])[:5]
    real_words = sorted([w for w in weights if w[1] < 0], key=lambda x: x[1])[:5]

    return {
        "fake_words": [[w, float(v)] for w, v in fake_words],
        "real_words": [[w, float(v)] for w, v in real_words],
    }