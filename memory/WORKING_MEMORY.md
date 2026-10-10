# Working memory (temporary)

Notes for picking the work up in a new session, so nobody has to guess how far it has
got. This is a scratch record, not documentation: the project's real state lives in
`docs/01_PROJECT_STATUS.md`, `research/REQUIREMENTS.md` and `CHANGELOG.md`. Delete this
directory once it stops being useful.

Last updated: 2026-10-10, at commit `9060e4f` (76 commits on the branch).

## Standing instructions from the owner

- Every commit is authored as **Mozenjii <mhbamdm@gmail.com>**, the only contributor.
  No `Co-Authored-By`, no session links, no mention of an AI assistant in commits.
- Work only through GitHub. Develop on `claude/project-continuation-8yt9bp`.
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

## Handoff to the local session

`memory/LOCAL_SESSION_PROMPT.md` is the prompt for the Claude Code session on the
owner's machine: pull first, merge any local memory into this file, then revise the
architecture and documentation to the revised plan (ADR-032, R-25). The cloud session
leaves the docs alone until that is pushed, so the two do not conflict.
