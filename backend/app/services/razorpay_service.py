# Razorpay Service
#
# Wraps Razorpay's official Python SDK to create real Test Mode Payment
# Links. This is REAL Razorpay Test Mode integration - not simulated.
# No live money is ever involved; Test Mode uses sandboxed test cards.

import os
import razorpay
from dotenv import load_dotenv

load_dotenv()

_client = None


def get_client():
    global _client
    if _client is None:
        key_id = os.getenv("RAZORPAY_KEY_ID")
        key_secret = os.getenv("RAZORPAY_KEY_SECRET")
        _client = razorpay.Client(auth=(key_id, key_secret))
    return _client


def create_payment_link(
    amount_rupees: float,
    description: str,
    customer_name: str,
    customer_email: str,
    customer_contact: str = None,
    reference_id: str = None,
) -> dict:
    """
    Creates a real Razorpay Test Mode Payment Link.

    amount_rupees is converted to paise (Razorpay's smallest currency unit
    for INR - 1 rupee = 100 paise), since the Razorpay API expects amounts
    in the smallest currency unit, not decimal rupees.
    """
    client = get_client()

    amount_paise = int(round(amount_rupees * 100))

    payload = {
        "amount": amount_paise,
        "currency": "INR",
        "description": description,
        "customer": {
            "name": customer_name,
            "email": customer_email,
        },
        "notify": {
            "sms": False,  # keep False for dev/testing to avoid real SMS sends
            "email": False,
        },
        "reminder_enable": False,
    }

    if customer_contact:
        payload["customer"]["contact"] = customer_contact

    if reference_id:
        payload["reference_id"] = reference_id

    payment_link = client.payment_link.create(payload)
    return payment_link
