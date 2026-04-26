"""
AnemiaCare RAG Backend — Flask API
------------------------------------
Endpoint:  POST /chat
Deploy to: Render.com (free tier) or Railway.app

Environment variable required:
  OPENROUTER_API_KEY   →  your OpenRouter key
"""

import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import rag_engine

# ── App Setup ───────────────────────────────────────────────
app = Flask(__name__)
CORS(app)  # Allow requests from React Native app

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "meta-llama/llama-3.1-8b-instruct:free"

# ── Initialize RAG at startup ────────────────────────────────
print("[Server] Initializing RAG engine...")
rag_engine.initialize()
print("[Server] RAG engine ready. Starting Flask...")


# ── Health Check ─────────────────────────────────────────────
@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "AnemiaCare RAG Backend"})


# ── Main Chat Endpoint ────────────────────────────────────────
@app.route("/chat", methods=["POST"])
def chat():
    """
    Request body (JSON):
    {
        "message": "What foods should I eat for anemia?",
        "history": [
            {"role": "user",      "content": "..."},
            {"role": "assistant", "content": "..."}
        ],
        "language": "en"   // "en" | "ur" | "sd"
    }

    Response (JSON):
    {
        "reply": "...",
        "sources_used": 3
    }
    """
    if not OPENROUTER_API_KEY:
        return jsonify({"error": "OPENROUTER_API_KEY not set on server"}), 500

    data = request.get_json(silent=True)
    if not data or "message" not in data:
        return jsonify({"error": "Missing 'message' field"}), 400

    user_message = data["message"].strip()
    history       = data.get("history", [])
    language      = data.get("language", "en")

    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    # ── Step 1: Retrieve relevant knowledge chunks ────────────
    relevant_chunks = rag_engine.retrieve(user_message, top_k=4)
    context_text = "\n\n".join(
        [f"[Fact {i+1}]: {chunk}" for i, chunk in enumerate(relevant_chunks)]
    )

    # ── Step 2: Build system prompt with retrieved context ────
    lang_instruction = {
        "en": "Always respond in English.",
        "ur": "ہمیشہ اردو میں جواب دیں۔ (Always respond in Urdu.)",
        "sd": "هميشه سنڌي ۾ جواب ڏيو. (Always respond in Sindhi.)",
    }.get(language, "Always respond in English.")

    system_prompt = f"""You are AnemiaCare Assistant, a helpful health chatbot for an anemia management app used in Pakistan.

RELEVANT KNOWLEDGE (from verified medical sources):
{context_text}

INSTRUCTIONS:
- Answer the user's question using ONLY the facts provided above.
- If the facts don't cover the question, give general safe advice and suggest seeing a doctor.
- Be warm, concise, and clear — maximum 3-4 sentences.
- Never diagnose a medical condition. Always recommend consulting a doctor for serious symptoms.
- {lang_instruction}
- Be culturally sensitive to Pakistani users."""

    # ── Step 3: Build message history for LLM ─────────────────
    # Keep last 6 messages to avoid token overflow
    trimmed_history = history[-6:] if len(history) > 6 else history

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(trimmed_history)
    messages.append({"role": "user", "content": user_message})

    # ── Step 4: Call OpenRouter LLM ───────────────────────────
    try:
        response = requests.post(
            OPENROUTER_URL,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "HTTP-Referer": "https://anemiacare.app",
                "X-Title": "AnemiaCare",
            },
            json={
                "model": MODEL,
                "messages": messages,
                "max_tokens": 512,
                "temperature": 0.5,
            },
            timeout=30,
        )
        response.raise_for_status()
        result = response.json()

        if "choices" in result and result["choices"]:
            reply = result["choices"][0]["message"]["content"].strip()
            return jsonify({
                "reply": reply,
                "sources_used": len(relevant_chunks),
            })
        else:
            error_msg = result.get("error", {}).get("message", "No response from LLM")
            return jsonify({"error": error_msg}), 502

    except requests.exceptions.Timeout:
        return jsonify({"error": "LLM request timed out. Please try again."}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Network error: {str(e)}"}), 502
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500


# ── Run ───────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
