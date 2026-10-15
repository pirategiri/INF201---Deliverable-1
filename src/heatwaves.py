
from pathlib import Path

import pandas as pd
import yaml

from src.data_loader import get_daily_data


def count_heatwaves(station_id, year, output_dir="outputs"):
    """Count heatwaves and save a YAML summary.

    A heatwave is five or more consecutive calendar days
    with daily maximum temperature >= 27 degrees Celsius.
    """

    year = int(year)

    data = get_daily_data(
        station_id=station_id,
        element="max(air_temperature P1D)",
        start_date=f"{year}-01-01",
        end_date=f"{year}-12-31",
    )

    data = data.set_index("date").sort_index()

    # Include every calendar day. Missing observations break a run.
    calendar = pd.date_range(
        start=f"{year}-01-01",
        end=f"{year}-12-31",
        freq="D",
    )

    daily_values = data["value"].reindex(calendar)
    hot_days = daily_values.ge(27).fillna(False)

    heatwaves = []
    run_start = None
    previous_day = None

    for date, is_hot in hot_days.items():
        if is_hot:
            if run_start is None:
                run_start = date

            previous_day = date

        else:
            if run_start is not None:
                duration = (previous_day - run_start).days + 1

                if duration >= 5:
                    heatwaves.append({
                        "start_date": run_start.strftime("%Y-%m-%d"),
                        "end_date": previous_day.strftime("%Y-%m-%d"),
                        "duration_days": duration,
                    })

                run_start = None
                previous_day = None

    # Handle a heatwave that continues through 31 December.
    if run_start is not None:
        duration = (previous_day - run_start).days + 1

        if duration >= 5:
            heatwaves.append({
                "start_date": run_start.strftime("%Y-%m-%d"),
                "end_date": previous_day.strftime("%Y-%m-%d"),
                "duration_days": duration,
            })

    summary = {
        "station_id": station_id,
        "year": year,
        "threshold_celsius": 27,
        "minimum_consecutive_days": 5,
        "number_of_heatwaves": len(heatwaves),
        "heatwaves": heatwaves,
    }

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    filename = f"heatwaves_{station_id}_{year}.yml"
    file_path = output_path / filename

    with file_path.open("w", encoding="utf-8") as file:
        yaml.safe_dump(
            summary,
            file,
            sort_keys=False,
            allow_unicode=True,
        )

    print(f"Heatwave summary saved to: {file_path}")

    return summary
