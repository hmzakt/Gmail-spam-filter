# 📧 Gmail Spam Filter

A simple yet powerful **ML-powered Gmail Spam Filter** that classifies your latest 10 emails as **Spam** or **Not Spam**, and optionally moves spam directly to the spam folder — all using Flask, Gmail API, and scikit-learn.

![Python](https://img.shields.io/badge/Python-3.10-blue?style=flat-square)
![Flask](https://img.shields.io/badge/Flask-API-success?style=flat-square)
![ML](https://img.shields.io/badge/Machine%20Learning-Logistic%20Regression-orange?style=flat-square)
![Gmail API](https://img.shields.io/badge/Gmail%20API-Enabled-red?style=flat-square)

---

## 🚀 Features

- 🔐 Secure Gmail integration using OAuth2
- 🧠 Trained spam classifier using **Naive Bayes**
- ✉️ Fetches latest 10 emails from your inbox
- ✅ Classifies emails as **Spam** or **Not Spam**
- 🚮 Auto-moves spam emails to Gmail's spam folder
- 🌐 CORS-enabled backend ready for frontend integration

---

## 🛠️ Tech Stack

| Component     | Tech                        |
|---------------|-----------------------------|
| Backend       | Flask, Gmail API, Joblib    |
| ML Model      | Naive Bayes (scikit-learn)  |
| Data Cleaning | Custom regex preprocessing  |
| Deployment    | Localhost (demo)            |

---


---

## 🔐 Authentication

This app uses Google's OAuth2 flow. You must:

1. Create a **Google Cloud project**
2. Enable the **Gmail API**
3. Add yourself as a **tester**
4. Download and rename `credentials.json` to your project directory

For personal testing, your email must be added to the OAuth2 test user list.

---

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/gmail-spam-filter-demo.git
cd gmail-spam-filter-demo

# Create a virtual environment (optional)
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run the Flask API
python app.py
```

---

## 🗃️ Dataset

This project uses a custom-labeled dataset of spam and non-spam emails for training the classifier.  
The dataset is inspired by and adapted from a **Kaggle competition** and enriched with synthetic examples for better generalization.

> Note: The dataset used for training (`train.csv`, `test.csv`, `submission.csv`) is not included in the public repo. You may replace it with your own labeled dataset.

[🔗 Kaggle Dataset](https://www.kaggle.com/competitions/ds100fa19)
