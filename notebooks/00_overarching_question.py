import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md(
        r"""
        # IRED-88 Research Copilot

        **A single repo where data, literature, structure, and prediction answer
        one question together.**

        This demo walks an enzyme-engineering analysis the way a research
        copilot should: every question pulls on the data files, the knowledge
        base (`kb/`), the crystal structure, or a structure-prediction tool --
        usually more than one at a time. The repo is scaffolded with
        [pyds-cli](https://github.com/ericmjl/pyds-cli) (cookiecutter data
        science layout), the notebooks are [marimo](https://marimo.io)
        notebooks, and every claim traces to a file in the repo.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The overarching question

        > **Where do activity-improving mutations of the enzyme IRED-88 come
        > from -- and could we have seen them coming by combining DMS data,
        > structure, prediction, and literature?**

        IRED-88 is an imine reductase studied in
        Ma et al., _ACS Catalysis_ 2021 ("Machine-Directed Evolution of an
        Imine Reductase for Activity and Stereoselectivity"), Eric Ma's
        project from his Novartis days. The deep mutational scanning (DMS)
        dataset, the enantioselectivity data, and the crystal structure
        (PDB 7OG3) all come from that paper's public supporting information.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The question ladder

        Each notebook answers one question; together they answer the big one.

        | # | Notebook | Question | Data it leans on |
        |---|----------|----------|------------------|
        | Q1 | `01_dms_activity_map.py` | Which single mutations improve IRED-88, and where do they sit along the sequence? | DMS activity table (SI-002) |
        | Q2 | `02_structure_context.py` | Are the beneficial positions where the structure says they should be? | DMS + crystal structure (7OG3) |
        | Q3 | `03_knowledge_base.py` | What does prior work already know about our top hits? | `kb/papers/*.md` |
        | Q4 | `04_structure_prediction.py` | What does prediction see that the crystal cannot? | ESMFold prediction + 7OG3 |
        | Q5 | `05_additivity.py` | Doubles and triples: additive or epistatic? (Does the KB's claim survive the data?) | SI-003 combos + SI-002 singles + site classes |
        | Q6 | `06_masked_recovery.py` | If the DMS had a hole where the literature matters, would we have noticed? | everything |

        The four modalities, all in one repo:

        - `data/raw/` -- DMS + enantioselectivity tables (paper SI, public)
        - `kb/` -- six literature notes with frontmatter, searchable via
          `ired_88_research_copilot/kb.py`
        - `data/external/7OG3.pdb` -- the 1.9 A crystal structure
        - `data/external/ired88_esmfold.pdb` -- ESMFold prediction
          (regenerate with `scripts/predict_structure_esmfold.py`)
        """
    )
    return


@app.cell
def _(data, mo):
    import pandas as pd

    _singles = data.extract_single_mutants(data.load_si002())
    _top5 = _singles.nlargest(5, "mean")[["mutation", "mean", "count"]]
    _wt = data.load_si002()
    _wt_row = _wt[_wt["mutation"].isna()]
    _baseline = _wt_row["mean"].iloc[0]

    mo.md(
        f"""
        ## Teaser: the DMS dataset in one table

        {len(_singles):,} single mutants of the 304-residue enzyme were
        measured (of {304 * 19:,} possible). The unlabeled wild-type
        reference row (n={int(_wt_row["count"].iloc[0])} measurements) has
        mean activity **{_baseline:.3f}**; the median single mutant scores
        **{_singles["mean"].median():.3f}**. Here are the top 5:

        {_top5.to_string(index=False)}

        Now open `01_dms_activity_map.py` and let's find out where they live.
        """
    )
    return (pd,)


@app.cell
def _():
    from ired_88_research_copilot import data

    return (data,)


if __name__ == "__main__":
    app.run()
