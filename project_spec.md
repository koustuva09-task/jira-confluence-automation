# Migration Delivery Metrics Dashboard

## 1. Document Status

- **Status:** Draft for review
- **Audience:** Scrum team, Scrum Master, engineering leadership, and migration stakeholders
- **Primary owner:** Scrum Master
- **Team size:** 10 people
- **Delivery model:** Two-week Scrum sprints
- **Source system:** Jira

## 2. Product Summary

Build an automated dashboard that uses Jira data to measure team delivery performance and predictability for a migration project. The first release will focus on sprint commitment versus completion, spillover, velocity, migration progress by epic, and blocked work.

The dashboard must provide:

1. A concise leadership view of delivery trends and migration progress.
2. An operational team view that explains missed commitments and highlights blocked work.
3. Consistent, auditable metric definitions based on Jira data.

The dashboard is intended to support team improvement and delivery planning. Individual metrics must not be presented as employee performance rankings.

## 3. Goals

### 3.1 Primary Goals

- Measure sprint delivery predictability over time.
- Compare committed story points with completed story points.
- Identify work that spills into later sprints.
- Track velocity without encouraging it to be used as a productivity target.
- Show migration completion by epic.
- Surface blocked issues that threaten sprint or migration outcomes.
- Reduce manual reporting effort for the Scrum Master.
- Give the Scrum team and leadership a shared view of delivery health.

### 3.2 Success Measures

- Dashboard data refreshes automatically from Jira.
- The Scrum Master no longer needs to manually compile routine sprint metrics.
- Dashboard totals can be reconciled with Jira for a selected sprint.
- Users can identify commitment, completion, spillover, and scope change for a sprint.
- Users can identify blocked work and the affected migration epic.
- Users can view delivery trends for at least the previous six completed sprints.

## 4. Non-Goals for the First Release

- Ranking or scoring individual team members.
- Measuring individual productivity using story points or issue counts.
- Replacing Jira as the system of record.
- Editing Jira issues from the dashboard.
- Forecasting with machine-learning models.
- Integrating source control, CI/CD, incident, finance, or time-tracking systems.
- Detailed defect, quality, capacity, or flow-efficiency analytics.
- Portfolio reporting across multiple unrelated projects.

## 5. Users and Access

### 5.1 Scrum Master

Needs to:

- Review current-sprint delivery health.
- Explain changes to sprint scope.
- Identify spillover and blocked issues.
- Compare recent velocity and predictability.
- Prepare sprint reviews, retrospectives, and leadership updates.

### 5.2 Scrum Team

Needs to:

- Understand current commitment and progress.
- See blocked work and aging blockers.
- Review delivery trends during sprint planning and retrospectives.
- Understand migration progress without navigating multiple Jira reports.

### 5.3 Leadership and Stakeholders

Needs to:

- See whether sprint delivery is predictable.
- Understand migration progress by epic.
- Identify risks without requiring issue-level Jira knowledge.
- Review trends rather than isolated sprint results.

### 5.4 Access Model

- Dashboard access must be read-only.
- Only authenticated users may access dashboard data.
- Access should be limited to approved team members and stakeholders.
- Jira credentials must use a dedicated read-only integration identity where supported.
- Individual issue details must respect the visibility rules of the source Jira project.

## 6. Source Data and Jira Assumptions

### 6.1 Jira Structure

- Migration work is organized as **epics containing stories and tasks**.
- Work is planned in **two-week sprints**.
- Work is estimated using **story points**.
- An issue is complete when its Jira status belongs to the **Done status category**.
- Jira is the authoritative source for issue status, sprint assignment, epic relationship, estimates, and blocker state.

### 6.2 Required Jira Fields

| Data | Jira field or source |
|---|---|
| Issue identifier | Issue key |
| Issue title | Summary |
| Work type | Issue type |
| Current status | Status and status category |
| Estimate | Story points |
| Sprint | Sprint field |
| Epic | Parent or epic-link relationship, depending on Jira configuration |
| Assignee | Assignee |
| Created date | Created timestamp |
| Resolution date | Resolution timestamp |
| Status history | Issue changelog |
| Sprint history | Issue changelog |
| Estimate history | Issue changelog, when available |
| Blocker state | Configured blocked status, flag, link, or label |

### 6.3 Jira Configuration Inputs

The implementation must make these values configurable:

- Jira site URL.
- Jira project key or keys.
- Jira board ID.
- Story-point field ID.
- Epic relationship field or hierarchy behavior.
- Included issue types.
- Done status category mapping.
- Blocked-work rule.
- Dashboard timezone.
- Refresh schedule.
- Number of historical sprints displayed.

## 7. Metric Definitions

Metrics must be calculated from issue state at the relevant point in time. Current Jira state alone is insufficient for historical commitment and scope-change calculations.

### 7.1 Sprint Commitment

