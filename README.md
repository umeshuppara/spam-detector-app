# 📧 Email Spam Detector App

A Machine Learning-based web application that classifies emails/messages as **Spam or Not Spam** using Natural Language Processing (NLP).

---

## 🌐 Live Demo
👉 https://spam-detector-app-37suonnlgjuc8j3oenuthu.streamlit.app/

---

## 📌 Project Overview

This project detects whether a given email/message is spam or not using a trained Machine Learning model.  
It provides a simple web interface where users can enter text and get instant predictions along with confidence scores.

The application also stores prediction history and provides analytics visualization.

---

## ✨ Features

- 📩 Classify email/message as Spam or Not Spam  
- 📊 Shows prediction confidence score  
- 📜 Stores prediction history  
- 🗑 Delete individual or all history  
- 📈 Analytics dashboard (charts and graphs)  
- 🎨 Simple and clean web UI  

---

## 🧠 How It Works

1. User enters email/message text  
2. Text is converted into numerical features using TF-IDF  
3. Machine Learning model processes the input  
4. Model predicts:
   - Spam  
   - Not Spam  
5. Result is displayed with confidence score  
6. Data is stored in local database  

---

## 🛠 Tech Stack

- Python 🐍  
- Streamlit (Web Interface)  
- Scikit-learn (Machine Learning)  
- Pandas (Data handling)  
- Matplotlib (Visualization)  
- SQLite (Database for history)  
- NLP (TF-IDF Vectorization)  

---
