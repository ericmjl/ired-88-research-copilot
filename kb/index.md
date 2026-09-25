# Knowledge base index

One markdown note per paper in [`papers/`](papers/), with YAML frontmatter
(title, authors, year, doi, url, tags). Both humans and agents read these
notes during analysis; `ired_88_research_copilot/kb.py` provides
programmatic search over them.

## Notes

| Note | Year | Why it is in the KB |
|------|------|---------------------|
| [Aleku 2016, AoIRED structure](papers/aleku-2016-aoired.md) | 2016 | Reference IRED crystal structure (PDB 5FWN) |
| [Schober 2019, GSK LSD1 IRED](papers/schober-2019-lsd1-ired.md) | 2019 | Industrial IRED evolution precedent (>38,000x) |
| [Alley 2019, UniRep](papers/alley-2019-unirep.md) | 2019 | Sequence representations used in the anchor paper |
| [Ma 2021, IRED-88 MDE](papers/ma-2021-machine-directed-evolution.md) | 2021 | Anchor paper: DMS + MDE, PDB 7OG3 |
| [Biswas 2021, Low-N](papers/biswas-2021-low-n.md) | 2021 | Sample-efficient engineering; the "LowN" experiment rows |
| [Gilio 2022, IRED review](papers/gilio-2022-ired-review.md) | 2022 | Independent mechanistic reading of the IRED-88 story |

## Querying the KB programmatically

```python
from ired_88_research_copilot import kb

notes = kb.load_all_notes()
hits = kb.search_notes(notes, "S220 active site mouth")
for note, score in hits:
    print(score, note.citation)
    print(kb.snippet_for(note, "S220 active site mouth"))
```

## Conventions for agents

- Every claim in a note must trace to the cited paper (or, for the anchor
  paper, to Eric Ma's first-person blog summary).
- When a notebook or analysis uses a KB fact, cite the note file in the
  output markdown cell.
- Add new papers as `papers/<first-author>-<year>-<short-name>.md` with the
  same frontmatter keys, then add a row to the table above.
