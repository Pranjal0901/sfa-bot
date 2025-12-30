from typing import Tuple

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

def rule_based_intent(query: str) -> Tuple[str | None, float]:
    q = query.lower()

    if q.strip() in ["hi", "hello", "hey", "good morning", "good evening", "good afternoon"]:
        return "GREETING", 0.9

    if "top" in q and ("sales rep" in q or "sales representative" in q or "performer" in q):
        return "GET_TOP_PERFORMERS_REPORT", 0.85

    if "low" in q or "worst" in q or "underperform" in q:
        return "GET_LOW_PERFORMERS_REPORT", 0.8

    if "sales" in q and ("summary" in q or "total" in q or "overall"):
        return "GET_SALES_SUMMARY", 0.75

    if "sales" in q and ("trend" in q or "growth"):
        return "GET_SALES_TREND", 0.8

    if "compare" in q and "sales" in q:
        return "GET_SALES_COMPARISON", 0.8

    if "revenue" in q:
        return "GET_TOTAL_REVENUE", 0.8

    if "route" in q and "chemist" in q:
        return "GET_ROUTE_CHEMIST_REPORT", 0.9

    return None, 0.0
