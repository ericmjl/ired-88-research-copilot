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
    mo.md(r"""# Q3 -- What does prior work already know about our top hits?""")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        `kb/papers/` holds one markdown note per paper with YAML
        frontmatter. `kb.py` searches them programmatically.
        """
    )
    return


@app.cell
def _():
    # load all notes; show a small index table
    return


@app.cell
def _():
    # search: "S220 active site mouth stereoselectivity" -> show snippets
    return


@app.cell
def _():
    # search: "linear additivity combining mutations"
    return


@app.cell
def _():
    # search: "A296 296 C-terminal tail" -- expect silence
    return


@app.cell
def _(mo):
    mo.md(r"""## Answer""")
    return


if __name__ == "__main__":
    app.run()
