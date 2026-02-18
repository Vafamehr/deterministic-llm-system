"""
Validation entrypoint for delay_risk_pipeline.

Rule: pipeline code must call validate_inputs() before feature engineering,
training, or scoring.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List

import pandas as pd


@dataclass
class ValidationResult:
    ok: bool
    errors: List[str]
    warnings: List[str]
    stats: Dict[str, Any]



@dataclass
class ValidationRules:
    max_missing_frac: float = 0.5

    # column -> (min, max)
    numeric_ranges: Dict[str, tuple[float, float]] = field(default_factory=dict)


def validate_inputs(
    df: pd.DataFrame,
    *,
    mode: str,
    rules: ValidationRules | None = None,
    id_col: str = "project_id",
    time_col: str = "snapshot_week",
    label_col: str = "will_slip_4_6w",
    ) -> ValidationResult:
    """
    Minimal validation:
    - required columns exist
    - train mode has labels
    - dataframe is not empty
    - no duplicate (project_id, snapshot_week)
    """
    if rules is None:
        rules = ValidationRules()

    errors: List[str] = []
    warnings: List[str] = []
    stats: Dict[str, Any] = {}

    # --- Required columns ---
    required = {id_col, time_col}
    missing = sorted(list(required - set(df.columns)))
    if missing:
        errors.append(f"Missing required columns: {missing}")

    # --- Label required only for training ---
    if mode == "train" and label_col not in df.columns:
        errors.append(f"Training mode requires label_col '{label_col}'.")

    # --- Empty dataframe ---
    if len(df) == 0:
        errors.append("DataFrame has 0 rows.")

    # --- Duplicate key check ---
    if all(c in df.columns for c in [id_col, time_col]):
        dup_mask = df.duplicated([id_col, time_col])
        if dup_mask.any():
            dup_examples = df.loc[dup_mask, [id_col, time_col]].head(10)
            errors.append("Duplicate (id_col, time_col) keys found.")
            errors.append("Examples:\n" + dup_examples.to_string(index=False))

    # --- Stats (safe even if errors exist) ---
    stats["n_rows"] = int(df.shape[0])
    stats["n_cols"] = int(df.shape[1])
    if id_col in df.columns:
        stats["n_projects"] = int(df[id_col].nunique())

    ok = len(errors) == 0



    null_fraction = df.isna().mean()

    high_null_cols = null_fraction[null_fraction > rules.max_missing_frac]

    if len(high_null_cols) > 0:
        warnings.append(
            f"Columns with >{rules.max_missing_frac:.0%} missing values: "
            + ", ".join(high_null_cols.index.tolist())
        )


        # --- Numeric type sanity ---
    numeric_columns = df.select_dtypes(include=["number"]).columns

    if len(numeric_columns) == 0:
        warnings.append("No numeric columns detected — check data types.")


        # --- Example range check (if column exists) ---
    # --- Range checks from config ---
    for col, (lo, hi) in rules.numeric_ranges.items():
        if col not in df.columns:
            continue

        invalid = df[(df[col] < lo) | (df[col] > hi)]
        if len(invalid) > 0:
            errors.append(f"{col} outside [{lo},{hi}] for {len(invalid)} rows.")



    return ValidationResult(ok=ok, errors=errors, warnings=warnings, stats=stats)




import json
from datetime import datetime
from pathlib import Path


def write_validation_report(
    result: ValidationResult,
    *,
    output_dir: str | Path,
    mode: str,
) -> Path:
    """
    Persist validation results to disk for auditing/debugging.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    report = {
        "timestamp": datetime.now().isoformat(),
        "mode": mode,
        "ok": result.ok,
        "errors": result.errors,
        "warnings": result.warnings,
        "stats": result.stats,
    }

    output_path = output_dir / "validation_report.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    return output_path
