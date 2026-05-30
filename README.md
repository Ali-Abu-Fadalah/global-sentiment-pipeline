# Global Sentiment Pipeline

A lightweight Python pipeline that automatically pulls articles from public news feeds, uses the Hugging Face Serverless API for sentiment classification, and saves the structured logs directly to a MongoDB Atlas cloud cluster.

## Why This Project?

Analyzing market sentiment is critical for timely decision-making, but deploying deep learning models locally often requires significant compute resources, high VRAM GPU hardware, and complex container orchestration. 

This project solves that problem by building a **fully serverless, zero-local-hardware-overhead pipeline**. It ingests public RSS feeds dynamically, leverages cloud-hosted AI inference, and streams structured logs directly into a cloud database. This architecture is perfect for resource-constrained environments (like a local student laptop) while remaining highly scalable.

---

## Tech Stack

| Technology | Purpose | Key Benefit |
| :--- | :--- | :--- |
| **Python 3** | Core Pipeline Logic | Lightweight scripting & rich package ecosystem |
| **Hugging Face Serverless Inference** | Sentiment Classification | DistilBERT model inference with zero local GPU/RAM overhead |
| **MongoDB Atlas** | Structured Log Storage | Scalable, document-based cloud database |
| **Yahoo Finance RSS** | Ingestion Stream | Standardized, real-time public market news |

---

## System Architecture

```mermaid
graph TD
    A[Yahoo Finance RSS Feed] -->|1. Ingest XML Data| B[Python Script app.py]
    B -->|2. HTTP Request: Send Title| C[Hugging Face Serverless API]
    C -->|3. JSON Response: Sentiment & Conf.| B
    B -->|4. Store Log Document| D[(MongoDB Atlas Cluster)]
    B -.->|5. Threshold Alert (Optional)| E[Discord Webhook]
    
    style A fill:#ffcc00,stroke:#333,stroke-width:2px
    style B fill:#3399ff,stroke:#333,stroke-width:2px
    style C fill:#ff9999,stroke:#333,stroke-width:2px
    style D fill:#47d147,stroke:#333,stroke-width:2px
    style E fill:#9999ff,stroke:#333,stroke-dasharray: 5 5
```

---

## How to Run It

If you want to run this pipeline locally, you can recreate the exact environment in seconds:

### 1. Recreate the Virtual Environment
Create a clean virtual environment and activate it:
```powershell
# Create environment
python -m venv venv

# Activate on Windows (PowerShell)
.\venv\Scripts\activate

# Activate on Mac/Linux
source venv/bin/activate
```

### 2. Install Dependencies
Install all package blueprints from `requirements.txt`:
```powershell
pip install -r requirements.txt
```

### 3. Configure Local Environment Variables
Create a local `.env` file in the root directory (this file is excluded from git) and fill it with your own API keys:
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

### 4. Run the Pipeline
```powershell
python app.py
```
