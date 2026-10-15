import matplotlib.pyplot as plt
import pandas as pd


def plot_temperature_and_precipitation(
    temperature: pd.DataFrame,
    precipitation: pd.DataFrame
) -> pd.DataFrame:
    """Plot temperature and precipitation using separate y-axes."""

    combined = temperature.merge(
        precipitation,
        on="date",
        how="outer",
        suffixes=("_temperature", "_precipitation"),
    ).sort_values("date")

    fig, ax1 = plt.subplots(figsize=(13, 5))

    ax1.plot(
        combined["date"],
        combined["value_temperature"],
        label="Mean temperature",
        linewidth=1.5,
    )
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Temperature (°C)")
    ax1.grid(True, alpha=0.3)

    ax2 = ax1.twinx()
    ax2.bar(
        combined["date"],
        combined["value_precipitation"],
        width=0.8,
        alpha=0.3,
        label="Daily precipitation",
    )
    ax2.set_ylabel("Precipitation (check returned unit)")

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

    ax1.set_title("Daily Temperature and Precipitation in Ås, 2025")

    fig.tight_layout()
    plt.show()

    return combined


def compare_temperatures(
    temperature_1925: pd.DataFrame,
    temperature_2025: pd.DataFrame
) -> pd.DataFrame:
    """Align and plot daily mean temperatures by month and day."""

    old = temperature_1925[["date", "value"]].copy()
    new = temperature_2025[["date", "value"]].copy()

    old["day"] = old["date"].dt.strftime("%m-%d")
    new["day"] = new["date"].dt.strftime("%m-%d")

    old = old[["day", "value"]].rename(columns={"value": "1925"})
    new = new[["day", "value"]].rename(columns={"value": "2025"})

    comparison = (
        old.merge(new, on="day", how="outer")
        .sort_values("day")
        .reset_index(drop=True)
    )

    fig, ax = plt.subplots(figsize=(13, 5))

    ax.plot(comparison["day"], comparison["1925"], label="1925")
    ax.plot(comparison["day"], comparison["2025"], label="2025")

    # Show fewer date labels so they remain readable.
    tick_positions = list(range(0, len(comparison), 30))
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(
        comparison["day"].iloc[tick_positions],
        rotation=45,
        ha="right",
    )

    ax.set_title("Daily Mean Temperature: 1925 vs 2025")
    ax.set_xlabel("Month-Day")
    ax.set_ylabel("Temperature (°C)")
    ax.legend()
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    plt.show()

    return comparison


def compare_summary_statistics(
    temperature_1925: pd.DataFrame,
    temperature_2025: pd.DataFrame
) -> pd.DataFrame:
    """Compare summary statistics for the two years."""

    statistics = pd.DataFrame({
        "1925": temperature_1925["value"].agg(
            ["mean", "median", "min", "max"]
        ),
        "2025": temperature_2025["value"].agg(
            ["mean", "median", "min", "max"]
        ),
    })

    statistics.index = ["Mean", "Median", "Minimum", "Maximum"]

    return statistics
