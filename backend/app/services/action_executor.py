from backend.app.services.razorpay_service import create_payment_link


def execute_action(
    action_type: str,
    transaction_amount: float,
    customer_name: str,
    customer_email: str,
    reference_id: str,
) -> dict:
    if action_type == "PAYMENT_LINK":
        try:
            link = create_payment_link(
                amount_rupees=transaction_amount,
                description="RecoverAI automated payment recovery",
                customer_name=customer_name,
                customer_email=customer_email,
                reference_id=reference_id,
            )
            return {
                "executed": True,
                "real_or_simulated": "real",
                "result": "payment_link_created",
                "details": {"payment_link_id": link["id"], "short_url": link["short_url"]},
            }
        except Exception as e:
            return {
                "executed": False,
                "real_or_simulated": "real",
                "result": "payment_link_creation_failed",
                "details": {"error": str(e)},
            }

    if action_type == "RETRY":
        return {
            "executed": True,
            "real_or_simulated": "simulated",
            "result": "retry_scheduled",
            "details": {},
        }

    if action_type == "CUSTOMER_NUDGE":
        return {
            "executed": True,
            "real_or_simulated": "simulated",
            "result": "nudge_logged",
            "details": {"note": "Would send a reminder message to the customer."},
        }

    if action_type == "ESCALATE":
        return {
            "executed": True,
            "real_or_simulated": "simulated",
            "result": "escalated_to_human_review",
            "details": {},
        }

    return {
        "executed": True,
        "real_or_simulated": "simulated",
        "result": "no_action_taken",
        "details": {},
    }
