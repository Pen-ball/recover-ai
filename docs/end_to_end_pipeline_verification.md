# End-to-End Pipeline - Verified Live

## What Was Built

The full RecoverAI closed loop is now wired into the live Razorpay
webhook flow. When a real payment.failed event arrives:

1. Customer is found or created (matched by email).
2. Transaction is recorded with status=failed.
3. Failure is diagnosed: Razorpay's real error_code/error_reason is
   mapped to RecoverAI's internal failure categories.
4. ML model predicts recovery probability (trained model, real inference).
5. Expected Recovery Value is calculated (deterministic formula).
6. Decision Engine selects a candidate action .
7. Policy Engine approves or blocks it .
8. LLM (Gemini) generates a human-readable explanation, with automatic
   fallback if unavailable.
9. Action Executor carries out the final action - creates a REAL
   Razorpay Payment Link for PAYMENT_LINK actions, or logs a clearly
   labeled SIMULATED action for RETRY/CUSTOMER_NUDGE/ESCALATE/STOP.
10. Every step is written to the audit_logs table with timestamps,
    decisions, and reasons.

## Verified Live Run

A real Test Mode payment was intentionally failed (insufficient balance
scenario). Result, entirely from real code execution:

- Transaction: Rs 650.00, diagnosed as insufficient_balance
- ML-predicted recovery probability: 46.9%
- Decision: CUSTOMER_NUDGE (moderate probability - not high enough for
  an immediate Payment Link, not low enough to stop)
- Policy: APPROVED (no rules violated)
- Expected Recovery Value: Rs 299.91
- LLM explanation generated successfully, correctly referencing the
  failure reason and expected value
- Action executed (simulated - CUSTOMER_NUDGE has no real Razorpay API
  equivalent, correctly labeled as such)
- Full audit trail recorded: payment_failure_detected -> policy_evaluated
  -> action_executed, each with timestamp and reasoning

## Real vs Simulated in This Flow

- REAL: webhook receipt, signature verification, ML inference, LLM call,
  database writes, and Payment Link creation (when action = PAYMENT_LINK).
- SIMULATED (clearly labeled via real_or_simulated field): RETRY,
  CUSTOMER_NUDGE, ESCALATE, STOP actions, since Razorpay has no generic
  API for these - documented honestly per project requirements.

## Debugging Notes (honest record)

- Multiple stale PowerShell windows from earlier terminal sessions caused confusion
  about which server instance was actually running the latest code.
  Resolved by closing all terminals and restarting exactly two tracked
  windows (server + tunnel) from scratch.
- ngrok's free tier assigned the same stable forwarding URL across
  restarts in this session, so the webhook URL registered in Razorpay's
  dashboard did not need to be updated.
