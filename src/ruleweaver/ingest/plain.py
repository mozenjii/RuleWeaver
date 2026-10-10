"""Unstructured sources: memoranda, notices and tables of published figures.

A regulation is addressed clause by clause. The documents that carry the numbers a
regulation reads — the annual FNS cost-of-living memo, the HHS poverty guidelines — have
no paragraph markers to address, so they are ingested as one block of canonical text with
no clauses. A span citing one is checked by its quote alone, against the whole text, and
its citation is descriptive: it says which table and row a reviewer should look at.

Two transport forms are read: plain text, and HTML with its markup dropped. A PDF is
recorded in the manifest as the authoritative file but read through a text rendering that
the manifest pins separately (`text_file`, `text_sha256`), because extracting text from a
PDF depends on the extractor and the result is what a quote is checked against.
"""

from __future__ import annotations

import html
import re
from html.parser import HTMLParser
from pathlib import Path

from .document import SourceDocument


class _Text(HTMLParser):
    """Collects character data, dropping scripts and styles."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self._skip = 0

    def handle_starttag(self, tag, attrs) -> None:
        if tag in ("script", "style"):
            self._skip += 1

    def handle_endtag(self, tag) -> None:
        if tag in ("script", "style") and self._skip:
            self._skip -= 1

    def handle_data(self, data) -> None:
        if not self._skip:
            self.parts.append(data)


def html_text(raw: str) -> str:
    """The text a reader sees, with line structure kept (GovInfo serves tables in `<pre>`)."""
    parser = _Text()
    parser.feed(raw)
    parser.close()
    return html.unescape("".join(parser.parts))


def parse_plain(raw: bytes, *, source_id: str, citation: str | None = None,
                title: str | None = None, html_markup: bool = False,
                point_in_time: str | None = None, retrieved_at: str | None = None,
                sha256: str | None = None) -> SourceDocument:
    text = raw.decode("utf-8")
    if html_markup:
        text = html_text(text)
    text = re.sub(r"\r\n?", "\n", text).strip("\n")
    return SourceDocument(source_id=source_id, citation=citation or source_id,
                          title=title or citation or source_id, text=text, clauses=[],
                          point_in_time=point_in_time, retrieved_at=retrieved_at,
                          sha256=sha256)


def is_plain(path: Path) -> bool:
    return path.suffix.lower() in (".txt", ".htm", ".html", ".pdf")
