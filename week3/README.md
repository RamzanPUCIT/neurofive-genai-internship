# RAG Mini-Project — Chat With Your Own Document

**Week 3 | Generative AI & Prompt Engineering | NeuroFive Solutions**
Internee: Muhammad Ramzan

A Retrieval-Augmented Generation pipeline built with LangChain + FAISS that answers questions from a 4-page PDF instead of the model's training data.

> The source PDF is a real person's CV. It is not committed to this repo for privacy.

## Stack

| Component | Used |
|---|---|
| Orchestration | LangChain |
| Vector store | FAISS (local) |
| Embeddings | fastembed — BAAI/bge-small-en-v1.5 (CPU, no API key) |
| LLM | Groq — openai/gpt-oss-20b, temperature=0 |

## Pipeline

PDF (4 pages) → 42 chunks (250 chars, 50 overlap) → 384-dim vectors → FAISS index → retrieve top-k → grounded prompt → answer or NOT IN DOCUMENT

## Run

    pip install -r requirements.txt
    python rag.py
