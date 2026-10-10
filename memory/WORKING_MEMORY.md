# Working memory (temporary)

Notes for picking the work up in a new session, so nobody has to guess how far it has
got. This is a scratch record, not documentation: the project's real state lives in
`docs/01_PROJECT_STATUS.md`, `research/REQUIREMENTS.md` and `CHANGELOG.md`. Delete this
directory once it stops being useful.

Last updated: 2026-10-10. Pulled baseline: `77184e6`; last code change: `9060e4f`.

## Standing instructions from the owner

- Every commit is authored as **Mozenjii <mhbamdm@gmail.com>**, the only contributor.
  No co-author trailers, session links or tooling attribution in published text.
- Develop only on `claude/project-continuation-8yt9bp`; local work and ordinary pushes
  to that branch are authorised. Never reset, discard or force-push state.
- **Do not** merge, open a pull request or cut a release yet ("Not yet").
- Make the code back every claim; do not drop a claim because the code cannot do it yet.
  Commercialising can wait. The goal is a first version that works and that people like.
- Target market: the US and Europe.

## Where things stand

- Python compiler that turns regulations into executable, source-linked rules
  (Apache-2.0). Golden corpus: 15 SNAP rules from 7 CFR 271.2, 273.9 and 273.10.
- Tests: 554 pass with all extras (`.[dev,review,openfisca]`). On the base install, 403
  pass and 16 skip. ruff and mypy are clean.
- CI (`.github/workflows/tests.yml`): Python 3.11–3.13 matrix with every extra, a
  base-install job, and a package job that builds the wheel and Docker image. Green on
  `9060e4f`, the last code change. Check the latest run before starting.

## Done in this stretch, in order

1. Made CI green and honest; decoupled the core from the web stack.
2. Built and executed the OpenFisca export (equivalence harness under openfisca-core).
3. Added a Docker image, `/healthz`, PostgreSQL support and tag-driven releases.
4. Added the calculation API (`ruleweaver serve`) with API keys, metering and a
   replayable `record` on every answer.
5. Ran the simulated market review (20 personas, three rounds) and stored it in
   `research/`. The reviews are **simulated**; treat them as hypotheses.
6. Started working through `research/REQUIREMENTS.md`. Done: R-01, R-02, R-03, R-04,
   R-08, R-09, R-12, R-14, R-15, R-28.
   - R-04 (latest): the SNAP example carries the official FY2026 tables for the 48
     states and DC, each value citing its row in the FNS memo of 13 Aug 2025 or the HHS
     2025 poverty guidelines. Both documents are in `examples/snap/sources/` with
     checksums; `tests/test_snap_tables.py` checks every figure against them.

## Next, in priority order

- **R-37:** add the FY2027 tables (FNS memo of Aug 2026, in force from 1 Oct 2026).
  Until then the package answers unknown from 1 Oct 2026, which is already past.
- **R-05:** keyed audit chain with the key held outside the database, plus checkpoint
  export and verify.
- **R-06:** one identity per reviewer (OIDC or per-user keys); the author of a rule
  cannot approve it.
- **R-25:** intended-purpose and non-reliance statement; rewrite ADR-021/022 as
  positions, not conclusions.
- **R-36:** households of nine or more need a rule for FNS's rounded per-member
  increment ($459 net, $596 gross), not more table rows.
- Then the P1 items: R-16 change-impact report, R-17 parity command, R-10 reasons for
  unknown, R-11 pseudonymous reviewers, R-13 SBOM and signing, R-18/R-19 ingestion,
  R-29 accessibility.

## Things that are easy to get wrong

- Never type a published figure from memory. Fetch the official document, store it in
  `examples/snap/sources/`, record its sha256 in the manifest, and cite the row.
- usda.gov, fns.usda.gov, aspe.hhs.gov and federalregister.gov refuse automated
  requests. GovInfo works for Federal Register text. The FY2026 FNS memo came from the
  Alaska Department of Health's copy; check it against FNS's own copy by hand.
