import pandas as pd


def summarize_projects(df: pd.DataFrame) -> pd.DataFrame:
    """
    Collapse project-week rows into one record per project.
    This is what downstream reasoning consumes.
    """

    summary = (
        df.groupby("project_id")
        .agg(
            weeks_observed=("weeks_observed", "max"),
            avg_staffing=("staffing_level", "mean"),
            staffing_volatility=("staffing_roll_std_3", "mean"),
            progress=("week_progress", "max"),
        )
        .reset_index()
    )

    return summary
