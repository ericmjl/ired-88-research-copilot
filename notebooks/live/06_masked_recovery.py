import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import altair as alt
    import marimo as mo
    import numpy as np
    import pandas as pd

    from ired_88_research_copilot import data, kb, structure

    return alt, data, kb, mo, np, pd, structure


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""# Q6 -- If the DMS had a hole where the literature matters, would we have noticed?"""
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Punch a hole in the DMS at exactly the positions the KB talks
        about -- extracted programmatically, no hardcoding -- then ask the
        other three modalities to nominate what the data lost.
        """
    )
    return


@app.cell
def _():
    # kb.extract_mutation_positions(notes) -> the mask set
    # data.mask_positions(singles, positions) -> the blinded dataset
    return


@app.cell
def _():
    # blinded per-position activity with bands over the masked positions
    return


@app.cell
def _():
    # recovery attempt 1: site classes of the masked positions (structure)
    return


@app.cell
def _():
    # recovery attempt 2: prediction-vs-crystal deviation, masked positions highlighted
    return


@app.cell
def _():
    # recovery attempt 3: KB search (acknowledge the circularity!)
    return


@app.cell
def _():
    # unmask and score: best single + rank per masked position
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Answer""")
    return


if __name__ == "__main__":
    app.run()