**Definition:** Sum of story points assigned to the sprint at the sprint start timestamp.

```text
Committed Story Points = SUM(story points at sprint start for issues in sprint at sprint start)
```

Default behavior:

- Capture the baseline at the official Jira sprint start.
- Exclude subtasks unless subtasks are independently estimated and explicitly configured for inclusion.
- Display unestimated committed issues separately; do not treat them as zero-point completed work without disclosure.

### 7.2 Completed Story Points

**Definition:** Sum of committed and added issue story points that were in the Done status category at the sprint end timestamp.

```text
Completed Story Points = SUM(story points for sprint issues in Done at sprint end)
```

For an active sprint, use the current time as the provisional end timestamp and label the value **Completed so far**.

### 7.3 Predictability

**Definition:** Percentage of the original sprint commitment completed by sprint end.

```text
Predictability % = Completed Points from Original Commitment / Committed Story Points * 100
```

Rules:

- Work added after sprint start is not included in the numerator for commitment predictability.
- Added work is reported separately.
- If committed story points equal zero, predictability is shown as **Not applicable**, not 0% or 100%.

### 7.4 Added Scope

**Definition:** Story points for issues added to the sprint after the sprint start timestamp.

```text
Added Scope = SUM(points added after sprint start)
```

Display both:

- Points added.
- Percentage of original commitment added.

### 7.5 Removed Scope

**Definition:** Story points for issues present at sprint start but removed before sprint end.

```text
Removed Scope = SUM(points removed after sprint start)
```

Removed scope must not be counted as completed.

### 7.6 Spillover

**Definition:** Work in the original sprint commitment that was not Done at sprint end.

```text
Spillover Points = Committed Story Points - Completed Points from Original Commitment - Removed Committed Points
```

The dashboard must show:

- Spillover points.
- Spillover issue count.
- Spillover percentage of retained commitment.
- Destination sprint when the issue was subsequently moved.

### 7.7 Velocity

**Definition:** Total story points completed by sprint end for issues assigned to that sprint.

```text
Sprint Velocity = SUM(points completed in sprint)
```

Display:

- Velocity by sprint.
- Rolling average over the previous three completed sprints.
- Optional six-sprint average when at least six completed sprints are available.

Velocity must be labeled as a team planning measure, not an individual productivity measure.

### 7.8 Migration Progress by Epic

For each migration epic:

```text
Epic Completion % = Done Child Story Points / Total Child Story Points * 100
```

Display:

- Epic key and name.
- Total, completed, remaining, and unestimated work.
- Completion percentage by story points.
- Child issue count by status category.
- Number of blocked child issues.
- Target date or fix version when available.

If an epic has no estimated child issues, use issue-count completion and label the basis clearly.

### 7.9 Blocked Work

An issue is blocked when it matches the configured Jira blocker rule. Supported rules should include:

- Jira flag is active.
- Status belongs to a configured blocked-status list.
- Configured label is present.
- An unresolved blocking issue link exists.

Display:

- Issue key and summary.
- Epic.
- Assignee.
- Story points.
- Current status.
- Blocked-since timestamp.
- Blocked age in calendar days.
- Blocking reason or linked blocker when available.

If Jira does not record when the blocker began, show blocked age as unavailable rather than inferring an inaccurate date.

## 8. Dashboard Requirements

### 8.1 Global Filters

- Jira project.
- Board.
- Sprint.
- Epic.
- Status category.
- Assignee for operational filtering only.
- Date range for trend views.

Filters must persist while the user navigates between dashboard sections.

### 8.2 Executive Summary

Show:

- Current or selected sprint name and dates.
- Committed story points.
- Completed story points.
- Predictability percentage.
- Added and removed scope.
- Spillover points.
- Three-sprint rolling velocity.
- Overall migration completion.
- Active blocker count.
- Blockers older than a configurable threshold.

Use status indicators with accessible text and icons; do not rely on color alone.

### 8.3 Sprint Predictability View

Show for at least six completed sprints:

- Committed versus completed story points.
- Predictability percentage.
- Added and removed scope.
- Spillover.
- Velocity.
- Three-sprint rolling velocity.

Selecting a sprint must reveal the contributing issues and indicate whether each issue was:

- In the original commitment.
- Added after sprint start.
- Removed after sprint start.
- Completed by sprint end.
- Spilled over.

### 8.4 Migration Epic View

Show:

- Progress for every included migration epic.
- Completed and remaining story points.
- Unestimated issue count.
- Current sprint contribution.
- Blocker count.
- Sort by completion, remaining work, blocker count, or target date.

Selecting an epic must show its child issues and their current delivery state.

### 8.5 Blocked Work View

Show active blockers sorted by blocked age descending by default.

Provide:

- Epic and sprint context.
- Assignee.
- Blocked age.
- Story points at risk.
- Direct link to the Jira issue.
- Filters for sprint, epic, and assignee.

