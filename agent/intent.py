import re


def extract_intent(question: str):
    """
    Extract structured business intent from a natural-language question.

    Returns:
        region
        metric
        previous_quarter
        current_quarter
        intent
    """

    question_lower = question.lower()

    # =====================================================
    # REGION
    # =====================================================

    region = None

    if re.search(r"\beurope\b|\beuropean\b", question_lower):
        region = "Europe"

    elif re.search(r"\basia\b|\basian\b", question_lower):
        region = "Asia"


    # =====================================================
    # METRIC
    # =====================================================

    metric = None

    if re.search(r"\bmargin\b|\bmargins\b", question_lower):
        metric = "margin"

    elif re.search(r"\brevenue\b", question_lower):
        metric = "revenue"

    elif re.search(r"\bcost\b|\bcosts\b", question_lower):
        metric = "cost"

    elif re.search(r"\bchurn\b", question_lower):
        metric = "churn"


    # =====================================================
    # QUARTERS
    # =====================================================

    quarters = re.findall(
        r"\bq[1-4]\b",
        question_lower
    )

    previous_quarter = None
    current_quarter = None

    if len(quarters) >= 2:

        previous_quarter = quarters[0].upper()
        current_quarter = quarters[1].upper()

    elif len(quarters) == 1:

        current_quarter = quarters[0].upper()


    # =====================================================
    # INTENT
    # =====================================================

    comparison_words = [
        "compare",
        "change",
        "changed",
        "difference",
        "drop",
        "dropped",
        "increase",
        "increased",
        "decrease",
        "decreased",
        "decline",
        "declined",
        "performance",
        "between",
        "from",
        "why"
    ]

    if any(word in question_lower for word in comparison_words):

        intent = "comparison"

    else:

        intent = "metric_lookup"


    # =====================================================
    # RETURN STRUCTURED INTENT
    # =====================================================

    return {
        "region": region,
        "metric": metric,
        "previous_quarter": previous_quarter,
        "current_quarter": current_quarter,
        "intent": intent
    }