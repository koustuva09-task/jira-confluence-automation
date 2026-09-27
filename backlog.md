# Migration Delivery Metrics Dashboard — Implementation Backlog

## Delivery approach

- [ ] Deliver the complete first-release scope as one MVP sequence across the phases below.
- [ ] Prioritize Jira configuration and historical data capture first, then trustworthy metric calculations, then dashboard views.
- [ ] Keep all dashboard access read-only; do not add individual performance rankings or scoring.
- [ ] Treat Jira as the system of record and preserve the last valid synchronized data when a refresh fails.
- [ ] Resolve the listed Jira and hosting decisions during Setup before implementation depends on them.

## Setup

- [ ] Confirm Jira deployment type (Cloud or Data Center), site URL, migration project key(s), Scrum board ID, and whether the first release covers one board.
- [ ] Obtain a dedicated read-only Jira integration identity and confirm its project and issue visibility.
- [ ] Select the approved hosting environment, technology stack, identity provider, and dashboard authorization roles.
- [ ] Inventory Jira custom fields and record IDs for story points, epic relationships, sprint, flags, and any target-date or fix-version data.
- [ ] Confirm included issue types and whether independently estimated subtasks are included in metrics.
- [ ] Agree on the blocked-work rule, including the applicable flag, blocked statuses, labels, or issue-link types.
- [ ] Confirm whether sprint commitment is baselined at the official Jira sprint start and document sprint-boundary semantics.
- [ ] Decide how estimate changes after sprint start affect commitment, added/removed scope, completed points, and velocity.
- [ ] Set dashboard timezone, active and historical refresh intervals, freshness threshold, retry limits, and historical retention period.
- [ ] Agree on configurable leadership status thresholds and confirm epic target dates or releases are reliable enough to display.
- [ ] Validate Jira changelog access and retention; identify fields whose history is unavailable or unreliable and require snapshots.
- [ ] Manually reconcile sample commitment, completion, scope change, spillover, and velocity calculations for two completed sprints.
- [ ] Define expected data volume, user load, and operational ownership for synchronization alerts and dashboard support.

## Core Features

### Data foundation and metric engine

- [ ] Define the normalized project, board, sprint, epic, issue, estimate-event, sprint-event, status-event, blocker-event, snapshot, metric-result, and sync-run data model.
- [ ] Persist Jira IDs and issue keys, source timestamps in UTC, source visibility/deletion state, and metric-definition version.
- [ ] Add constraints and idempotent upsert behavior so replaying Jira records or events does not duplicate data.
- [ ] Implement event and snapshot storage sufficient to reconstruct sprint-start membership, estimates, scope changes, sprint-end status, completion time, and blocker transitions.
- [ ] Implement versioned metric definitions and a recalculation path that does not silently replace historical values with current Jira state.
- [ ] Calculate sprint commitment from issue membership and estimates at the sprint start; disclose unestimated committed issues separately.
- [ ] Calculate completed points at sprint end from issues in the Done status category, including an as-of-now provisional value labeled “Completed so far” for the active sprint.
- [ ] Calculate predictability using only original-commitment points completed by sprint end; return “Not applicable” when commitment is zero.
- [ ] Calculate added and removed scope from sprint membership history, keeping removed commitment out of completed totals.
- [ ] Calculate spillover points, issue count, and retained-commitment percentage; record the destination sprint when an issue moves later.
- [ ] Calculate sprint velocity, a three-completed-sprint rolling average, and an optional six-sprint average when enough history exists.
- [ ] Calculate epic total, completed, remaining, and unestimated work; use issue-count completion when no child issues are estimated and label the basis.
- [ ] Calculate epic child issue counts by status category, current-sprint contribution, target metadata, and active blocked-child count.
- [ ] Identify active blockers using configured rules and expose blocked-since time and calendar-day age only when Jira history supports an accurate start time.
- [ ] Preserve unavailable or unknown metric values explicitly; never substitute zero or infer unavailable historical dates.

### API and dashboard

- [ ] Implement read-only endpoints for dashboard summary, sprint list and metrics, sprint issue drill-down, epic list and detail, blockers, and synchronization status.
- [ ] Return stable identifiers and an `asOf` timestamp; validate filters explicitly and paginate issue-level results.
- [ ] Apply project, board, sprint, epic, status-category, assignee, and date-range filters consistently across views and preserve selections during navigation.
- [ ] Build the executive summary with sprint dates, commitment, completion, predictability, scope change, spillover, rolling velocity, migration completion, and blocker counts.
- [ ] Build a trend view for at least six completed sprints with committed versus completed points, predictability, added/removed scope, spillover, velocity, and rolling velocity.
- [ ] Add sprint drill-down that classifies each issue as original commitment, added, removed, completed by sprint end, or spilled over.
- [ ] Build migration epic progress with completed and remaining points, unestimated work, current-sprint contribution, blocker count, target metadata, and sorting by completion, remaining work, blockers, or target date.
- [ ] Add epic drill-down showing child issues and their current delivery state.
- [ ] Build a blocked-work view sorted by blocked age descending by default, with epic/sprint context, assignee, points at risk, age, and Jira issue link.
- [ ] Provide blocker filters for sprint, epic, and assignee; use assignee only for operational filtering, not performance reporting.
- [ ] Show last successful synchronization, configured timezone, current/stale state, and metric-definition help text on every dashboard view.
- [ ] Ensure aggregate metrics can be drilled down to their contributing Jira issues and link directly to Jira.
- [ ] Make charts responsive and provide accessible text summaries or equivalent tables, keyboard operation, and status indicators that do not rely on color alone.
- [ ] Enforce authenticated, read-only access and ensure issue details shown by the dashboard respect source Jira visibility.
- [ ] Meet the target of initial filtered dashboard load within 3 seconds and synchronized filter updates within 2 seconds under expected usage.
- [ ] Use pagination or virtualization for issue lists and avoid exposing credentials or unnecessary personal data in API responses.

