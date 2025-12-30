from typing import Tuple

from src.orchestrator.rule_based_entity_extractor.rule_entity_extractor import rule_based_intent
from src.orchestrator.llm_based_entity_extractor.llm_entity_extractor import llm_based_intent

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

    # 1️⃣ Rule-based FIRST
    intent, confidence = rule_based_intent(query)

    if intent and confidence >= CONFIDENCE_THRESHOLD:
        return intent, confidence, "RULE_BASED"

    # 2️⃣ LLM fallback
    intent, confidence = llm_based_intent(query)
    return intent, confidence, "LLM"


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
