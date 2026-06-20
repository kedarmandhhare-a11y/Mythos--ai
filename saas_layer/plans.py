from datetime import datetime, timedelta


class PlanManager:
    """
    MYTHOS V4 - SaaS Plan + Subscription Engine
    Handles:
    - Plans
    - Subscription management
    - Usage tracking
    - Feature access control
    """

    def __init__(self):

        # ==================================
        # SAAS PLANS
        # ==================================
        self.plans = {
            "free": {
                "name": "Free",
                "price": 0,
                "monthly_limit": 50,
                "features": [
                    "Basic AI Chat",
                    "Limited Requests",
                    "Community Support"
                ]
            },

            "pro": {
                "name": "Pro",
                "price": 9,
                "monthly_limit": 2000,
                "features": [
                    "Advanced AI Models",
                    "WhatsApp Integration",
                    "Instagram Integration",
                    "Priority Support"
                ]
            },

            "enterprise": {
                "name": "Enterprise",
                "price": 29,
                "monthly_limit": 10000,
                "features": [
                    "All AI Models",
                    "Unlimited Integrations",
                    "Dedicated Support",
                    "Custom AI Routing",
                    "Team Access"
                ]
            }
        }

        # ==================================
        # ACTIVE SUBSCRIPTIONS (IN-MEMORY DB)
        # ==================================
        self.subscriptions = {}

    # ==================================
    # GET ALL PLANS
    # ==================================
    def get_plans(self):
        return self.plans

    # ==================================
    # GET SINGLE PLAN
    # ==================================
    def get_plan(self, plan_name: str):
        return self.plans.get(plan_name)

    # ==================================
    # VALIDATE PLAN
    # ==================================
    def is_valid_plan(self, plan_name: str):
        return plan_name in self.plans

    # ==================================
    # SUBSCRIBE USER
    # ==================================
    def subscribe(self, user_id: str, plan_name: str):

        plan = self.get_plan(plan_name)

        if not plan:
            return {
                "status": "error",
                "error": "Invalid plan"
            }

        self.subscriptions[user_id] = {
            "plan": plan_name,
            "status": "active",
            "start_date": datetime.utcnow().isoformat() + "Z",
            "end_date": (datetime.utcnow() + timedelta(days=30)).isoformat() + "Z",
            "usage": 0
        }

        return {
            "status": "subscribed",
            "user_id": user_id,
            "plan": plan_name
        }

    # ==================================
    # CHECK USAGE LIMIT
    # ==================================
    def check_limit(self, user_id: str):

        sub = self.subscriptions.get(user_id)

        if not sub:
            return {
                "allowed": False,
                "reason": "No subscription found"
            }

        plan = self.get_plan(sub["plan"])

        if not plan:
            return {
                "allowed": False,
                "reason": "Invalid plan in subscription"
            }

        if sub["usage"] >= plan["monthly_limit"]:
            return {
                "allowed": False,
                "reason": "Limit exceeded",
                "remaining": 0
            }

        return {
            "allowed": True,
            "remaining": plan["monthly_limit"] - sub["usage"]
        }

    # ==================================
    # INCREMENT USAGE (ADD USAGE)
    # ==================================
    def add_usage(self, user_id: str, amount: int = 1):

        if user_id in self.subscriptions:
            self.subscriptions[user_id]["usage"] += amount

    # ==================================
    # GET SUBSCRIPTION STATUS
    # ==================================
    def status(self, user_id: str):

        return self.subscriptions.get(user_id, {
            "plan": "free",
            "usage": 0,
            "status": "not_subscribed"
        })

    # ==================================
    # FEATURE CHECK
    # ==================================
    def has_feature(self, user_id: str, feature: str):

        sub = self.subscriptions.get(user_id)

        if not sub:
            return False

        plan = self.get_plan(sub["plan"])

        if not plan:
            return False

        return feature in plan["features"]

    # ==================================
    # RESET MONTHLY USAGE
    # ==================================
    def reset_usage(self, user_id: str):

        if user_id in self.subscriptions:
            self.subscriptions[user_id]["usage"] = 0
            self.subscriptions[user_id]["start_date"] = datetime.utcnow().isoformat() + "Z"
            self.subscriptions[user_id]["end_date"] = (
                datetime.utcnow() + timedelta(days=30)
            ).isoformat() + "Z"

    # ==================================
    # GET ALL SUBSCRIPTIONS (ADMIN)
    # ==================================
    def get_all_subscriptions(self):
        return self.subscriptions
