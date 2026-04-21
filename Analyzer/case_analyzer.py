#!/usr/bin/env python3

import json
import sys
from pathlib import Path


def load_case_input(input_path: Path) -> dict:
    with input_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def build_report(case_data: dict) -> dict:
    case_id = case_data.get("case_id", "unknown_case")
    os_type = case_data.get("os", "unknown")
    target_file = case_data.get("target_file", "")
    scanner_alert = case_data.get("scanner_alert", "")
    recommended_action = case_data.get("recommended_action", "")

    if target_file and "quarantine" in recommended_action.lower():
        status = "ready_for_quarantine"
        risk_level = "medium"
        action_taken = "Generated quarantine recommendation"
        reason = "Flagged file identified and quarantine was recommended for safe dependency validation"
        next_steps = [
            "Run the appropriate quarantine script for the operating system",
            "Monitor application and service behavior",
            "Check for dependency or startup failures",
            "Restore the file if issues occur",
            "Remove permanently only after validation"
        ]
    else:
        status = "needs_review"
        risk_level = "unknown"
        action_taken = "Unable to determine safe action from provided input"
        reason = "Case data did not clearly support quarantine workflow"
        next_steps = [
            "Review case input",
            "Confirm target artifact path",
            "Confirm recommended remediation action"
        ]

    report = {
        "case_id": case_id,
        "os": os_type,
        "target_file": target_file,
        "scanner_alert": scanner_alert,
        "status": status,
        "risk_level": risk_level,
        "action_taken": action_taken,
        "reason": reason,
        "next_steps": next_steps
    }

    return report


def write_report(report: dict, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: python analyze_logs.py <input_json> <output_json>")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    if not input_path.is_file():
        print(f"Input file not found: {input_path}")
        sys.exit(1)

    case_data = load_case_input(input_path)
    report = build_report(case_data)
    write_report(report, output_path)

    print("Analysis complete.")
    print(f"Input:  {input_path}")
    print(f"Output: {output_path}")


if __name__ == "__main__":
    main()