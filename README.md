# 🏛️ Confucius Agent

**Hierarchical Memory for AI Agents on Qwen Cloud**

> *"Not all context is equal."* — Confucius Paper (Meta + Harvard, arXiv:2512.10398)

<div align="center">
  <a href="https://confucius.wagnersolutionsai.com" target="_blank">
    <img src="https://img.shields.io/badge/Live%20Demo-🚀-8A2BE2?style=for-the-badge&logo=streamlit" alt="Live Demo">
  </a>
  &nbsp;
  <a href="https://github.com/SebaWag/confucius-agent" target="_blank">
    <img src="https://img.shields.io/badge/GitHub-Repo-181717?style=for-the-badge&logo=github" alt="GitHub">
  </a>
  &nbsp;
  <a href="https://arxiv.org/abs/2512.10398" target="_blank">
    <img src="https://img.shields.io/badge/Paper-Confucius%20🏛️-FF6B6B?style=for-the-badge" alt="Paper">
  </a>
</div>

---

---

## 🏆 Global AI Hackathon Series with Qwen Cloud — Track: MemoryAgent

**Confucius Agent** implements the **3-tier hierarchical memory system** from the Confucius paper on top of **Qwen Cloud**. Unlike traditional RAG that treats all context equally, our architecture distinguishes between:

| Tier | Priority | Type | Storage | Description |
|------|----------|------|---------|-------------|
| 🏛️ **Mental Models** | 🔴 Highest | Canonical knowledge | ChromaDB + Vector Search | Company policies, rules, verified facts |
| 📝 **Observations** | 🟡 Medium | Persistent learnings | PostgreSQL + Time-index | Patterns, decisions, notes from sessions |
| 📦 **Raw Facts** | 🟢 Lowest | Ephemeral context | Redis + TTL decay | Conversation logs, temporary data |

**Result:** An agent that never contradicts itself, reduces token consumption by up to 60%, and retrieves relevant information in milliseconds.

---

## 🎮 Live Demo

> 🚀 **Try it now without installing anything:**  
> 👉 **[https://confucius.wagnersolutionsai.com](https://confucius.wagnersolutionsai.com)**
>
> Upload documents, chat with the agent, and inspect the 3-tier memory in real time.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Docker & Docker Compose
- Qwen Cloud API key (or any OpenAI-compatible API for dev)

### 1. Clone & Setup
```bash
git clone https://github.com/your-org/confucius-agent.git
cd confucius-agent
cp .env.example .env
# Edit .env with your API keys
```

### 2. Start Infrastructure
```bash
docker compose up -d
```
Starts: Redis (Raw Facts), PostgreSQL (Observations), ChromaDB (Mental Models)

### 3. Run Demo
```bash
pip install -r requirements.txt
streamlit run demo/app.py
```

### 4. Chat with the Agent
Open http://localhost:8501 and ask anything. The agent:
1. 🏛️ Checks Mental Models first (canonical truth)
2. 📝 Queries Observations (past learnings)
3. 📦 Reviews Raw Facts (current context)
4. 🧠 Answers with priority-ranked knowledge

---

## 📁 Project Structure

```
confucius-agent/
├── confucius/                  # Core library
│   ├── __init__.py
│   ├── config.py               # Dual API config (Qwen ↔ Fallback)
│   ├── qwen_client.py          # OpenAI-compatible client
│   ├── agent.py                # Main agent with tool calling
│   └── memory/
│       ├── mental_models.py    # Layer 1: ChromaDB + embeddings
│       ├── observations.py     # Layer 2: PostgreSQL + time-index
│       ├── raw_facts.py        # Layer 3: Redis + TTL decay
│       └── retrieval_pipeline.py  # Priority-based orchestrator
├── demo/
│   └── app.py                  # Streamlit interface
├── tests/                      # Test suite
├── docker-compose.yml          # Infrastructure as code
├── Dockerfile                  # Demo container
└── requirements.txt            # Python dependencies
```

---

## 🔄 Dual API Mode

Develop with **any OpenAI-compatible API** (DeepSeek, Kimi, OpenAI), then switch to **Qwen Cloud** for submission:

```python
# In .env:
API_MODE=fallback                    # Use during development
FALLBACK_API_KEY=sk-...              # Your dev API key
FALLBACK_BASE_URL=https://api.deepseek.com/v1

# Switch to Qwen Cloud for submission:
API_MODE=qwen
QWEN_API_KEY=sk-...                  # Qwen Cloud hackathon credits
QWEN_BASE_URL=https://dashscope-intl.aliyuncs.com/compatible-mode/v1
```

---

## 📊 Memory Retrieval Pipeline

```
User Query
    │
    ▼
┌─────────────────────────────────────────┐
│       Parallel Query All Tiers          │
├────────────────┬────────────┬───────────┤
│  🏛️ Mental     │ 📝 Obser-  │ 📦 Raw    │
│  Models        │ vations    │ Facts     │
│  (ChromaDB)    │ (Postgres) │ (Redis)   │
└───────┬────────┴─────┬──────┴─────┬─────┘
        │              │            │
        ▼              ▼            ▼
    Priority      Recency       TTL-based
    Score +      Weight ×      Age Check
    Threshold    Confidence
        │              │            │
        └──────────────┴────────────┘
                    │
                    ▼
        Ranked Context (by priority)
                    │
                    ▼
        LLM (Qwen Cloud) → Response
```

---

## 🧪 Testing

```bash
pytest tests/ -v
```

---

## 📝 License

MIT — Open source for the Qwen Cloud Global AI Hackathon 2026

Built with ❤️ by Wagner Solutions AI for the **MemoryAgent** track.
