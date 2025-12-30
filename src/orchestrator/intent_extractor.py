import os, sys
from typing import Tuple
from openai import OpenAI
# ============================================================
# 1. OpenAI Client
# ============================================================

client = OpenAI()  # API key via OPENAI_API_KEY env var

# ============================================================
# 2. Allowed / Controlled Intents (FINITE)
# ============================================================
ALLOWED_INTENTS = {
    "GREETING",
    "GET_SALES_SUMMARY",
    "GET_SALES_TREND",
    "GET_SALES_COMPARISON",
    "GET_TOTAL_REVENUE",
    "GET_TOP_PERFORMERS_REPORT",
    "GET_LOW_PERFORMERS_REPORT",
    "GET_SALES_REP_PERFORMANCE",
    "GET_SALES_REP_ROUTE",
    "GET_SALES_REP_ATTENDANCE",
    "GET_TARGET_VS_ACHIEVEMENT",
    "GET_PENDING_TARGETS",
    "GET_ORDER_SUMMARY",
    "GET_CANCELLED_ORDERS",
    "GET_TOP_PRODUCTS",
    "GET_LOW_SELLING_PRODUCTS",
    "GET_PRODUCT_WISE_SALES",
    "GET_REGION_WISE_SALES",
    "GET_DISTRIBUTOR_PERFORMANCE",
    "GET_RETAILER_VISITS",
    "GET_RETAILER_ORDER_HISTORY",
    "GET_RETAILER_OUTSTANDING",
    "GET_SALES_ALERTS",
    "GET_ANOMALIES",
    "GET_SALES_FORECAST",
    "GET_INSIGHTS",
    "UNKNOWN",
}

# ============================================================
# 3. Rule-based Intent Detection (FAST PATH)
# ============================================================
from typing import Tuple

def rule_based_intent(query: str) -> Tuple[str | None, float]:
    q = query.lower()

    if q.strip() in ["hi", "hello", "hey", "good morning", "good evening", "good afternoon"]:
        return "GREETING", 0.9

    if "help" in q or "what can you do" in q:
        return "HELP", 0.85

    if "top" in q and ("sales rep" in q or "sales representative" in q or "performer" in q):
        return "GET_TOP_PERFORMERS_REPORT", 0.85

    if "low" in q or "worst" in q or "underperform" in q:
        return "GET_LOW_PERFORMERS_REPORT", 0.8

    if "sales" in q and ("summary" in q or "total" in q or "overall"):
        return "GET_SALES_SUMMARY", 0.75

    if "sales" in q and ("trend" in q or "growth" in q):
        return "GET_SALES_TREND", 0.8

    if "compare" in q and "sales" in q:
        return "GET_SALES_COMPARISON", 0.8

    if "revenue" in q:
        return "GET_TOTAL_REVENUE", 0.8
    
    if "performance" in q and ("rep" in q or "sales rep" in q):
        return "GET_SALES_REP_PERFORMANCE", 0.8

    if "route" in q and ("rep" in q or "sales rep"):
        return "GET_SALES_REP_ROUTE", 0.85

    if "attendance" in q or "present" in q or "absent" in q:
        return "GET_SALES_REP_ATTENDANCE", 0.85

    if "target" in q and ("achievement" in q or "achieved" in q):
        return "GET_TARGET_VS_ACHIEVEMENT", 0.85

    if "pending target" in q or ("target" in q and "pending" in q):
        return "GET_PENDING_TARGETS", 0.8

    if "order" in q and ("summary" in q or "total" in q):
        return "GET_ORDER_SUMMARY", 0.8

    if "cancel" in q and "order" in q:
        return "GET_CANCELLED_ORDERS", 0.85

    if "top" in q and "product" in q:
        return "GET_TOP_PRODUCTS", 0.85

    if "low" in q and "product" in q:
        return "GET_LOW_SELLING_PRODUCTS", 0.8

    if "product" in q and "sales" in q:
        return "GET_PRODUCT_WISE_SALES", 0.8

    if "region" in q or "area" in q:
        return "GET_REGION_WISE_SALES", 0.8

    if "distributor" in q:
        return "GET_DISTRIBUTOR_PERFORMANCE", 0.85

    if "visit" in q and ("retailer" in q or "chemist" in q):
        return "GET_RETAILER_VISITS", 0.85

    if "order history" in q and ("retailer" in q or "chemist" in q):
        return "GET_RETAILER_ORDER_HISTORY", 0.85

    if "outstanding" in q or "due" in q:
        return "GET_RETAILER_OUTSTANDING", 0.85

    if "alert" in q:
        return "GET_SALES_ALERTS", 0.85

    if "anomaly" in q or "unusual" in q or "abnormal" in q:
        return "GET_ANOMALIES", 0.85

    if "forecast" in q or "prediction" in q:
        return "GET_SALES_FORECAST", 0.8

    if "insight" in q or "analysis" in q or "why" in q:
        return "GET_INSIGHTS", 0.75

    if "route" in q and "chemist" in q:
        return "GET_ROUTE_CHEMIST_REPORT", 0.9

    return None, 0.0