### 8.6 Data Freshness and Auditability

Every view must show:

- Last successful Jira synchronization time.
- Timezone used for calculations.
- Whether data is current or stale.
- Metric definition help text.

Users must be able to drill from an aggregate metric to the Jira issues contributing to it.

## 9. Automation and Data Processing

### 9.1 Data Refresh

Proposed default:

- Refresh active sprint data every 15 minutes.
- Refresh historical sprint data daily.
- Run an additional synchronization shortly after a sprint is completed.
- Provide a manual refresh action for authorized administrators.

Refresh frequency must remain configurable to respect Jira API limits.

### 9.2 Historical Snapshots

The system must retain or reconstruct:

- Sprint start membership.
- Story-point value at sprint start.
- Sprint additions and removals.
- Status at sprint end.
- Completion timestamp.
- Blocker transitions when available.

If changelog history cannot reliably reconstruct a metric, the system must store scheduled snapshots. It must not silently substitute current values for historical values.

### 9.3 Synchronization Failures

- Record the failed synchronization time and error.
- Preserve the most recent valid data.
- Mark the dashboard as stale.
- Notify the configured administrator after repeated failures.
- Never display a failed or partial synchronization as current data.
- Retry transient failures with bounded exponential backoff.

## 10. Proposed Technical Architecture

The technology stack remains open, but the system should use these logical components:

1. **Jira connector**
   - Authenticates to Jira with read-only credentials.
   - Retrieves boards, sprints, issues, fields, and changelogs.
   - Handles pagination and rate limits.

2. **Synchronization worker**
   - Performs incremental refreshes.
   - Normalizes Jira records.
   - Captures sprint and issue snapshots.
   - Records synchronization status.

3. **Metrics service**
   - Applies versioned metric definitions.
   - Calculates sprint, epic, and blocker aggregates.
   - Returns drill-down records for auditability.

4. **Persistent data store**
   - Stores normalized issue data, historical events, snapshots, metric results, and sync logs.
   - Supports recalculation when metric definitions change.

5. **Dashboard web application**
   - Provides responsive summary, trend, epic, and blocker views.
   - Enforces authentication and read-only access.
   - Links issue details back to Jira.

6. **Scheduler and monitoring**
   - Runs synchronization jobs.
   - Tracks job health and data freshness.
   - Sends failure notifications.

## 11. Conceptual Data Model

### 11.1 Core Entities

| Entity | Purpose |
|---|---|
| JiraProject | Configured source project |
| JiraBoard | Scrum board and board settings |
| Sprint | Sprint identity, state, start date, and end date |
| Epic | Migration epic and optional target metadata |
| Issue | Normalized Jira issue |
| IssueEstimateEvent | Story-point changes over time |
| IssueSprintEvent | Sprint additions and removals |
| IssueStatusEvent | Status changes over time |
| IssueBlockEvent | Blocked and unblocked transitions |
| SprintSnapshot | Issue state captured at sprint boundaries |
| MetricResult | Versioned calculated metric |
| SyncRun | Synchronization status, timing, and error details |

### 11.2 Data Integrity Requirements

- Jira issue keys and IDs must be retained.
- Source timestamps must be retained in UTC.
- Dashboard timestamps must be rendered in the configured timezone.
- Metric results must record the metric-definition version.
- Reprocessing the same Jira event must be idempotent.
- Deleted or inaccessible Jira issues must be marked, not silently removed from historical reports.

## 12. API Requirements

The dashboard backend should expose read-only endpoints equivalent to:

- `GET /api/dashboard/summary`
- `GET /api/sprints`
- `GET /api/sprints/{sprintId}/metrics`
- `GET /api/sprints/{sprintId}/issues`
- `GET /api/epics`
- `GET /api/epics/{epicId}`
- `GET /api/blockers`
- `GET /api/sync/status`

API responses must:

- Include an `asOf` timestamp.
- Return explicit validation errors for invalid filters.
- Support pagination for issue-level lists.
- Use stable identifiers.
- Avoid exposing Jira credentials or unnecessary personal data.

## 13. Security and Privacy

- Store Jira credentials in a secrets manager or protected environment configuration.
- Never expose Jira tokens to the browser.
- Use encrypted transport for all Jira and dashboard traffic.
- Apply least-privilege, read-only Jira access.
- Require authenticated dashboard access.
- Log administrative actions and synchronization activity.
- Avoid individual performance scores and public comparisons between team members.
- Retain only Jira user attributes required for dashboard display.
- Follow organizational data-retention and access-control policies.

## 14. Non-Functional Requirements

### 14.1 Performance

- Initial dashboard load should complete within 3 seconds for normal filtered views under expected team usage.
- Filter changes should return updated aggregates within 2 seconds when data is already synchronized.
- Issue lists must use pagination or virtualization.

