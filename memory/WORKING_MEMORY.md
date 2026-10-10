# Working memory (temporary)

Notes for picking the work up in a new session, so nobody has to guess how far it has
got. This is a scratch record, not documentation: the project's real state lives in
`docs/01_PROJECT_STATUS.md`, `research/REQUIREMENTS.md` and `CHANGELOG.md`. Delete this
directory once it stops being useful.

Last updated: 2026-10-11. Pulled baseline: `77184e6`; reconciled integration: `41b7e7c`.

## Standing instructions from the owner

- Every commit is authored as **Mozenjii <mhbamdm@gmail.com>**, the only contributor.
  No co-author trailers, session links or tooling attribution in published text.
- The owner subsequently authorised reconciling both the continuation branch and
  `mozenji/production-readiness-foundation` into `main`, then continuing on `main`
  with ordinary pushes. This supersedes the branch-only/no-main-merge restriction.
  Never reset, discard, delete a branch or force-push state.
- No pull request, tag or release is authorised.
- Make the code back every claim; do not drop a claim because the code cannot do it yet.
  Commercialising can wait. The goal is a first version that works and that people like.
- Target market: the US and Europe.

## Where things stand

- Python compiler that turns regulations into executable, source-linked rules
  (Apache-2.0). Golden corpus: 15 SNAP rules from 7 CFR 271.2, 273.9 and 273.10.
- Pulled baseline: 554 tests. Reconciled main: **558 passed**, **92.14% coverage**
  (`.[dev,review,openfisca]`); fresh base install: **403 passed, 16 skipped**.
  Ruff, mypy (55 source files) and dependency consistency checks pass.
- CI (`.github/workflows/tests.yml`): Python 3.11–3.13 matrix with every extra, a
  base-install job, and a package job that builds the wheel and Docker image. Green on
  `9060e4f` historically; that is not evidence for reconciled main. Check the latest run.

## Done in this stretch, in order

1. Made CI green and honest; decoupled the core from the web stack.
2. Built and executed the OpenFisca export (equivalence harness under openfisca-core).
3. Added a Docker image, `/healthz`, PostgreSQL support and tag-driven releases.
4. Added the calculation API (`ruleweaver serve`) with API keys, metering and a
   replayable `record` on every answer.
5. Ran the simulated market review (20 personas, three rounds) and stored it in
   `research/`. The reviews are **simulated**; treat them as hypotheses.
6. Started working through `research/REQUIREMENTS.md`. Implemented portions: R-01, R-02, R-03, R-04,
   R-08, R-09, R-12, R-14, R-15, R-28. R-01 is now **Partial**: seeded faults and
   aggregate metrics work, but the combined requirement also needs pseudonymisation
   (R-11). R-25 documentation is complete; counsel review remains outstanding.
   - R-04 (latest): the SNAP example carries the official FY2026 tables for the 48
     states and DC, each value citing its row in the FNS memo of 13 Aug 2025 or the HHS
     2025 poverty guidelines. Both documents are in `examples/snap/sources/` with
     checksums; `tests/test_snap_tables.py` checks every figure against them.

## Next, in priority order

- **R-37:** retrieve and verify FY2027 tables in force from 1 Oct 2026; check the
  official publication details rather than assuming a memo date.
  Until then the package answers unknown from 1 Oct 2026, which is already past.
- **R-05:** keyed audit chain with the key held outside the database, plus checkpoint
  export and verify.
- **R-06:** one identity per reviewer (OIDC or per-user keys); the author of a rule
  cannot approve it.
- **R-25:** documentation complete; commercial intended-use counsel review pending.
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

The relevant local locations are `D:/Code/RuleWeaver/CLAUDE.md`,
`D:/Code/RuleWeaver/.claude/` and
`C:/Users/MOHIB/.claude/projects/D--Code-NICXON/memory/`.
The project-memory directory contains six files:
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

## Completed revised plan and branch reconciliation

