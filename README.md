# RecoverAI

Autonomous Revenue Recovery Agent for Razorpay
Built for the Razorpay AI Buildathon — Track 3: AI Revenue Recovery

## The Problem

Merchants using Razorpay lose revenue when payments fail — bank issues,
insufficient funds, abandoned checkouts, authentication failures. Most
businesses have no systematic way to detect this revenue at risk,
diagnose why it happened, or decide whether and how to recover it.

## The Solution

RecoverAI is a closed-loop AI system that detects failed payments in
real time via Razorpay webhooks, diagnoses the failure, predicts
recovery probability using a trained machine learning model, calculates
expected recovery value, decides on the safest and highest-value
recovery action, checks that decision against deterministic safety
policies, executes the approved action (creating a real Razorpay
Payment Link when appropriate), and records a full audit trail.

One-line pitch: RecoverAI doesn't just detect failed payments — it
decides the safest and highest-value recovery action, executes it
within strict policy boundaries, and measures the revenue it actually
recovers.

## Architecture

See docs/architecture_diagram.md for the full flow diagram.

Razorpay Webhook -> FastAPI Backend -> Diagnosis -> ML Prediction ->
Expected Value -> Decision Engine -> Policy Gate -> Action Executor ->
Audit Trail -> React Dashboard

Critical design principle: the LLM never directly controls payment
actions. It only explains decisions already made by deterministic code.
A separate Policy Engine has final veto authority over any AI-
recommended action.

## Tech Stack

- Backend: FastAPI, SQLAlchemy, PostgreSQL
- ML: scikit-learn (Logistic Regression), XGBoost (compared, not selected)
- AI: Google Gemini (decision explanations only, with tested fallback)
- Payments: Razorpay Python SDK, real Test Mode integration
- Frontend: React, Vite, Tailwind CSS, Recharts
- Testing: pytest (21 automated tests)
- Deployment: Render (backend), Vercel (frontend), Neon (database)

## Real vs Simulated

REAL: Razorpay Test Mode Payment Link creation, webhook receipt and
signature verification, ML inference, LLM calls, database persistence.

SIMULATED (explicitly labeled in code and API responses via a
real_or_simulated field): RETRY, CUSTOMER_NUDGE, ESCALATE, and STOP
actions, since Razorpay has no generic API for these.

## Machine Learning

Trained on a synthetic dataset of 20,000 transactions with engineered,
documented relationships between failure type, customer history, and
recovery outcome (see docs/synthetic_data_assumptions.md). Logistic
Regression and XGBoost were compared honestly; see
docs/ml_model_results.md for full metrics and the reasoning behind
model selection.

## Measured Results

A controlled batch experiment compared a simple Baseline strategy
against the full RecoverAI pipeline on the same 20,000 transactions.

[PASTE YOUR ACTUAL RUN 2 NUMBERS HERE FROM docs/batch_experiment_results.md]

Full methodology in docs/batch_experiment_results.md.

## Safety and Policy Engine

Four deterministic rules govern every AI-recommended action: minimum
recovery probability, maximum retry count, maximum transaction amount
for fully-automated actions, and a cooldown period between actions on
the same case. All four rules are individually tested; see
docs/testing.md.

## Setup Instructions

1. Clone the repo: git clone [YOUR REPO URL]
2. Backend: cd backend, pip install -r requirements.txt
3. Create a .env file (see .env.example for required variables)
4. Run database migrations: python -m backend.app.db.create_tables
5. Start backend: uvicorn backend.app.main:app --reload
6. Frontend: cd frontend, npm install, npm run dev

## Environment Variables Required

DATABASE_URL, GEMINI_API_KEY, RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET,
RAZORPAY_WEBHOOK_SECRET

## Testing

python -m pytest backend/tests/ -v

21 automated tests covering the policy engine, decision engine,
expected value calculations, webhook signature verification, and
diagnosis mapping. See docs/testing.md.

## Live Demo

Frontend: [YOUR VERCEL URL]
Backend API docs: [YOUR RENDER URL]/docs

## Limitations

- Synthetic data is used for ML training and batch experimentation,
  clearly documented as such throughout.
- Simulated actions (RETRY, CUSTOMER_NUDGE, ESCALATE, STOP) reflect the
  real constraint that Razorpay has no generic API for these operations.
- Free-tier hosting means the backend may take 30-60 seconds to respond
  after periods of inactivity (cold start).

## Future Improvements

- Real SMS/email delivery for CUSTOMER_NUDGE actions
- Merchant-configurable policy thresholds via a settings UI
- Support for subscription/recurring payment recovery flows
- A/B testing framework for comparing decision strategies live

## Documentation

Full methodology and verification documents are in the docs/ folder,
including synthetic data assumptions, ML model results, batch
experiment results, Razorpay Test Mode verification, webhook
integration verification, end-to-end pipeline verification, and the
testing suite documentation.