# 🧠 Trustworthy RAG-Powered Customer Support Bot

> A Retrieval-Augmented Generation (RAG) system for multi-domain customer support, comparing **LLaMA**, **Mistral 7B**, and **Gemma** as LLM backends.

**Course:** DSCI 6004 — Natural Language Processing, Spring 2025  
**Authors:** Rohit Kumar Sah and Jagadish Kumar Pakalapati  
**Paper:** [`NLP_Final_Report.docx`](NLP_Final_Report.docx)

---

## 📋 Table of Contents

1. [Project Overview](#-project-overview)
2. [System Architecture](#-system-architecture)
3. [Repository Structure](#-repository-structure)
4. [Quick Start](#-quick-start)
5. [Installation](#-installation)
6. [Running the App](#-running-the-app)
7. [Knowledge Base](#-knowledge-base)
8. [How It Works](#-how-it-works)
9. [Evaluation Benchmark](#-evaluation-benchmark)
10. [Results Summary](#-results-summary)
11. [Extending the System](#-extending-the-system)
12. [Known Limitations](#-known-limitations)
13. [Output Demo](#-Output-Demo)


---

## 🔍 Project Overview

This project implements a **trustworthy RAG-powered customer support bot** that grounds every response in a verifiable external knowledge base — eliminating hallucination by design. Instead of relying on a language model's parametric memory, the system:

1. **Retrieves** the most relevant support document for each user query using dual-method retrieval (BM25 + semantic scoring)
2. **Detects intent** from the query (password reset, refund, billing, shipping, or fallback)
3. **Generates a grounded answer** using one of three selectable LLM backends
4. **Displays both retrieval results** side-by-side so users can verify the source

The system is deployed as an interactive **Streamlit** web application and supports knowledge bases built from real-world customer support documentation.

### Why RAG for Customer Support?

| Problem with vanilla LLMs | How RAG solves it |
|---|---|
| Hallucinate confident but wrong answers | Answers grounded in retrieved documents |
| Stale knowledge after training cutoff | Knowledge base updated independently |
| No source traceability | Retrieved document shown alongside answer |
| Expensive to retrain per domain | Swap knowledge base without touching the model |

---

## 🏗 System Architecture

```
User Query
    │
    ├──────────────────────────────────┐
    ▼                                  ▼
BM25Okapi                     Semantic Scorer
(rank_bm25)                   (word-overlap)
    │                                  │
    └──────────────┬───────────────────┘
                   ▼
          Knowledge Base (5 docs)
          Microsoft · FedEx · Apple · Google
                   │
                   ▼ top-1 document
          Intent Detection
          password | refund | billing | shipping | fallback
                   │
                   ▼ base answer
    ┌──────────────┼──────────────┐
    ▼              ▼              ▼
  LLaMA        Mistral 7B      Gemma
 (concise)    (+ elaboration)  (simple)
    └──────────────┼──────────────┘
                   ▼
         Streamlit Response Panel
         (answer + dual retrieval display)
```

---

## 📁 Repository Structure

```
rag-customer-support-bot/
│
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── .gitignore
├── README.md                       # This file
│
├── data/                           # Knowledge base documents
│   ├── microsoft_support.txt       # Microsoft Support homepage
│   ├── fedex_tracking.txt          # FedEx shipment tracking page
│   ├── apple_support_refund.txt    # Apple Support — App Store refunds
│   ├── apple_support_refund_2.txt  # Apple Support — duplicate (retrieval test)
│   └── google_account_help.txt     # Google Account — password help
│
├── docs/
│   └── rag_paper_final.docx        # Full conference-style research paper
│
└── slides/
    └── (add presentation slides here)
```

---

## ⚡ Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/rag-customer-support-bot.git
cd rag-customer-support-bot

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501` in your browser.

---

## 🛠 Installation

### Prerequisites

| Requirement | Version |
|---|---|
| Python | 3.9 or higher |
| pip | Latest recommended |
| OS | Windows / macOS / Linux |
| RAM | 4 GB minimum |
| GPU | Not required (CPU-only deployment) |

### Step-by-Step

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/rag-customer-support-bot.git
cd rag-customer-support-bot
```

**2. Create a virtual environment** (strongly recommended)
```bash
python -m venv venv
source venv/bin/activate    # macOS/Linux
venv\Scripts\activate       # Windows
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Fix the data folder path in app.py**

Open `app.py` and update `doc_path` on line ~13:
```python
# Change this:
doc_path = r"/Users/rohitkumarsah/Desktop/rag_app/data"

# To this (works on any machine):
doc_path = os.path.join(os.path.dirname(__file__), "data")
```

---

## 🚀 Running the App

```bash
streamlit run app.py
```

### Using the Interface

| UI Element | Description |
|---|---|
| **Ask your question** | Type any customer support question |
| **Select Model** | Choose LLaMA, Mistral, or Gemma from the dropdown |
| **Generate Answer** | Click to run retrieval + answer generation |
| **Final Answer panel** | The model's formatted response |
| **BM25 Result** | Top document from keyword-weighted retrieval |
| **FAISS Result** | Top document from semantic word-overlap retrieval |
| **Sidebar** | Shows how many documents are loaded |

### Example Queries to Try

```
How do I reset my Google password?
How do I request a refund for an App Store purchase?
How do I track my FedEx package?
How do I update my billing information?
I was charged for a subscription I didn't want. What do I do?
```

---

## 📚 Knowledge Base

The system comes pre-loaded with five customer support documents covering four domains:

| File | Domain | Topics |
|---|---|---|
| `microsoft_support.txt` | Microsoft | Account sign-in, Microsoft 365, Copilot, devices |
| `fedex_tracking.txt` | FedEx | Shipment tracking, delivery management, door tags |
| `apple_support_refund.txt` | Apple | App Store refund requests, iTunes, Apple Books |
| `apple_support_refund_2.txt` | Apple | Duplicate — used to test retrieval consistency |
| `google_account_help.txt` | Google | Password change, account recovery, sign-in |

### Adding Your Own Documents

To extend the knowledge base with new support articles:

1. Save the document as a plain `.txt` file
2. Place it in the `data/` folder
3. Restart the Streamlit app — it auto-loads all `.txt` files in the folder

```bash
# Example: adding an AWS support page
echo "Your AWS support content here..." > data/aws_support.txt
streamlit run app.py
```

**Tips for best results:**
- Use **article-level pages** rather than homepage/navigation pages
- Keep documents under ~2,000 tokens for clean BM25 scoring
- Use consistent domain terminology so BM25 keyword matching is effective

---

## ⚙️ How It Works

### 1. Retrieval

Two methods run in parallel on every query:

**BM25 (Sparse retrieval)**
```python
from rank_bm25 import BM25Okapi
tokenized_docs = [doc.lower().split() for doc in documents]
bm25 = BM25Okapi(tokenized_docs)
scores = bm25.get_scores(query.lower().split())
best_doc = documents[np.argmax(scores)]
```
BM25 weights rare query terms higher — excellent for domain-specific terminology like "refund", "tracking number", "password reset".

**Semantic scorer (Lightweight)**
```python
def faiss_search(query):
    for doc in documents:
        score = sum(word in doc.lower() for word in query.lower().split())
    # returns doc with highest word-overlap score
```
Counts how many query words appear in each document. Handles broad/open-ended queries better than BM25.

The **semantic result** is passed as context to the answer generator. Both results are displayed in the UI for transparency.

### 2. Intent Detection

```
if "password" in query   →  password response
elif "refund" in query   →  refund response
elif "billing" in query  →  billing response
elif "shipping" in query →  shipping response
else                     →  context[:200]  (fallback)
```

### 3. Model-Specific Formatting

| Model | Format | Verbosity |
|---|---|---|
| **LLaMA** | `🧠 LLaMA Response:\n\n{answer}` | Low |
| **Mistral** | `⚡ Mistral Response (Detailed):\n\n{answer}\n\nThis provides more explanation.` | Medium |
| **Gemma** | `💎 Gemma Response (Simple):\n\n{answer}` | Low |

---

## 📝 Evaluation Benchmark

We evaluated the system on 15 domain-specific questions:

| # | Question | Intent | Source |
|---|---|---|---|
| Q1 | How do I reset a forgotten Microsoft account password? | password | Microsoft |
| Q2 | What are the steps to request a refund for an App Store purchase? | refund | Apple |
| Q3 | How can I track my FedEx package? | shipping | FedEx |
| Q4 | How do I change my Google Account password? | password | Google |
| Q5 | What happens to my other devices after I change my Google password? | password | Google |
| Q6 | How do I update my billing information on my Microsoft account? | billing | Microsoft |
| Q7 | I was charged for a subscription I did not want. How do I get a refund? | refund | Apple |
| Q8 | How long does FedEx standard shipping usually take? | shipping | FedEx |
| Q9 | I cannot find the Apple charge on reportaproblem.apple.com. What should I do? | refund | Apple |
| Q10 | How do I sign in to Microsoft 365? | fallback | Microsoft |
| Q11 | How do I set up FedEx Delivery Manager to redirect a package? | shipping | FedEx |
| Q12 | What should I do if my Google Account password reset email never arrives? | password | Google |
| Q13 | Can a family organizer request a refund for a family member's Apple purchase? | refund | Apple |
| Q14 | How do I install Microsoft 365 after purchasing a subscription? | fallback | Microsoft |
| Q15 | What tools does Microsoft provide to report a security or privacy concern? | fallback | Microsoft |

---

## 📊 Results Summary

### Retrieval Accuracy

| Method | Overall | Keyword queries | Fallback queries |
|---|---|---|---|
| BM25 | **86.7%** | **100%** | 33.3% |
| Semantic scorer | 80.0% | 91.7% | **66.7%** |

### Response Quality (1–5 scale, manual evaluation, mean across 15 questions)

| Dimension | LLaMA | Mistral | Gemma |
|---|---|---|---|
| Faithfulness | **4.3** | 4.1 | **4.3** |
| Answer Relevancy | 4.2 | **4.4** | 4.0 |
| Completeness | 3.9 | **4.5** | 3.6 |
| Conciseness | 4.1 | 3.2 | **4.6** |
| **Overall mean** | **4.13** | 4.05 | **4.13** |

### Key Findings

- **LLaMA** — Best overall balance; reliable, faithful, on-topic. Recommended for general-purpose deployment.
- **Mistral** — Best for complex queries needing elaboration; highest completeness score.
- **Gemma** — Best for simple/high-volume queries; most concise and token-efficient.
- **BM25 is the stronger retriever** on keyword-intent queries (100% accuracy).
- **Retrieval quality is the primary bottleneck** — all models fail equally when the retrieved document is poor quality.

---

## 🔧 Extending the System

### Swap in a Live LLM via Ollama

```python
import requests

def generate_answer_llm(context, query, model_name):
    prompt = f"""Answer using ONLY the context below.
Context: {context}
Question: {query}
Answer:"""
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": model_name,   # "llama3", "mistral", or "gemma"
        "prompt": prompt,
        "stream": False
    })
    return response.json()["response"]
```

Install Ollama from [ollama.com](https://ollama.com), then:
```bash
ollama pull llama3
ollama pull mistral
ollama pull gemma
```

### Upgrade to Dense Retrieval (Sentence-Transformers + FAISS)

```python
from sentence_transformers import SentenceTransformer
import faiss, numpy as np

embedder = SentenceTransformer("all-MiniLM-L6-v2")
doc_embeddings = embedder.encode(documents, convert_to_numpy=True)
index = faiss.IndexFlatIP(doc_embeddings.shape[1])
faiss.normalize_L2(doc_embeddings)
index.add(doc_embeddings)

def dense_search(query, k=1):
    q_emb = embedder.encode([query], convert_to_numpy=True)
    faiss.normalize_L2(q_emb)
    _, I = index.search(q_emb, k)
    return documents[I[0][0]]
```

Install: `pip install sentence-transformers faiss-cpu`

### Add Conversational Memory

```python
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display history
for msg in st.session_state.chat_history:
    st.chat_message(msg["role"]).write(msg["content"])

# Append to history
st.session_state.chat_history.append({"role": "user", "content": query})
st.session_state.chat_history.append({"role": "assistant", "content": answer})
```

### Hybrid BM25 + Dense Retrieval

```python
def hybrid_search(query, alpha=0.5):
    bm25_scores = bm25.get_scores(query.lower().split())
    dense_scores = dense_similarities(query)   # from FAISS
    combined = alpha * normalize(bm25_scores) + (1 - alpha) * normalize(dense_scores)
    return documents[np.argmax(combined)]
```

---

## ⚠️ Known Limitations

| Limitation | Impact | Suggested Fix |
|---|---|---|
| Homepage docs contain nav text | Fallback queries return menu items, not answers | Use article-level URLs for scraping |
| Intent detection is keyword-only | Synonyms like "charged" don't trigger "billing" | Use a small intent classifier or embedding similarity |
| No multi-turn memory | Each query is independent | Add `st.session_state` chat history |
| Word-overlap ≠ true semantic search | Misses paraphrases and synonyms | Replace with Sentence-Transformers + FAISS |
| Fixed `doc_path` in app.py | Breaks on other machines | Change to `os.path.dirname(__file__)` |
| 5-document knowledge base | Limited topic coverage | Add more support articles per domain |
| No RAGAS automated evaluation | Manual scoring only | Integrate RAGAS with OpenAI judge model |

---


### Key References

- Lewis et al. (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.* NeurIPS.
- Jiang et al. (2023). *Mistral 7B.* arXiv:2310.06825.
- Touvron et al. (2023). *LLaMA: Open and Efficient Foundation Language Models.* arXiv:2302.13971.
- Google DeepMind (2024). *Gemma: Open Models Based on Gemini Research and Technology.*
- Es et al. (2023). *RAGAS: Automated Evaluation of Retrieval Augmented Generation.* arXiv:2309.15217.
- Robertson & Zaragoza (2009). *The Probabilistic Relevance Framework: BM25 and Beyond.*

---
### Output Demo
<img width="1600" height="676" alt="image" src="https://github.com/user-attachments/assets/95f2b821-c777-42ef-9c07-3a80673944b4" />
<img width="1600" height="696" alt="image" src="https://github.com/user-attachments/assets/5e6a7629-f4b6-4b92-943e-17208701d780" />

---

<div align="center">
Built with ❤️ for DSCI 6004 · Spring 2025
</div>
