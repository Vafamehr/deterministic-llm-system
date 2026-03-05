"""
Pipeline entrypoint.

Run from: projects/delay_risk_pipeline
Set env:  PYTHONPATH=src

This script orchestrates:
load → validate → feature construction → representation → fact packets → assessment
and writes artifacts to outputs/
"""

from __future__ import annotations
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import json
from pathlib import Path

import pandas as pd
from datetime import datetime
from pathlib import Path

from delay_risk.validation.validate import (
    ValidationRules,
    validate_inputs,
    write_validation_report,
)
from delay_risk.features.build_features import build_features
from delay_risk.representation.summarize import summarize_projects
from delay_risk.representation.fact_packets import build_fact_packets

# src/ imports (PYTHONPATH=src)
from orchestrator import run_pipeline
from fact_packet_reader import load_fact_packets


# ------------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------------

DATA_PATH = Path("data/sample_projects.csv")
OUTPUT_DIR = Path("outputs")


# ------------------------------------------------------------------
# IO
# ------------------------------------------------------------------

def load_data(path: Path) -> pd.DataFrame:
    """Data interface (simple CSV load for now)."""
    return pd.read_csv(path)


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


# ------------------------------------------------------------------
# PIPELINE
# ------------------------------------------------------------------

def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading data...")
    df = load_data(DATA_PATH)

    print("Running validation...")
    rules = ValidationRules(numeric_ranges={})
    result = validate_inputs(df, mode="score", rules=rules)

    report_path = write_validation_report(
        result,
        output_dir=OUTPUT_DIR,
        mode="score",
    )
    print(f"Validation report saved to {report_path}")

    if not result.ok:
        raise RuntimeError("Validation failed. See report.")

    print("Building features...")
    feat_df = build_features(df)
    feature_file = OUTPUT_DIR / "feature_table.csv"
    feat_df.to_csv(feature_file, index=False)
    print(f"Feature table written to {feature_file}")

    print("Summarizing projects (representation layer)...")
    summary_df = summarize_projects(feat_df)
    summary_file = OUTPUT_DIR / "project_summary.csv"
    summary_df.to_csv(summary_file, index=False)
    print(f"Project summary written to {summary_file}")

    print("Building fact packets...")
    packet_df = build_fact_packets(summary_df)
    packet_file = OUTPUT_DIR / "project_fact_packets.csv"
    packet_df.to_csv(packet_file, index=False)
    print(f"Project fact packets written to {packet_file}")

    print("Running assessment (orchestrator)...")
    fact_packets = load_fact_packets(packet_file)
    assessment = run_pipeline(fact_packets)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    final_file = OUTPUT_DIR / f"final_assessment_{timestamp}.json"

    # Save historical run artifact
    write_json(final_file, assessment)
    print(f"Final assessment written to {final_file}")

    # Save latest example snapshot for GitHub / demos
    RUNS_DIR = Path("runs")
    RUNS_DIR.mkdir(exist_ok=True)

    example_run = RUNS_DIR / "example_run.json"
    write_json(example_run, assessment)

    print(f"Example run artifact written to {example_run}")

    print("Pipeline complete.")


if __name__ == "__main__":
    main()