import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd

    from ired_88_research_copilot import kb, theme

    return kb, mo, pd, theme


@app.cell
def _(mo, theme):
    mo.md(
        f"""
        <span style="background:{theme.KB};color:white;padding:3px 12px;
        border-radius:12px;font-size:12px;font-weight:600">Q3 / 6 · THE KNOWLEDGE BASE</span>

        # What does prior work already know about our top hits?

        `kb/papers/` holds one markdown note per paper: YAML frontmatter for
        structure, prose for claims. This is what makes the repo a *research
        copilot* rather than a folder of data -- analysis questions can be
        answered not just from numbers, but from what the literature already
        established, searched programmatically via
        `ired_88_research_copilot/kb.py`.
        """
    )
    return


@app.cell
def _(kb):
    notes = kb.load_all_notes()
    return (notes,)


@app.cell(hide_code=True)
def _(mo, notes, pd):
    notes_df = pd.DataFrame(
        [
            {
                "note": note.path.name,
                "year": note.year,
                "title": note.title[:72] + ("..." if len(note.title) > 72 else ""),
                "tags": ", ".join(note.tags[:4]),
            }
            for note in notes
        ]
    )
    notes_block = mo.vstack(
        [
            mo.md(r"""## The six notes in the KB"""),
            mo.ui.table(notes_df, page_size=6, selection=None),
        ]
    )
    notes_block
    return (notes_block,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Ask the KB anything

        Edit the query below -- the search re-runs as you type. Terms are
        matched against every note's title, tags, and body; notes matching
        more distinct terms rank higher.
        """
    )
    return


@app.cell
def _(mo):
    kb_query = mo.ui.text(
        value="S220 active site mouth stereoselectivity",
        label="KB query",
        full_width=True,
    )
    kb_query
    return (kb_query,)


@app.cell(hide_code=True)
def _(kb, kb_query, mo, notes):
    def render_hit(note, score, query):
        """Render one KB hit as an accordion entry.

        :param note: The matched :class:`~ired_88_research_copilot.kb.KBNote`.
        :param score: Match score from ``kb.search_notes``.
        :param query: The query that produced the hit.
        :returns: An accordion element for this hit.
        """
        plural = "s" if score != 1 else ""
        body = mo.md(
            f"> {kb.snippet_for(note, query)}\n\n"
            f"Source file: `kb/papers/{note.path.name}`"
        )
        return mo.accordion(
            {f"**{note.citation}** (matched {score} term{plural})": body},
            lazy=True,
        )

    query_text = kb_query.value
    ranked_hits = kb.search_notes(notes, query_text)
    if ranked_hits:
        hit_blocks = [
            render_hit(note, score, query_text) for note, score in ranked_hits[:3]
        ]
    else:
        hit_blocks = [
            mo.callout(
                mo.md(
                    f"**No note matches `{query_text}`.** The KB's silence is a "
                    "result too: it means prior published work (as captured "
                    "here) has nothing to say about this query."
                ),
                kind="warn",
            )
        ]
    mo.vstack(
        [
            mo.md(
                f"### Results for `{query_text}` "
                f"({len(ranked_hits)} of {len(notes)} notes matched)"
            )
        ]
        + hit_blocks
    )
    return (ranked_hits,)


@app.cell
def _(kb, mo, notes):
    a296_hits = kb.search_notes(notes, "A296I")
    mo.callout(
        mo.md(
            f"""
            A **{len(a296_hits)}-note silence**: querying the KB for
            **A296I** -- the strongest DMS hit -- returns nothing. No prior
            work (as captured here) has interpreted this mutation. That is a
            genuine open question, not a failure of the KB. The KB tells us
            what is *known*; what to do about the unknown is Q4's job
            (structure prediction) -- and ultimately the lab's. Try it in
            the query box above.
            """
        ),
        kind="neutral",
    )
    return


@app.cell
def _(mo):
    mo.callout(
        mo.md(
            r"""
            ### Answer -- Q3

            - The KB explains the #2 DMS hit: **S220T** was independently
              interpreted as "at the mouth of the active site cleft",
              restricting access of the wrong substrate conformer and lifting
              ee from 30% to 96% (Gilio et al. 2022, reading Ma et al. 2021).
              Our distance-to-cofactor analysis called S220 "distal"; the KB
              corrects the *interpretation*, not the geometry.
            - The KB warns that **linear additivity holds outside the active
              site** but breaks down inside it -- a falsifiable claim that
              Q5 will test against the data.
            - It documents the engineered winner (**Q194L/S220T/H230Y**,
              99% ee) and the ML-guided alternative (M129L/A156S/Y177W).
            - The KB is **silent on A296I**. Prior work ends where this demo
              begins -- which is the point of a copilot, not an oracle.
            """
        ),
        kind="success",
    )
    return


if __name__ == "__main__":
    app.run()
