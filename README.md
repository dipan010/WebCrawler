# 📰 Web Crawler

This repository is an end-to-end data pipeline for scraping, transforming, and storing logistics and supply chain-related news articles. It combines web crawlers, NewsAPI integration, transformation logic, and S3 uploads orchestrated through Apache Airflow.

---

## 🚀 Setup Instructions

### 1. Clone the repo
```cmd
git clone https://github.com/your-org/WebCrawler.git
cd WebCrawler
```

### 2. Create virtual environment
```cmd
python -m venv .venv
source .venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 3. Install dependencies
```cmd
pip install -r requirements.txt
```

### 4. Configure `.env` for AWS/NewsAPI
Create a `.env` file in root with:
```env
AWS_PROFILE=your-profile-name
NEWSAPI_KEY=your-api-key
```

---

## 🧩 How It Works

### ✅ Airflow DAG Flow:
```
fetch_newsapi → upload_raw → transform + upload_processed to S3
run_spiders → upload_raw → transform + upload_processed to S3
```

Each phase is modular, logged, and testable independently.

---

## 🧪 Unit Tests

### Run all tests:
```bash
pytest tests/ -v
```

### Breakdown:
| Test File                      | Purpose                                     |
|-------------------------------|---------------------------------------------|
| `test_pipeline_runner.py`     | Runs all spiders and validates output merge |
| `test_transform.py`           | Tests HTML cleaning, normalization          |
| `test_process_articles.py`    | Tests deduplication, transformation         |
| `test_uploader_raw.py`        | Tests S3 upload from raw file               |

> You can mock S3 with `moto` or test against a dev AWS bucket.

---
