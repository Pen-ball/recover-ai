# Tests for Razorpay webhook signature verification.
#
# Verifies our webhook endpoint correctly accepts genuinely signed
# requests and rejects requests with invalid/tampered signatures - this
# is what prevents attackers from sending fake webhook events.

import hmac
import hashlib
import razorpay


TEST_SECRET = "test_webhook_secret_12345"


def _sign(body: str, secret: str) -> str:
    return hmac.new(
        secret.encode("utf-8"), body.encode("utf-8"), hashlib.sha256
    ).hexdigest()


def test_valid_signature_is_accepted():
    body = '{"event": "payment.failed", "id": "evt_test123"}'
    valid_signature = _sign(body, TEST_SECRET)

    client = razorpay.Client(auth=("dummy", "dummy"))
    # Should NOT raise an exception for a genuinely matching signature
    client.utility.verify_webhook_signature(body, valid_signature, TEST_SECRET)


def test_invalid_signature_is_rejected():
    body = '{"event": "payment.failed", "id": "evt_test123"}'
    wrong_signature = "0000000000000000000000000000000000000000000000000000000000000000"

    client = razorpay.Client(auth=("dummy", "dummy"))
    try:
        client.utility.verify_webhook_signature(body, wrong_signature, TEST_SECRET)
        assert False, "Expected SignatureVerificationError to be raised"
    except razorpay.errors.SignatureVerificationError:
        pass  # correctly rejected


def test_tampered_body_is_rejected():
    original_body = '{"event": "payment.failed", "id": "evt_test123"}'
    valid_signature = _sign(original_body, TEST_SECRET)

    # Attacker modifies the body AFTER the signature was generated
    tampered_body = '{"event": "payment.failed", "id": "evt_HACKED"}'

    client = razorpay.Client(auth=("dummy", "dummy"))
    try:
        client.utility.verify_webhook_signature(tampered_body, valid_signature, TEST_SECRET)
        assert False, "Expected SignatureVerificationError to be raised"
    except razorpay.errors.SignatureVerificationError:
        pass  # correctly rejected
