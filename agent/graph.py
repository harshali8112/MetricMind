from typing import TypedDict

from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END

from agent.tools import (
    get_metric,
    get_business_data,
    compare_business_data
)


# =========================================================
# STATE
# =========================================================

class AgentState(TypedDict):
    question: str
    answer: str


# =========================================================
# LOCAL LLM
# =========================================================

llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0
)


# =========================================================
# INTENT EXTRACTION
# =========================================================

def extract_intent(question: str):
    """
    Extract basic business intent from the user's question.

    Current supported:
    - Region
    - Previous quarter
    - Current quarter
    - Metric
    """

    question_lower = question.lower()

    # -------------------------
    # Region
    # -------------------------

    if "europe" in question_lower:
        region = "Europe"

    elif "asia" in question_lower:
        region = "Asia"

    else:
        region = None


    # -------------------------
    # Quarters
    # -------------------------

    previous_quarter = None
    current_quarter = None

    if "q2" in question_lower and "q3" in question_lower:

        previous_quarter = "Q2"
        current_quarter = "Q3"

    elif "q1" in question_lower and "q2" in question_lower:

        previous_quarter = "Q1"
        current_quarter = "Q2"


    # -------------------------
    # Metric
    # -------------------------

    if "margin" in question_lower:
        metric = "margin"

    elif "revenue" in question_lower:
        metric = "revenue"

    elif "cost" in question_lower:
        metric = "cost"

    elif "churn" in question_lower:
        metric = "churn"

    else:
        metric = None


    return {
        "region": region,
        "previous_quarter": previous_quarter,
        "current_quarter": current_quarter,
        "metric": metric
    }


# =========================================================
# PROCESS QUESTION
# =========================================================

def process_question(state: AgentState):

    question = state["question"]

    # -----------------------------------------
    # Extract user intent
    # -----------------------------------------

    intent = extract_intent(question)

    region = intent["region"]
    previous_quarter = intent["previous_quarter"]
    current_quarter = intent["current_quarter"]
    metric = intent["metric"]


    # =====================================================
    # CASE 1: COMPARISON QUESTION
    # =====================================================

    if (
        region
        and previous_quarter
        and current_quarter
        and metric
    ):

        # -----------------------------------------
        # Get semantic metric definition
        # -----------------------------------------

        metric_definition = get_metric.invoke({
            "metric_name": metric
        })


        # -----------------------------------------
        # Get verified business comparison
        # -----------------------------------------

        comparison_data = compare_business_data.invoke({
            "region": region,
            "previous_quarter": previous_quarter,
            "current_quarter": current_quarter
        })


        # -----------------------------------------
        # Give verified information to LLM
        # -----------------------------------------

        prompt = f"""
You are the AI Orchestrator of MetricMind,
an Enterprise Business Intelligence system.

USER QUESTION:
{question}

EXTRACTED INTENT:

Region: {region}
Previous Quarter: {previous_quarter}
Current Quarter: {current_quarter}
Metric: {metric}

SEMANTIC LAYER METRIC DEFINITION:
{metric_definition}

VERIFIED BUSINESS ANALYSIS:
{comparison_data}

Your task is to explain the result using ONLY
the verified information above.

IMPORTANT RULES:

1. The VERIFIED BUSINESS ANALYSIS is authoritative.

2. Do NOT recalculate numbers.

3. Do NOT create new numbers.

4. Do NOT change the direction of any change.

5. Do NOT invent business causes.

6. Do NOT mention competition, inflation,
   tariffs, customer behavior, market conditions,
   or any other cause unless explicitly provided
   in the verified data.

7. Keep the answer concise.

Return EXACTLY this structure:

Summary:
<one sentence>

Evidence:
- Revenue: <verified change>
- Cost: <verified change>
- Margin: <verified change>

Reason:
<explain why the margin changed using only
the verified data>
"""

        response = llm.invoke(prompt)

        return {
            "question": question,
            "answer": response.content
        }


    # =====================================================
    # CASE 2: METRIC DEFINITION QUESTION
    # =====================================================

    elif metric:

        metric_result = get_metric.invoke({
            "metric_name": metric
        })


        prompt = f"""
You are the AI Orchestrator of MetricMind.

USER QUESTION:
{question}

SEMANTIC LAYER RESULT:
{metric_result}

Answer using ONLY the Semantic Layer result.

Rules:

- Do not invent numbers.
- Do not invent business facts.
- Keep the answer concise.
"""

        response = llm.invoke(prompt)

        return {
            "question": question,
            "answer": response.content
        }


    # =====================================================
    # CASE 3: INFORMATION NOT AVAILABLE
    # =====================================================

    else:

        return {
            "question": question,
            "answer": (
                "I could not identify a supported business "
                "metric, region, or time period from the question."
            )
        }


# =========================================================
# LANGGRAPH
# =========================================================

builder = StateGraph(AgentState)

builder.add_node(
    "process_question",
    process_question
)

builder.add_edge(
    START,
    "process_question"
)

builder.add_edge(
    "process_question",
    END
)

graph = builder.compile()