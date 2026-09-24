# =========================================================
# METRICMIND - INTENT EXTRACTION
# =========================================================

import re


# =========================================================
# METRIC SYNONYMS
# =========================================================

METRIC_SYNONYMS = {

    "revenue": [
        "revenue",
        "revenues",
        "sales",
        "sale",
        "income",
        "turnover"
    ],

    "margin": [
        "margin",
        "margins",
        "profit margin",
        "profitability",
        "profitability rate"
    ],

    "cost": [
        "cost",
        "costs",
        "expense",
        "expenses",
        "spending",
        "expenditure"
    ],

    "churn": [
        "churn",
        "customer churn",
        "attrition",
        "customer attrition"
    ]
}


# =========================================================
# REGION SYNONYMS
# =========================================================

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
# EXTRACT METRIC
# =========================================================

def extract_metric(question_lower):

    # Check longer phrases first

    metric_patterns = [

        (
            "margin",
            [
                "profit margin",
                "profitability rate",
                "profitability",
                "margins",
                "margin"
            ]
        ),

        (
            "revenue",
            [
                "revenue",
                "revenues",
                "sales",
                "sale",
                "income",
                "turnover"
            ]
        ),

        (
            "cost",
            [
                "costs",
                "cost",
                "expenses",
                "expense",
                "spending",
                "expenditure"
            ]
        ),

        (
            "churn",
            [
                "customer churn",
                "customer attrition",
                "churn",
                "attrition"
            ]
        )
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
# EXTRACT REGION
# =========================================================

def extract_region(question_lower):

    for region, words in REGION_SYNONYMS.items():

        for word in words:

            if re.search(
                rf"\b{re.escape(word)}\b",
                question_lower
            ):

                return region

    return None


# =========================================================
# EXTRACT QUARTERS
# =========================================================

def extract_quarters(question_lower):

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

    return (
        previous_quarter,
        current_quarter
    )


# =========================================================
# EXTRACT INTENT TYPE
# =========================================================

def extract_intent_type(question_lower):

    # Explicit comparison language
    comparison_patterns = [
        "compare",
        "comparison",
        "difference",
        "between",
        "from",
        "versus",
        "vs",
        "change",
        "changed",
        "drop",
        "dropped",
        "fall",
        "fell",
        "increase",
        "increased",
        "decrease",
        "decreased",
        "decline",
        "declined",
        "growth",
        "grew"
    ]

    for pattern in comparison_patterns:

        if re.search(
            rf"\b{re.escape(pattern)}\b",
            question_lower
        ):
            return "comparison"

    # Questions containing "why" indicate
    # a causal/change-oriented question.
    # Treat them as comparison only when
    # change language is also present.
    if re.search(r"\bwhy\b", question_lower):

        change_words = [
            "drop",
            "dropped",
            "fall",
            "fell",
            "decrease",
            "decreased",
            "decline",
            "declined",
            "increase",
            "increased",
            "change",
            "changed",
            "lower",
            "higher"
        ]

        for word in change_words:

            if re.search(
                rf"\b{re.escape(word)}\b",
                question_lower
            ):
                return "comparison"

    return "metric_lookup"


# =========================================================
# MAIN INTENT EXTRACTION
# =========================================================

def extract_intent(question: str):

    question_lower = (
        question
        .lower()
        .strip()
    )

    region = extract_region(
        question_lower
    )

    metric = extract_metric(
        question_lower
    )

    previous_quarter, current_quarter = (
        extract_quarters(
            question_lower
        )
    )

    intent = extract_intent_type(
        question_lower
    )

    return {

        "region": region,

        "metric": metric,

        "previous_quarter":
            previous_quarter,

        "current_quarter":
            current_quarter,

        "intent": intent
    }