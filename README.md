# Global Sentiment Pipeline

A lightweight Python pipeline that automatically pulls articles from public news feeds, uses the Hugging Face Serverless API for sentiment classification, and saves the structured logs directly to a MongoDB Atlas cloud cluster.

## Features
- **RSS Feed Ingestion:** Pulls top financial and global news from Yahoo Finance RSS.
- **Serverless AI Sentiment Analysis:** Uses Hugging Face's active router endpoint to analyze article titles using the `distilbert/distilbert-base-uncased-finetuned-sst-2-english` model.
- **Cloud Database Logging:** Directly connects and logs the sentiment results to MongoDB Atlas using `pymongo`.
- **Lightweight:** Uses only the bare minimum dependencies (`requests`, `feedparser`, `pymongo`, `python-dotenv`) to save local disk space.

## Prerequisites
- Python 3.x
- A MongoDB Atlas account and cluster
- A Hugging Face account with a Fine-grained Access Token (with Inference permissions enabled)

## Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Ali-Abu-Fadalah/global-sentiment-pipeline.git
   cd global-sentiment-pipeline
   ```

2. **Create a virtual environment and install dependencies:**
   ```bash
   python -m venv venv
   
   # Activate on Windows:
   .\venv\Scripts\activate
   # Activate on Mac/Linux:
   source venv/bin/activate
   
   pip install requests pymongo python-dotenv feedparser huggingface_hub
   ```

3. **Configure Environment Variables:**
   Create a `.env` file in the root directory (this file is git-ignored for security) and add your credentials:
   ```env
   # MongoDB Atlas Cloud Database Configuration
   MONGO_URI="mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?appName=<appname>"
   DB_NAME="market_intelligence"
   COLLECTION_NAME="sentiment_logs"
   
   # Hugging Face Serverless AI API Configuration
   HF_API_TOKEN="your_fine_grained_huggingface_token_here"
   HF_MODEL_ID="distilbert/distilbert-base-uncased-finetuned-sst-2-english"
   
   # System Configuration
   ALERT_THRESHOLD="0.80"
   DISCORD_WEBHOOK_URL="placeholder"
   ```

## Usage
Simply run the script within your virtual environment:

```bash
python app.py
```

The script will fetch the latest articles, classify them, print the results to the terminal, and insert them directly into your MongoDB Atlas database.