### 14.2 Reliability

- Scheduled synchronization must be idempotent.
- A failed refresh must not corrupt previously valid metrics.
- Historical sprint results must remain stable unless Jira history changes or metrics are intentionally recalculated.

### 14.3 Accessibility

- Target WCAG 2.1 AA.
- All charts must have textual summaries or accessible tables.
- Keyboard navigation must be supported.
- Status must not be represented by color alone.

### 14.4 Maintainability

- Jira field mappings and blocker rules must be configurable.
- Metric formulas must have automated unit tests.
- Jira integration must have contract or fixture-based tests.
- Metric-definition changes must be versioned and documented.

### 14.5 Observability

- Log synchronization start, completion, duration, record counts, and failures.
- Track Jira API rate-limit events.
- Track the age of the latest successful synchronization.
- Alert when data freshness exceeds a configurable threshold.

## 15. Acceptance Criteria for the First Release

1. An authenticated user can select any of the most recent six completed sprints.
2. The dashboard shows committed, completed, added, removed, and spillover story points for the selected sprint.
3. Commitment is based on sprint-start state rather than current Jira state.
4. Completion is based on the Done status category at sprint end.
5. Predictability excludes work added after sprint start from original-commitment completion.
6. Each aggregate sprint metric can be reconciled through an issue-level drill-down.
7. Velocity and a three-sprint rolling average are displayed.
8. Migration epics show completion by story points and clearly disclose unestimated work.
9. Active blockers show issue, epic, assignee, and blocked age when that age is available.
10. Dashboard views link directly to relevant Jira issues.
11. The latest synchronization timestamp and stale-data state are visible.
12. Jira API or synchronization failures are surfaced and do not appear as successful refreshes.
13. No view ranks individuals by story points, velocity, or completed issue count.
14. Automated tests cover metric calculations, including zero commitment, scope change, estimate change, unestimated issues, and spillover.

## 16. Required Test Scenarios

- Issue committed and completed within the sprint.
- Committed issue not completed and carried to the next sprint.
- Issue added after sprint start and completed.
- Issue added after sprint start and not completed.
- Issue removed after sprint start.
- Estimate changed during the sprint.
- Issue completed after the sprint end timestamp.
- Completed issue reopened before sprint end.
- Issue with no estimate.
- Sprint with zero committed points.
- Issue moved between migration epics.
- Blocked issue subsequently unblocked.
- Jira synchronization interrupted after partial retrieval.
- Jira issue deleted or no longer visible to the integration identity.

## 17. Delivery Phases

### Phase 1: Discovery and Jira Mapping

- Confirm Jira project and board.
- Identify custom field IDs.
- Define the authoritative blocked-work rule.
- Validate changelog availability and retention.
- Confirm timezone and sprint-boundary behavior.
- Reconcile sample metrics manually for two completed sprints.

### Phase 2: Data Foundation

- Implement Jira authentication and synchronization.
- Store normalized issues, history, and sprint snapshots.
- Add synchronization health reporting.
- Implement and test metric calculations.

### Phase 3: Dashboard MVP

- Build executive summary.
- Build sprint predictability trends and drill-down.
- Build migration epic progress view.
- Build blocked-work view.
- Add filters, freshness indicators, and Jira links.

### Phase 4: Validation and Rollout

- Reconcile at least six historical sprints with Jira.
- Conduct Scrum team usability review.
- Conduct leadership reporting review.
- Document metric definitions and operating procedures.
- Deploy with monitoring and access controls.

## 18. Open Decisions

These items were not resolved during the initial interview and must be confirmed before implementation:

1. Exact Jira deployment type: Cloud or Data Center.
2. Jira site URL, project key, and board ID.
3. Authentication method and integration identity.
4. Exact rule used to identify blocked work.
5. Whether sprint commitment uses the official Jira sprint start or a manually approved baseline.
6. Treatment of estimate changes after sprint start for velocity and scope reporting.
7. Included issue types and whether estimated subtasks are included.
8. Dashboard timezone.
9. Hosting environment and approved technology stack.
10. Identity provider and role-based access requirements.
11. Required refresh frequency and Jira API-rate constraints.
12. Historical data-retention period.
13. Leadership thresholds for status indicators.
14. Whether epic target dates or releases are consistently maintained in Jira.

## 19. Working Assumptions Pending Confirmation

- Sprint commitment is baselined at the official Jira sprint start.
- Scope added or removed after sprint start is reported separately.
- The dashboard initially covers one Jira Scrum board and one migration project.
- The first release displays the current sprint plus at least six completed sprints.
- Active data refreshes every 15 minutes.
- The organization will provide a read-only Jira integration identity.
- Jira changelogs are available; boundary snapshots will supplement them where required.
- Metric thresholds are informational and configurable rather than hard-coded performance targets.

