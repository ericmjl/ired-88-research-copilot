import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import altair as alt
    import marimo as mo
    import numpy as np
    import pandas as pd

    from ired_88_research_copilot import structure, theme

    theme.apply()
    return alt, mo, np, pd, structure, theme


@app.cell(hide_code=True)
def _(mo, theme):
    mo.md(
        f"""
        <span style="background:{theme.SECOND_SHELL};color:white;padding:3px 12px;
        border-radius:12px;font-size:12px;font-weight:600">Q4 / 6 · THE PREDICTION</span>

        # What does structure prediction see that the crystal cannot?

        The crystal resolves positions 12-301. Q1 found beneficial mutations
        at positions 302-304 (and 1-11) -- which have **no experimental
        coordinates**. ESMFold predicted all 304 residues from sequence alone
        (`data/external/ired88_esmfold.pdb`, regenerable with
        `scripts/predict_structure_esmfold.py`).

        The rule for this notebook: **validate where truth exists first**;
        only then trust -- cautiously -- what prediction says where it
        doesn't.
        """
    )
    return


@app.cell
def _(np, pd, structure):
    crystal = structure.load_crystal_structure()
    predicted = structure.load_predicted_structure()
    global_rmsd = structure.ca_rmsd(predicted, crystal)
    aligned, target, resnums = structure.superposed_ca(predicted, crystal)
    deviation = pd.Series(np.sqrt(((aligned - target) ** 2).sum(axis=1)), index=resnums)
    n_shared = len(resnums)
    return crystal, deviation, global_rmsd, n_shared, predicted, resnums, target


