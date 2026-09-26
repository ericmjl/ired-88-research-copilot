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


@app.cell
def _(mo):
    mo.md(
        r"""
        # Q6 -- If the DMS had a hole where the literature matters, would we have noticed?

        Saturation-mutagenesis libraries always have gaps: some oligo pools
        fail, some positions never clone. So let's **intentionally punch a
        hole** in the DMS data -- at exactly the positions the knowledge
        base talks about -- and ask whether the other three modalities
        (structure, prediction, KB) could nominate what the data lost.

        The twist to watch for: the mask itself is **derived from the KB
        programmatically** -- we read the mutation tokens out of the notes,
        no hardcoding.
        """
    )
    return


@app.cell
def _(data, kb):
    notes = kb.load_all_notes()
    kb_positions = kb.extract_mutation_positions(notes)
    mask_positions_list = sorted(kb_positions)
    singles = data.extract_single_mutants(data.load_si002())
    masked = data.mask_positions(singles, mask_positions_list)
    return kb_positions, mask_positions_list, masked, notes, singles


@app.cell
def _(kb_positions, mo, pd):
    mention_df = pd.DataFrame(
        [
            {"position": pos, "mentions": "; ".join(mentions)}
            for pos, mentions in kb_positions.items()
        ]
    )
    mo.vstack(
        [
            mo.md(
                f"""
                ## The mask, extracted from the knowledge base

                Scanning the six notes for `S220T`-style tokens (including
                tokens inside combination strings) yields
                **{len(kb_positions)} positions**: the KB's cast of
                characters, no hardcoding.
                """
            ),
            mention_df,
        ]
    )
    return (mention_df,)


@app.cell
def _(alt, mask_positions_list, masked, mo, pd):
    by_position = (
        masked.groupby("pos").agg(mean_activity=("mean", "mean")).reset_index()
    )
    hole_df = pd.DataFrame({"pos": mask_positions_list})
    band = alt.Chart(hole_df).mark_rect(color="red", opacity=0.25).encode(x="pos:Q")
    masked_line = (
        alt.Chart(by_position, title="DMS after masking the KB-annotated positions")
        .mark_line(point=True)
        .encode(
            x=alt.X("pos:Q", title="Sequence position"),
            y=alt.Y("mean_activity:Q", title="Mean activity at position"),
        )
        .properties(width=900, height=260)
    )
    mo.vstack(
        [
            mo.md(
                """
                ## The data, with the hole punched in

                We removed every measurement at the masked positions. The
                red bands are the blind spot. Everything the demos before
                this one celebrated about the DMS is still there -- except
                the literature's favourite positions.
                """
            ),
            masked_line + band,
        ]
    )
    return (masked_line,)


@app.cell
def _(data, mask_positions_list, mo, pd, structure):
    crystal = structure.load_crystal_structure()
    distances = {
        resnum: structure.min_ligand_distance(crystal, resnum)
        for resnum in crystal.observed_resnums
    }
    recovery_structure = pd.DataFrame(
        {
            "position": mask_positions_list,
            "resolved_in_crystal": [p in distances for p in mask_positions_list],
            "site_class": [
                structure.site_class(distances.get(p)) for p in mask_positions_list
            ],
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
            recovery_structure,
        ]
    )
    return (recovery_structure,)


@app.cell
def _(alt, mask_positions_list, mo, np, pd, structure):
    crystal_pred = structure.load_crystal_structure()
    predicted = structure.load_predicted_structure()
    aligned, target, resnums = structure.superposed_ca(predicted, crystal_pred)
    deviation = pd.Series(np.sqrt(((aligned - target) ** 2).sum(axis=1)), index=resnums)
    dev_df = deviation.reset_index()
    dev_df.columns = ["pos", "deviation"]
    dev_df["kb_position"] = dev_df["pos"].isin(mask_positions_list)
    median_deviation = float(deviation.median())
    dev_chart = (
        alt.Chart(dev_df, title="Prediction-vs-crystal deviation (mobility hint)")
        .mark_line(point=True)
        .encode(
            x=alt.X("pos:Q", title="Sequence position"),
            y=alt.Y("deviation:Q", title="C-alpha deviation (A)"),
            color=alt.Color("kb_position:N", title="Masked (KB) position"),
            tooltip=["pos", "deviation"],
        )
        .properties(width=900, height=260)
    )
    mo.vstack(
        [
            mo.md(
                f"""
                ## Recovery attempt 2 -- structure prediction

                Q4 showed the prediction deviates most from the crystal
                around positions 207-243. Do the masked positions stand out
                in that mobility profile? (Median deviation across the
                protein: {median_deviation:.2f} A.)
                """
            ),
            dev_chart,
        ]
    )
    return (dev_chart, dev_df, median_deviation)


