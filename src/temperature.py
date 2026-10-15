
import matplotlib.pyplot as plt
import pandas as pd


def summary_statistics(data):
    """Calculate mean, median, minimum, and maximum."""

    values = data["value"].dropna()

    return values.agg(["mean", "median", "min", "max"])


def calculate_moving_average(data, window=7):
    """Calculate a rolling average over the requested number of days."""

    if window < 1:
        raise ValueError("window must be at least 1.")

    result = data.copy().sort_values("date")
    result["moving_average"] = (
        result["value"].rolling(window=window, min_periods=window).mean()
    )

    return result


def plot_temperature(data, title="Daily Mean Air Temperature"):
    """Plot daily temperature over time."""

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(data["date"], data["value"], linewidth=1)
    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Temperature (°C)")
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    plt.show()


def plot_moving_average(data, window=7):
    """Plot daily temperatures as points and the moving average as a line."""

    result = calculate_moving_average(data, window=window)

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.scatter(
        result["date"],
        result["value"],
        s=12,
        label="Daily mean temperature",
    )

    ax.plot(
        result["date"],
        result["moving_average"],
        linewidth=2,
        label=f"{window}-day moving average",
    )

    ax.set_title(f"Daily Temperature and {window}-Day Moving Average")
    ax.set_xlabel("Date")
    ax.set_ylabel("Temperature (°C)")
    ax.legend()
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    plt.show()

    return result