## Integration

- [ ] Implement Jira authentication using protected environment configuration or a secrets manager; keep credentials exclusively on the server.
- [ ] Implement Jira retrieval for configured projects, boards, sprints, issues, fields, issue changelogs, epic relationships, and blocker signals.
- [ ] Handle Jira pagination, rate limits, transient failures, and deployment-specific API behavior.
- [ ] Normalize Jira records and custom-field mappings into the agreed internal data model.
- [ ] Implement incremental synchronization and scheduled refreshes for active sprint data and historical sprint data using configured intervals.
- [ ] Trigger an additional synchronization shortly after sprint completion and support an authorized administrator’s manual refresh action.
- [ ] Capture scheduled boundary snapshots wherever Jira changelog data cannot reliably reconstruct required historical state.
- [ ] Record synchronization start, completion, duration, record counts, failures, rate-limit events, and last successful timestamp.
- [ ] Make synchronization idempotent and transactional enough that a partial retrieval cannot overwrite valid data or produce a success-shaped partial result.
- [ ] On failure, retain the most recent valid data, expose the error and stale state, and retry transient errors using bounded exponential backoff.
- [ ] Notify the configured administrator after repeated failures and alert when data freshness exceeds the configured threshold.
- [ ] Handle deleted or newly inaccessible Jira issues by marking their visibility/deletion state while retaining historical reporting context.
- [ ] Configure encrypted transport for Jira and dashboard traffic and apply least-privilege read-only Jira permissions.

## Testing

- [ ] Unit-test metric formulas and boundary timestamps, including zero commitment and unestimated issues.
- [ ] Test an issue committed and completed within a sprint, and one committed but carried into a later sprint.
- [ ] Test issues added after sprint start that are completed and not completed by sprint end.
- [ ] Test an issue removed after sprint start and verify removed points are neither completed nor counted as spillover.
- [ ] Test estimate changes during a sprint and verify configured treatment across commitment, scope, completion, and velocity.
- [ ] Test completion after sprint end and an issue reopened before sprint end against the Done-category-at-boundary rule.
- [ ] Test a zero-point sprint returns predictability as “Not applicable.”
- [ ] Test estimate-free epics use issue-count completion and clearly disclose the basis and unestimated work.
- [ ] Test an issue moved between epics and verify historical sprint reporting and current epic progress remain consistent.
- [ ] Test blocker transitions, unblocking, missing blocked-since history, and age calculation in calendar days.
- [ ] Add Jira contract or fixture-based tests for pagination, field mapping, changelog parsing, rate limits, and API errors.
- [ ] Test interrupted/partial synchronization to confirm prior valid metrics remain intact and dashboard freshness becomes stale.
- [ ] Test idempotent replay of Jira issues and history events.
- [ ] Test deleted or inaccessible Jira issues remain represented appropriately in historical results.
- [ ] Test API validation errors, stable identifiers, `asOf` timestamps, and pagination for issue lists.
- [ ] Test filter consistency and persistence across dashboard sections and verify drill-downs reconcile to aggregate metrics.
- [ ] Test authentication, authorization, read-only behavior, Jira visibility constraints, and absence of tokens in browser/API output.
- [ ] Add accessibility checks for keyboard navigation, accessible chart alternatives, and non-color status cues.
- [ ] Verify performance targets for initial views, filter changes, and large issue lists using representative data.
- [ ] Reconcile at least six historical sprints with Jira and investigate every variance before release.
- [ ] Conduct Scrum team usability review and leadership reporting review; record and resolve release-blocking findings.
- [ ] Verify no view ranks or scores individual contributors by story points, velocity, or issue counts.

## Documentation

- [ ] Document Jira setup inputs, custom-field mappings, included issue types, blocker rule, and unresolved environment-specific configuration.
- [ ] Publish versioned metric definitions covering commitment, completion, predictability, added/removed scope, spillover, velocity, epic progress, and blocker age.
- [ ] Document how to interpret unestimated work, zero commitment, provisional active-sprint completion, stale data, unavailable history, and issue visibility changes.
- [ ] Write deployment and configuration instructions for secrets, identity provider, access roles, timezone, refresh schedule, thresholds, and retention.
- [ ] Write synchronization operations guidance covering manual refresh, retries, alert response, rate limits, and recovery after partial or failed runs.
- [ ] Document data model, API endpoints, filters, pagination, validation errors, and metric-definition versioning for maintainers.
- [ ] Provide user guidance for Scrum Masters, team members, and leadership on dashboard views, filters, drill-downs, and Jira links.
- [ ] Document accessibility behavior and explicitly state that velocity is a team planning measure, not an individual productivity target.
- [ ] Record reconciliation evidence and operating procedures for validating selected sprint totals against Jira.
