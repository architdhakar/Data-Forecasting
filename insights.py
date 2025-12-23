import numpy as np

def analyze_metric(series):
    start, end = series.iloc[0], series.iloc[-1]
    change = end - start
    pct_change = (change / start) * 100 if start != 0 else 0

    if pct_change > 5:
        trend = "Strong Increase"
    elif pct_change > 1:
        trend = "Moderate Increase"
    elif pct_change < -5:
        trend = "Strong Decrease"
    elif pct_change < -1:
        trend = "Moderate Decrease"
    else:
        trend = "Stable"

    return trend, round(pct_change, 2)


def generate_insight(metric, trend, pct):
    if "Increase" in trend:
        return f"{metric} has increased by {pct}%, indicating positive growth."
    elif "Decrease" in trend:
        return f"{metric} has decreased by {pct}%, indicating potential issues."
    else:
        return f"{metric} has remained stable with minimal change."


def improvement_suggestion(metric, trend):
    metric = metric.lower()

    if "revenue" in metric or "sales" in metric:
        if "Decrease" in trend:
            return "Consider reviewing pricing strategy, marketing effectiveness, or customer retention."
        return "Focus on scaling operations while maintaining margins."

    if "cost" in metric:
        if "Increase" in trend:
            return "Investigate operational inefficiencies and supplier contracts."
        return "Cost control appears effective."

    if "employee" in metric:
        if "Increase" in trend:
            return "Ensure workforce growth aligns with productivity."
        return "Evaluate hiring strategy and workload distribution."

    return "Monitor this metric and investigate external or internal influencing factors."
