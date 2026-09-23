from agent.graph import graph


# =========================================================
# METRICMIND
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
# CONTINUOUS QUESTION LOOP
# =========================================================

while True:

    question = input("\nAsk MetricMind: ").strip()

    # -----------------------------------------------------
    # EXIT COMMANDS
    # -----------------------------------------------------

    if question.lower() in [
        "exit",
        "exit()",
        "quit",
        "quit()"
    ]:

        print("\nExiting MetricMind...")

        break

    # -----------------------------------------------------
    # EMPTY INPUT
    # -----------------------------------------------------

    if not question:

        print("\nPlease enter a question.")

        continue

    # -----------------------------------------------------
    # RUN LANGGRAPH
    # -----------------------------------------------------

    result = graph.invoke({
        "question": question,
        "answer": ""
    })

    # -----------------------------------------------------
    # DISPLAY ANSWER
    # -----------------------------------------------------

    print("\n----------------------------------------")

    print("AI Orchestrator Answer:")

    print("----------------------------------------")

    print(result["answer"])

    print("----------------------------------------")