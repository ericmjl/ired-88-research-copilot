"""Tests for knowledge base utilities."""

from ired_88_research_copilot import kb


def test_all_notes_load():
    """All six KB notes load with frontmatter metadata."""
    notes = kb.load_all_notes()
    assert len(notes) == 6
    assert all(note.title for note in notes)
    assert all(note.year for note in notes)
    years = [note.year for note in notes]
    assert years == sorted(years)


def test_search_finds_anchor_paper_for_s220():
    """Querying S220 surfaces the mechanistic reading in the review."""
    notes = kb.load_all_notes()
    hits = kb.search_notes(notes, "S220 active site mouth")
    assert hits
    names = [note.path.name for note, _ in hits]
    assert "gilio-2022-ired-review.md" in names


def test_search_ranks_anchor_paper_first_for_dms():
    """A DMS query ranks the anchor paper at or near the top."""
    notes = kb.load_all_notes()
    hits = kb.search_notes(notes, "deep mutational scan DMS IRED-88")
    top_names = [note.path.name for note, _ in hits[:2]]
    assert "ma-2021-machine-directed-evolution.md" in top_names


def test_snippet_mentions_query_term():
    """Snippets are excerpted around the first query-term hit."""
    notes = kb.load_all_notes()
    note = next(n for n in notes if "gilio" in n.path.name)
    snippet = kb.snippet_for(note, "S220T")
    assert "S220" in snippet


def test_extract_mutation_positions():
    """The KB's mutation tokens map to exactly the six known positions."""
    notes = kb.load_all_notes()
    positions = kb.extract_mutation_positions(notes)
    assert set(positions) == {129, 156, 177, 194, 220, 230}
    assert any("S220T" in mention for mention in positions[220])


def test_extract_mutation_positions_no_false_positives():
    """Identifiers like IRED88, ZPL389, and 5FWN do not match."""
    import tempfile
    from pathlib import Path

    with tempfile.TemporaryDirectory() as tmp:
        note_path = Path(tmp) / "fake-note.md"
        note_path.write_text(
            "---\ntitle: fake\nyear: 2024\n---\n\nIRED88 and ZPL389 and 5FWN and si_002 and H4 receptor.\n"
        )
        positions = kb.extract_mutation_positions([kb.load_note(note_path)])
    assert positions == {}
