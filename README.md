# AuraAI

### An AI-powered academic assistant backend, tailored by role

Built by [Biswarup Goswami](https://github.com/goswamibiswarup369-ops)

Repo: [AuraAI](https://github.com/goswamibiswarup369-ops/AuraAI)

---

## 🌟 About

**AuraAI** is a FastAPI backend that powers an AI assistant designed to adapt its responses based on who's using it — a student, a teacher, or faculty. Rather than a one-size-fits-all chatbot, AuraAI tailors its tone, focus, and depth of response to the user's role, using Groq's fast LLM inference under the hood.

It also automatically detects the latest available, working Groq chat model at runtime — so the app doesn't break every time a model gets renamed or decommissioned.

---

## ✨ Features

- 🎭 **Role-aware responses** — distinct system prompts for:
  - **Student** — an Expert Academic Mentor focused on study tips and simplicity
  - **Teacher** — a Curriculum Specialist focused on lesson plans and pedagogy
  - **Faculty** — an Academic Strategist focused on research and university operations
- 🔄 **Self-healing model selection** — automatically scans your Groq account for the newest valid chat model, filtering out audio/vision/guard models, so you're never stuck on a decommissioned model ID.
- 🎛️ **Configurable depth & temperature** — adjustable per-request via a `settings` object (e.g. response depth, creativity/temperature).
- 🔐 **Secure API key handling** — the Groq API key is loaded from environment variables (`.env`), never hardcoded in source.
- 🌐 **CORS-enabled API** — ready to be called directly from a separate frontend.

---

## 🛠️ Tech Stack

- **Backend**: Python, FastAPI, Pydantic
- **AI**: Groq API (auto-selected chat completion models)
- **Frontend**: Static HTML (`frontend/index.html`)
- **Environment management**: python-dotenv

---

## 📂 Project Structure

```
AuraAI/
├── Backend/
│   ├── app.py             # FastAPI app: model auto-detection + /feature endpoint
│   ├── .env                # GROQ_API_KEY (not committed)
│   └── .gitignore
└── frontend/
    └── index.html          # Frontend interface
```

---

## ⚡ Setup & Run

### 1. Clone the repository
```bash
git clone https://github.com/goswamibiswarup369-ops/AuraAI.git
cd AuraAI/Backend
```

### 2. Install dependencies
```bash
pip install fastapi uvicorn requests python-dotenv
```

### 3. Configure your API key
Create a `.env` file inside `Backend/` with:
```
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Run the server
```bash
uvicorn app:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

### 5. Serve the frontend
Open `frontend/index.html` in your browser (or serve it via a local static server) to interact with the assistant through the UI.

---

## 📡 API

### `POST /feature`

**Request body:**
```json
{
  "feature": "summarize",
  "context": "Explain photosynthesis for a 10th grade class",
  "role": "teacher",
  "settings": {
    "depth": "detailed",
    "temp": 0.5
  }
}
```

**Response:**
```json
{
  "result": "AI-generated response here...",
  "model": "llama-3.3-70b-versatile"
}
```

---

## ⚠️ Notes

- Requires a valid [Groq API key](https://console.groq.com) to function.
- `.env` is excluded from version control — never commit real API keys.

---

## 📄 License

This project is currently unlicensed / all rights reserved by the author. Feel free to reach out via GitHub with questions or feedback.
