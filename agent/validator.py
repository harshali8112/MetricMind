# =========================================================
# METRICMIND - QUERY VALIDATOR
# =========================================================

SUPPORTED_METRICS = {
    "revenue",
    "margin",
    "cost",
    "churn"
}

SUPPORTED_REGIONS = {
    "Europe",
    "Asia"
}

SUPPORTED_QUARTERS = {
    "Q1",
    "Q2",
    "Q3",
    "Q4"
}

SUPPORTED_OPERATIONS = {
    "lookup",
    "compare",
    "multi_step"
}


# =========================================================
# MAIN VALIDATOR
# =========================================================

def validate_query_plan(query_plan: dict) -> dict:
    """
    Validate a Query Planner output before it
    reaches the Semantic Layer.

    The validator does not calculate business data.
    It only checks whether the query is safe and valid.
    """

    # -----------------------------------------------------
    # Basic structure
    # -----------------------------------------------------

    if not isinstance(query_plan, dict):

        return {
            "valid": False,
            "reason": "Query plan must be a dictionary."
        }

    if query_plan.get("status") != "valid":

        return {
            "valid": False,
            "reason": "Query Planner produced an invalid plan."
        }

    operation = query_plan.get("operation")

    if operation not in SUPPORTED_OPERATIONS:

        return {
            "valid": False,
            "reason":
                f"Unsupported operation: {operation}"
        }

    # -----------------------------------------------------
    # Validate metric
    # -----------------------------------------------------

    metric = query_plan.get(
        "metric"
    )

    primary_metric = query_plan.get(
        "primary_metric"
    )

    metric_to_validate = (
        metric
        if metric
        else primary_metric
    )

    if metric_to_validate:

        if metric_to_validate not in SUPPORTED_METRICS:

            return {
                "valid": False,
                "reason":
                    f"Unsupported metric: "
                    f"{metric_to_validate}"
            }

    # -----------------------------------------------------
    # Validate region
    # -----------------------------------------------------

    region = query_plan.get("region")

    if region:

        if region not in SUPPORTED_REGIONS:

            return {
                "valid": False,
                "reason":
                    f"Unsupported region: {region}"
            }

    # -----------------------------------------------------
    # Validate single lookup
    # -----------------------------------------------------

    if operation == "lookup":

        if not metric:

            return {
                "valid": False,
                "reason":
                    "Metric is required for lookup."
            }

        period = query_plan.get("period")

        if period:

            if period not in SUPPORTED_QUARTERS:

                return {
                    "valid": False,
                    "reason":
                        f"Unsupported quarter: {period}"
                }

        return {
            "valid": True,
            "reason": "Query passed validation."
        }

    # -----------------------------------------------------
    # Validate comparison
    # -----------------------------------------------------

    if operation == "compare":

        if not region:

            return {
                "valid": False,
                "reason":
                    "Region is required for comparison."
            }

        previous_period = query_plan.get(
            "previous_period"
        )

        current_period = query_plan.get(
            "current_period"
        )

        if not previous_period:

            return {
                "valid": False,
                "reason":
                    "Previous period is required "
                    "for comparison."
            }

        if not current_period:

            return {
                "valid": False,
                "reason":
                    "Current period is required "
                    "for comparison."
            }

        if previous_period not in SUPPORTED_QUARTERS:

            return {
                "valid": False,
                "reason":
                    f"Unsupported previous period: "
                    f"{previous_period}"
            }

        if current_period not in SUPPORTED_QUARTERS:

            return {
                "valid": False,
                "reason":
                    f"Unsupported current period: "
                    f"{current_period}"
            }

        if previous_period == current_period:

            return {
                "valid": False,
                "reason":
                    "Previous and current periods "
                    "cannot be the same."
            }

        return {
            "valid": True,
            "reason": "Query passed validation."
        }

    # -----------------------------------------------------
    # Validate multi-step query
    # -----------------------------------------------------

    if operation == "multi_step":

        queries = query_plan.get(
            "queries"
        )

        if not queries:

            return {
                "valid": False,
                "reason":
                    "Multi-step query must contain "
                    "at least one query."
            }

        if not isinstance(queries, list):

            return {
                "valid": False,
                "reason":
                    "Multi-step queries must be a list."
            }

        for query in queries:

            if not isinstance(query, dict):

                return {
                    "valid": False,
                    "reason":
                        "Each multi-step query "
                        "must be a dictionary."
                }

            metric = query.get("metric")

            if metric not in SUPPORTED_METRICS:

                return {
                    "valid": False,
                    "reason":
                        f"Unsupported metric in "
                        f"multi-step query: {metric}"
                }

            query_region = query.get(
                "region"
            )

            if query_region not in SUPPORTED_REGIONS:

                return {
                    "valid": False,
                    "reason":
                        f"Unsupported region in "
                        f"multi-step query: "
                        f"{query_region}"
                }

            previous_period = query.get(
                "previous_period"
            )

            current_period = query.get(
                "current_period"
            )

            if previous_period not in SUPPORTED_QUARTERS:

                return {
                    "valid": False,
                    "reason":
                        f"Unsupported previous period "
                        f"in multi-step query: "
                        f"{previous_period}"
                }

            if current_period not in SUPPORTED_QUARTERS:

                return {
                    "valid": False,
                    "reason":
                        f"Unsupported current period "
                        f"in multi-step query: "
                        f"{current_period}"
                }

            if previous_period == current_period:

                return {
                    "valid": False,
                    "reason":
                        "Multi-step query cannot "
                        "compare the same period."
                }

        return {
            "valid": True,
            "reason":
                "Multi-step query passed validation."
        }

    return {
        "valid": False,
        "reason":
            "Query could not be validated."
    }