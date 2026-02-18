import pandas as pd


def row_to_fact_packet(row: pd.Series) -> str:
    """
    Convert one project summary row into a compact, LLM-readable fact packet.
    Deterministic. No model calls. No guesswork.
    """
    project_id = row["project_id"]

    progress = float(row.get("progress", 0))
    weeks = int(row.get("weeks_observed", 0))

    avg_staffing = row.get("avg_staffing", None)
    volatility = row.get("staffing_volatility", None)

    lines = [
        f"Project: {project_id}",
        f"Progress: {progress:.2f}",
        f"Weeks observed: {weeks}",
    ]

    if pd.notna(avg_staffing):
        lines.append(f"Avg staffing: {float(avg_staffing):.2f}")

    if pd.notna(volatility):
        lines.append(f"Staffing volatility (3w std avg): {float(volatility):.2f}")

    return "\n".join(lines)


def build_fact_packets(summary_df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a 'fact_packet' column to the project summary table.
    """
    out = summary_df.copy()
    out["fact_packet"] = out.apply(row_to_fact_packet, axis=1)
    return out
