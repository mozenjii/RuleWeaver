# Prompt for the local session

Paste everything below the line into the Claude Code session on the local machine.

---

You are continuing work on RuleWeaver (github.com/mozenjii/RuleWeaver). A cloud session
has been working on the branch `claude/project-continuation-8yt9bp` and has pushed
everything. Your local copy is probably behind, and there may be a local memory folder
that the cloud session has never seen. Work in this order and do not skip steps.

## Rules that apply to everything you do

- Every commit is authored as **Mozenjii <mhbamdm@gmail.com>**. Set it in this repo
  (`git config user.name "Mozenjii"`, `git config user.email "mhbamdm@gmail.com"`).
  Add no `Co-Authored-By` line, no session link, and no mention of Claude or any AI
  assistant in commit messages, code or docs.
- Work on `claude/project-continuation-8yt9bp` only. Do **not** merge to `main`, open a
  pull request, tag or release.
- `CLAUDE.md`, `AGENTS.md` and `.claude/` are gitignored on purpose. Never commit them.
- The project claims only what the code does, and the code is built up to what the
  project should be able to claim. Never drop a claim just because the code cannot back
  it yet: mark it as not built yet and make sure a requirement in
  `research/REQUIREMENTS.md` covers it.
- Do not discard, overwrite or force-push anything. If something would be lost, stop
  and ask me.

## Step 1 — Look before touching anything

1. Run `git status`, `git stash list`, `git branch -vv` and `git log --oneline -5`.
2. If there are uncommitted changes, do **not** pull over them. Commit them on a new
   local branch named `local-backup-<today's date>` (authored as above), or stash them,
   and tell me what they were.
3. Find every local memory or notes folder: a `memory/` folder in the repo (tracked or
   untracked), `CLAUDE.md`, anything under `.claude/`, and Claude Code's own project
   memory (under `~/.claude/projects/`). List what you found.
4. If an **untracked** `memory/` folder exists in the repo, the pull will collide with
   the one the cloud session pushed. Move it aside first, for example to
   `../ruleweaver-local-memory-backup/`, and keep it until step 3 is done.

## Step 2 — Pull first

```bash
git fetch origin
git checkout claude/project-continuation-8yt9bp
git pull --ff-only origin claude/project-continuation-8yt9bp
```

If `--ff-only` fails, the local branch has commits the remote lacks. Do not rebase or
reset. Show me `git log --oneline origin/claude/project-continuation-8yt9bp..HEAD` and
wait for me to decide. After pulling, `git log -1` should show commit `fce68ff` or later.

## Step 3 — Merge the memories

1. Read `memory/WORKING_MEMORY.md` (from the cloud session) and every local memory you
   found in step 1.
2. Merge them into `memory/WORKING_MEMORY.md`, keeping everything that is still true.
   Where they disagree, the repository and the newest commit win; list each conflict
   under a "Reconciled" heading so I can check it.
3. Put no secrets, tokens, passwords or personal data other than the author name and
   email in the file.
