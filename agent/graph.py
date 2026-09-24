# =========================================================
# METRICMIND - AI ORCHESTRATOR GRAPH
# =========================================================

from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama

from agent.intent import extract_intent
from agent.query_planner import create_query_plan
from agent.validator import validate_query_plan
from agent.semantic_api import SemanticLayerAPI


# =========================================================
# LLM
# =========================================================

llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0
)


# =========================================================
# SEMANTIC LAYER
# =========================================================

semantic_api = SemanticLayerAPI()


# =========================================================
# STATE
# =========================================================

class AgentState(TypedDict):
    question: str
    answer: str
    trace: dict


# =========================================================
# PROCESS QUESTION
# =========================================================

def process_question(state: AgentState):

    question = state["question"]

    # -----------------------------------------------------
    # TRACE INITIALIZATION
    # -----------------------------------------------------

    trace = {
        "question": question,
        "intent": None,
        "query_plan": None,
        "validation": None,
        "semantic_layer": None,
        "execution": None
    }

    # =====================================================
    # STEP 1 - INTENT EXTRACTION
    # =====================================================

    intent = extract_intent(question)

    trace["intent"] = intent

    # =====================================================
    # STEP 2 - QUERY PLANNING
    # =====================================================

    query_plan = create_query_plan(intent)

    trace["query_plan"] = query_plan

    # -----------------------------------------------------
    # Invalid query plan
    # -----------------------------------------------------

    if query_plan.get("status") != "valid":

        reason = query_plan.get(
            "reason",
            "Unknown query planning error."
        )

        trace["validation"] = {
            "valid": False,
            "reason": reason
        }

        trace["execution"] = {
            "status": "blocked",
            "steps": []
        }

        return {
            "answer": (
                "I could not create a valid "
                "business query plan.\n\n"
                f"Reason: {reason}"
            ),
            "trace": trace
        }

    # =====================================================
    # STEP 3 - QUERY VALIDATION
    # =====================================================

    validation = validate_query_plan(
        query_plan
    )

    trace["validation"] = validation

    # -----------------------------------------------------
    # Validation failed
    # -----------------------------------------------------

    if not validation.get("valid"):

        reason = validation.get(
            "reason",
            "Query validation failed."
        )

        trace["execution"] = {
            "status": "blocked",
            "steps": []
        }

        return {
            "answer": (
                "The query could not be executed.\n\n"
                f"Reason: {reason}"
            ),
            "trace": trace
        }

    # =====================================================
    # STEP 4 - SEMANTIC LAYER EXECUTION
    # =====================================================

    semantic_result = semantic_api.execute_query(
        query_plan
    )

    trace["semantic_layer"] = {
        "source": semantic_result.get(
            "source",
            "semantic_layer"
        ),
        "operation": semantic_result.get(
            "operation"
        ),
        "status": semantic_result.get(
            "status"
        )
    }

    # -----------------------------------------------------
    # Semantic Layer error
    # -----------------------------------------------------

    if semantic_result.get("status") != "success":

        message = semantic_result.get(
            "message",
            "Semantic Layer execution failed."
        )

        trace["execution"] = {
            "status": "failed",
            "steps": []
        }

        return {
            "answer": (
                "The Semantic Layer could not "
                "complete the request.\n\n"
                f"Reason: {message}"
            ),
            "trace": trace
        }

    # =====================================================
    # STEP 5 - LOOKUP
    # =====================================================

    if query_plan.get("operation") == "lookup":

        metric = query_plan.get(
            "metric"
        )

        region = query_plan.get(
            "region"
        )

        period = query_plan.get(
            "period"
        )

        data = semantic_result.get(
            "data",
            {}
        )

        value = data.get(
            "value"
        )

        # -------------------------------------------------
        # Metric definition lookup
        #
        # Example:
        # "What is margin?"
        # -------------------------------------------------

        if value is None:

            metric_definition = (
                semantic_result.get(
                    "metric_definition"
                )
            )

            if metric_definition:

                answer = metric_definition

            else:

                answer = (
                    "The requested business value "
                    "is not available."
                )

        # -------------------------------------------------
        # Numeric metric lookup
        #
        # Example:
        # "What is the revenue in Asia Q3?"
        # -------------------------------------------------

        else:

            if metric == "revenue":

                answer = (
                    f"The revenue in {region} "
                    f"for {period} is "
                    f"${value:,}."
                )

            elif metric == "cost":

                answer = (
                    f"The cost in {region} "
                    f"for {period} is "
                    f"${value:,}."
                )

            elif metric == "margin":

                answer = (
                    f"The margin in {region} "
                    f"for {period} is "
                    f"{value}%."
                )

            elif metric == "churn":

                answer = (
                    f"The churn in {region} "
                    f"for {period} is "
                    f"{value}%."
                )

            else:

                answer = (
                    f"The value of {metric} "
                    f"is {value}."
                )

        # -------------------------------------------------
        # Execution trace
        # -------------------------------------------------

        trace["execution"] = {
            "status": "success",
            "steps": [
                {
                    "step": 1,
                    "metric": metric,
                    "status": "success"
                }
            ]
        }

        return {
            "answer": answer,
            "trace": trace
        }

    # =====================================================
    # STEP 6 - SINGLE COMPARISON
    # =====================================================

    if query_plan.get("operation") == "compare":

        verified_analysis = (
            semantic_result.get(
                "verified_analysis",
                {}
            )
        )

        metric = query_plan.get(
            "metric"
        )

        region = query_plan.get(
            "region"
        )

        previous_period = query_plan.get(
            "previous_period"
        )

        current_period = query_plan.get(
            "current_period"
        )

        if metric == "revenue":

            change = verified_analysis.get(
                "revenue_change"
            )

            percentage = verified_analysis.get(
                "revenue_percentage_change"
            )

            answer = (
                f"Revenue in {region} changed "
                f"from {previous_period} to "
                f"{current_period} by "
                f"${change:,} "
                f"({percentage}%)."
            )

        elif metric == "cost":

            change = verified_analysis.get(
                "cost_change"
            )

            percentage = verified_analysis.get(
                "cost_percentage_change"
            )

            answer = (
                f"Cost in {region} changed "
                f"from {previous_period} to "
                f"{current_period} by "
                f"${change:,} "
                f"({percentage}%)."
            )

        elif metric == "margin":

            change = verified_analysis.get(
                "margin_change"
            )

            direction = verified_analysis.get(
                "margin_direction"
            )

            answer = (
                f"Margin in {region} changed "
                f"from {previous_period} to "
                f"{current_period} by "
                f"{change} percentage points. "
                f"{direction}"
            )

        else:

            answer = (
                "The comparison was completed "
                "using verified Semantic Layer data."
            )

        trace["execution"] = {
            "status": "success",
            "steps": [
                {
                    "step": 1,
                    "metric": metric,
                    "status": "success"
                }
            ]
        }

        return {
            "answer": answer,
            "trace": trace
        }

    # =====================================================
    # STEP 7 - MULTI-STEP ANALYSIS
    # =====================================================

    if query_plan.get("operation") == "multi_step":

        steps = semantic_result.get(
            "steps",
            []
        )

        if not steps:

            trace["execution"] = {
                "status": "failed",
                "steps": []
            }

            return {
                "answer": (
                    "No verified analysis steps "
                    "were returned by the Semantic Layer."
                ),
                "trace": trace
            }

        # -------------------------------------------------
        # Build execution trace
        # -------------------------------------------------

        execution_steps = []

        for step in steps:

            execution_steps.append(
                {
                    "step": step.get("step"),
                    "metric": step.get("metric"),
                    "status": step.get(
                        "result",
                        {}
                    ).get(
                        "status",
                        "unknown"
                    )
                }
            )

        trace["execution"] = {
            "status": "success",
            "steps": execution_steps
        }

        # -------------------------------------------------
        # Find primary margin analysis
        # -------------------------------------------------

        margin_result = None
        revenue_result = None
        cost_result = None

        for step in steps:

            metric = step.get(
                "metric"
            )

            result = step.get(
                "result",
                {}
            )

            if metric == "margin":
                margin_result = result

            elif metric == "revenue":
                revenue_result = result

            elif metric == "cost":
                cost_result = result

        # -------------------------------------------------
        # Generate deterministic answer
        # -------------------------------------------------

        if margin_result:

            analysis = margin_result.get(
                "verified_analysis",
                {}
            )

            margin_change = analysis.get(
                "margin_change"
            )

            revenue_percentage = (
                analysis.get(
                    "revenue_percentage_change"
                )
            )

            cost_percentage = (
                analysis.get(
                    "cost_percentage_change"
                )
            )

            growth_relationship = (
                analysis.get(
                    "growth_relationship"
                )
            )

            region = query_plan.get(
                "region"
            )

            previous_period = query_plan.get(
                "previous_period"
            )

            current_period = query_plan.get(
                "current_period"
            )

            # -------------------------------------------------
            # Main explanation
            # -------------------------------------------------

            if margin_change > 0:

                direction = "increased"

            elif margin_change < 0:

                direction = "decreased"

            else:

                direction = "remained unchanged"

            answer = (
                f"Summary:\n"
                f"{region} margins {direction} "
                f"by {abs(margin_change)} "
                f"percentage points from "
                f"{previous_period} to "
                f"{current_period}.\n\n"
                f"Evidence:\n"
                f"- Revenue: "
                f"{revenue_percentage}%\n"
                f"- Cost: "
                f"{cost_percentage}%\n"
                f"- Margin: "
                f"{margin_change} percentage points\n\n"
                f"Reason:\n"
                f"The margin {direction} because "
                f"{growth_relationship.lower()}"
            )

        else:

            answer = (
                "The multi-step business analysis "
                "was completed successfully using "
                "verified Semantic Layer data."
            )

        return {
            "answer": answer,
            "trace": trace
        }

    # =====================================================
    # UNSUPPORTED OPERATION
    # =====================================================

    trace["execution"] = {
        "status": "failed",
        "steps": []
    }

    return {
        "answer": (
            "The requested operation is not "
            "supported by MetricMind."
        ),
        "trace": trace
    }


# =========================================================
# BUILD LANGGRAPH
# =========================================================

builder = StateGraph(
    AgentState
)

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