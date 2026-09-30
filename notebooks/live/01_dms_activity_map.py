import marimo

__generated_with = "0.25.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Q1 -- Which single mutations improve IRED-88's activity?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Nearly all ~6,000 possible single mutants were measured.
    `mean` = activity (paper SI-002), `count` = number of measurements.
    """)
    return


@app.cell
def _():
    # load SI-002, extract single mutants, find the WT reference row
    return


@app.cell
def _():
    # heatmap: position x mutant residue, colored by activity
    return


@app.cell
def _():
    # top-15 single mutants, bar chart
    return


@app.cell
def _():
    # per-position mean activity, with lines at the crystal boundary (12, 301)
    return


@app.cell
def _():
    # bonus if time: a position slider + per-mutant bar chart (the explorer)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Answer
    """)
    return


if __name__ == "__main__":
    app.run()
