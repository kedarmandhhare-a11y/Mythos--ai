import os
import stripe
from datetime import datetime


class StripeBilling:
    """
    MYTHOS V4 - SaaS Stripe Billing Engine
    Production-ready subscription system
    """

    def __init__(self):
        self.secret_key = os.getenv("STRIPE_SECRET_KEY")
        self.webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

        if self.secret_key:
            stripe.api_key = self.secret_key

        # ==================================
        # SAAS PRODUCT PLANS
        # ==================================
        self.products = {
            "pro": {
                "price_id": os.getenv("STRIPE_PRO_PRICE_ID"),
                "name": "Pro Plan"
            },
            "enterprise": {
                "price_id": os.getenv("STRIPE_ENTERPRISE_PRICE_ID"),
                "name": "Enterprise Plan"
            }
        }

    # ==================================
    # READY CHECK
    # ==================================
    def is_ready(self):
        return self.secret_key is not None and self.webhook_secret is not None

    # ==================================
    # CREATE CHECKOUT SESSION
    # ==================================
    def create_checkout_session(self, user_id: str, plan: str, success_url: str, cancel_url: str):

        try:
            if plan not in self.products:
                return {
                    "status": "error",
                    "error": "Invalid plan"
                }

            price_id = self.products[plan]["price_id"]

            if not price_id:
                return {
                    "status": "error",
                    "error": "Price ID not configured"
                }

            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                mode="subscription",
                line_items=[
                    {
                        "price": price_id,
                        "quantity": 1
                    }
                ],
                metadata={
                    "user_id": user_id,
                    "plan": plan
                },
                success_url=success_url,
                cancel_url=cancel_url
            )

            return {
                "status": "success",
                "checkout_url": session.url,
                "session_id": session.id
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    # ==================================
    # VERIFY WEBHOOK
    # ==================================
    def verify_webhook(self, payload: bytes, sig_header: str):

        try:
            event = stripe.Webhook.construct_event(
                payload,
                sig_header,
                self.webhook_secret
            )

            return {
                "status": "success",
                "event": event
            }

        except stripe.error.SignatureVerificationError:
            return {
                "status": "error",
                "error": "Invalid webhook signature"
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    # ==================================
    # HANDLE PAYMENT SUCCESS
    # ==================================
    def handle_success(self, event: dict):

        try:
            session = event["data"]["object"]

            user_id = session.get("metadata", {}).get("user_id")
            plan = session.get("metadata", {}).get("plan")

            return {
                "status": "payment_success",
                "user_id": user_id,
                "plan": plan,
                "customer": session.get("customer"),
                "subscription_id": session.get("subscription"),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    # ==================================
    # HEALTH CHECK
    # ==================================
    def health_check(self):

        return {
            "status": "healthy" if self.is_ready() else "not_ready",
            "stripe_connected": self.is_ready()
      }
