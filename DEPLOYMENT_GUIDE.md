# AnemiaCare RAG Backend — Deployment Guide

## Project Structure
```
anemia-rag-backend/
├── app.py                    ← Flask API server
├── rag_engine.py             ← RAG pipeline (FAISS + embeddings)
├── knowledge_base.py         ← All anemia knowledge chunks
├── requirements.txt          ← Python dependencies
├── render.yaml               ← Render.com deploy config
└── ChatbotScreen_updated.jsx ← Updated React Native file
```

---

## Step 1: Push to GitHub

1. Create a new repo on github.com (e.g. `anemiacare-backend`)
2. Run in terminal:
```bash
cd anemia-rag-backend
git init
git add .
git commit -m "Initial RAG backend"
git remote add origin https://github.com/YOUR_USERNAME/anemiacare-backend.git
git push -u origin main
```

---

## Step 2: Deploy on Render.com (FREE)

1. Go to https://render.com → Sign up free
2. Click **New → Web Service**
3. Connect your GitHub → Select `anemiacare-backend`
4. Fill in settings:
   - **Name:** anemiacare-rag-backend
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app --workers 1 --timeout 120`
   - **Instance Type:** Free
5. Add Environment Variable:
   - Key: `OPENROUTER_API_KEY`
   - Value: `sk-or-v1-...` (your key)
6. Click **Create Web Service**

⏳ First deploy takes ~5 minutes (downloads the AI embedding model).

Your URL will be: `https://anemiacare-rag-backend.onrender.com`

---

## Step 3: Update React Native App

In `ChatbotScreen_updated.jsx`, replace line:
```js
const BACKEND_URL = 'https://YOUR-APP-NAME.onrender.com';
```
with your actual Render URL, e.g.:
```js
const BACKEND_URL = 'https://anemiacare-rag-backend.onrender.com';
```

Then replace your existing `ChatbotScreen.jsx` with `ChatbotScreen_updated.jsx`.

---

## Step 4: Test Locally First (Optional)

```bash
cd anemia-rag-backend
pip install -r requirements.txt
export OPENROUTER_API_KEY=sk-or-v1-your-key-here
python app.py
```

Test with curl:
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What foods are good for anemia?", "language": "en"}'
```

---

## How RAG Works (for your FYP presentation)

```
User Question
     ↓
[Embedding Model]  ← converts question to numbers (vector)
     ↓
[FAISS Vector Search]  ← finds most similar knowledge chunks
     ↓
[Top 4 Relevant Facts]  ← e.g. "iron-rich foods", "iron absorption"
     ↓
[System Prompt + Facts + Question]  ← sent to LLM
     ↓
[LLM generates answer]  ← grounded in your knowledge base
     ↓
Response to user
```

This means the AI answers are:
✅ Based on verified anemia facts (not hallucinated)
✅ Specific to your app's domain
✅ Can be extended by adding more chunks to knowledge_base.py

---

## Adding More Knowledge

To add new facts, just add strings to the `ANEMIA_CHUNKS` list in `knowledge_base.py`:

```python
ANEMIA_CHUNKS = [
    # ... existing chunks ...
    "Your new fact about anemia here.",
]
```

Then redeploy — the index rebuilds automatically at startup.

---

## Notes for FYP Report

- **Embedding model:** sentence-transformers/all-MiniLM-L6-v2 (Apache 2.0 license)
- **Vector database:** FAISS by Meta (MIT license)
- **LLM:** Llama 3.1 8B via OpenRouter (free tier)
- **Architecture:** RAG (Retrieval-Augmented Generation)
- **Languages supported:** English, Urdu, Sindhi
