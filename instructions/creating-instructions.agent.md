- Keep reusable instruction files in `./instructions/` and name them `[verb]-[topic].agent.md` using hyphen-separated words.
- Keep each instruction focused on one workflow and write short, actionable bullet points in English.
- Add each instruction to `./instructions/main.agent.md` with a concise description and trigger keywords.
- When an instruction is added or changed, update relevant IDE entry points or prompt wrappers so agents can discover it.
- For VS Code with GitHub Copilot:
  + Reference `./instructions/main.agent.md` from `.github/copilot-instructions.md`.
  + Ask Copilot to load the catalog completely and reload it for each prompt.
  + Add reusable prompt wrappers under `.github/prompts/` when they improve discoverability.
  + Enable instruction files in `.vscode/settings.json`.
- Keep platform-independent workflow guidance in `instructions/`; keep IDE-specific loading instructions in the relevant entry point or wrapper.
- When updating instructions, read and preserve useful existing requirements, and make targeted changes.
- Verify that catalog links and entry-point references resolve after changes.
