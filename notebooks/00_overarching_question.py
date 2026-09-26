import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import altair as alt
    import marimo as mo

    from ired_88_research_copilot import data, theme

    theme.apply()
    return alt, data, mo, theme


@app.cell
def _(mo, theme):
    mo.md(
        f"""
        <div style="background:linear-gradient(135deg, {theme.PRIMARY} 0%, #134e4a 100%);
                    border-radius:16px; padding:28px 32px; color:white;">
        <div style="font-size:13px; letter-spacing:2px; opacity:0.85;
                    text-transform:uppercase;">AI as a Research Co-Pilot · Live demo</div>
        <h1 style="margin:10px 0 6px 0; font-size:34px; line-height:1.15;">
        The IRED-88 Research Copilot</h1>
        <div style="font-size:15px; opacity:0.92;">
        One enzyme, four data modalities, one question ladder -- in a single repo.</div>
        </div>
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        An enzyme-engineering campaign produced a deep mutational scan, an
        enantioselectivity table, a 1.9 A crystal structure, and a set of
        engineered variants. Around it sits a small **knowledge base** of six
        papers. This demo runs the round-trip between all four modalities --
        and asks one question on the way:

        > #### Where do activity-improving mutations of the enzyme IRED-88 come from -- and could we have seen them coming?
        """
    )
    return


@app.cell
def _(data, mo):
    singles = data.extract_single_mutants(data.load_si002())
    si002 = data.load_si002()
    wt_mean = float(si002[si002["mutation"].isna()]["mean"].iloc[0])
    cover_stats = mo.hstack(
        [
            mo.stat(
                value=f"{len(singles):,}",
                label="single mutants",
                caption="of 5,776 possible",
            ),
            mo.stat(value="81%", label="library coverage", caption="cloned & measured"),
            mo.stat(
                value="310", label="engineered variants", caption="doubles & triples"
            ),
            mo.stat(value="6", label="KB papers", caption="kb/papers/"),
            mo.stat(value="290", label="crystal residues", caption="of 304 (PDB 7OG3)"),
        ],
        justify="space-between",
        widths="equal",
    )
    cover_stats
    return cover_stats, singles, wt_mean


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The question ladder

        Each notebook answers one question; together they answer the big one.
        Everything runs top-to-bottom with no hidden state -- every claim
        traces to a cell, a file, or a KB note.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        | # | Notebook | Question | Leans on |
        |---|----------|----------|----------|
        | **Q1** | `01_dms_activity_map.py` | Which mutations improve activity, and where do they sit? | DMS table (SI-002) |
        | **Q2** | `02_structure_context.py` | Are the hits where the structure says they should be? | DMS + PDB 7OG3 |
        | **Q3** | `03_knowledge_base.py` | What does prior work already know? | `kb/papers/*.md` |
        | **Q4** | `04_structure_prediction.py` | What does prediction see that the crystal cannot? | ESMFold + 7OG3 |
        | **Q5** | `05_additivity.py` | Doubles & triples: additive or epistatic? | SI-003 + site classes |
        | **Q6** | `06_masked_recovery.py` | If the DMS had a hole where the literature matters? | everything |
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The four modalities

        | Modality | Where | What it is good at |
        |----------|-------|--------------------|
        | **DMS + ee data** | `data/raw/` | *Discovery* -- finding hits nobody guessed |
        | **Crystal structure** | `data/external/7OG3.pdb` | *Mechanism filtering* -- killing bad priors |
        | **Knowledge base** | `kb/` | *Explanation & recovery* -- naming what worked and why |
        | **Structure prediction** | `data/external/ired88_esmfold.pdb` | *Blind-spot extension* -- with a confidence score attached |

        Helper code lives in `ired_88_research_copilot/` (`data.py`,
        `structure.py`, `kb.py`, `theme.py`), with tests in `tests/`.
        Presenting live? `notebooks/live/` holds empty skeleton twins of
        every notebook.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Run it

        ```bash
        pixi install
        pixi run marimo edit notebooks/
        ```

        Data source: supporting information of Ma et al.,
        *ACS Catal.* **2021**, 11 (20), 12433-12445
        ([10.1021/acscatal.1c02786](https://pubs.acs.org/doi/abs/10.1021/acscatal.1c02786)),
        from Eric Ma's enzyme-engineering work at Novartis. Crystal structure:
        [PDB 7OG3](https://www.rcsb.org/structure/7OG3). Use the bundled data
        for demos and teaching; cite the paper for anything beyond that.

        Start with `01_dms_activity_map.py`.
        """
    )
    return


if __name__ == "__main__":
    app.run()
