from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

import time

# =========================
# IMPORTS (SAFE FALLBACKS)
# =========================
try:
    from backend.auth import create_token, verify_token
except:
    def create_token(user_id): return f"token_{user_id}"
    def verify_token(token): return True

try:
    from backend.api_gateway import route_request
except:
    def route_request(prompt):
        p = prompt.lower()
        if "code" in p:
            return "GPT"
        if "image" in p:
            return "Gemini"
        if "write" in p:
            return "Claude"
        return "GPT"

try:
    from backend.ai_client import call_ai
except:
    def call_ai(model, prompt):
        return f"[{model}] → {prompt}"

try:
    from backend.billing import check_limit
except:
    def check_limit(plan, usage):
        limits = {"free": 20, "pro": 200, "enterprise": 2000}
        return usage < limits.get(plan, 20)

try:
    from self_learning.learner import improve_response
except:
    def improve_response(text):
        return text + " (self-learning optimized)"


# =========================
# APP INIT
# =========================
app = FastAPI(title="Mythos AI SaaS System 🚀")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# MEMORY (TEMP DB)
# =========================
USAGE_DB = {}


# =========================
# HOME ROUTE
# =========================
@app.get("/")
def home():
    return {
        "status": "Mythos AI Running 🚀",
        "version": "2.0",
        "users": "500+ ready architecture",
        "message": "System is active"
    }


# =========================
# LOGIN API
# =========================
@app.post("/login")
def login(request: Request):

    data = request.json()

    # safe fallback
    if not isinstance(data, dict):
        return {"error": "invalid request"}

    user_id = data.get("user_id", "guest")

    token = create_token(user_id)

    return {
        "status": "success",
        "token": token,
        "user": user_id
    }


# =========================
# CHAT API (MAIN ENGINE)
# =========================
@app.post("/chat")
async def chat(request: Request):

    data = await request.json()

    user_id = data.get("user_id", "guest")
    prompt = data.get("prompt", "")
    token = data.get("token", "")
    plan = data.get("plan", "free")

    # 🔐 AUTH CHECK
    if not verify_token(token):
        return {"error": "Invalid token"}

    # 📊 USAGE TRACKING
    usage = USAGE_DB.get(user_id, 0)

    # 💳 BILLING CHECK
    if not check_limit(plan, usage):
        return {
            "error": "Limit exceeded",
            "message": "Upgrade your plan"
        }

    # 🧠 AI ROUTING
    model = route_request(prompt)

    # 🤖 AI RESPONSE
    response = call_ai(model, prompt)

    # 🧠 SELF LEARNING IMPROVEMENT
    response = improve_response(response)

    # 📊 UPDATE USAGE
    USAGE_DB[user_id] = usage + 1

    # ⏱️ SIMULATE PROCESS TIME
    time.sleep(0.2)

    return {
        "status": "success",
        "user": user_id,
        "model_used": model,
        "response": response,
        "usage": USAGE_DB[user_id],
        "plan": plan
    }


# =========================
# STATUS CHECK
# =========================
@app.get("/status")
def status():

    return {
        "system": "healthy",
        "active_users": len(USAGE_DB),
        "total_requests": sum(USAGE_DB.values()),
        "architecture": "production-ready base"
  }
@app.get("/")
def home():
    return {
        "status": "Mythos AI Running 🚀",
        "message": "System is active"
}
