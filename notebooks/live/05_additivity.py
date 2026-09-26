import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import altair as alt
    import marimo as mo
    import numpy as np
    import pandas as pd

    from ired_88_research_copilot import data

    return alt, data, mo, np, pd


@app.cell
def _(mo):
    mo.md(r"""# Q5 -- Doubles and triples: additive or epistatic?""")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Q3's KB claim: additivity outside the active site, harder inside.
        The combination data live in SI-003 (`ratio` = conversion). Test it.
        """
    )
    return


@app.cell
def _():
    # load SI-003; conversion vs ee scatter, colored by strategy
    return


@app.cell
def _():
    # scale bridge: singles in BOTH tables -> linear fit mean -> ratio
    # (WT reference row comes from SI-002)
    return


@app.cell
def _():
    # combos: split_combination, keep only fully-covered combinations
    return


@app.cell
def _():
    # additive expectation in log-odds space:
    # expected logit = logit(WT) + sum(logit(single) - logit(WT))
    # epistasis = logit(observed) - expected logit
    return


@app.cell
def _():
    # expected vs observed scatter with a diagonal, colored by strategy
    return


@app.cell
def _():
    # median epistasis by experiment (bar chart); watch for assay ceiling
    return


@app.cell
def _(mo):
    mo.md(r"""## Answer""")
    return


if __name__ == "__main__":
    app.run()
