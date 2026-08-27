# RecoverAI — Autonomous Revenue Recovery Agent for Razorpay

Built for the Razorpay AI Buildathon (Track 3: AI Revenue Recovery).

RecoverAI is an intelligent, policy-governed agent system that automatically diagnoses payment failures, predicts recovery probability, evaluates expected recovery value, selects optimized recovery actions, and executes them safely within strict policy boundaries.

One-Line Pitch: RecoverAI doesn't just detect failed payments — it decides the safest and highest-value recovery action, executes it within strict policy boundaries, and measures the revenue it actually recovers.

---

## Architecture Overview

+-------------------+     +------------------+     +-----------------------+
| Razorpay Webhook  | --> | Event Collector  | --> |  FastAPI Backend      |
| / Test Mode Cards |     | (Signature Verif)|     | (Database Transaction)|
+-------------------+     +------------------+     +-----------------------+
                                                               |
                                                               v
+-------------------+     +------------------+     +-----------------------+
| Decision Explainer| <-- |  Policy Engine   | <-- | Decision & EV Engine  |
| (Gemini + Fallback)    | (Safety Gate Veto)|     | (Logistic Regression) |
+-------------------+     +------------------+     +-----------------------+
          |                                                    
          v                                                    
+-------------------+     +------------------+                 
| Action Executor   | --> | Audit Trail &    |                 
| (Payment Links)   |     | React Dashboard  |                 
+-------------------+     +------------------+                 

---

## Core Technical Principles

1. Policy Engine Overrides LLM & AI Decision:
   The LLM (Google Gemini) NEVER makes operational payment decisions. It only generates natural language explanations for decisions made by deterministic algorithms. Final authorization resides strictly in a deterministic Policy Engine enforcing rate limits, maximum amount ceilings, and cooldown periods.

2. Transparent Real vs Simulated Boundaries:
   - REAL: Razorpay Test Mode Payment Links, Webhook receipt & HMAC-SHA256 signature verification, ML inference (scikit-learn), PostgreSQL CRUD, and Gemini API calls.
   - SIMULATED: RETRY, CUSTOMER_NUDGE, ESCALATE, and STOP actions (because Razorpay lacks direct APIs for arbitrary retry execution, these are logged internally with real_or_simulated=simulated).

---

## Key Benchmark Results

Evaluated across a full-scale synthetic dataset of 20,000 transactions (5,000 customers):

- Revenue at Risk: Rs 10,07,02,827.98
- Baseline Strategy (Fixed Retries):
  - Net Revenue Recovered: Rs 2,58,34,409.12
  - Recovery Rate: 25.73%
- RecoverAI Agent:
  - Net Revenue Recovered: Rs 3,28,54,635.86
  - Recovery Rate: 32.70%
- Empirical Lift: +27.2% Net Recovery Improvement over Baseline

---

## Machine Learning Model

- Production Model: Logistic Regression (Selected over XGBoost based on higher ROC-AUC: 0.781 vs 0.774).
- Rationale: Logistic Regression naturally fits the linear patterns in payment failure data while offering lightweight, zero-latency inference for real-time webhooks.

---

## Project Structure

recover-ai/
  backend/           FastAPI app, database models, policy & decision engines
  frontend/          React (Vite) + Tailwind CSS dashboard & audit trail UI
  ml/                Model training script & saved production binaries
  simulator/         Synthetic dataset generators & batch simulation engine
  docs/              Honest technical verification reports & architecture docs
  docker-compose.yml Unified containerization setup

---

## Quick Start (Docker)

1. Ensure Docker Desktop is running.
2. Build and launch:
   docker-compose up --build -d
3. Open Dashboard at http://localhost
4. Open API docs at http://localhost:8000/docs