- `tests/conftest.py` holds **constructed** test tables (a standard deduction of 180,
  below its minimum on purpose, and a `lowmax` jurisdiction). They are not the real
  figures; `with_tables()` swaps them in for tests that need them.
- An effective date's `effective_to` is exclusive.
- The OpenFisca export imports OpenFisca-Core, which is AGPL-3.0-or-later.
- Before each push: `ruff check src tests`, `mypy src`, and `pytest` on both an
  all-extras and a base install. Update `research/REQUIREMENTS.md` and `CHANGELOG.md`.

## Local inventory and merge

The initial checkout was clean, with no stash and no repository memory directory.
The former local branch was `mozenji/production-readiness-foundation` at `15a9d06`;
it remains intact. No backup branch or directory move was needed. The requested
branch fast-forwarded to `77184e6`. The configured remote still uses the old repository
name, NICXON; it was not changed.

The local project-memory directory named `D--Code-NICXON` contains six files:
`MEMORY.md`, `ruleweaver-state.md`, `commit-incrementally.md`,
`no-tooling-config-in-repo.md`, `codex-app-not-cli.md` and
`gstack-decision-slug-windows.md`. All were read. The repository's local instruction
file imports the owner contract; local launch settings start the reviewer on port
8123; settings and the enforcement hook contain tooling configuration, not additional
product decisions. Local permission settings were inspected without publishing their
contents. No secrets or runtime database records were copied.

Other projects' memory directories were inventoried but not imported: their project
facts do not belong here. The old local notes remain untouched; the local instruction
file now points here as the shared handoff record.

Retained guidance: commit one coherent document or theme at a time, stage explicit
paths, keep local tooling out of version control, check source byte hashes on Windows,
use contiguous quotations, and preserve repeated CFR marker levels. Source line endings
are pinned by `.gitattributes`; ingestion and provenance tests protect the latter two.
Desktop tooling may not have its command-line executable installed; detect actual
availability before using an external review process. The old Windows decision-log
slug warning is historical and must be rechecked before applying its workaround.

## Reconciled

- The old index says the proposal layer is absent and its state note reports 317 tests.
  The current modules implement segmentation and extraction; the pulled baseline
  expects 554 tests with the installed extras. Repository and fresh verification win.
- The local note says OpenFisca is absent. The code generator, YAML exporter and
  differential harness are now present, per ADR-031 and the adapter tests. Agreement
  with the native evaluator is consistency evidence, not independent policy truth.
- The local note describes an insecure default reviewer header. The current default
  refuses to start without signed sessions or a configured trusted proxy. Individually
  bound identity and author/approver separation remain unbuilt (R-06).
- The local note says lint and type checking are absent. Both are configured and pass;
  mypy checks 55 source files. Invoke through `.venv/Scripts/python.exe -m mypy` locally.
- The old SNAP monetisation rationale and complete-pipeline wording do not establish
  product readiness. The owner's revised plan prioritises a good self-hosted compiler,
  change impact and independent verification, rather than an outreach deadline.
- Old authentication/CLI-availability notes are not current verification or a reason
  to bypass the owner's no-PR/no-release boundary.
- After switching, pre-existing `.codex/` and `.coverage` became visible as untracked
  because this branch has different ignore rules. Preserve them locally, never stage them.

## Local verification and next work

Installation: editable `.[dev,review,openfisca]` in the existing Python 3.11 environment.
Ruff passes; mypy passes on 55 source files. The first test run failed because the
nested OpenFisca runner collected across drives and reached a protected Windows junction.
All three runner tests pass with a fresh repository-local `--basetemp` under
`.pytest_cache/`. No project code or dependency source was changed. Use this invocation
for the full suite and record its result before pushing:

```powershell
$taskTemp = Join-Path (Get-Location) ('.pytest_cache/run-' + [guid]::NewGuid().ToString('N'))
.venv/Scripts/python.exe -m pytest --basetemp $taskTemp -o addopts='' -q
```

Next: documentation-only revised plan, ADR-032, intended-purpose revision R-25, and
Built / Partial / Planned evidence. The handoff instructions are in
`memory/LOCAL_SESSION_PROMPT.md`. Do not fix code as part of this pass.
