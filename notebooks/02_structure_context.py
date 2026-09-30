import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import altair as alt
    import marimo as mo
    import pandas as pd

    from ired_88_research_copilot import data, structure, theme

    theme.apply()
    return alt, data, mo, pd, structure, theme


@app.cell(hide_code=True)
def _(mo, theme):
    mo.md(
        f"""
        <span style="background:{theme.DISTAL};color:white;padding:3px 12px;
        border-radius:12px;font-size:12px;font-weight:600">Q2 / 6 · THE STRUCTURE</span>

        # Are the hits where the structure says they should be?

        A structure turns a list of positions into *mechanism*. We have the
        IRED-88 crystal structure (PDB **7OG3**, 1.9 A, NADP cofactor bound).
        The question for enzyme engineering: do the activity-improving
        mutations cluster at the active site, near it, or far away?
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **A numbering detail that matters here:** 7OG3's ATOM records are
        numbered by the wild-type protein sequence, so PDB residue number =
        DMS position. The crystal resolves positions **12-301**; positions
        **1-11** and **302-304** are disordered and have no coordinates.
        Every distance below is measured in the protein's coordinate frame
        to the bound NADP cofactor.
        """
    )
    return


@app.cell
def _(data, structure):
    crystal = structure.load_crystal_structure()
    ligand_distances = {
        resnum: structure.min_ligand_distance(crystal, resnum)
        for resnum in crystal.observed_resnums
    }
    singles = data.extract_single_mutants(data.load_si002())
    by_position = (
        singles.groupby("pos").agg(mean_activity=("mean", "mean")).reset_index()
    )
    by_position["site_class"] = by_position["pos"].map(
        lambda p: structure.site_class(ligand_distances.get(p))
    )
    return by_position, ligand_distances, singles


@app.cell(hide_code=True)
def _(alt, by_position, mo, theme):
    class_colors = [
        theme.ACTIVE_SITE,
        theme.SECOND_SHELL,
        theme.DISTAL,
        theme.UNRESOLVED,
    ]
    class_chart = (
        alt.Chart(
            by_position,
            title="Per-position mean activity, colored by distance to the NADP cofactor",
        )
        .mark_bar(size=3)
        .encode(
            x=alt.X("pos:Q", title="Sequence position"),
            y=alt.Y("mean_activity:Q", title="Mean activity at position"),
            color=alt.Color(
                "site_class:N",
                sort=theme.SITE_CLASS_ORDER,
                scale=alt.Scale(domain=theme.SITE_CLASS_ORDER, range=class_colors),
                title="Site class",
            ),
            tooltip=["pos", "mean_activity", "site_class"],
        )
        .properties(width=860, height=280)
    )
    legend_note = mo.md(
        r"""
        <span style="color:{red};font-weight:600">red</span> = active site
        (&lt; 6 A) · <span style="color:{amber};font-weight:600">amber</span> =
        second shell (6-12 A) ·
        <span style="color:{blue};font-weight:600">blue</span> = distal
        (&gt; 12 A) · <span style="color:{grey};font-weight:600">grey</span> =
        no coordinates
        """.format(
            red=theme.ACTIVE_SITE,
            amber=theme.SECOND_SHELL,
            blue=theme.DISTAL,
            grey=theme.UNRESOLVED,
        )
    )
    mo.vstack([legend_note, class_chart])
    return (class_chart,)


@app.cell(hide_code=True)
def _(ligand_distances, mo, singles, structure):
    top15 = singles.nlargest(15, "mean").copy()
    top15["site class"] = top15["pos"].map(
        lambda p: structure.site_class(ligand_distances.get(p))
    )
    top15["in crystal"] = top15["pos"].map(lambda p: p in ligand_distances)
    top_table = mo.ui.table(
        top15[["mutation", "pos", "mean", "count", "site class", "in crystal"]],
        page_size=15,
        selection=None,
    )
    annotated_md = mo.md(r"""## The top 15, annotated""")
    mo.vstack([annotated_md, top_table])
    return (top_table,)


@app.cell(hide_code=True)
def _(alt, by_position, mo, pd, theme):
    top50 = set(by_position.nlargest(50, "mean_activity")["pos"])
    all_classes = by_position["site_class"].value_counts().rename("all positions")
    top_classes = (
        by_position[by_position["pos"].isin(top50)]["site_class"]
        .value_counts()
        .rename("top 50 positions")
    )
    class_df = pd.concat([all_classes, top_classes], axis=1).fillna(0).astype(int)
    class_long = class_df.reset_index().melt(
        "site_class", var_name="group", value_name="n"
    )
    enrichment_chart = (
        alt.Chart(
            class_long, title="Where the top-50 positions sit, against all positions"
        )
        .mark_bar()
        .encode(
            x=alt.X("group:N", title=None, sort=["all positions", "top 50 positions"]),
            y=alt.Y("n:Q", title="Number of positions"),
            color=alt.Color(
                "site_class:N",
                sort=theme.SITE_CLASS_ORDER,
                scale=alt.Scale(
                    domain=theme.SITE_CLASS_ORDER,
                    range=[
                        theme.ACTIVE_SITE,
                        theme.SECOND_SHELL,
                        theme.DISTAL,
                        theme.UNRESOLVED,
                    ],
                ),
                title="Site class",
            ),
            xOffset="site_class:N",
            tooltip=["group", "site_class", "n"],
        )
        .properties(width=520, height=300)
    )
    enrichment_md = mo.md(
        r"""
        ## The enrichment test

        If activity improvements came from active-site chemistry, the top-50
        positions should be red. They are not: **zero of the top 50** are
        active-site positions. The improvement signal lives in distal
        positions -- and in the grey band the crystal cannot see.
        """
    )
    mo.vstack([enrichment_md, enrichment_chart])
    return (enrichment_chart,)


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        mo.md(
            r"""
            ### Answer -- Q2

            - **None of the top-50 positions are within 6 A of the NADP
              cofactor**; only 8 sit in the 6-12 A second shell. The rest are
              distal (32) or invisible to the crystal -- **10 of the 13
              unresolved positions land in the top 50**.
            - The famous lead **S220T** sits >12 A from the cofactor by atom
              distance, yet the literature calls it "the mouth of the active
              site cleft". Distance-to-cofactor is not distance-to-substrate:
              the *substrate* binds in a cleft whose entrance S220 guards.
            - The top hit **A296I** is resolved (position 296), but hot
              positions **302-304** have no coordinates at all.
            - Engineering implication: beneficial mutations act through
              **access, dynamics, and stability** -- not direct chemistry.
            """
        ),
        kind="success",
    )
    return


if __name__ == "__main__":
    app.run()
