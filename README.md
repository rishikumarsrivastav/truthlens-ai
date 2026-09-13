<div align="center">

# 🛡️ TruthLens AI

### Explainable Fake News Detection using Machine Learning & NLP

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python">
  <img src="https://img.shields.io/badge/Flask-Web%20Framework-black?logo=flask">
  <img src="https://img.shields.io/badge/Machine%20Learning-Passive%20Aggressive-orange">
  <img src="https://img.shields.io/badge/NLP-TF--IDF-green">
  <img src="https://img.shields.io/badge/Status-Active-success">
  <img src="https://img.shields.io/badge/License-MIT-blue">
</p>

**An AI-powered web application that detects fake news, explains its predictions, estimates credibility, and supports multilingual translation.**

</div>

---

# 📖 Overview

**TruthLens AI** is a machine learning-powered fake news detection system designed to help users identify misinformation. Instead of only predicting whether a news article is **Real** or **Fake**, the application also explains **why** the prediction was made using Explainable AI techniques.

The system combines Natural Language Processing (NLP), Machine Learning, credibility analysis, and multilingual translation to provide transparent and accessible results.

---

# ✨ Key Features

### 📰 Fake News Detection
- Predicts whether a news article is **Real** or **Fake**
- Fast and accurate classification using Machine Learning

### 🧠 Explainable AI
- Highlights important words influencing the prediction
- Makes AI decisions easy to understand

### 📊 Credibility Score
- Displays confidence percentage
- Visual confidence meter for better interpretation

### 🌐 Multilingual Translation
- Translate predictions and explanations into multiple languages
- Improves accessibility for diverse users

### 🎨 Interactive Web Interface
- Clean and responsive UI
- Instant prediction results
- User-friendly experience

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
- Passive Aggressive Classifier (PAC)

### Dataset
- WELFake Dataset

### Libraries
- Scikit-learn
- Pandas
- NumPy
- Pickle

---

# 📂 Project Structure

```text
TruthLensAI/
│
├── App/
│   ├── credibility.py
│   ├── explainer.py
│   ├── preprocessor.py
│   ├── routes.py
│   ├── translator.py
│   └── __init__.py
│
├── Data/
│   ├── WELFake_Dataset.csv
│   ├── WELFake_Cleaned.csv
│   └── source_credibility.json
│
├── Model/
│   ├── pac_model.pkl
│   └── tfidf_vectorizer.pkl
│
├── Notebook/
│   └── explore.ipynb
│
├── Static/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── run.py
├── train_model.py
├── data_cleaning.py
├── requirements.txt
└── README.md
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

## 6. Run the application

```bash
python run.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

---

# 🔄 Workflow

```text
User Input
     │
     ▼
Text Preprocessing
     │
     ▼
TF-IDF Vectorization
     │
     ▼
Passive Aggressive Classifier
     │
     ▼
Prediction
     │
     ├── Fake / Real
     ├── Confidence Score
     ├── Explanation
     └── Translation
```

---

# 🚀 Future Improvements

- ✅ BERT-based Fake News Detection
- ✅ Live News API Integration
- ✅ Fact-check API Integration
- ✅ Speech-to-Text Support
- ✅ Dark Mode
- ✅ User Authentication
- ✅ Cloud Deployment (Render/AWS)

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

**Built with ❤️ by Rishi Kumar Srivastav**

</div>
