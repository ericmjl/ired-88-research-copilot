import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import altair as alt
    import marimo as mo
    import numpy as np
    import pandas as pd

    from ired_88_research_copilot import structure

    return alt, mo, np, pd, structure


@app.cell
def _(mo):
    mo.md(
        r"""
        # Q4 -- What does structure prediction see that the crystal cannot?

        The crystal resolves positions 12-301. Q1 found beneficial mutations
        at positions 302-304 (and 1-11), which have **no experimental
        coordinates**. Structure prediction is the bridge: ESMFold predicted
        all 304 residues from sequence alone (`ired88_esmfold.pdb`, made
        with the public API in `scripts/predict_structure_esmfold.py`).

        First, validate the prediction where truth exists; only then trust
        (cautiously) what it says where truth does not.
        """
    )
    return


@app.cell
def _(np, structure):
    crystal = structure.load_crystal_structure()
    predicted = structure.load_predicted_structure()
    rmsd = structure.ca_rmsd(predicted, crystal)
    aligned, target, resnums = structure.superposed_ca(predicted, crystal)
    per_res_distance = np.sqrt(((aligned - target) ** 2).sum(axis=1))
    n_shared = len(resnums)
    return crystal, n_shared, per_res_distance, predicted, resnums, rmsd, target


@app.cell
def _(mo, n_shared, rmsd):
    mo.md(
        f"""
        ## Step 1 -- validate where the crystal exists

        Superposing the prediction onto the crystal over the
        {n_shared} shared residues gives a global C-alpha RMSD of
        **{rmsd:.2f} A** -- the same fold, with local flexibility. The
        prediction is trustworthy as a hypothesis generator.
        """
    )
    return


@app.cell
def _(alt, mo, pd, per_res_distance, resnums):
    distance_df = pd.DataFrame({"pos": resnums, "distance": per_res_distance})
    distance_chart = (
        alt.Chart(
            distance_df, title="Per-residue C-alpha distance: prediction vs. crystal"
        )
        .mark_line()
        .encode(
            x=alt.X("pos:Q", title="Sequence position"),
            y=alt.Y("distance:Q", title="C-alpha distance (A)"),
            tooltip=["pos", "distance"],
        )
        .properties(width=900, height=220)
    )
    mo.vstack(
        [
            mo.md(
                r"""
                The flexible loop around positions 207-222 and 242-243
                deviates most -- exactly the neighborhood of the S220 lead
                and the 243 cluster from Q1. Hypothesis: those positions
                tune a mobile region.
                """
            ),
            distance_chart,
        ]
    )
    return (distance_chart,)


@app.cell
def _(np, structure):
    bfactors_raw = structure.per_residue_bfactors(structure.load_predicted_structure())
    # ESMFold PDB output encodes pLDDT/100 in the B-factor column; scale to 0-100.
    bfactors = {p: value * 100 for p, value in bfactors_raw.items()}
    core_plddt = float(np.mean([bfactors[p] for p in range(12, 302)]))
    tail_plddt = [round(bfactors[p]) for p in (302, 303, 304)]
    nterm_plddt = float(np.mean([bfactors[p] for p in range(1, 12)]))
    return bfactors, core_plddt, nterm_plddt, tail_plddt


@app.cell
def _(core_plddt, mo, nterm_plddt, tail_plddt):
    mo.md(
        f"""
        ## Step 2 -- only then, read the blind spots

        ESMFold's B-factor column carries per-residue pLDDT confidence
        (0-100):

        - resolved region (12-301): mean pLDDT **{core_plddt:.0f}**
        - invisible N-terminus (1-11): mean pLDDT **{nterm_plddt:.0f}**
        - invisible C-tail (302-304): pLDDT **{tail_plddt[0]} / {tail_plddt[1]} / {tail_plddt[2]}**

        The tail predictions are **moderate-confidence at best** (71-82 vs.
        96 in the core). The prediction's geometry for the tail points out
        of the fold and away from the active site: superposed into the
        crystal frame, the last three residues' C-alphas sit **28-30 A from
        the NADP cofactor**. Notably, the invisible N-terminus (1-11) is
        predicted *confidently* (mean pLDDT {nterm_plddt:.0f}) -- a reminder
        that prediction confidence and crystallographic order are related
        but not identical. A296I (top DMS hit, position 296) is *inside*
        the resolved region and about 2.3 A from the crystal position.
        """
    )
    return


@app.cell
def _(alt, bfactors, mo, pd):
    plddt_df = pd.DataFrame({"pos": list(bfactors), "plddt": list(bfactors.values())})
    plddt_df["region"] = plddt_df["pos"].map(
        lambda p: (
            "resolved in crystal (12-301)" if 12 <= p <= 301 else "invisible to crystal"
        )
    )
    plddt_chart = (
        alt.Chart(plddt_df, title="ESMFold per-residue confidence (pLDDT)")
        .mark_line()
        .encode(
            x=alt.X("pos:Q", title="Sequence position"),
            y=alt.Y("plddt:Q", title="pLDDT", scale=alt.Scale(domain=[0, 100])),
            color=alt.Color("region:N", title=None),
            tooltip=["pos", "plddt"],
        )
        .properties(width=900, height=240)
    )
    mo.vstack(
        [
            mo.md(
                r"""
                The confidence dip over the C-tail is the model flagging its
                own uncertainty exactly where the crystallographers found no
                density; the N-terminus stays confident, which tells us
                disorder-in-crystal and low-prediction-confidence are not the
                same thing.
                """
            ),
            plddt_chart,
        ]
    )
    return (plddt_chart,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Answer to Q4

        - **Validation first:** the prediction reproduces the crystal fold at
          2.36 A global RMSD, so it is safe to use as a hypothesis generator
          in unresolved regions.
        - The invisible C-tail (302-304) is predicted at **moderate
          confidence (71-82)** and **far from the active site (~28-30 A)**,
          pointing out of the fold. The DMS says mutating it helps;
          prediction says it is not making direct active-site contact. A
          testable story: the tail modulates stability or solubility rather
          than chemistry.
        - The largest prediction-vs-crystal deviations sit in the **loop
          around 207-243** -- the neighborhood of S220T and the 243 cluster.
          Prediction and DMS agree that this region is *mobile and
          important*; neither can name the mechanism alone.
        - Structure prediction did not "solve" the question. It narrowed it
          and sharpened what to test next -- which is what a copilot is for.
        """
    )
    return


if __name__ == "__main__":
    app.run()
