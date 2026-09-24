# =========================================================
# METRICMIND - SEMANTIC LAYER API CLIENT
# =========================================================


class SemanticLayerAPI:
    """
    Interface between the AI Orchestrator and
    the Semantic Layer.

    The Orchestrator sends a structured query.
    The Semantic Layer returns verified business data.

    Calculations are performed before the data
    reaches the LLM.
    """

    def __init__(self):
        self.base_url = None

    def execute_query(self, query_plan: dict) -> dict:

        if query_plan.get("status") != "valid":
            return {
                "status": "error",
                "message": "Invalid query plan."
            }

        operation = query_plan.get("operation")

        if operation == "compare":
            return self._mock_comparison(query_plan)

        if operation == "lookup":
            return self._mock_lookup(query_plan)

        if operation == "multi_step":
            return self._execute_multi_step(query_plan)

        return {
            "status": "error",
            "message":
                f"Unsupported operation: {operation}"
        }

    # =====================================================
    # MULTI-STEP EXECUTION
    # =====================================================

    def _execute_multi_step(self, query_plan: dict):

        queries = query_plan.get("queries", [])

        if not queries:
            return {
                "status": "error",
                "message":
                    "No queries found in multi-step plan."
            }

        results = []

        for query in queries:

            result = self._mock_comparison(query)

            if result["status"] != "success":

                return {
                    "status": "error",
                    "message":
                        f"Multi-step execution failed "
                        f"at step {query.get('step')}. "
                        f"{result.get('message')}"
                }

            results.append({
                "step": query.get("step"),
                "metric": query.get("metric"),
                "result": result
            })

        return {
            "status": "success",
            "source": "semantic_layer",
            "operation": "multi_step",
            "primary_metric":
                query_plan.get("primary_metric"),
            "region":
                query_plan.get("region"),
            "previous_period":
                query_plan.get("previous_period"),
            "current_period":
                query_plan.get("current_period"),
            "steps": results
        }

    # =====================================================
    # COMPARISON QUERY
    # =====================================================

    def _mock_comparison(self, query_plan: dict):

        region = query_plan["region"]
        metric = query_plan["metric"]

        previous_period = query_plan["previous_period"]
        current_period = query_plan["current_period"]

        business_data = {

            ("Europe", "Q2"): {
                "revenue": 1000000,
                "cost": 760000,
                "margin": 24
            },

            ("Europe", "Q3"): {
                "revenue": 1100000,
                "cost": 902000,
                "margin": 18
            },

            ("Asia", "Q2"): {
                "revenue": 800000,
                "cost": 560000,
                "margin": 30
            },

            ("Asia", "Q3"): {
                "revenue": 900000,
                "cost": 585000,
                "margin": 35
            }
        }

        previous_key = (
            region,
            previous_period
        )

        current_key = (
            region,
            current_period
        )

        if previous_key not in business_data:

            return {
                "status": "error",
                "message":
                    f"No data available for "
                    f"{region} {previous_period}."
            }

        if current_key not in business_data:

            return {
                "status": "error",
                "message":
                    f"No data available for "
                    f"{region} {current_period}."
            }

        previous = business_data[previous_key]
        current = business_data[current_key]

        revenue_change = (
            current["revenue"]
            - previous["revenue"]
        )

        cost_change = (
            current["cost"]
            - previous["cost"]
        )

        margin_change = (
            current["margin"]
            - previous["margin"]
        )

        revenue_percentage_change = (
            revenue_change
            / previous["revenue"]
        ) * 100

        cost_percentage_change = (
            cost_change
            / previous["cost"]
        ) * 100

        if revenue_percentage_change > cost_percentage_change:

            growth_relationship = (
                "Revenue grew faster than cost."
            )

        elif revenue_percentage_change < cost_percentage_change:

            growth_relationship = (
                "Cost grew faster than revenue."
            )

        else:

            growth_relationship = (
                "Revenue and cost grew at "
                "the same rate."
            )

        if margin_change > 0:

            margin_direction = "Margin increased."

        elif margin_change < 0:

            margin_direction = "Margin decreased."

        else:

            margin_direction = (
                "Margin remained unchanged."
            )

        return {

            "status": "success",

            "source": "semantic_layer",

            "operation": "compare",

            "query": {

                "metric": metric,

                "region": region,

                "previous_period":
                    previous_period,

                "current_period":
                    current_period
            },

            "data": {

                "previous": previous,

                "current": current
            },

            "verified_analysis": {

                "revenue_change":
                    revenue_change,

                "revenue_percentage_change":
                    round(
                        revenue_percentage_change,
                        2
                    ),

                "cost_change":
                    cost_change,

                "cost_percentage_change":
                    round(
                        cost_percentage_change,
                        2
                    ),

                "margin_change":
                    round(
                        margin_change,
                        2
                    ),

                "growth_relationship":
                    growth_relationship,

                "margin_direction":
                    margin_direction
            }
        }

    # =====================================================
    # SINGLE METRIC LOOKUP
    # =====================================================

    def _mock_lookup(self, query_plan: dict):

        metric = query_plan["metric"]

        region = query_plan.get("region")

        period = query_plan.get("period")

        metric_definitions = {

            "revenue":
                "Revenue = Total sales generated by the business.",

            "margin":
                "Margin = (Revenue - Cost) / Revenue * 100.",

            "cost":
                "Cost = Total business cost incurred during the period.",

            "churn":
                "Churn = Percentage of customers who stopped using the service."
        }

        if metric not in metric_definitions:

            return {
                "status": "error",
                "message":
                    f"Metric '{metric}' not found."
            }

        # ---------------------------------------------
        # Business data
        # ---------------------------------------------

        business_data = {

            ("Europe", "Q2"): {
                "revenue": 1000000,
                "cost": 760000,
                "margin": 24
            },

            ("Europe", "Q3"): {
                "revenue": 1100000,
                "cost": 902000,
                "margin": 18
            },

            ("Asia", "Q2"): {
                "revenue": 800000,
                "cost": 560000,
                "margin": 30
            },

            ("Asia", "Q3"): {
                "revenue": 900000,
                "cost": 585000,
                "margin": 35
            }
        }

        # ---------------------------------------------
        # If region and period are provided,
        # return the actual business value.
        # ---------------------------------------------

        if region and period:

            key = (
                region,
                period
            )

            if key not in business_data:

                return {
                    "status": "error",
                    "message":
                        f"No data available for "
                        f"{region} {period}."
                }

            data = business_data[key]

            value = data[metric]

            return {

                "status": "success",

                "source": "semantic_layer",

                "operation": "lookup",

                "query": {

                    "metric": metric,

                    "region": region,

                    "period": period
                },

                "metric_definition":
                    metric_definitions[metric],

                "data": {

                    "value": value
                }
            }

        # ---------------------------------------------
        # Metric definition only
        # ---------------------------------------------

        return {

            "status": "success",

            "source": "semantic_layer",

            "operation": "lookup",

            "query": {

                "metric": metric,

                "region": region,

                "period": period
            },

            "metric_definition":
                metric_definitions[metric]
        }