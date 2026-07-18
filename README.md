# ShopBot+ 🤖

An AI customer support agent for e-commerce, built on a production-grade backend stack. ShopBot+ answers customer questions using retrieval-augmented generation (RAG) over a store knowledge base and looks up real order statuses from a live database — all through a single conversational interface.

🔗 **Live demo:** [shopbot-plus.onrender.com](https://shopbot-plus.onrender.com)
📦 **Repo:** [github.com/hayamot0/shopbot-plus](https://github.com/hayamot0/shopbot-plus)

---

## What it does

ShopBot+ is a ReAct-style AI agent with two tools:

- **`search_knowledge_base`** — retrieves answers from store policies, product info, and FAQs using RAG (Pinecone vector search)
- **`check_order_status`** — looks up real order data (status, item, customer) from a PostgreSQL database

The agent is explicitly scoped to store-related questions — it won't answer off-topic queries with general knowledge, keeping it predictable and on-brand for a business context.

---

## Architecture

```
User → FastAPI → LangGraph ReAct Agent → [search_knowledge_base | check_order_status]
                        ↓                          ↓                    ↓
                   Gemini (LLM)              Pinecone (RAG)      PostgreSQL (orders)
```

- **Backend:** FastAPI
- **Database:** PostgreSQL (SQLAlchemy ORM)
- **Vector store:** Pinecone (RAG over knowledge base)
- **Agent orchestration:** LangGraph (ReAct pattern — reasoning, tool calls, looping)
- **LLM:** Google Gemini (`gemini-2.5-flash`)
- **Interoperability:** MCP (Model Context Protocol) — exposes the same tools to external clients like Claude Desktop
- **Observability:** LangSmith tracing
- **Deployment:** Docker, deployed on Render

---

## Project structure

```
shopbot-plus/
├── main.py            # FastAPI app, routes, DB dependency injection
├── agent.py            # LangGraph ReAct agent, tools, state graph
├── rag.py              # Pinecone-backed RAG chain
├── ingest.py            # One-time script to populate the Pinecone index
├── mcp_server.py        # MCP server exposing the same tools externally
├── database.py          # SQLAlchemy engine/session setup
├── models.py            # Order table definition
├── schemas.py           # Pydantic request/response schemas
├── config.py             # Environment/config loading
├── knowledge_base/      # Source docs for RAG (policies, FAQs, product info)
├── frontend/             # Chat UI (served via Jinja2)
└── Dockerfile
```

---

## Running it locally

**1. Clone and install**
```bash
git clone https://github.com/hayamot0/shopbot-plus.git
cd shopbot-plus
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**2. Set environment variables**

Create a `.env` file:
```
DATABASE_URL=postgresql://user:password@host:5432/dbname
GOOGLE_API_KEY=your_gemini_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX=shopbot-plus
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_PROJECT=shopbot-plus
```

**3. Populate the knowledge base (one-time)**
```bash
python ingest.py
```

**4. Run with Docker**
```bash
docker build -t shopbot-plus .
docker run --env-file .env -p 8000:8000 shopbot-plus
```

Visit `http://localhost:8000` for the chat UI, or `http://localhost:8000/docs` for the interactive API docs.

---

## Example interactions

**Order lookup:**
> "What's the status of order ORD-1003?"
> → *Order 1003: item=Smart Watch, status=delivered, customer=Lina Meziane*

**Knowledge base:**
> "What's your return policy?"
> → *Answered using RAG retrieval from store policy docs*

**Out-of-scope:**
> "What's the capital of Algeria?"
> → *Politely declines — the agent stays scoped to store-related questions by design*

---

## Why this project

ShopBot+ is a rebuild of an earlier project (the original [ShopBot](https://github.com/hayamot0/shopbot)) upgraded to a production-oriented stack: FastAPI instead of Flask, PostgreSQL instead of a simpler local store, Pinecone instead of FAISS, and full Docker containerization with cloud deployment. It's built as a reusable template and proof of concept for AI-powered business automation — the kind of "AI employee" that can be adapted to real customer support workflows.

---

## Tech stack summary

| Layer | Tool |
|---|---|
| API | FastAPI |
| Agent orchestration | LangGraph |
| LLM | Google Gemini |
| Vector DB | Pinecone |
| Relational DB | PostgreSQL |
| Interoperability | MCP |
| Observability | LangSmith |
| Containerization | Docker |
| Deployment | Render |
