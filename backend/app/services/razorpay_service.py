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
            "sms": False,
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
