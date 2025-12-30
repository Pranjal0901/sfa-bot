from fastapi import FastAPI
from pydantic import BaseModel
from src.orchestrator.intent_orchestrator import extract_intent

app = FastAPI(title="SFA Chat Test API")

# -------------------------
# Request Model
# -------------------------
class ChatRequest(BaseModel):
    query: str

# -------------------------
# Response Model
# -------------------------
class ChatResponse(BaseModel):
    query: str
    intent: str
    confidence: float
    source: str


# -------------------------
# Test Endpoint
# -------------------------
@app.post("/sfa-chat-test", response_model=ChatResponse)
def sfa_chat_test(payload: ChatRequest):
    intent, confidence, source = extract_intent(payload.query)

    return ChatResponse(
        query=payload.query,
        intent=intent,
        confidence=confidence,
        source=source,
    )
