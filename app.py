import streamlit as st

from agent.graph import graph


# =========================================================
# METRICMIND - STREAMLIT UI
# =========================================================

st.set_page_config(
    page_title="MetricMind",
    page_icon="📊",
    layout="wide"
)

st.title("📊 MetricMind")
st.subheader("Agentic Semantic BI Engine")

st.write(
    "Ask a business question and let the AI Orchestrator "
    "plan, validate, execute and explain the analysis."
)


# =========================================================
# QUESTION INPUT
# =========================================================

question = st.text_input(
    "Ask MetricMind",
    placeholder="Why did European margins drop from Q2 to Q3?"
)


# =========================================================
# EXAMPLES
# =========================================================

st.markdown("### Example Questions")

st.markdown("""
- What is the revenue in Asia Q3?
- What happened to European costs in Q3?
- Why did European margins drop from Q2 to Q3?
- Why did Asian margins change from Q2 to Q3?
- What is margin?
""")


# =========================================================
# RUN ORCHESTRATOR
# =========================================================

if st.button("🔍 Analyze", type="primary"):

    if not question.strip():

        st.warning("Please enter a business question.")

    else:

        with st.spinner("MetricMind is analyzing..."):

            result = graph.invoke(
                {
                    "question": question,
                    "answer": "",
                    "trace": {}
                }
            )

        # -------------------------------------------------
        # ANSWER
        # -------------------------------------------------

        st.markdown("## 💡 AI Orchestrator Answer")

        st.success(result["answer"])

        # -------------------------------------------------
        # TRACE
        # -------------------------------------------------

        trace = result.get("trace", {})

        with st.expander("🔎 View Orchestrator Trace"):

            st.markdown("### 1️⃣ Intent")

            if trace.get("intent"):
                st.json(trace["intent"])

            st.markdown("### 2️⃣ Query Plan")

            if trace.get("query_plan"):
                st.json(trace["query_plan"])

            st.markdown("### 3️⃣ Validation")

            validation = trace.get("validation")

            if validation:

                if validation.get("valid"):
                    st.success("✓ Query passed validation.")
                else:
                    st.error("✗ Query failed validation.")

                st.json(validation)

            st.markdown("### 4️⃣ Semantic Layer")

            if trace.get("semantic_layer"):
                st.json(trace["semantic_layer"])

            st.markdown("### 5️⃣ Execution")

            if trace.get("execution"):
                st.json(trace["execution"])


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "MetricMind | AI Orchestrator | "
    "Enterprise Analytics & Agentic AI"
)