# =========================================================
# METRICMIND - QUERY PLANNER
# =========================================================

def create_query_plan(intent: dict) -> dict:
    """
    Convert extracted intent into a structured
    Semantic Layer query plan.

    The Query Planner decides WHAT information
    the Orchestrator needs.

    It does NOT calculate business metrics.
    """

    # =====================================================
    # EXTRACT INTENT INFORMATION
    # =====================================================

    region = intent.get("region")
    metric = intent.get("metric")

    previous_quarter = intent.get(
        "previous_quarter"
    )

    current_quarter = intent.get(
        "current_quarter"
    )

    intent_type = intent.get(
        "intent"
    )

    # =====================================================
    # BASIC METRIC VALIDATION
    # =====================================================

    if not metric:

        return {
            "status": "invalid",
            "reason":
                "No supported business metric identified."
        }

    # =====================================================
    # COMPARISON QUERY
    # =====================================================

    if intent_type == "comparison":

        # -------------------------------------------------
        # Region required
        # -------------------------------------------------

        if not region:

            return {
                "status": "invalid",
                "reason":
                    "Region is required for a comparison query."
            }

        # -------------------------------------------------
        # Two periods required
        # -------------------------------------------------

        if not previous_quarter:

            return {
                "status": "invalid",
                "reason":
                    "Previous quarter is required "
                    "for a comparison query."
            }

        if not current_quarter:

            return {
                "status": "invalid",
                "reason":
                    "Current quarter is required "
                    "for a comparison query."
            }

        # =================================================
        # MULTI-STEP PLAN
        # =================================================

        queries = [

            {
                "step": 1,

                "operation": "compare",

                "metric": metric,

                "region": region,

                "previous_period":
                    previous_quarter,

                "current_period":
                    current_quarter
            }
        ]

        # -------------------------------------------------
        # Margin analysis requires Revenue + Cost
        # -------------------------------------------------

        if metric == "margin":

            queries.append(
                {
                    "step": 2,

                    "operation": "compare",

                    "metric": "revenue",

                    "region": region,

                    "previous_period":
                        previous_quarter,

                    "current_period":
                        current_quarter
                }
            )

            queries.append(
                {
                    "step": 3,

                    "operation": "compare",

                    "metric": "cost",

                    "region": region,

                    "previous_period":
                        previous_quarter,

                    "current_period":
                        current_quarter
                }
            )

        # =================================================
        # RETURN MULTI-STEP PLAN
        # =================================================

        return {

            "status": "valid",

            "operation": "multi_step",

            "primary_metric":
                metric,

            "region":
                region,

            "previous_period":
                previous_quarter,

            "current_period":
                current_quarter,

            "queries":
                queries
        }

    # =====================================================
    # SINGLE METRIC LOOKUP
    # =====================================================

    if intent_type == "metric_lookup":

        return {

            "status": "valid",

            "operation": "lookup",

            "metric":
                metric,

            "region":
                region,

            "period":
                current_quarter
        }

    # =====================================================
    # UNSUPPORTED INTENT
    # =====================================================

    return {

        "status": "invalid",

        "reason":
            f"Unsupported intent type: {intent_type}"
    }