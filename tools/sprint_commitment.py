#!/usr/bin/env python3
"""Calculate sprint commitment from an issue snapshot captured at sprint start.

Snapshot JSON format:
{
  "sprint_id": "42",
  "issues": [
    {
      "key": "PROJ-123",
      "issue_type": "Story",
      "sprint_ids_at_start": ["42"],
      "story_points_at_start": 5
    }
  ]
}

Use null for story_points_at_start when an issue was unestimated at sprint start.
"""

import argparse
import json
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any


def is_subtask(issue_type: str) -> bool:
    normalized = "".join(character for character in issue_type.casefold() if character.isalnum())
    return normalized in {"subtask", "subtasks"}


def validate_snapshot(snapshot: Any, sprint_id: str) -> list[dict[str, Any]]:
    if not isinstance(snapshot, dict):
        raise ValueError("snapshot must be a JSON object")
    if str(snapshot.get("sprint_id", "")) != sprint_id:
        raise ValueError(
            f"snapshot sprint_id {snapshot.get('sprint_id')!r} does not match "
            f"requested sprint {sprint_id!r}"
        )

    issues = snapshot.get("issues")
    if not isinstance(issues, list):
        raise ValueError("snapshot 'issues' must be a JSON array")

    validated: list[dict[str, Any]] = []
    seen_keys: set[str] = set()
    for index, issue in enumerate(issues):
        prefix = f"issues[{index}]"
        if not isinstance(issue, dict):
            raise ValueError(f"{prefix} must be a JSON object")

        key = issue.get("key")
        if not isinstance(key, str) or not key.strip():
            raise ValueError(f"{prefix}.key must be a non-empty string")
        if key in seen_keys:
            raise ValueError(f"duplicate issue key {key!r} in snapshot")
        seen_keys.add(key)

        issue_type = issue.get("issue_type")
        if not isinstance(issue_type, str) or not issue_type.strip():
            raise ValueError(f"{prefix}.issue_type must be a non-empty string")

        sprint_ids = issue.get("sprint_ids_at_start")
        if not isinstance(sprint_ids, list):
            raise ValueError(f"{prefix}.sprint_ids_at_start must be a JSON array")
        if any(not isinstance(value, (str, int)) or isinstance(value, bool) for value in sprint_ids):
            raise ValueError(f"{prefix}.sprint_ids_at_start values must be strings or integers")

        if "story_points_at_start" not in issue:
            raise ValueError(f"{prefix}.story_points_at_start is required; use null if unestimated")
        raw_points = issue["story_points_at_start"]
        if raw_points is None:
            points = None
        else:
            if isinstance(raw_points, bool) or not isinstance(raw_points, (int, float, Decimal)):
                raise ValueError(f"{prefix}.story_points_at_start must be a non-negative number or null")
            try:
                points = Decimal(str(raw_points))
            except InvalidOperation as error:
                raise ValueError(
                    f"{prefix}.story_points_at_start must be a non-negative number or null"
                ) from error
            if not points.is_finite() or points < 0:
                raise ValueError(f"{prefix}.story_points_at_start must be finite and non-negative")

        validated.append(
            {
                "key": key,
                "issue_type": issue_type,
                "sprint_ids_at_start": sprint_ids,
                "story_points_at_start": points,
            }
        )

    return validated


def read_snapshot(path: Path, sprint_id: str) -> list[dict[str, Any]]:
    try:
        with path.open(encoding="utf-8") as snapshot_file:
            snapshot = json.load(snapshot_file, parse_float=Decimal)
    except OSError as error:
        raise ValueError(f"cannot read snapshot file {path}: {error}") from error
    except json.JSONDecodeError as error:
        raise ValueError(f"invalid JSON in {path}: {error}") from error
    return validate_snapshot(snapshot, sprint_id)


def format_points(points: Decimal) -> str:
    return format(points.normalize(), "f")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Calculate commitment using sprint-start issue membership and estimates "
            "from a JSON snapshot."
        ),
        epilog=(
            "The snapshot must contain sprint_id and issues with key, issue_type, "
            "sprint_ids_at_start, and story_points_at_start fields. Use null for "
            "an unestimated issue. Subtasks are excluded unless --include-subtasks is set."
        ),
    )
    parser.add_argument("sprint_id", help="identifier of the sprint to calculate")
    parser.add_argument(
        "--snapshot",
        required=True,
        type=Path,
        help="path to JSON data captured or reconstructed for the sprint start",
    )
    parser.add_argument(
        "--include-subtasks",
        action="store_true",
        help="include subtask estimates when calculating commitment",
    )
    args = parser.parse_args()

    try:
        issues = read_snapshot(args.snapshot, args.sprint_id)
    except ValueError as error:
        parser.error(str(error))

    committed = [
        issue
        for issue in issues
        if any(str(value) == args.sprint_id for value in issue["sprint_ids_at_start"])
        and (args.include_subtasks or not is_subtask(issue["issue_type"]))
    ]
    estimated_total = sum(
        (
            issue["story_points_at_start"]
            for issue in committed
            if issue["story_points_at_start"] is not None
        ),
        start=Decimal(0),
    )
    unestimated = [
        issue["key"] for issue in committed if issue["story_points_at_start"] is None
    ]

    print(f"Sprint: {args.sprint_id}")
    print(f"Total estimated sprint commitment: {format_points(estimated_total)} story points")
    print("Unestimated committed issues:")
    if unestimated:
        for key in unestimated:
            print(f"- {key}")
    else:
        print("- None")


if __name__ == "__main__":
    main()
