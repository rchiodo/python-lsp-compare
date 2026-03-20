import pandas as pd


def build_report() -> pd.DataFrame:
    frame = pd.DataFrame(
        {
            "team": ["search", "search", "editor", "editor"],
            "tickets": [4, 6, 3, 5],
            "hours": [12.5, 14.0, 8.5, 9.0],
        }
    )
    grouped = frame.groupby("team").agg({"tickets": "sum", "hours": "mean"})
    grouped["velocity"] = grouped["tickets"] / grouped["hours"]
    return grouped.reset_index()


report = build_report()
velocity_series = report["velocity"]