# 🎵 Lyrics Semantic Search

A semantic search engine for song lyrics built with
Sentence Transformers and FAISS.

Instead of searching for exact keywords, this project retrieves songs based on their semantic meaning.

---

## Features

- Load lyrics from text files
- Generate embeddings using Sentence Transformers
- Store vectors with FAISS
- Perform semantic similarity search
- REST API built with FastAPI

---

## Tech Stack

- Python
- FastAPI
- Sentence Transformers
- FAISS
- NumPy

---

## Architecture

Lyrics (.txt)

↓

Sentence Transformer

↓

Embeddings

↓

FAISS Index

↓

Semantic Search API