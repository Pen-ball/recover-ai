# Automated Test Suite

## Coverage

21 automated tests covering the core deterministic logic of RecoverAI:

### Policy Engine (6 tests)
Verifies all 4 safety rules fire correctly: minimum recovery probability,
max retry count, max automated transaction amount, and cooldown period -
both the blocked case AND the approved case for boundary conditions
(e.g. action allowed again once cooldown expires).

### Decision Engine (6 tests)
Verifies the deterministic action selector picks the correct action
across the full range of probability/retry-count scenarios: STOP,
ESCALATE, PAYMENT_LINK, CUSTOMER_NUDGE, RETRY.

### Expected Recovery Value (3 tests)
Verifies the ERV formula's math is correct, that risk penalty increases
with retry count, and that STOP actions have zero intervention cost.

### Webhook Signature Verification (3 tests)
Security-critical: verifies genuinely signed requests are accepted,
invalid signatures are rejected, and a TAMPERED payload with a stolen
valid signature is correctly rejected (simulates an attacker
intercepting and modifying a webhook).

### Diagnosis Service (3 tests)
Verifies Razorpay error codes/reasons correctly map to RecoverAI's
internal failure categories, with correct fallback behavior for
unrecognized inputs.

## Running the Tests

From the project root, with the virtual environment active:

    python -m pytest backend\tests\ -v

## Result

All 21 tests pass in under 1 second. This suite covers both happy paths
and failure paths per project requirements, focusing on the
safety-critical and deterministic components (policy engine, decision
engine, webhook security) that the system's trustworthiness depends on.
