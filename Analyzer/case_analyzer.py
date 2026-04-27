#!/usr/bin/env python3

import argparse
import json
from pathlib import Path


def load_case_input(input_path: Path) -> dict:
    with input_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def get_recommended_script(os_type: str) -> str:
    os_type = os_type.lower()

    if os_type == "linux":
        return "quarantine_file.sh"

    if os_type == "windows":
        return "quarantine_file.ps1"

    return "manual_review_required"


def build_report(case_data: dict) -> dict:
    case_id = case_data.get("case_id", "unknown_case")
    os_type = case_data.get("os", "unknown")
    target_file = case_data.get("target_file", "")
    scanner_alert = case_data.get("scanner_alert", "")
    recommended_action = case_data.get("recommended_action", "")

    recommended_script = get_recommended_script(os_type)

    if target_file and "quarantine" in recommended_action.lower():
        status = "ready_for_quarantine"
        risk_level = "medium"
        action_taken = "Generated quarantine recommendation"
        reason = (
            "Flagged file identified and quarantine was recommended "
            "for safe dependency validation."
        )
        next_steps = [
            f"Run the recommended script: {recommended_script}",
            "Move the file to a quarantine directory instead of deleting it",
            "Monitor application and service behavior",
            "Check for dependency or startup failures",
            "Restore the file if issues occur",
            "Remove permanently only after validation"
        ]
    else:
        status = "needs_review"
        risk_level = "unknown"
        action_taken = "Unable to determine safe action from provided input"
        reason = "Case data did not clearly support the quarantine workflow."
        next_steps = [
            "Review case input",
            "Confirm target artifact path",
            "Confirm recommended remediation action"
        ]

    return {
        "case_id": case_id,
        "os": os_type,
        "target_file": target_file,
        "scanner_alert": scanner_alert,
        "status": status,
        "risk_level": risk_level,
        "recommended_script": recommended_script,
        "action_taken": action_taken,
        "reason": reason,
        "next_steps": next_steps
    }


def write_report(report: dict, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=2)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze a structured support case input file and generate a case report."
    )

    parser.add_argument(
        "-i",
        "--input",
        required=True,
        help="Path to the case input JSON file."
    )

    parser.add_argument(
        "-o",
        "--output",
        required=True,
        help="Path where the generated report JSON should be written."
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.is_file():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    case_data = load_case_input(input_path)
    report = build_report(case_data)
    write_report(report, output_path)

    print("Analysis complete.")
    print(f"Input:  {input_path}")
    print(f"Output: {output_path}")
    print(f"Status: {report['status']}")
    print(f"Recommended script: {report['recommended_script']}")


if __name__ == "__main__":
    main()