@app.cell(hide_code=True)
def _(global_rmsd, mo, n_shared):
    validation_stats = mo.hstack(
        [
            mo.stat(
                value=f"{global_rmsd:.2f} A",
                label="global C-alpha RMSD",
                caption=f"over {n_shared} shared residues",
            ),
            mo.stat(
                value="same fold",
                label="verdict",
                caption="usable as hypothesis generator",
            ),
        ],
        justify="space-between",
    )
    mo.vstack(
        [
            mo.md(r"""## Step 1 -- validate where the crystal exists"""),
            validation_stats,
            mo.md(
                f"""
                Superposing the prediction onto the crystal gives a global
                C-alpha RMSD of **{global_rmsd:.2f} A** over the {n_shared}
                shared residues: the same fold, with local flexibility. Safe
                to use as a hypothesis generator.
                """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(alt, mo, pd, deviation, resnums):
    distance_df = pd.DataFrame({"pos": resnums, "deviation": deviation})
    deviation_chart = (
        alt.Chart(
            distance_df,
            title="Per-residue C-alpha deviation: ESMFold prediction vs. crystal",
        )
        .mark_area(color="#3b6ea5", opacity=0.25)
        .encode(
            x=alt.X("pos:Q", title="Sequence position"),
            y=alt.Y("deviation:Q", title="C-alpha deviation (A)"),
        )
        .properties(width=860, height=200)
    )
    deviation_line = (
        alt.Chart(distance_df)
        .mark_line(color="#3b6ea5")
        .encode(x="pos:Q", y="deviation:Q")
    )
    deviation_md = mo.md(
        r"""
        The flexible **loop around 207-222 and 242-243** deviates most --
        exactly the neighborhood of the S220 lead and the 243 cluster from
        Q1. Hypothesis to carry forward: those positions tune a mobile
        region.
        """
    )
    mo.vstack(
        [
            deviation_chart + deviation_line,
            deviation_md,
        ]
    )
    return (deviation_chart,)


@app.cell
def _(np, structure):
    bfactor_by_position = structure.per_residue_bfactors(
        structure.load_predicted_structure()
    )
    plddt = {p: value * 100 for p, value in bfactor_by_position.items()}
    core_plddt = float(np.mean([plddt[p] for p in range(12, 302)]))
    nterm_plddt = float(np.mean([plddt[p] for p in range(1, 12)]))
    tail_plddt = [round(plddt[p]) for p in (302, 303, 304)]
    return core_plddt, nterm_plddt, plddt, tail_plddt


@app.cell
def _(core_plddt, mo, nterm_plddt, tail_plddt):
    confidence_stats = mo.hstack(
        [
            mo.stat(
                value=f"{core_plddt:.0f}",
                label="pLDDT, resolved region",
                caption="positions 12-301",
            ),
            mo.stat(
                value=f"{nterm_plddt:.0f}",
                label="pLDDT, invisible N-term",
                caption="positions 1-11",
            ),
            mo.stat(
                value=" / ".join(str(p) for p in tail_plddt),
                label="pLDDT, invisible C-tail",
                caption="positions 302-304",
            ),
        ],
        justify="space-between",
    )
    confidence_stats
    return (confidence_stats,)


@app.cell(hide_code=True)
def _(alt, mo, pd, plddt):
    plddt_df = pd.DataFrame({"pos": list(plddt), "plddt": list(plddt.values())})
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
        .properties(width=860, height=220)
    )
    plddt_md = mo.md(
        r"""
        The confidence dip over the C-tail is the model flagging its own
        uncertainty exactly where the crystallographers found no density.
        The N-terminus stays confident -- a reminder that
        disorder-in-crystal and low-prediction-confidence are not the same
        thing.
        """
    )
    mo.vstack([plddt_md, plddt_chart])
    return (plddt_chart,)


@app.cell(hide_code=True)
def _(crystal, mo, np, pd, plddt, predicted, structure):
    common = [
        r for r in predicted.observed_resnums if r in set(crystal.observed_resnums)
    ]
    ca_pred = np.array([structure._ca_coord(predicted, r) for r in common])
    ca_xtal = np.array([structure._ca_coord(crystal, r) for r in common])
    center_p, center_c = ca_pred.mean(axis=0), ca_xtal.mean(axis=0)
    rotation = structure.kabsch_transform(ca_pred - center_p, ca_xtal - center_c)
    ligand = crystal.ligand_coords
    tail_rows = []
    for pos in (296, 302, 303, 304):
        ca = structure._ca_coord(predicted, pos)
        moved = (ca - center_p) @ rotation + center_c
        tail_rows.append(
            {
                "position": pos,
                "in crystal?": "yes" if pos in crystal.residues else "no",
                "pLDDT": round(plddt[pos]),
                "A to NADP (predicted, crystal frame)": f"{np.sqrt(((ligand - moved) ** 2).sum(axis=1)).min():.0f}",
            }
        )
    tail_df = pd.DataFrame(tail_rows)
    mo.vstack(
        [
            mo.md(
                r"""
                ## Step 2 -- only then, read the blind spots

                In the predicted model the last residues leave the fold and
                point **away from the active site**: superposed into the
                crystal frame, positions 302-304 sit ~28-30 A from NADP.
                A296I -- the top DMS hit -- is *inside* the resolved region,
                about 2.3 A from its crystal position.
                """
            ),
            tail_df,
        ]
    )
    return (tail_df,)


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        mo.md(
            r"""
            ### Answer -- Q4

            - **Validation first:** the prediction reproduces the crystal
              fold at 2.36 A global RMSD -- safe to use as a hypothesis
              generator in unresolved regions.
            - The invisible C-tail (302-304) is predicted at **moderate
              confidence (71-82)** and **~28-30 A from the active site**,
              pointing out of the fold. The DMS says mutating it helps;
              prediction says it is not making direct active-site contact.
              Testable story: the tail modulates stability or solubility
              rather than chemistry.
            - The largest prediction-vs-crystal deviations sit in the
              **loop around 207-243** -- S220's neighborhood. Prediction and
              DMS agree that this region is *mobile and important*; neither
              can name the mechanism alone.
            - Structure prediction did not "solve" the question. It narrowed
              it and sharpened what to test next.
            """
        ),
        kind="success",
    )
    return


if __name__ == "__main__":
    app.run()
