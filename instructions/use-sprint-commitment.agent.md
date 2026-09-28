# Using the Sprint Commitment Calculator

- Use `./tools/sprint_commitment.py` when asked to calculate total estimated commitment for a sprint and list committed issues that have no estimate.
- Explain that the calculator reads a JSON snapshot; it does not connect to Jira or reconstruct history itself. The input must represent issue membership and estimates at the sprint's official start.
- Prepare or obtain a UTF-8 JSON snapshot with this structure:

  ```json
  {
    "sprint_id": "42",
    "issues": [
      {
        "key": "PROJ-123",
        "issue_type": "Story",
        "sprint_ids_at_start": ["42"],
        "story_points_at_start": 5
      },
      {
        "key": "PROJ-124",
        "issue_type": "Task",
        "sprint_ids_at_start": ["42"],
        "story_points_at_start": null
      }
    ]
  }
  ```

- Include each relevant issue with its Jira key, issue type, sprint IDs at sprint start, and story-point estimate at sprint start. Use `null` for an unestimated issue. Issues not assigned to the selected sprint at sprint start are not counted.
- Run from the repository root with the required sprint identifier and snapshot path:

  ```sh
  python3 tools/sprint_commitment.py 42 --snapshot path/to/snapshot.json
  ```

- To include independently estimated subtasks, only when explicitly requested or configured for the calculation, add `--include-subtasks`.
- Report the script's output clearly: sprint ID, total estimated sprint commitment in story points, and the unestimated committed issue keys. Preserve “None” when there are no unestimated committed issues.
- Do not treat current sprint membership or current estimates as sprint-start values. If reliable boundary data is unavailable, explain the limitation and do not present the result as an auditable sprint-start commitment.
- Do not silently omit malformed, duplicate, or mismatched snapshot data. Surface the script's error and correct the input before reporting a result.
- Do not edit Jira or claim the tool refreshed or verified source data; it only calculates from the supplied snapshot.
