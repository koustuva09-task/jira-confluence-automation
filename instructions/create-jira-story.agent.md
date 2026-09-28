# Creating a Jira Story from Business Requirements

Use this workflow when turning one or more business requirements into a Jira story draft.

## Input format

Accept business requirements in free-form text or in this structure:

- **Business goal:** The outcome the business or user needs.
- **User or stakeholder:** Who benefits from the change.
- **Problem or opportunity:** What need or pain point the change addresses.
- **Context and scope:** Relevant workflows, systems, and what is included or excluded.
- **Acceptance notes:** Known examples, rules, or conditions of success.
- **Constraints and dependencies:** Compliance, security, technical, timing, or cross-team needs.
- **Jira conventions:** Project-specific fields, templates, labels, components, or terminology, if known.

Do not require every field. Use only information supported by the supplied requirements and context.

## Processing steps

- Identify the user or stakeholder, desired outcome, business value, and boundaries of the requested change.
- Consolidate duplicate requirements and preserve distinct requirements without broadening their scope.
- Check whether the work describes one independently deliverable user outcome. If it contains multiple unrelated outcomes, recommend splitting it into separate stories.
- Draft a concise story summary and a user-story statement in the form “As a [user], I want [capability], so that [benefit]” when the user is known. If the user is not known, use neutral wording and mark the user as an open question rather than inventing one.
- Convert each supported business rule into a specific, observable acceptance criterion. Prefer Given/When/Then where it clarifies behavior; include relevant success, validation, and error cases when supported.
- Separate requirements from implementation suggestions. Do not prescribe architecture or technical design unless the input requires it.
- Identify missing information that materially affects scope, behavior, acceptance, or risk. Ask concise clarifying questions before drafting when the ambiguity prevents a useful story; otherwise draft and list the unresolved items under Open Questions.
- Include assumptions only when necessary to produce a draft, label them explicitly, and never present them as confirmed requirements.
- Review the draft for clarity, testability, scope boundaries, and consistency with the supplied Jira conventions.

## Output format

Produce a Jira-ready Markdown draft with these fields in order:

1. **Summary** — concise, action-oriented title.
2. **Story** — user-story statement or a neutral outcome statement if the user is unknown.
3. **Description** — business context, desired outcome, and scope.
4. **Acceptance Criteria** — numbered, independently verifiable criteria; use Given/When/Then where appropriate.
5. **Out of Scope** — include only boundaries supported by the input; otherwise omit.
6. **Dependencies** — list known dependencies; write “None identified” only when the input supports that conclusion, otherwise omit or flag as unknown.
7. **Assumptions and Open Questions** — clearly distinguish assumptions from unanswered questions; omit empty subsections.
8. **Jira Metadata** — include only supplied or explicitly requested fields, such as project, issue type, priority, labels, component, or epic.

Do not add story points, assignee, priority, labels, component, epic, or other Jira metadata unless supplied or explicitly requested. When the user asks for a different template, follow that template while preserving the same information and constraints.

## Constraints

- Do not invent business rules, actors, values, systems, permissions, deadlines, dependencies, or acceptance outcomes.
- Preserve the intent and terminology of the business requirements; flag contradictions instead of silently resolving them.
- Keep acceptance criteria measurable, unambiguous, and focused on externally observable behavior.
- Keep the story small enough to represent one coherent outcome; recommend splitting oversized or unrelated work.
- Do not turn the story into a task breakdown or implementation plan unless requested.
- Do not include sensitive personal data, credentials, or secrets in the story.
- Do not create, edit, or submit a Jira issue. Produce a draft for review unless the user explicitly asks for an available Jira action.
- Use concise, professional language and avoid unsupported claims.
