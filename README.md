# RecoverAI

Autonomous Revenue Recovery Agent for Razorpay
Built for the Razorpay AI Buildathon — Track 3: AI Revenue Recovery

## The Problem
Merchants using Razorpay lose revenue when payments fail. Most have no
systematic way to detect this revenue at risk, diagnose why, or decide
whether and how to recover it.

## The Solution
RecoverAI detects failed payments in real time via Razorpay webhooks,
diagnoses the failure, predicts recovery probability with a trained ML
model, calculates expected recovery value, decides on the safest and
highest-value action, checks that decision against deterministic safety
policy, executes the approved action (creating a real Razorpay Payment
Link when appropriate), and records a full audit trail.

## Architecture
See docs/architecture_diagram.md.
Critical design principle: the LLM never directly controls payment
actions. It only explains decisions already made by deterministic code.
A separate Policy Engine has final veto authority.

## Tech Stack
FastAPI, SQLAlchemy, PostgreSQL (Neon), scikit-learn, XGBoost (compared),
Google Gemini, Razorpay Python SDK, React, Vite, Tailwind CSS, pytest.
Deployed: Render (backend), Vercel (frontend), Neon (database).

## Real vs Simulated
REAL: Razorpay Test Mode Payment Link creation, webhook signature
verification, ML inference, LLM calls, database persistence.
SIMULATED (labeled via real_or_simulated field): RETRY, CUSTOMER_NUDGE,
ESCALATE, STOP actions - Razorpay has no generic API for these.

## Measured Results
[PASTE YOUR REAL 20,000-transaction Run 2 numbers from
docs/batch_experiment_results.md here]

## Live Demo
Frontend: https://recover-ai-gamma.vercel.app
Backend docs: https://recoverai-backend-cylo.onrender.com/docs

## Setup
1. git clone [your repo URL]
2. cd backend, pip install -r requirements.txt
3. Create .env (see .env.example)
4. python -m backend.app.db.create_tables
5. uvicorn backend.app.main:app --reload
6. cd frontend, npm install, npm run dev

## Testing
python -m pytest backend/tests/ -v
21 automated tests - see docs/testing.md

## Documentation
Full methodology docs in docs/ folder.

## Limitations
- Synthetic data used for ML training, documented as such throughout.
- Simulated actions reflect real Razorpay API constraints, not shortcuts.
- Free-tier hosting may show a brief delay on first request after idle.

## Future Improvements
- Real SMS/email delivery for nudges
- Merchant-configurable policy thresholds
- Subscription/recurring payment recovery support
