# Predictive-Care-AI

Next‑generation multi‑agent intelligence for proactive health orchestration and personalized care.

## Overview
- Backend: Python Flask API orchestrating four agents (Risk, RAG, Recommendation, Memory).
- Frontend: React (Vite) interface collecting biometrics and visualizing agent outputs.
- LLM providers: OpenAI, Groq, Gemini with automatic fallback; local SQLite memory, optional Supabase.

## Architecture
- RiskPredictionAgent: RandomForest model predicts risk level from `age`, `bmi`, `bp`, `sugar`, `lifestyle` and adds a concise LLM interpretation.
- MedicalKnowledgeAgent (RAG): Retrieves evidence‑based guidelines (SentenceTransformers + FAISS). Falls back to safe defaults if embeddings unavailable.
- RecommendationAgent: Synthesizes a structured, personalized care plan from risk and guidelines.
- MemoryAgent: Persists recent interactions to `backend/data/health_memory.db` (SQLite). Optional cloud sync via Supabase.
- OrchestratorAgent: Coordinates all agents and returns a single structured response.

## API
Base URL: `http://localhost:5000`

- `GET /api/health-check`
  - Returns service status.

- `POST /api/analyze`
  - Body:
    ```json
    {
      "user_data": { "age": 35, "bmi": 24.2, "bp": 120, "sugar": 95, "lifestyle": "Moderate" },
      "history": []
    }
    ```
  - Response (example):
    ```json
    {
      "risk_analysis": { "risk_level": "Medium", "explanation": "..." },
      "guidelines": ["..."],
      "recommendation": "Markdown plan ..."
    }
    ```

## Setup
### Prerequisites
- Python 3.10+
- Node.js 18+

### Backend
1. Create env file at repo root:
   ```
   OPENAI_API_KEY=...
   GROQ_API_KEY=...
   GOOGLE_API_KEY=...
   SUPABASE_URL=...
   SUPABASE_KEY=...
   ```
2. Install and run:
   ```powershell
   cd d:\preventivecare\backend
   python -m venv .venv
   .\.venv\Scripts\Activate
   pip install -r requirements.txt
   python app.py
   ```
   - First run will train or load the risk model and initialize RAG.

### Frontend
```powershell
cd d:\preventivecare\frontend
npm install
npm run dev
```
- UI expects backend at `http://localhost:5000`. Adjust `App.jsx` if using a different host/port.

## Training a Real Risk Model
A starter dataset is included at `AI_in_HealthCare_Dataset.csv`.
```powershell
cd d:\preventivecare\backend
python train_risk_model.py
```
Saves model to `backend/models/risk_model.pkl` and encoders to `backend/models/le.pkl`.

## Environment Variables
- `OPENAI_API_KEY`, `GROQ_API_KEY`, `GOOGLE_API_KEY`: any subset works; provider fallback is automatic.
- `SUPABASE_URL`, `SUPABASE_KEY`: optional; enable cloud memory.
- `PORT`: optional; defaults to `5000`.

## Data & Storage
- Local memory DB: `backend/data/health_memory.db` (auto‑created).
- Models: `backend/models/` (`risk_model.pkl`, `le.pkl`).

## Security
- `.env` is ignored via `.gitignore`. Never commit secrets.
- Use GitHub Repository Secrets for CI/CD and deployments.

## Troubleshooting
- "System Error: No valid LLM API keys": add at least one provider key to `.env`.
- RAG disabled: if SentenceTransformers or FAISS cannot initialize, default guidelines are used.
- CORS/connection issues: ensure backend on `5000` and frontend dev server is running.

## Project Structure
```
preventivecare/
├── backend/      # Flask API + agents, models, utils
├── frontend/     # React (Vite) UI
├── AI_in_HealthCare_Dataset.csv
└── README.md
```

## License
For educational and prototyping purposes. Replace or add license as needed.