@app.cell
def _(kb, mo, notes):
    hits = kb.search_notes(notes, "activity ee improvement mutation variant")
    hits_blocks = [
        mo.md(
            f"**{note.citation}**\n\n> {kb.snippet_for(note, 'S220T ee improvement')}"
        )
        for note, _ in hits[:2]
    ]
    mo.md(
        r"""
        ## Recovery attempt 3 -- the knowledge base

        The mask came *from* the KB, so of course the KB "recovers" these
        positions -- that circularity is the point, and we will say so
        plainly in the answer. The KB is an independent record of what the
        campaign learned, with a different failure mode than the data.
        """
    )
    mo.vstack(hits_blocks)
    return (hits,)


@app.cell
def _(data, kb_positions, mask_positions_list, mo, pd, singles):
    ranked = singles.sort_values("mean", ascending=False).reset_index(drop=True)
    rank_of = {mutation: i + 1 for i, mutation in enumerate(ranked["mutation"])}
    score_rows = []
    for pos in mask_positions_list:
        best = singles[singles["pos"] == pos].nlargest(1, "mean").iloc[0]
        score_rows.append(
            {
                "position": pos,
                "best_single": best["mutation"],
                "activity": round(best["mean"], 3),
                "rank_of_4720": rank_of[best["mutation"]],
                "kb_named": [
                    m.split(" (")[0] for m in kb_positions[pos] if "gilio" in m
                ][0],
            }
        )
    score_df = pd.DataFrame(score_rows)
    mo.vstack(
        [
            mo.md(
                r"""
                ## Unmask and score

                What did the hole actually hide? Here is the best single
                mutant at each masked position, its rank among all 4,720
                single mutants, and the exact mutation the KB names at that
                position.
                """
            ),
            score_df,
        ]
    )
    return (score_df,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Answer to Q6

        - **The hole hid the #2 single mutant of the entire campaign**
          (S220T, rank 2 of 4,720), plus two more top-25 hits (A156G at 23,
          Y177W at 25). A silent gap in a library is not a neutral event.
        - **The structure alone would not have recovered them**: five of six
          masked positions are distal or second-shell -- exactly the "nothing
          special here" annotation that Q2 showed most top hits carry.
        - **Prediction gives a real partial signal**: S220 (4.2 A) and Q194
          (2.7 A) stand out of the mobility profile, H230 mildly (2.3 A);
          the rest are unremarkable. Interesting, but it takes the KB to
          connect mobility to "mutate here".
        - **The KB recovers all six -- by construction**, and we should be
          upfront that this is a workflow demonstration, not a blind test:
          the mask was derived from the KB, so "recovery" is built in. What
          the demo genuinely shows is the *division of labour*: the KB
          carries knowledge the data lost; the data carries hits the KB
          never heard of.
        - **The reverse case is the honest counterweight**: A296I -- the #1
          single mutant of the campaign -- is absent from the KB. Data finds
          what literature lacks; literature recovers what data loses. A
          research copilot needs both, and the quick round-trip between
          them.

        ## The overarching question, answered

        > **Where do activity-improving mutations of IRED-88 come from --
        > and could we have seen them coming?**

        Mostly **not from the active site**: they come from distal
        positions, a mobile loop (207-243), and the termini, acting through
        access, dynamics, and stability rather than chemistry. Could we
        have seen them coming? **The DMS finds them** (including hits the
        literature never interpreted), **structure filters the naive
        "mutate the active site" prior**, **the KB explains the leads and
        recovers what a data gap would erase**, and **prediction extends
        the structure into its blind spots with an honesty score
        attached**. No single modality answers the question; the copilot
        move is the round-trip between all four -- in one repo, in six
        notebooks, in one session.
        """
    )
    return


if __name__ == "__main__":
    app.run()
