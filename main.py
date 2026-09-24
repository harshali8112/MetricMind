from agent.graph import graph


# =========================================================
# METRICMIND - CLI
# =========================================================

print("\n========================================")
print("              METRICMIND")
print("========================================")

print("\nEnterprise Analytics & Agentic AI")

print("\nAsk a business question.")
print("Example:")
print("Why did Asian margins change from Q2 to Q3?")

print("\nType 'exit' or 'quit' to stop.")


# =========================================================
# TRACE DISPLAY
# =========================================================

def display_trace(trace):

    print("\n========================================")
    print("          METRICMIND TRACE")
    print("========================================")

    # -------------------------
    # Intent
    # -------------------------

    intent = trace.get("intent")

    if intent:

        print("\n[1] INTENT")

        print(
            f"Region: {intent.get('region')}"
        )

        print(
            f"Metric: {intent.get('metric')}"
        )

        print(
            f"Previous Period: "
            f"{intent.get('previous_quarter')}"
        )

        print(
            f"Current Period: "
            f"{intent.get('current_quarter')}"
        )

        print(
            f"Intent Type: "
            f"{intent.get('intent')}"
        )

    # -------------------------
    # Query Plan
    # -------------------------

    query_plan = trace.get("query_plan")

    if query_plan:

        print("\n[2] QUERY PLAN")

        print(
            f"Status: "
            f"{query_plan.get('status')}"
        )

        print(
            f"Operation: "
            f"{query_plan.get('operation')}"
        )

        if query_plan.get("metric"):
            print(
                f"Metric: "
                f"{query_plan.get('metric')}"
            )

        if query_plan.get("primary_metric"):
            print(
                f"Primary Metric: "
                f"{query_plan.get('primary_metric')}"
            )

        if query_plan.get("region"):
            print(
                f"Region: "
                f"{query_plan.get('region')}"
            )

        if query_plan.get("period"):
            print(
                f"Period: "
                f"{query_plan.get('period')}"
            )

        if query_plan.get("previous_period"):
            print(
                f"Previous Period: "
                f"{query_plan.get('previous_period')}"
            )

        if query_plan.get("current_period"):
            print(
                f"Current Period: "
                f"{query_plan.get('current_period')}"
            )

    # -------------------------
    # Validation
    # -------------------------

    validation = trace.get("validation")

    if validation:

        print("\n[3] VALIDATION")

        if validation.get("valid"):

            print("✓ Query passed validation.")

        else:

            print("✗ Query failed validation.")

        print(
            f"Reason: "
            f"{validation.get('reason')}"
        )

    # -------------------------
    # Semantic Layer
    # -------------------------

    semantic_layer = trace.get(
        "semantic_layer"
    )

    if semantic_layer:

        print("\n[4] SEMANTIC LAYER")

        print(
            f"Source: "
            f"{semantic_layer.get('source')}"
        )

        print(
            f"Operation: "
            f"{semantic_layer.get('operation')}"
        )

        status = semantic_layer.get(
            "status"
        )

        if status == "success":

            print("Status: ✓ SUCCESS")

        else:

            print(
                f"Status: ✗ {status}"
            )

    # -------------------------
    # Execution
    # -------------------------

    execution = trace.get("execution")

    if execution:

        print("\n[5] EXECUTION")

        print(
            f"Status: "
            f"{execution.get('status')}"
        )

        steps = execution.get(
            "steps",
            []
        )

        for step in steps:

            print(
                f"✓ Step {step.get('step')}: "
                f"{step.get('metric')} "
                f"→ {step.get('status')}"
            )

    print("\n========================================")


# =========================================================
# MAIN LOOP
# =========================================================

while True:

    question = input(
        "\nAsk MetricMind: "
    ).strip()

    # -------------------------
    # Exit
    # -------------------------

    if question.lower() in [
        "exit",
        "exit()",
        "quit",
        "quit()"
    ]:

        print(
            "\nExiting MetricMind..."
        )

        break

    # -------------------------
    # Empty question
    # -------------------------

    if not question:

        print(
            "\nPlease enter a question."
        )

        continue

    # -------------------------
    # Run Orchestrator
    # -------------------------

    result = graph.invoke(
        {
            "question": question,
            "answer": "",
            "trace": {}
        }
    )

    # -------------------------
    # Answer
    # -------------------------

    print(
        "\n----------------------------------------"
    )

    print(
        "AI Orchestrator Answer:"
    )

    print(
        "----------------------------------------"
    )

    print(
        result["answer"]
    )

    print(
        "----------------------------------------"
    )

    # -------------------------
    # Trace option
    # -------------------------

    show_trace = input(
        "\nView execution trace? (y/n): "
    ).strip().lower()

    if show_trace in ["y", "yes"]:

        display_trace(
            result["trace"]
        )