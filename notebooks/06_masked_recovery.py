import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import altair as alt
    import marimo as mo
    import numpy as np
    import pandas as pd

    from ired_88_research_copilot import data, kb, structure, theme

    theme.apply()
    return alt, data, kb, mo, np, pd, structure, theme


@app.cell
def _(mo, theme):
    mo.md(
        f"""
        <span style="background:{theme.ACTIVE_SITE};color:white;padding:3px 12px;
        border-radius:12px;font-size:12px;font-weight:600">Q6 / 6 · THE STRESS TEST</span>

        # If the DMS had a hole where the literature matters, would we have noticed?

        Saturation-mutagenesis libraries always have gaps: oligo pools fail,
        some positions never clone. So let's **punch a hole in the DMS on
        purpose** -- at exactly the positions the knowledge base talks about
        -- and ask whether the other three modalities could nominate what
        the data lost.
        """
    )
    return


@app.cell
def _(data, kb):
    notes = kb.load_all_notes()
    kb_positions = kb.extract_mutation_positions(notes)
    mask_list = sorted(kb_positions)
    singles = data.extract_single_mutants(data.load_si002())
    masked = data.mask_positions(singles, mask_list)
    return kb_positions, mask_list, masked, notes, singles


@app.cell(hide_code=True)
def _(kb_positions, mo, pd):
    mention_df = pd.DataFrame(
        [
            {
                "position": pos,
                "KB mentions": " · ".join(m.split(" (")[0] for m in mentions),
                "source notes": len(mentions),
            }
            for pos, mentions in kb_positions.items()
        ]
    )
    mask_md = mo.md(
        r"""
        ## The mask, extracted from the knowledge base

        Scanning all six notes for `S220T`-style tokens -- including tokens
        inside combination strings like `Q194L; S220T; H230Y` -- yields the
        KB's cast of characters. No hardcoding anywhere.
        """
    )
    mo.vstack([mask_md, mention_df])
    return (mention_df,)


@app.cell(hide_code=True)
def _(alt, mask_list, masked, mo, pd, singles, theme):
    by_position = (
        masked.groupby("pos").agg(mean_activity=("mean", "mean")).reset_index()
    )
    full_by_position = (
        singles.groupby("pos").agg(full_mean=("mean", "mean")).reset_index()
    )
    hole_df = pd.DataFrame(
        {"start": [p - 0.5 for p in mask_list], "end": [p + 0.5 for p in mask_list]}
    )
    hole_bands = (
        alt.Chart(hole_df)
        .mark_rect(color=theme.ACTIVE_SITE, opacity=0.18)
        .encode(x="start:Q", x2="end:Q")
    )
    masked_line = (
        alt.Chart(
            by_position, title="The DMS after masking -- red bands are the blind spot"
        )
        .mark_line(point=True, color=theme.PRIMARY)
        .encode(
            x=alt.X("pos:Q", title="Sequence position"),
            y=alt.Y("mean_activity:Q", title="Mean activity at position"),
        )
        .properties(width=860, height=260)
    )
    ghost_line = (
        alt.Chart(full_by_position)
        .mark_line(color=theme.MUTED, strokeDash=[2, 3], opacity=0.5)
        .encode(x="pos:Q", y="full_mean:Q")
    )
    band_md = mo.md(
        f"""
        {len(singles) - len(masked)} measurements vanish. The grey dashed
        line is the truth we are pretending not to know -- watch what the
        red bands are hiding.
        """
    )
    mo.vstack([band_md, masked_line + ghost_line + hole_bands])
    return (masked_line,)


