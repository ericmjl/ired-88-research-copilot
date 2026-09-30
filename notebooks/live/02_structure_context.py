import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import altair as alt
    import marimo as mo
    import pandas as pd

    from ired_88_research_copilot import data, structure

    return alt, data, mo, pd, structure


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""# Q2 -- Are the beneficial positions where the structure says they should be?"""
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        PDB 7OG3 (1.9 A, NADP bound). ATOM residue number = DMS position;
        the crystal resolves positions 12-301.
        """
    )
    return


@app.cell
def _():
    # crystal structure + minimum NADP distance per position
    # join the site classes onto the DMS per-position means
    return


@app.cell
def _():
    # per-position activity, colored by site class
    return


@app.cell
def _():
    # top-15 mutants annotated with site class + resolved status
    return


@app.cell
def _():
    # enrichment: site-class distribution of the top-50 positions vs. all
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Answer""")
    return


if __name__ == "__main__":
    app.run()
