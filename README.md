<div align="center">

# 🛡️ TruthLens AI

### Explainable Fake News Detection using Machine Learning & NLP

https://truthlens-ai-2zy0.onrender.com/
 
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python">
  <img src="https://img.shields.io/badge/Flask-Web%20Framework-black?logo=flask">
  <img src="https://img.shields.io/badge/Machine%20Learning-Logistic%20Regression-orange">
  <img src="https://img.shields.io/badge/NLP-TF--IDF-green">
  <img src="https://img.shields.io/badge/Status-Active-success">
  <img src="https://img.shields.io/badge/License-MIT-blue">
</p>

**A web app that checks WhatsApp forwards and news text, gives a True / False / Unverified result, shows a trust score, and highlights the words behind the decision.**

</div>

---

# 📖 Overview

**TruthLens AI** helps people check a message before they forward it. You paste a WhatsApp message or news text, optionally add the link it came from, and the app tells you whether it looks reliable.

It does not only give a label. It also shows how much it trusts the message, which words pushed the result towards fake or real, and how credible the source website is. Messages in Hindi and other languages are translated to English before they are checked.

---

# ✨ Key Features

### 📰 Fake News Detection
- Classifies a message as **True**, **False** or **Unverified**
- Says "Unverified" instead of guessing when the message is too short or unclear

### 🧠 Explainable AI
- Uses LIME to highlight the words that pushed the result towards fake (red) or real (green)

### 📊 Trust Score
- Trust score from 0 to 100% shown on a visual meter
- Combines the text analysis (70%) with the credibility of the source link (30%)
- A message that sounds real but links to a known fake-news site is marked Unverified

### 🔗 Source Credibility
- Checks the link against a list of Indian and international news sites
- Unknown websites get a neutral score

### 🌐 Multilingual Input
- Detects the language of the message
- Translates non-English text (for example Hindi) to English before checking it, and shows both versions

### 🎨 Clean Web Interface
- Built for pasting WhatsApp forwards
- Works on phone and desktop

---

# 🛠️ Tech Stack

### Frontend
- HTML5
- CSS3
- JavaScript

### Backend
- Python
- Flask

### Machine Learning
- TF-IDF Vectorizer
- Logistic Regression
- LIME (word highlighting)

### Datasets
- WELFake Dataset
- Kaggle fake news dataset (combined with WELFake, duplicates removed)

### Libraries
- Scikit-learn
- Pandas
- NumPy
- langdetect
- deep-translator
- Pickle

---

# 📂 Project Structure

```text
TruthLensAI/
│
├── App/
│   ├── __init__.py
│   ├── credibility.py
│   ├── explainer.py
│   ├── preprocessor.py
│   ├── routes.py
│   ├── text_utils.py
│   └── translator.py
│
├── Data/
│   ├── fake_news_cleaned.csv
│   ├── source_credibility.json
│   ├── WELFake_Dataset.csv
│   └── Combined_Cleaned.csv        (created by data_cleaning.py)
│
├── Model/                          (created by train_model.py)
│   ├── lr_model.pkl
│   └── tfidf_vectorizer.pkl
│
├── Notebook/
│   └── explore.ipynb
│
├── Static/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── venv/
├── checkmodel.py
├── data_cleaning.py
├── train_model.py
├── README.md
├── requirements.txt
├── run.py
│
└── .gitignore
```

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/Jokerwor/truthlens-ai.git
```

## 2. Navigate to the project

```bash
cd truthlens-ai
```

## 3. Create a virtual environment

```bash
python -m venv venv
```

## 4. Activate the virtual environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

## 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🧪 Train the Model

The datasets and trained model files are large, so they are not stored in the repository. Put `WELFake_Dataset.csv` and the new Kaggle dataset inside the `Data/` folder, then run these from the project root:

```bash
python data_cleaning.py
python train_model.py
python checkmodel.py
```

- `data_cleaning.py` merges the datasets, cleans the text, removes duplicates and saves `Data/Combined_Cleaned.csv`
- `train_model.py` trains the model and saves it in the `Model/` folder
- `checkmodel.py` tries a few sample messages. Fake-style messages should score high and real-style messages low

Labels are `0 = real` and `1 = fake` everywhere in the project.

---

# ▶️ Run the Application

```bash
python run.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

Do not open `Static/index.html` directly. The page needs the Flask server to work.

---

# 🔄 Workflow

```text
User Message (+ optional source link)
     │
     ▼
WhatsApp Text Cleaning
     │
     ▼
Language Detection → Translation to English
     │
     ▼
TF-IDF Vectorization
     │
     ▼
Logistic Regression  →  probability of fake
     │
     ▼
Combine with Source Credibility
     │
     ├── True / False / Unverified
     ├── Trust Score
     ├── Highlighted Words (LIME)
     └── Translation Panel
```

---

# ⚠️ Limitations

- The training data is mostly US political news from 2016–2017, so results on Indian or WhatsApp-style messages are a first-pass signal, not a final answer
- Very short messages are marked Unverified
- The model checks writing style, not facts. Always confirm with a trusted fact-checking source before forwarding

---

# 🚀 Future Improvements

- [ ] Train on real WhatsApp forwards with verified labels
- [ ] BERT-based fake news detection
- [ ] Live news API integration
- [ ] Fact-check API integration
- [ ] Better support for Hinglish (Hindi written in English letters)
- [ ] Speech-to-text support
- [ ] Dark mode
- [ ] Cloud deployment (Render/AWS)

---

# 📸 Screenshots

> Add screenshots here after uploading them.

### Home Page

```
screenshots/home.png
```

### Prediction Result

```
screenshots/result.png
```

### Explainability Panel

```
screenshots/explanation.png
```

---

# 🤝 Contributing

Contributions are welcome!

1. Fork the repository.
2. Create a new branch.
3. Commit your changes.
4. Push to your branch.
5. Open a Pull Request.

---

# 👨‍💻 Author

**Rishi Kumar Srivastav**

- 💼 Aspiring AI & Machine Learning Engineer
- 🌐 GitHub: https://github.com/Jokerwor
- 💼 LinkedIn: **Add your LinkedIn profile here**

---

# 📜 License

This project is licensed under the **MIT License**.

---

<div align="center">

⭐ If you found this project useful, consider giving it a **Star** on GitHub!

</div>
