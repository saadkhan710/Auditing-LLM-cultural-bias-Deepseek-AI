# 🧠 Cultural Text Analytics & WordCloud Dashboard

## Overview

A Python-based text analysis and visualization script for exploring and comparing texts across different cultural identities. The project groups narrative text data by culture, cleans the content using custom stopwords and regular expressions, and then visualizes the top words using frequency tables and word clouds. This tool is ideal for examining cross-cultural patterns, communication styles, and common linguistic themes in qualitative datasets.

## ✨ Features

- 🌍 **Culture-Based Grouping**: Texts automatically grouped by cultural identity
- ❌ **Custom Stopwords**: Filters names and common filler words
- 🧹 **Text Cleaning Pipeline**: Lowercasing, punctuation/digit removal
- 📊 **Top Words Table**: Displays most frequent words per culture
- ☁️ **Word Clouds**: Visualize dominant terms within each cultural group

---

## 🛠️ Technologies Used

- Python 3.10+
- Matplotlib (Visualizations)
- WordCloud (Natural language cloud art)
- Collections (Counter)
- `re` (Regex for cleaning)
- `defaultdict` (Efficient text grouping)

---

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/saadkhan710/Auditing-LLM-cultural-bias-Deepseek-AI.git
cd Auditing-LLM-cultural-bias-Deepseek-AI

# 2. Set up virtual environment
python -m venv venv

# Activate virtual environment:
# On Windows
.\venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate

```

## 🔧 Installation
```bash

pip install -r requirements.txt

```

## 📁 Project Structure
```bash
Auditing-LLM-cultural-bias-Deepseek-AI/
├── main.py                   # Core script: processing & visualizations
├── requirements.txt          # Package dependencies
└── README.md                 # This file
```

## 💡 How It Works
```bash
Group text by culture
Clean and tokenize text
Filter stopwords and short words

Generate:
Frequency table (top 15 words)
Word Cloud (per culture)

```

## 👨‍💻 Author
```bash
Saad Khan
MSc Information Systems, University College Dublin
```



