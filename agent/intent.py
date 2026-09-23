import re


# =========================================================
# BUSINESS LANGUAGE NORMALIZATION
# =========================================================

METRIC_SYNONYMS = {
    "revenue": [
        "revenue",
        "revenues",
        "sales",
        "sale",
        "income"
    ],

    "margin": [
        "margin",
        "margins",
        "profitability",
        "profit margin",
        "profitability rate"
    ],

    "cost": [
        "cost",
        "costs",
        "expense",
        "expenses"
    ],

    "churn": [
        "churn",
        "customer churn",
        "attrition"
    ]
}


REGION_SYNONYMS = {
    "Europe": [
        "europe",
        "european"
    ],

    "Asia": [
        "asia",
        "asian"
    ]
}


# =========================================================
# FIND METRIC
# =========================================================

def extract_metric(question_lower):
    """
    Convert natural business language into
    a standard MetricMind metric.
    """

    # Check longer phrases first
    # Example: "profit margin" before "margin"

    metric_patterns = [

        ("margin", [
            "profit margin",
            "profitability rate",
            "profitability",
            "margins",
            "margin"
        ]),

        ("revenue", [
            "revenue",
            "revenues",
            "sales",
            "sale",
            "income"
        ]),

        ("cost", [
            "costs",
            "cost",
            "expenses",
            "expense"
        ]),

        ("churn", [
            "customer churn",
            "churn",
            "attrition"
        ])
    ]

    for metric, words in metric_patterns:

        for word in words:

            if re.search(
                rf"\b{re.escape(word)}\b",
                question_lower
            ):
                return metric

    return None


# =========================================================
# FIND REGION
# =========================================================

def extract_region(question_lower):
    """
    Convert regional language into
    standard MetricMind region names.
    """

    for region, words in REGION_SYNONYMS.items():

        for word in words:

            if re.search(
                rf"\b{re.escape(word)}\b",
                question_lower
            ):
                return region

    return None


# =========================================================
# FIND QUARTERS
# =========================================================

def extract_quarters(question_lower):
    """
    Extract explicit quarters such as Q1, Q2, Q3, Q4.
    """

    quarters = re.findall(
        r"\bq[1-4]\b",
        question_lower
    )

    quarters = [
        quarter.upper()
        for quarter in quarters
    ]

    previous_quarter = None
    current_quarter = None

    if len(quarters) >= 2:

        previous_quarter = quarters[0]
        current_quarter = quarters[1]

    elif len(quarters) == 1:

        current_quarter = quarters[0]

    return previous_quarter, current_quarter


# =========================================================
# FIND INTENT
# =========================================================

def extract_intent_type(question_lower):
    """
    Determine whether the user wants:
    - comparison
    - metric lookup
    """

    comparison_words = [
        "compare",
        "comparison",
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
        "growth",
        "grew",
        "performance",
        "between",
        "from",
        "why",
        "how did"
    ]

    for word in comparison_words:

        if word in question_lower:

            return "comparison"

    return "metric_lookup"


# =========================================================
# MAIN INTENT EXTRACTION
# =========================================================

def extract_intent(question: str):
    """
    Extract structured business intent
    from a natural-language question.

    Returns:

        region
        metric
        previous_quarter
        current_quarter
        intent
    """

    question_lower = question.lower().strip()

    # -----------------------------------------------------
    # REGION
    # -----------------------------------------------------

    region = extract_region(question_lower)

    # -----------------------------------------------------
    # METRIC
    # -----------------------------------------------------

    metric = extract_metric(question_lower)

    # -----------------------------------------------------
    # QUARTERS
    # -----------------------------------------------------

    previous_quarter, current_quarter = extract_quarters(
        question_lower
    )

    # -----------------------------------------------------
    # INTENT
    # -----------------------------------------------------

    intent = extract_intent_type(
        question_lower
    )

    # -----------------------------------------------------
    # RETURN STRUCTURED INTENT
    # -----------------------------------------------------

    return {
        "region": region,
        "metric": metric,
        "previous_quarter": previous_quarter,
        "current_quarter": current_quarter,
        "intent": intent
    }