# ============================================================
# 4. OpenAI Prompt (STRICT)
# ============================================================

INTENT_PROMPT = """
You are an intent classification system.

Classify the user query into ONE of the following intents:
-GREETING
-GET_SALES_TREND
-GET_SALES_SUMMARY
-GET_SALES_COMPARISON
-GET_TOTAL_REVENUE
-GET_TOP_PERFORMERS_REPORT
-GET_LOW_PERFORMERS_REPORT
-GET_SALES_REP_PERFORMANCE
-GET_SALES_REP_ROUTE
-GET_SALES_REP_ATTENDANCE
-GET_TARGET_VS_ACHIEVEMENT
-GET_PENDING_TARGETS
-GET_ORDER_SUMMARY
-GET_CANCELLED_ORDERS
-GET_TOP_PRODUCTS
-GET_LOW_SELLING_PRODUCTS
-GET_PRODUCT_WISE_SALES
-GET_REGION_WISE_SALES
-GET_DISTRIBUTOR_PERFORMANCE
-GET_RETAILER_VISITS
-GET_RETAILER_ORDER_HISTORY
-GET_RETAILER_OUTSTANDING
-GET_SALES_ALERTS
-GET_ANOMALIES
-GET_SALES_FORECAST
-GET_INSIGHTS
-UNKNOWN

Rules:
- Return ONLY the intent name.
- No explanation.
- No extra text.
- If unsure, return UNKNOWN.

User query:
"{query}"
"""
# ============================================================
# 5. LLM-based Intent Detection (FALLBACK)
# ============================================================

def llm_based_intent(query: str) -> Tuple[str, float]:
    prompt = INTENT_PROMPT.format(query=query)

    response = client.chat.completions.create(
        model="gpt-4o-mini",     
        messages=[
            {"role": "system", "content": "You classify intents only."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,         
    )

    intent = response.choices[0].message.content.strip()

    if intent not in ALLOWED_INTENTS:
        return "UNKNOWN", 0.0

    confidence = 0.9 if intent != "UNKNOWN" else 0.3
    return intent, confidence


# ============================================================
# 6. HYBRID ORCHESTRATOR (MAIN ENTRY POINT)
# ============================================================

CONFIDENCE_THRESHOLD = 0.8

def extract_intent(query: str) -> Tuple[str, float, str]:
    """
    Returns:
        intent (str)
        confidence (float)
        source ("RULE_BASED" | "LLM")
    """

    if not query or not query.strip():
        return "UNKNOWN", 0.0, "RULE_BASED"

    intent, confidence = rule_based_intent(query)
    if intent and confidence >= CONFIDENCE_THRESHOLD:
        return intent, confidence, "RULE_BASED"

    intent, confidence = llm_based_intent(query)
    return intent, confidence, "LLM"

# ============================================================
# 7. Fallback Message (for UNKNOWN)
# ============================================================

def unknown_intent_response():
    return {
        "type": "fallback",
        "message": (
            "I can help with sales analytics like:\n"
            "- Top sales performers\n"
            "- Sales summary\n"
            "- Route-wise chemist reports\n\n"
            "Please tell me what report you need."
        )
    }
