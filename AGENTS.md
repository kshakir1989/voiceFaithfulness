# Agent rules (voiceFaithfulness)

GitHub: `kshakir1989/voiceFaithfulness`. This repository is **voiceFaithfulness only**. Do not edit other FreshUSA products or other GitHub repos in the same session.

- **Action-Report (NON-NEGOTIABLE):** Before each non-trivial step, pause with bullets of concrete changes plus an Explanation paragraph (not What/Why/How). Wait for **go**, a question, or an explicit skip.
- Ask before commands, edits, commits, or deploys unless the owner already said **go** on that chunk.
- Spec first for user-facing behavior. Do not commit `plan.md` unless the owner asks.
- Keep `spec-architecture.png` current when Spec Kit artifacts change.
- **Chunk = commit + push (NON-NEGOTIABLE):** after each reviewable slice, commit on this repo’s implementation branch and immediately `git push` that same branch. Standing owner order: no second commit/push ask after **go** on that chunk.
- **Working tree always clean** before the next chunk. Never commit `backend/.env`. `plan.md` stays untracked.
- Run backend tests from `backend/` and frontend/e2e from `frontend/` (or repo scripts).

## Git

- Default branch is **`main`**. Do not push feature work to `main`.
- Implementation branches (e.g. `v1.1`); land via PR into `main` after ship (or when agreed).
- **UI / UX:** Figma design frames first. PRs that touch UI cite the Figma **node URL**.
