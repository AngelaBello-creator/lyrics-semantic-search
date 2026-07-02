# Lyrics Semantic Search API

A semantic search API for song lyrics built with Python, FastAPI, Sentence Transformers and FAISS.

The project demonstrates how vector embeddings and semantic search can be used to retrieve songs based on meaning rather than exact keyword matching.

---

## Overview

Traditional search engines rely on keyword matching.

This project uses transformer embeddings and a FAISS vector index to perform semantic retrieval over song lyrics.

Example query:

```text
songs about jealousy
```

Possible result:

```text
Pienso en tu mirá — Rosalía
```

without requiring the word *jealousy* to appear in the lyrics.

---

## Features

- Load lyrics from text files
- Parse song metadata
- Generate document embeddings using Sentence Transformers
- Build a FAISS vector index
- Perform semantic similarity search
- Expose a REST API with FastAPI
- Automatic OpenAPI / Swagger documentation
- Typed response models using Pydantic
- Structured application logging

---

## Technology Stack

| Technology | Purpose |
|------------|---------|
| Python | Backend |
| FastAPI | REST API |
| Sentence Transformers | Embedding generation |
| FAISS | Vector similarity search |
| NumPy | Numerical operations |
| Pydantic | Response validation |
| Uvicorn | ASGI server |

---

## Architecture

```text
                 +------------------+
                 |  Lyrics (.txt)   |
                 +------------------+
                          |
                          v
                 +------------------+
                 | Metadata Parser  |
                 +------------------+
                          |
                          v
                 +------------------+
                 | Song Objects     |
                 +------------------+
                          |
                          v
           +------------------------------+
           | Sentence Transformer Model   |
           +------------------------------+
                          |
                          v
                 +------------------+
                 | Vector Embeddings|
                 +------------------+
                          |
                          v
                 +------------------+
                 | FAISS Index      |
                 +------------------+
                          |
                          v
                 +------------------+
                 | FastAPI          |
                 +------------------+
                          |
                          v
                    JSON Response
```

---

## Project Structure

```text
lyrics-semantic-search/
│
├── app/
│   ├── api.py
│   ├── config.py
│   ├── loader.py
│   ├── models.py
│   ├── schemas.py
│   └── vector_search.py
│
├── data/
├── tests/
│
├── main.py
├── requirements.txt
└── README.md
```

---

## Dataset Format

Each document follows a simple structure.

```text
Title: Chulo
Artist: Bad Gyal
Album: La Joia
Year: 2023
Genre: Urban
Language: Spanish

Lyrics...
```

Song lyrics are not included in this repository for copyright reasons.

---

## API

### Health

```http
GET /health
```

Response

```json
{
  "status": "ok"
}
```

---

### Songs

```http
GET /songs
```

Returns every indexed song together with its metadata.

---

### Semantic Search

```http
GET /search?q=jealousy&limit=3
```

Example response

```json
{
  "query": "jealousy",
  "limit": 3,
  "results": [
    {
      "title": "Pienso en tu mirá",
      "artist": "Rosalía",
      "album": "El Mal Querer",
      "year": 2018,
      "genre": "Flamenco Pop",
      "language": "Spanish",
      "score": 1.816,
      "lyrics_preview": "Me da miedo cuando sale..."
    }
  ]
}
```

Swagger UI is available at:

```text
http://127.0.0.1:8000/docs
```

---

## How It Works

### 1. Document Loading

Lyrics are loaded from the `data/` directory and parsed into `Song` objects.

### 2. Embedding Generation

Each complete lyric is converted into a dense vector representation using the Sentence Transformer model:

```text
sentence-transformers/all-MiniLM-L6-v2
```

Each embedding contains 384 dimensions.

### 3. Index Construction

Embeddings are stored inside a FAISS `IndexFlatL2`.

The current implementation performs exact nearest-neighbour search using Euclidean distance.

### 4. Semantic Retrieval

A user query is embedded using the same model.

FAISS retrieves the closest vectors, which are mapped back to their corresponding songs.

---

## Installation

Clone the repository.

```bash
git clone https://github.com/AngelaBello-creator/lyrics-semantic-search.git
```

Create a virtual environment.

```bash
py -m venv .venv
```

Activate it.

```bash
.venv\Scripts\Activate.ps1
```

Install dependencies.

```bash
pip install -r requirements.txt
```

Run the application.

```bash
py main.py
```

Open the API documentation.

```text
http://127.0.0.1:8000/docs
```

---

## Example Queries

```text
jealousy
```

```text
heartbreak
```

```text
romantic love
```

```text
songs about dancing
```

```text
party songs
```

```text
healing after a breakup
```

---

## Current Limitations

- Document-level embeddings only
- Index rebuilt on every application startup
- Small demonstration dataset
- Exact L2 similarity search
- No metadata filtering
- No reranking
- No hybrid retrieval

---

## Future Improvements

- Persist FAISS indices to disk
- Metadata filtering
- Docker support
- Unit tests with pytest
- Chunk-based indexing
- Hybrid search
- Reranking
- Retrieval-Augmented Generation (RAG)

---

## Learning Objectives

This project was developed to explore the engineering behind semantic search systems.

It demonstrates concepts including:

- Vector embeddings
- Information Retrieval
- Approximate nearest neighbour search
- REST API design
- Backend development for AI applications

The same architecture can be extended to semantic search over PDFs, documentation, legal text, customer support tickets or other unstructured documents.

---

## Author

Angela Bello