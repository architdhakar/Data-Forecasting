import numpy as np

def lagged_correlation(x, y, max_lag=6):
    best_lag = 0
    best_corr = 0

    for lag in range(1, max_lag + 1):
        shifted = x.shift(lag)
        corr = shifted.corr(y)

        if corr is not None and abs(corr) > abs(best_corr):
            best_corr = corr
            best_lag = lag

    return best_lag, best_corr


def sensitivity(x, y):
    x_pct = x.pct_change()
    y_pct = y.pct_change()

    aligned = x_pct.align(y_pct, join="inner")
    aligned = aligned[0].dropna(), aligned[1].dropna()

    if len(aligned[0]) < 3:
        return 0

    beta = np.polyfit(aligned[0], aligned[1], 1)[0]
    return beta


def trend_match(x, y):
    return np.sign(x.iloc[-1] - x.iloc[0]) == np.sign(y.iloc[-1] - y.iloc[0])


def causal_score(corr, lag_corr, beta, trend_sync):
    score = 0

    if abs(corr) > 0.7:
        score += 3
    elif abs(corr) > 0.4:
        score += 2

    if abs(lag_corr) > 0.5:
        score += 3

    if abs(beta) > 1:
        score += 2

    if trend_sync:
        score += 2

    return score


def influence_analysis(df, target_col):
    results = []
    y = df[target_col]

    for col in df.columns:
        if col == target_col:
            continue

        x = df[col]

        corr = x.corr(y)
        lag, lag_corr = lagged_correlation(x, y)
        beta = sensitivity(x, y)
        sync = trend_match(x, y)
        score = causal_score(corr, lag_corr, beta, sync)

        if score >= 6:  # only meaningful relations
            results.append({
                "factor": col,
                "score": score,
                "correlation": round(corr, 2),
                "lag": lag,
                "impact": round(beta, 2)
            })

    return sorted(results, key=lambda r: r["score"], reverse=True)
