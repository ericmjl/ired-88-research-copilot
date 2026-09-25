import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd

    from ired_88_research_copilot import kb

    return kb, mo, pd


@app.cell
def _(mo):
    mo.md(
        r"""
        # Q3 -- What does prior work already know about our top hits?

        The repo carries a small knowledge base in `kb/papers/`: one markdown
        note per paper, YAML frontmatter for structure, prose for the claims.
        This is what makes the repo a *research copilot* rather than a folder
        of data: an analysis question can be answered not just from numbers
        but from what the literature already established -- searchable
        programmatically via `ired_88_research_copilot/kb.py`.
        """
    )
    return


@app.cell
def _(kb):
    notes = kb.load_all_notes()
    return (notes,)


@app.cell
def _(mo, notes, pd):
    notes_df = pd.DataFrame(
        [
            {
                "note": note.path.name,
                "year": note.year,
                "title": note.title[:70] + ("..." if len(note.title) > 70 else ""),
                "tags": ", ".join(note.tags),
            }
            for note in notes
        ]
    )
    mo.md(
        r"""
        ## The six notes in the KB
        """
    )
    notes_df
    return (notes_df,)


@app.cell
def _(kb, mo, notes):
    query_s220 = "S220 active site mouth stereoselectivity"
    hits_s220 = kb.search_notes(notes, query_s220)
    s220_blocks = [
        mo.md(
            f"**{note.citation}** (score {score})\n\n> {kb.snippet_for(note, query_s220)}"
        )
        for note, score in hits_s220[:2]
    ]
    mo.md(
        r"""
        ## Ask the KB about S220, the heavily-replicated DMS lead
        """
    )
    mo.vstack([mo.md(f"Query: `{query_s220}`")] + s220_blocks)
    return (hits_s220, query_s220)


@app.cell
def _(kb, mo, notes):
    query_add = "linear additivity combining mutations"
    hits_add = kb.search_notes(notes, query_add)
    add_blocks = [
        mo.md(
            f"**{note.citation}** (score {score})\n\n> {kb.snippet_for(note, query_add)}"
        )
        for note, score in hits_add[:2]
    ]
    mo.md(
        r"""
        ## Ask the KB about combining mutations
        """
    )
    mo.vstack([mo.md(f"Query: `{query_add}`")] + add_blocks)
    return (hits_add, query_add)


@app.cell
def _(kb, mo, notes):
    hits_a296 = kb.search_notes(notes, "A296 296 C-terminal tail")
    mo.md(
        f"""
        ## Ask the KB about A296I, the strongest DMS hit

        Query: `A296 296 C-terminal tail`

        **Result: {len(hits_a296)} notes found anything.** The KB has
        nothing on A296I -- no prior work has interpreted this mutation.
        That is a genuine open question, not a failure of the KB: the KB
        tells us what is *known*. What we do about the unknown is the next
        notebook's job (structure prediction), and ultimately the lab's.
        """
    )
    return (hits_a296,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Answer to Q3

        - The KB explains the #2 DMS hit: **S220T** was independently
          interpreted as "at the mouth of the active site cleft",
          restricting access of the wrong substrate conformer and lifting
          ee from 30% to 96% (Gilio et al. 2022, reading the Ma et al.
          2021 results). Our distance-to-NADP analysis called S220
          "distal"; the KB corrects the *interpretation*, not the geometry.
        - The KB warns that **linear additivity holds outside the active
          site** but breaks down inside it -- directly relevant to how we
          combine the distal top hits.
        - The KB documents the winning engineered variant
          (**Q194L/S220T/H230Y**, 99% ee) and the ML-guided alternative
          (M129L/A156S/Y177W), which we will meet in the data in Q5.
        - The KB is **silent on A296I**. Prior work ends where our demo
          begins -- which is the point of a copilot rather than an oracle.
        """
    )
    return


if __name__ == "__main__":
    app.run()
