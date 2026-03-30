# Medico Bot

An AI-powered medical assistant chatbot built for medical students. It uses RAG (Retrieval Augmented Generation) to answer medical questions with cited PubMed references.

## Features

- Conversational medical Q&A with multi-turn history
- Semantic search over a medical knowledge base (Pinecone)
- PubMed citations as clickable markdown links
- ReAct agent pattern for reasoning and tool use
- Built with Streamlit for a simple web UI

## Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit |
| LLM | OpenAI GPT-3.5-turbo |
| Embeddings | Cohere (`embed-english-light-v3.0`) |
| Vector DB | Pinecone (serverless) |
| Agent Framework | LangChain ReAct |

## Architecture

```
User Query
    ↓
Pinecone similarity search → retrieve top-k medical docs
    ↓
LangChain ReAct Agent (GPT-3.5-turbo) + chat history + context
    ↓
Response with PubMed citations
    ↓
Streamlit UI
```

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
COHERE_API_KEY=your_cohere_api_key
PINECONE_API_KEY=your_pinecone_api_key
```

### 3. Pinecone index

The app expects a Pinecone index named `medulla` with:
- Dimension: `384`
- Metric: `cosine`
- Cloud: AWS `us-east-1` (serverless)

### 4. Run

```bash
streamlit run app.py
```

App will be available at `http://localhost:8501`.

## Project Structure

```
medico-bot/
├── app.py                  # Streamlit entry point
├── requirements.txt
├── chain/
│   ├── lc_chain.py         # LangChain agent setup
│   ├── embeddings.py       # Cohere embeddings init
│   ├── tools.py            # Agent tools
│   └── prompts/
│       └── system_prompt.py
├── database/
│   └── vector_search.py    # Pinecone similarity search
└── config/
    └── settings.py
```
