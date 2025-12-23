import numpy as np
import pandas as pd

def linear_forecast(series, periods):
    x = np.arange(len(series))
    y = series.values

    m, c = np.polyfit(x, y, 1)

    future_x = np.arange(len(series), len(series) + periods)
    future_y = m * future_x + c

    return future_y


def growth_forecast(last_value, growth_rate, periods):
    return [last_value * ((1 + growth_rate) ** i) for i in range(1, periods + 1)]