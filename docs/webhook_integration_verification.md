# Webhook Integration - Verified

## What Was Built

A real webhook endpoint (POST /webhooks/razorpay) that:
1. Verifies the X-Razorpay-Signature header using HMAC-SHA256 via the
   official razorpay Python SDK utility, confirming requests genuinely
   originate from Razorpay.
2. Rejects requests with invalid signatures (400 error).
3. Parses the verified payload and extracts the event type.
4. Checks for duplicate events using the webhook_events table's unique
   constraint on razorpay_event_id, before any processing.
5. Stores new events with full payload for audit purposes.
6. Responds quickly (per Razorpay's requirement for fast webhook
   acknowledgment).

## Infrastructure Used

- ngrok: creates a temporary public HTTPS tunnel to the local FastAPI
  server (localhost:8000), since Razorpay's servers cannot reach a
  local machine directly. Used only for local development - a real
  deployment (Phase 19) will have a permanent public URL instead.
- Webhook registered in Razorpay Dashboard (Test Mode) with events:
  payment.failed, payment_link.paid (plus Razorpay automatically
  triggers related events like payment.captured and order.paid on
  successful payments).

## Verified Results

- 6 real webhook events successfully received, signature-verified, and
  stored, triggered by 2 real Test Mode payment completions.
- Event types observed: payment_link.paid, payment.captured, order.paid.
- Duplicate event insert attempt correctly blocked by database
  IntegrityError (unique constraint on razorpay_event_id), confirmed via
  direct test.

## Debugging Notes (honest record)

- Initial 500 errors were caused by the FastAPI server having started
  BEFORE the RAZORPAY_WEBHOOK_SECRET was added to .env. Since
  load_dotenv() only reads environment variables at process startup,
  restarting the server was required after any .env change. This is a
  common gotcha worth remembering for future phases too.
- A transient DNS/connection error occurred once when calling the
  Razorpay API directly (unrelated to webhooks) - resolved on retry,
  confirmed to be a temporary network blip and not a code or
  configuration issue.
