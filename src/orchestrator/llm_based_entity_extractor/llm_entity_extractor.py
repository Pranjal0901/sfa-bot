import os
from typing import Tuple
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv() 

def llm_based_intent(query: str) -> Tuple[str, float]:
    """
    LLM fallback intent detection
    """

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        # Hard safety fallback
        return "UNKNOWN", 0.0

    client = OpenAI(api_key=api_key) 

    prompt = f"""
You are an intent classification system.

Return ONLY the intent name from this list:
- GREETING
- GET_SALES_SUMMARY
- GET_SALES_TREND
- GET_SALES_COMPARISON
- GET_TOTAL_REVENUE
- GET_TOP_PERFORMERS_REPORT
- GET_LOW_PERFORMERS_REPORT
- GET_SALES_REP_PERFORMANCE
- GET_SALES_REP_ROUTE
- GET_SALES_REP_ATTENDANCE
- GET_TARGET_VS_ACHIEVEMENT
- GET_PENDING_TARGETS
- GET_ORDER_SUMMARY
- GET_CANCELLED_ORDERS
- GET_TOP_PRODUCTS
- GET_LOW_SELLING_PRODUCTS
- GET_PRODUCT_WISE_SALES
- GET_REGION_WISE_SALES
- GET_DISTRIBUTOR_PERFORMANCE
- GET_RETAILER_VISITS
- GET_RETAILER_ORDER_HISTORY
- GET_RETAILER_OUTSTANDING
- GET_SALES_ALERTS
- GET_ANOMALIES
- GET_SALES_FORECAST
- GET_INSIGHTS
- UNKNOWN

User query:
"{query}"
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You classify intents only."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
    )

    intent = response.choices[0].message.content.strip()
    confidence = 0.9 if intent != "UNKNOWN" else 0.3

    return intent, confidence
