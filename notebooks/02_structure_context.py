import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import altair as alt
    import marimo as mo
    import pandas as pd

    from ired_88_research_copilot import data, structure

    return alt, data, mo, pd, structure


@app.cell
def _(mo):
    mo.md(
        r"""
        # Q2 -- Are the beneficial positions where the structure says they should be?

        A structure turns a list of positions into *mechanism*. We have the
        IRED-88 crystal structure (PDB **7OG3**, 1.9 A, with the NADP
        cofactor bound). The key question for enzyme engineering: do the
        activity-improving mutations cluster at the active site, near it, or
        far away from it?

        **A number detail that matters here:** 7OG3's ATOM records are
        numbered by the wild-type protein sequence, so PDB residue number =
        DMS position. The crystal resolves positions **12-301**; positions
        **1-11** and **302-304** are disordered and have no coordinates.
        """
    )
    return


@app.cell
def _(data, structure):
    crystal = structure.load_crystal_structure()
    distances = {
        resnum: structure.min_ligand_distance(crystal, resnum)
        for resnum in crystal.observed_resnums
    }
    singles = data.extract_single_mutants(data.load_si002())
    by_position = (
        singles.groupby("pos").agg(mean_activity=("mean", "mean")).reset_index()
    )
    by_position["site_class"] = by_position["pos"].map(
        lambda p: structure.site_class(distances.get(p))
    )
    return by_position, crystal, distances, singles


@app.cell
def _(alt, by_position, mo):
    class_colors = {
        "active_site": "#d62728",
        "second_shell": "#ff7f0e",
        "distal": "#4c78a8",
        "unresolved": "#bbbbbb",
    }
    class_chart = (
        alt.Chart(
            by_position, title="Per-position mean activity, colored by distance to NADP"
        )
        .mark_bar(size=3)
        .encode(
            x=alt.X("pos:Q", title="Sequence position"),
            y=alt.Y("mean_activity:Q", title="Mean activity at position"),
            color=alt.Color(
                "site_class:N",
                sort=["active_site", "second_shell", "distal", "unresolved"],
                scale=alt.Scale(domain=list(class_colors), range=list(class_colors)),
                title="Site class",
            ),
            tooltip=["pos", "mean_activity", "site_class"],
        )
        .properties(width=900, height=280)
    )
    mo.vstack(
        [
            mo.md(
                r"""
                Red = within 6 A of the cofactor (active site), orange = 6-12 A
                (second shell), blue = >12 A (distal), grey = no coordinates.
                """
            ),
            class_chart,
        ]
    )
    return (class_chart, class_colors)


@app.cell
def _(distances, mo, singles, structure):
    top15 = singles.nlargest(15, "mean").copy()
    top15["resnum"] = top15["pos"].map(structure.dms_position_to_resnum)
    top15["site_class"] = top15["pos"].map(lambda p: structure.site_class(distances[p]))
    top15["in_crystal"] = top15["pos"].map(lambda p: p in distances)
    top_table = top15[["mutation", "pos", "mean", "count", "site_class", "in_crystal"]]
    mo.vstack([mo.md(r"""## The top 15, annotated"""), top_table])
    return (top_table,)


@app.cell
def _(alt, by_position, mo, pd):
    top50 = set(by_position.nlargest(50, "mean_activity")["pos"])
    all_classes = by_position["site_class"].value_counts().rename("all_positions")
    top_classes = (
        by_position[by_position["pos"].isin(top50)]["site_class"]
        .value_counts()
        .rename("top_50_positions")
    )
    class_df = pd.concat([all_classes, top_classes], axis=1).fillna(0).astype(int)
    class_long = class_df.reset_index().melt(
        "site_class", var_name="group", value_name="n"
    )
    enrichment_chart = (
        alt.Chart(
            class_long, title="Where the top-50 positions sit (vs. all positions)"
        )
        .mark_bar()
        .encode(
            x=alt.X("group:N", title=None),
            y=alt.Y("n:Q", title="Number of positions"),
            color=alt.Color("site_class:N", title="Site class"),
            xOffset="site_class:N",
            tooltip=["group", "site_class", "n"],
        )
        .properties(width=500, height=280)
    )
    mo.vstack(
        [
            mo.md(
                r"""
                ## The enrichment test

                If activity improvements came from active-site chemistry, the
                top-50 positions should be red. They are not: **zero of the
                top 50** are active-site positions. The improvement signal
                lives in distal positions and in the grey band the crystal
                cannot see.
                """
            ),
            enrichment_chart,
        ]
    )
    return (enrichment_chart, top50)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Answer to Q2

        - **None of the top-50 positions are within 6 A of the NADP
          cofactor**; only 8 are in the 6-12 A second shell. The rest are
          distal (32) or invisible to the crystal (10 of the 13 unresolved
          positions land in the top 50!).
        - The famous lead **S220T** sits >12 A from the cofactor by atom
          distance -- yet the literature (next notebook) calls it "the mouth
          of the active site cleft". Distance-to-cofactor is not
          distance-to-substrate: the *substrate* binds in a cleft whose
          entrance S220 guards.
        - The top hit **A296I** is resolved in the crystal (position 296),
          but positions 302-304 -- also hot -- have no coordinates at all.
        - Enzyme-engineering implication (backed by the Ma et al. 2021
          analysis): beneficial mutations are often **distal**, acting
          through dynamics, stability, or access paths rather than direct
          chemistry.
        """
    )
    return


if __name__ == "__main__":
    app.run()