The original handoff in `LOCAL_SESSION_PROMPT.md` is historical. The owner explicitly
superseded its branch-only rule by authorising both branches into main. The continuation
was a descendant of main, so main fast-forwarded; a normal two-parent merge preserved
all eight unique local commits. Both original branch references remain intact. No stash,
reset, rebase, forced push, branch deletion, tag or release was used.

Documentation-only commits first updated every numbered document (00–15), README,
requirements and changelog. ADR-032 fixes the BUILD/FREEZE/CUT scope; ADR-021/022 are
intended-purpose positions, not legal conclusions. Normative IR requirements remain;
five spec/runtime contradictions are explicitly tracked as R-44. R-38–R-46 preserve
missing pack, gating, authoring, testing, benchmark, provenance and review claims.
Older locally deleted layout documentation is retained and rewritten to the actual tree.

The authorised branch reconciliation then combined local cookie CSRF, validation guards
and coverage enforcement with newer parameter review, editing, planted faults, service
and OpenFisca changes. The obsolete edit prohibition was replaced by semantic validation
of the corrected item in its package before recording. Parameter errors and global
validation failures block approval. Four regression cases bring 554 to 558 tests.
No new feature module, top-level application directory or dependency on the web stack
was added to the core. pytest-cov is the only merged development dependency.

Final local checks after the compatible-tool update: 558 passed in 23.58 seconds,
92.14% coverage; fresh provider/web-free
base environment 403 passed, 16 skipped in 6.92 seconds. Ruff and mypy pass on 55 source
files; pip check reports no broken dependencies. Golden corpus validation checks pinned
sources and passes with the existing RW3009 override warning. Baseline scenario allotment
is 609 for its historical period. These are implementation checks, not current-law or
independent policy certification. No container or remote deployment was launched here.

Independent read-only review checked the integration and documentation. It found three
proof/status errors (testgen path, IR schema evidence and R-01 pseudonymisation); these
were corrected. Degraded local documentation-skill helper availability remains a tooling
setup issue and was not silently repaired or published.

Owner decisions still needed: whether to start England Universal Credit/April uprating;
who supplies independent known-answer cases and qualified jurisdiction review; commercial
counsel, employer/IP permission, entity/insurance and backup maintainer arrangements
(R-32–R-35). Do not infer completion from the simulated reviews.

Continue on main. Next implementation follows R-37 → R-05 → R-06 → R-36 → R-39,
then report R-16, independent parity R-17 and content pack R-38 with the hardening work.
The complete not-built/partial inventory is `docs/01_PROJECT_STATUS.md` and the single
status tracker is `research/REQUIREMENTS.md`.

## Dependency-tool verification

The initial local dependency scan reported ten records for five unique advisories:
one in pytest 8.4.2 and four in setuptools 65.5.0. These were local development/bootstrap
tools; the scan found no advisory in the installed project runtime dependencies.
Installed versions were preserved in an ignored pre-update record. Setuptools was upgraded to a fixed release. A pytest 9 trial exposed OpenFisca 45
requiring pytest <9 and broke its nested runner, so pytest 8.4.2 was restored and the
suite rerun. The remaining Unix temporary-root advisory is documented rather than
reported as fixed. CI now creates a random private temporary root inherited by nested
runners; Windows runs also use fresh repository-local paths. This mitigates the
shared predictable-path exposure, not the installed version finding. Hatch remains
the build backend; no setuptools dependency was added. Dependency scanning, pinning
and signed supply-chain evidence remain a broader R-13 deliverable.

Upstream temporary-directory issue: https://github.com/pytest-dev/pytest/issues/13669.
The primary fix is pytest 9.0.3; removing the compatibility constraint requires a
separate OpenFisca maintenance decision under the frozen adapter scope.

Final dependency scan: two duplicate records for the one retained pytest advisory;
setuptools findings are resolved. No installed production runtime advisory reported.
The shared private-root CI step parses as YAML and Bash; remote CI must confirm the
Linux matrix and container job after push.
