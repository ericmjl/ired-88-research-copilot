"""Knowledge base utilities.

The knowledge base lives in ``kb/papers/`` as one markdown note per paper,
with YAML frontmatter carrying structured metadata (title, authors, year,
doi, url, tags). ``kb/index.md`` links every note. Both humans and agents
read these notes during analysis; this module gives notebooks programmatic
access so a query like "S220 active site mouth" returns the relevant notes.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from pyprojroot import here

KB_DIR: Path = here() / "kb"
PAPERS_DIR: Path = KB_DIR / "papers"

_FRONTMATTER = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


@dataclass
class KBNote:
    """One knowledge-base note (a paper summary).

    :param path: Path to the markdown note.
    :param title: Paper title.
    :param authors: First author et al. string.
    :param year: Publication year.
    :param doi: Digital object identifier, if available.
    :param url: URL for retrieval, if available.
    :param tags: Topic tags for the note.
    :param body: The note body (markdown, everything after frontmatter).
    """

    path: Path
    title: str
    authors: str = ""
    year: int | None = None
    doi: str = ""
    url: str = ""
    tags: list[str] = field(default_factory=list)
    body: str = ""

    @property
    def text(self) -> str:
        """Full searchable text of the note (title, tags, and body).

        :returns: Lowercased concatenation of title, tags, and body.
        """
        return " ".join([self.title, *self.tags, self.body]).lower()

    @property
    def citation(self) -> str:
        """Short citation line for display.

        :returns: A one-line citation string.
        """
        bits = [self.authors, f"({self.year}).", self.title]
        if self.doi:
            bits.append(f"DOI: {self.doi}")
        return " ".join(str(bit) for bit in bits)


def load_note(path: Path) -> KBNote:
    """Load a single knowledge-base note from a markdown file.

    :param path: Path to a markdown note with optional YAML frontmatter.
    :returns: The parsed :class:`KBNote`.
    """
    raw = path.read_text()
    meta: dict = {}
    body = raw
    match = _FRONTMATTER.match(raw)
    if match:
        meta = yaml.safe_load(match.group(1)) or {}
        body = raw[match.end() :]
    return KBNote(
        path=path,
        title=meta.get("title", path.stem),
        authors=meta.get("authors", ""),
        year=meta.get("year"),
        doi=meta.get("doi", ""),
        url=meta.get("url", ""),
        tags=meta.get("tags", []) or [],
        body=body.strip(),
    )


def load_all_notes(papers_dir: Path = PAPERS_DIR) -> list[KBNote]:
    """Load every note in the knowledge base papers directory.

    :param papers_dir: Directory containing the paper markdown notes.
    :returns: Notes sorted by year (ascending).
    """
    notes = [load_note(p) for p in sorted(papers_dir.glob("*.md"))]
    return sorted(notes, key=lambda n: (n.year is None, n.year))


def search_notes(notes: list[KBNote], query: str) -> list[tuple[KBNote, int]]:
    """Rank knowledge-base notes against a free-text query.

    Scoring counts how many query terms appear in each note's text; notes
    matching more distinct terms rank higher.

    :param notes: Notes to search.
    :param query: Free-text query, e.g. ``"S220 active site mouth"``.
    :returns: ``(note, score)`` pairs with score > 0, best first.
    """
    terms = [t.lower() for t in query.split() if t]
    scored = []
    for note in notes:
        score = sum(note.text.count(term) > 0 for term in set(terms))
        if score:
            scored.append((note, score))
    return sorted(scored, key=lambda pair: (-pair[1], pair[0].path.name))


def snippet_for(note: KBNote, query: str, width: int = 300) -> str:
    """Return the passage of a note most relevant to a query.

    :param note: The note to excerpt.
    :param query: Free-text query used to locate the passage.
    :param width: Maximum length of the returned snippet.
    :returns: A snippet centered on the first query-term occurrence.
    """
    text = note.body
    lower = text.lower()
    hit = min(
        (lower.find(t.lower()) for t in query.split() if lower.find(t.lower()) >= 0),
        default=0,
    )
    start = max(0, hit - width // 3)
    end = min(len(text), start + width)
    prefix = "..." if start > 0 else ""
    suffix = "..." if end < len(text) else ""
    return f"{prefix}{text[start:end].strip()}{suffix}"
