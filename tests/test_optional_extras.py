"""The core must work on an install that never asked for the reviewer application.

`ruleweaver.approval` is the execution gate and `ruleweaver.adapters.openfisca` refuses
unapproved rules; both read the review log. For three weeks both also imported FastAPI by
way of `review/__init__`, so a base install could not run `evaluate --require-approval`,
`export` or `token` — and CI, which installs the base package, failed at collection.

These tests run in a subprocess with the review extra's packages made unimportable, so
they hold even on a machine where those packages are installed.
"""

from __future__ import annotations

import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples" / "snap" / "rules.json"
BASELINE = ROOT / "examples" / "snap" / "scenarios" / "baseline.json"

# Everything the `review` extra brings in. Blocked by top-level name, so a submodule
# import such as `fastapi.testclient` is refused too.
REVIEW_EXTRA = ("fastapi", "starlette", "sqlalchemy", "jinja2", "uvicorn", "multipart")

BLOCKER = textwrap.dedent(f"""
    import importlib.abc
    import sys

    class Blocked(importlib.abc.MetaPathFinder):
        def find_spec(self, name, path=None, target=None):
            if name.split(".")[0] in {REVIEW_EXTRA!r}:
                raise ModuleNotFoundError(f"blocked for this test: {{name}}", name=name)
            return None

    sys.meta_path.insert(0, Blocked())
""")


def run_without_review_extra(body: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-c", BLOCKER + textwrap.dedent(body)],
        capture_output=True, text=True, cwd=ROOT, check=False,
    )


def test_the_blocker_actually_blocks():
    """A guard that blocks nothing would make every test below pass vacuously."""
    result = run_without_review_extra("import fastapi")
    assert result.returncode != 0
    assert "blocked for this test: fastapi" in result.stderr


@pytest.mark.parametrize("module", [
    "ruleweaver.approval",
    "ruleweaver.review",
    "ruleweaver.review.identity",
    "ruleweaver.adapters.openfisca",
    "ruleweaver.cli",
])
def test_core_module_imports_without_the_review_extra(module):
    result = run_without_review_extra(f"import {module}")
    assert result.returncode == 0, result.stderr


def test_the_execution_gate_fails_closed_without_the_review_extra():
    """The review log lives in a database the base install cannot open.

    That is a legitimate deployment, but not a licence to skip the gate: the command must
    refuse, say why, and execute nothing. Before the import was deferred it never got that
    far — it died on a traceback while importing the CLI.
    """
    result = run_without_review_extra(f"""
        import sys
        from ruleweaver.cli import main
        sys.exit(main(["evaluate", {str(FIXTURE)!r}, {str(BASELINE)!r},
                       "--require-approval"]))
    """)
    assert result.returncode == 1
    assert "Traceback" not in result.stderr, result.stderr
    assert "cannot read the review log" in result.stderr
    assert 'pip install "ruleweaver[review]"' in result.stderr
    assert result.stdout == ""


def test_a_token_can_be_minted_without_the_review_extra():
    """Minting is standard library. An operator issuing tokens needs no web server."""
    result = run_without_review_extra("""
        from ruleweaver.review.identity import SignedTokenResolver, mint_token
        secret = "s" * 48
        assert SignedTokenResolver(secret).verify(mint_token("alice", secret)) == "alice"
    """)
    assert result.returncode == 0, result.stderr
