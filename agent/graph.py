from typing import TypedDict

from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END

from agent.tools import (
    get_metric,
    compare_business_data
)

from agent.intent import extract_intent


# =========================================================
# AGENT STATE
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
# PROCESS USER QUESTION
# =========================================================

def process_question(state: AgentState):

    question = state["question"]

    # -----------------------------------------------------
    # STEP 1: Extract intent
    # -----------------------------------------------------

    intent = extract_intent(question)

    region = intent["region"]
    metric = intent["metric"]
    previous_quarter = intent["previous_quarter"]
    current_quarter = intent["current_quarter"]
    intent_type = intent["intent"]


    # =====================================================
    # COMPARISON QUERY
    # =====================================================

    if (
        intent_type == "comparison"
        and region
        and metric
        and previous_quarter
        and current_quarter
    ):

        # -------------------------------------------------
        # STEP 2: Get metric definition
        # -------------------------------------------------

        metric_definition = get_metric.invoke({
            "metric_name": metric
        })


        # -------------------------------------------------
        # STEP 3: Get verified business analysis
        # -------------------------------------------------

        comparison_data = compare_business_data.invoke({

            "region": region,

            "previous_quarter": previous_quarter,

            "current_quarter": current_quarter

        })


        # -------------------------------------------------
        # STEP 4: Give verified data to LLM
        # -------------------------------------------------

        prompt = f"""
You are the AI Orchestrator of MetricMind,
an Enterprise Business Intelligence system.

USER QUESTION:
{question}


EXTRACTED INTENT:

Region: {region}

Metric: {metric}

Previous Quarter: {previous_quarter}

Current Quarter: {current_quarter}


SEMANTIC LAYER METRIC DEFINITION:

{metric_definition}


VERIFIED BUSINESS ANALYSIS:

{comparison_data}


YOUR TASK:

Explain the verified business analysis
to the user in simple and concise language.


IMPORTANT RULES:

1. The VERIFIED BUSINESS ANALYSIS is authoritative.

2. Do NOT recalculate any numbers.

3. Do NOT create new numbers.

4. Do NOT change the direction of any change.

5. Do NOT invent business causes.

6. Do NOT mention competition, inflation,
   tariffs, customer behavior, market conditions,
   or any other cause unless explicitly present
   in the verified business analysis.

7. Use only the information provided above.

8. Keep the answer concise.


RETURN EXACTLY THIS STRUCTURE:


Summary:
<one sentence>


Evidence:
- Revenue: <verified change>
- Cost: <verified change>
- Margin: <verified change>


Reason:
<explain the change using only the verified data>
"""


        # -------------------------------------------------
        # STEP 5: LLM explanation
        # -------------------------------------------------

        response = llm.invoke(prompt)


        return {
            "question": question,
            "answer": response.content
        }


    # =====================================================
    # METRIC LOOKUP
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


Answer the user's question using ONLY
the Semantic Layer result.


RULES:

1. Do not invent numbers.

2. Do not invent business facts.

3. Do not infer unsupported causes.

4. Keep the answer concise.
"""


        response = llm.invoke(prompt)


        return {
            "question": question,
            "answer": response.content
        }


    # =====================================================
    # UNSUPPORTED QUERY
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
# LANGGRAPH WORKFLOW
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