4. Point your own local memory (`CLAUDE.md` or Claude Code's memory) at
   `memory/WORKING_MEMORY.md` as the shared record, so the local and cloud sessions
   read the same thing.
5. Commit ("Merge the local and cloud working memory") and push.

## Step 4 — Get your bearings, then check the environment

Read these first: `memory/WORKING_MEMORY.md`, `research/README.md`,
`research/REQUIREMENTS.md`, `research/simulated-reviews/round-3/r3-judgment.md`,
`research/simulated-reviews/round-3/r3-product-scope.md`, `docs/01_PROJECT_STATUS.md`,
`CHANGELOG.md`, `README.md`.

Then install and confirm a green baseline:

```bash
python -m venv .venv
.venv/bin/pip install -e ".[dev,review,openfisca]"
.venv/bin/ruff check src tests
.venv/bin/mypy src
.venv/bin/pytest -q          # expect 554 passed
```

If anything fails, stop and tell me; do not fix code as part of this task.

## Step 5 — Revise the product architecture and the documentation to the revised plan

### The revised plan

The simulated reviews in `research/` are hypotheses, not market evidence. The owner's
decision after reading them: **make the first version work and be good, rather than
racing to sell it.** So the product is:

- **What it is:** a compiler and verifier for benefit and tax rules. It turns the law and
  its published figures into executable rules. Each rule is linked to its source and
  can only run after a person has approved it. The deliverable people value is
  **change impact plus independent verification**: what a change in the law or an annual
  uprating does to results, linked to the clause, with a parity result against the
  user's own known-answer cases.
- **What it is not:** a hosted SaaS, a general rules engine, or an AI system that
  decides anything. The runtime is deterministic and has no model dependency. Model-
  assisted authoring is optional and kept separate.
- **How it is deployed:** self-hosted. Whoever builds or supports it never has access to
  anyone's personal data.
- **Content:** US SNAP (federal rules plus the official FY2026 tables for the 48 states
  and DC) is the reference corpus and demo. Benefits in England (Universal Credit plus
  the April uprating) is the leading candidate for the first content beyond SNAP. It is
  not started, and the decision to start it is the owner's.
- **Components and their stance** (use `r3-product-scope.md` FIX / BUILD / FREEZE / CUT,
  except that the owner rejected "delete the claim" in favour of "build the code"):
  - BUILD: source layer (eCFR XML, memos and notices; HTML/PDF R-18,
    legislation.gov.uk R-19); IR and evaluator; verification; the approval gate covering
    rules **and** parameter tables; the review app; change-impact report (R-16);
    parity command (R-17); a versioned, hashed release artefact for a content pack.
  - Hardening that remains: keyed audit chain (R-05), one identity per reviewer with
    author/approver separation (R-06), reviewer qualification (R-07), pseudonymous
    reviewers (R-11), unknown with reason codes (R-10), SBOM and signing (R-13),
    accessibility (R-29).
  - FREEZE (keep working, no new investment): the hosted calculation API (`service/`)
    as a self-hosted or synthetic-data option; OpenFisca export (maintain only; AGPL
    note); LLM extraction (optional).
  - CUT from the roadmap: Catala, LegalRuleML, PROV, Akoma Ntoso, OCR, plugin SDK, and
    hosted multi-tenant SaaS before there is a user; SOC 2, ISO 27001 and FedRAMP before
    a hosted offering.

### What to change

1. `docs/03_ARCHITECTURE.md`: redraw the architecture around the components above.
   Label every component **Built**, **Partial** or **Planned**, giving the module path or
   test that proves "Built" and the `R-xx` id for anything not done. Add the parameter
   gate, the unstructured source documents (`src/ruleweaver/ingest/plain.py`), the
   calculation service, fault seeding and the content-pack boundary. Remove what the
   plan cuts.
2. `docs/00_PROJECT_BRIEF.md` and `docs/02_PRODUCT_SPEC.md`: product statement, users,
   deployment model and functional requirements per the plan. Cross-reference
   requirement ids.
3. `docs/09_IMPLEMENTATION_ROADMAP.md` and `docs/10_BACKLOG.md`: replace them with the
   sequence from `research/REQUIREMENTS.md`, with remaining P0 items first: R-37 FY2027
   tables, R-05, R-06, R-25, R-36. Then P1. Do not duplicate statuses; point to
   `REQUIREMENTS.md` as the single source of truth for status.
4. `docs/11_DECISIONS.md`: add **ADR-032, the revised plan** (context: the simulated
   reviews; decision: as above; consequences; what would change it). Then do R-25:
   rewrite ADR-021 and ADR-022 so they state the project's intended purpose and
   positions, not legal conclusions. No "compliant with Art. 14", no "not an AI system"
   as a fact, no unverified dates. Add an intended-purpose and non-reliance statement.
   Mark the text "not legal advice; needs counsel review before any commercial use".
5. `docs/13_REPO_STRUCTURE.md`: match the real tree (`research/`, `memory/`,
   `src/ruleweaver/service/`, `src/ruleweaver/review/seeding.py`,
   `src/ruleweaver/ingest/plain.py`, `examples/snap/sources/` with its new documents).
6. `README.md`, `docs/01_PROJECT_STATUS.md`, `CHANGELOG.md`: align with all of the
   above. Fix any claim the code does not back, by marking it not built and pointing to
   its requirement. Keep the test counts true.
7. `research/REQUIREMENTS.md`: set R-25 to ✅ when step 4 is done. Add any new
   requirement you discover instead of building it.

### How to work

- This is a documentation task. Change no code except docstrings that make a claim the
  code does not back. If a doc claim needs code, add or point to a requirement instead.
- For every sentence that says something is built, find the file or test that proves it.
  If you cannot, it is not built.
- Make small commits, one per document or theme. Run `ruff`, `mypy` and `pytest` before
  each push, and check that every file path a doc mentions exists.
- When finished, update `memory/WORKING_MEMORY.md` (what changed, what is next), push,
  and give me a short summary covering:
  - what you found locally;
  - how the memories were merged;
  - which documents changed;
  - every claim you had to mark "not built";
  - any question that needs my decision.
