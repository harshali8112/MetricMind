from agent.intent import extract_intent


questions = [
    "Why did Asian margins change from Q2 to Q3?",
    "Compare European margin between Q2 and Q3.",
    "What happened to Asia's margin in Q3?",
    "Show me European revenue from Q1 to Q2."
]


for question in questions:

    print("\n========================================")

    print("Question:")
    print(question)

    print("\nExtracted Intent:")

    intent = extract_intent(question)

    print(intent)