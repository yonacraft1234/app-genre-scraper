# Genre Scraper

A high-performance FastAPI proxy service that fetches app genres, categories, and assigns distraction metrics from the Google Play Store. It uses multithreading for rapid concurrent lookups and fuzzy matching to ensure accurate app discovery.

## 🚀 Features

- **FastAPI Powered:** Fast, modern, and highly performant RESTful API.
- **Concurrent Scraping:** Uses `ThreadPoolExecutor` to handle multiple app lookups safely and simultaneously.
- **Smart App Matching:** Employs `rapidfuzz` to handle slight typos or misnamed applications against real Play Store results.
- **Distraction Evaluation:** Automatically determines a "distraction level" based on the application's discovered category.
- **Docker Ready:** Comes with a production-ready, lightweight Dockerfile.

## 📋 Prerequisites

- Python 3.11+
- Docker (optional, but recommended for containerized deployment)

## 🛠️ Setup & Installation

### Option 1: Running Locally (Native)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the development server:**
   ```bash
   python main.py
   # OR
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

### Option 2: Running with Docker

1. **Build the image:**
   ```bash
   docker build -t genre-scraper .
   ```

2. **Run the container:**
   ```bash
   docker run -p 8000:8000 genre-scraper
   ```

## 📖 API Documentation

By default, FastAPI automatically generates interactive API documentation. Once the server is running, visit:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

### Endpoints

#### **POST** `/genres`
Fetches genre and distraction information for a provided list of applications.

**Request Body:**
```json
{
  "apps": [
    "com.instagram.android",
    "TikTok",
    "Slack"
  ]
}
```

**Response:**
```json
{
  "results": [
    {
      "app": "TikTok",
      "status": "OK",
      "genre": "Social",
      "genre_id": "SOCIAL",
      "category": "social",
      "distraction_value": 85
    }
    // ...other results
  ]
}
```

## 📂 Project Structure

```text
├── main.py                  # FastAPI application entry point and routes
├── scraper.py               # Core scraping logic, multithreading & fuzzy string matching
├── distraction_levels.py    # Logic to evaluate distraction scoring based on categories
├── requirements.txt         # Python dependencies
├── Dockerfile               # Containerization instructions
└── types_lib/               # Pydantic models for request/response validation and types
    ├── scraper_types.py
    └── constants.py
```
