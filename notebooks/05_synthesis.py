import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import altair as alt
    import marimo as mo
    import pandas as pd

    from ired_88_research_copilot import data, kb, structure

    return alt, data, kb, mo, pd, structure


@app.cell
def _(mo):
    mo.md(
        r"""
        # Q5 -- What should we mutate next? (and what did we learn?)

        Everything converges here: the DMS ranking, the structural context,
        the knowledge base's mechanistic reading, and the prediction's
        blind-spot check -- plus the enantioselectivity table (SI-003),
        which records how every strategy (DMS, epPCR rounds 1-3, ML,
        structure-guided mutagenesis, Low-N) actually performed.
        """
    )
    return


@app.cell
def _(data, kb, structure):
    singles = data.extract_single_mutants(data.load_si002())
    notes = kb.load_all_notes()
    crystal = structure.load_crystal_structure()
    distances = {
        resnum: structure.min_ligand_distance(crystal, resnum)
        for resnum in crystal.observed_resnums
    }

    kb_evidence = {
        "S220T": "Gilio 2022: mouth of active-site cleft; ee 30% -> 96%",
        "A296I": "none -- open question",
    }
    shortlist = singles.nlargest(12, "mean").copy()
    shortlist["site_class"] = shortlist["pos"].map(
        lambda p: structure.site_class(distances.get(p))
    )
    shortlist["kb_evidence"] = shortlist["mutation"].map(
        lambda m: kb_evidence.get(m, "none (unstudied)")
    )
    shortlist_table = shortlist[
        ["mutation", "pos", "mean", "count", "site_class", "kb_evidence"]
    ]
    return distances, notes, shortlist_table, singles


@app.cell
def _(mo, shortlist_table):
    mo.md(
        r"""
        ## The annotated shortlist

        Ranking alone would say "mutate everything". The annotations change
        the ranking's meaning: S220T is literature-validated; A296I is
        unexplored territory; nothing at the very top touches the active
        site itself.
        """
    )
    shortlist_table
    return


@app.cell
def _(data):
    si003 = data.load_si003()
    return (si003,)


@app.cell
def _(alt, mo, si003):
    strategy_chart = (
        alt.Chart(
            si003,
            title="Every engineered variant: conversion vs. R-enantiomeric excess",
        )
        .mark_circle(size=70, opacity=0.8)
        .encode(
            x=alt.X(
                "ratio:Q", title="Fractional conversion", scale=alt.Scale(domain=[0, 1])
            ),
            y=alt.Y(
                "r_enantiomeric_excess:Q",
                title="R-enantiomeric excess",
                scale=alt.Scale(domain=[0, 1]),
            ),
            color=alt.Color("experiment:N", title="Strategy"),
            tooltip=["mutation", "experiment", "ratio", "r_enantiomeric_excess"],
        )
        .properties(width=750, height=420)
    )
    mo.md(
        r"""
        ## The strategy scoreboard

        Each dot is a variant; color is the strategy that produced it. The
        story of the paper, visible in one plot: DMS (dark blue) found the
        S220T starting point at moderate ee; epPCR rounds climbed ee toward
        1.0; ML and structure-guided rounds pushed conversion upward.
        """
    )
    strategy_chart
    return (strategy_chart,)


@app.cell
def _(mo, pd, si003):
    winner = si003[si003["mutation"] == "Q194L; S220T; H230Y"]
    winner_row = winner.iloc[0]
    eppcr3 = si003[si003["experiment"] == "EPPCR3"]
    best_conv = eppcr3.nlargest(3, "ratio")[
        ["mutation", "ratio", "r_enantiomeric_excess"]
    ]
    mo.md(
        f"""
        The KB's named winner, **Q194L/S220T/H230Y** (epPCR round 3 on the
        S220T backbone), is in the table with ee
        **{winner_row["r_enantiomeric_excess"]:.3f}** and conversion
        **{winner_row["ratio"]:.3f}** -- the variant the paper took to
        gram-scale synthesis of the drug ZPL389 (72% yield, >99% ee).

        Top-conversion EPPCR3 variants for comparison:

        {best_conv.to_string(index=False)}
        """
    )
    return (winner_row,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Answer to the overarching question

        > **Where do activity-improving mutations of IRED-88 come from -- and
        > could we have seen them coming?**

        **Where they come from:** mostly *not* the active site. The top-50
        positions contain zero residues within 6 A of the NADP cofactor;
        improvements come from distal positions, a mobile loop (207-243),
        and the protein's termini -- places that tune access, dynamics, and
        stability rather than chemistry directly.

        **Could we have seen them coming?**

        - The **DMS data alone** flags the positions -- including termini the
          crystal cannot resolve. Data beats structure for *discovery*.
        - The **structure** filters the mechanism: it kills the naive
          "mutate the active site" prior and flags S220's cleft-mouth
          position (which pure distance-to-cofactor mislabels as irrelevant).
        - The **knowledge base** explains the lead (S220T raises ee by
          blocking the wrong conformer), supplies the additivity caveat, and
          hands us the engineered winner -- but is silent on A296I.
        - The **prediction** extends the structure into its blind spots with
          a confidence score, and honestly declines to over-explain the
          low-confidence tail.

        No single modality answers the question. The copilot move is the
        *quick round-trip between all four* -- in one repo, in five
        notebooks, in one session.
        """
    )
    return


if __name__ == "__main__":
    app.run()