@app.cell(hide_code=True)
def _(mask_list, mo, pd, structure):
    crystal = structure.load_crystal_structure()
    distances = {
        resnum: structure.min_ligand_distance(crystal, resnum)
        for resnum in crystal.observed_resnums
    }
    structure_recovery = pd.DataFrame(
        {
            "position": mask_list,
            "site class": [structure.site_class(distances.get(p)) for p in mask_list],
        }
    )
    mo.vstack(
        [
            mo.md(
                r"""
                ## Recovery attempt 1 -- the crystal structure

                What would the structure alone say about the missing
                positions?
                """
            ),
            structure_recovery,
            mo.md(
                r"""
                Five of six are distal or second-shell -- exactly the
                "nothing special here" annotation that Q2 showed most top
                hits carry. **Structure alone would not have recovered them.**
                """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(alt, mask_list, mo, np, pd, structure, theme):
    crystal_pred = structure.load_crystal_structure()
    predicted = structure.load_predicted_structure()
    aligned, target_coords, shared_resnums = structure.superposed_ca(
        predicted, crystal_pred
    )
    ca_deviation = pd.Series(
        np.sqrt(((aligned - target_coords) ** 2).sum(axis=1)), index=shared_resnums
    )
    dev_df = ca_deviation.reset_index()
    dev_df.columns = ["pos", "deviation"]
    dev_df["masked (KB) position"] = dev_df["pos"].isin(mask_list)
    median_deviation = float(ca_deviation.median())
    dev_chart = (
        alt.Chart(
            dev_df,
            title="Prediction-vs-crystal deviation: mobility as a recovery hint",
        )
        .mark_line(point=True)
        .encode(
            x=alt.X("pos:Q", title="Sequence position"),
            y=alt.Y("deviation:Q", title="C-alpha deviation (A)"),
            color=alt.Color(
                "masked (KB) position:N",
                scale=alt.Scale(
                    domain=[False, True], range=[theme.MUTED, theme.ACTIVE_SITE]
                ),
            ),
            tooltip=["pos", "deviation"],
        )
        .properties(width=860, height=240)
    )
    dev_md = mo.md(
        f"""
        ## Recovery attempt 2 -- structure prediction

        Q4 showed the prediction deviates most around 207-243. Do the masked
        positions stand out in that mobility profile? (Protein-wide median
        deviation: {median_deviation:.2f} A.)
        """
    )
    mo.vstack([dev_md, dev_chart])
    return (dev_chart,)


@app.cell
def _(kb, mask_list, mo, notes):
    kb_recovery_hits = kb.search_notes(notes, "S220T ee improvement combination")
    kb_md = mo.md(
        f"""
        ## Recovery attempt 3 -- the knowledge base

        The mask came *from* the KB, so of course the KB "recovers" these
        positions -- and we should say so plainly: **this is a workflow
        demonstration, not a blind test**. The KB is an independent record
        of what the campaign learned, with a different failure mode than the
        data: it searched here and found {len(kb_recovery_hits)} notes
        naming the winners and their mechanisms.
        """
    )
    mo.vstack([kb_md])
    return


@app.cell(hide_code=True)
def _(data, kb_positions, mask_list, mo, pd, singles):
    ranked = singles.sort_values("mean", ascending=False).reset_index(drop=True)
    rank_of = {mutation: i + 1 for i, mutation in enumerate(ranked["mutation"])}
    score_rows = []
    for pos in mask_list:
        best = singles[singles["pos"] == pos].nlargest(1, "mean").iloc[0]
        score_rows.append(
            {
                "position": pos,
                "best single": best["mutation"],
                "activity": round(best["mean"], 3),
                "rank of 4,720": rank_of[best["mutation"]],
                "KB's named mutation": [
                    m.split(" (")[0] for m in kb_positions[pos] if "gilio" in m
                ][0],
            }
        )
    score_table = mo.ui.table(pd.DataFrame(score_rows), page_size=6, selection=None)
    mo.vstack(
        [
            mo.md(
                r"""
                ## Unmask and score

                What did the hole actually hide?
                """
            ),
            score_table,
        ]
    )
    return (score_table,)


@app.cell
def _(mo):
    mo.callout(
        mo.md(
            r"""
            ### Answer -- Q6

            - **The hole hid the #2 single mutant of the entire campaign**
              (S220T, rank 2 of 4,720) plus two more top-25 hits (A156G at
              23, Y177W at 25). A silent gap in a library is not a neutral
              event.
            - **Structure alone would not have recovered them.** **Prediction
              gives a real partial signal** (S220 at 4.2 A deviation, Q194 at
              2.7). **The KB recovers all six -- by construction**, and the
              circularity is the honest caveat.
            - **The reverse case is the counterweight:** A296I -- the #1
              single mutant -- is absent from the KB. Data finds what
              literature lacks; literature recovers what data loses.
            """
        ),
        kind="success",
    )
    return


@app.cell
def _(mo, theme):
    mo.md(
        f"""
        <div style="background:linear-gradient(135deg, {theme.PRIMARY} 0%, #134e4a 100%);
                    border-radius:16px; padding:26px 30px; color:white;">
        <div style="font-size:12px; letter-spacing:2px; opacity:0.85;
                    text-transform:uppercase;">The overarching question, answered</div>
        <h2 style="margin:10px 0 8px 0; font-size:22px; line-height:1.3;">
        Where do activity-improving mutations of IRED-88 come from -- and
        could we have seen them coming?</h2>
        <div style="font-size:14px; line-height:1.55; opacity:0.95;">
        Mostly <b>not from the active site</b>: they come from distal
        positions, a mobile loop (207-243), and the termini -- tuning access,
        dynamics, and stability rather than chemistry. Could we have seen
        them coming? <b>The DMS finds them</b> (including hits the literature
        never interpreted), <b>the structure filters the naive "mutate the
        active site" prior</b>, <b>the KB explains the leads and recovers
        what a data gap would erase</b>, and <b>prediction extends the
        structure into its blind spots with an honesty score attached</b>.
        No single modality answers the question -- the copilot move is the
        round-trip between all four. In one repo. In six notebooks. In one
        session.</div>
        </div>

        <div style="font-size:12px; color:{theme.MUTED}; margin-top:14px;">
        Built for the "AI as a Research Co-Pilot" course (UMass Chan Medical
        School). Data: supporting information of Ma et al., <i>ACS Catal.</i>
        2021, DOI 10.1021/acscatal.1c02786. Notebooks written with AI
        assistance (Claude + Codex, via the pi harness); every claim traces
        to a cell, a file in this repo, or a KB note.</div>
        """
    )
    return


if __name__ == "__main__":
    app.run()
