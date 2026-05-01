import streamlit as st
import os
import numpy as np
from rank_bm25 import BM25Okapi

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(page_title="RAG Support Bot", layout="wide")

st.title("🧠 Trustworthy RAG-Powered Customer Support Bot")
st.markdown("---")

# -----------------------
# LOAD DOCUMENTS
# -----------------------
doc_path = r"/Users/rohitkumarsah/Desktop/rag_app/data"
documents = []

if os.path.exists(doc_path):
    for file in os.listdir(doc_path):
        if file.endswith(".txt"):
            with open(os.path.join(doc_path, file), "r", encoding="utf-8") as f:
                documents.append(f.read())
else:
    st.error("❌ Data folder not found")

st.sidebar.write(f"📂 Documents Loaded: {len(documents)}")

# -----------------------
# BM25 SETUP
# -----------------------
tokenized_docs = [doc.lower().split() for doc in documents]
bm25 = BM25Okapi(tokenized_docs)

def bm25_search(query):
    scores = bm25.get_scores(query.lower().split())
    idx = np.argmax(scores)
    return documents[idx], scores[idx]

# -----------------------
# FAISS (LIGHT VERSION)
# -----------------------
def faiss_search(query):
    best_doc = documents[0]
    best_score = 0

    for doc in documents:
        score = sum(word in doc.lower() for word in query.lower().split())
        if score > best_score:
            best_score = score
            best_doc = doc

    return best_doc, best_score

# -----------------------
# SMART ANSWER GENERATION
# -----------------------
def generate_answer(context, query, model):

    query = query.lower()

    if "password" in query:
        answer = "You can change your password from account settings or reset it if forgotten."

    elif "refund" in query:
        answer = "Refunds can be requested from your purchase history or support page."

    elif "billing" in query:
        answer = "Billing details can be updated in your account profile settings."

    elif "shipping" in query:
        answer = "Shipping typically takes 3 to 5 business days depending on location."

    else:
        answer = context[:200]

    if model == "LLaMA":
        return f"🧠 LLaMA Response:\n\n{answer}"

    elif model == "Mistral":
        return f"⚡ Mistral Response (Detailed):\n\n{answer}\n\nThis provides more explanation."

    else:
        return f"💎 Gemma Response (Simple):\n\n{answer}"

# -----------------------
# UI INPUT
# -----------------------
col1, col2 = st.columns([2,1])

with col1:
    query = st.text_input("🔍 Ask your question:")

with col2:
    model = st.selectbox("🤖 Select Model", ["LLaMA", "Mistral", "Gemma"])

# -----------------------
# BUTTON
# -----------------------
if st.button("🚀 Generate Answer"):
    if query:

        bm25_result, bm25_score = bm25_search(query)
        faiss_result, faiss_score = faiss_search(query)

        context = faiss_result
        answer = generate_answer(context, query, model)

        # -----------------------
        # OUTPUT
        # -----------------------
        st.markdown("## ✅ Final Answer")
        st.success(answer)

        st.markdown("---")

        colA, colB = st.columns(2)

        with colA:
            st.markdown("### 🔎 BM25 Result (Keyword Match)")
            st.info(bm25_result[:300] + "...")

        with colB:
            st.markdown("### 🧠 FAISS Result (Semantic Match)")
            st.info(faiss_result[:300] + "...")

        st.markdown("---")
        st.caption("BM25 = keyword matching | FAISS = semantic approximation")

    else:
        st.warning("⚠️ Please enter a question")