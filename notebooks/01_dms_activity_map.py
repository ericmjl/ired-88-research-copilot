import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import altair as alt
    import marimo as mo
    import pandas as pd

    return alt, mo, pd


@app.cell
def _(mo):
    mo.md(
        r"""
        # Q1 -- Which single mutations improve IRED-88's activity?

        The deep mutational scan measured nearly all of the ~6,000 possible
        single mutants of the 304-residue enzyme. `mean` is the batch-adjusted
        activity from the paper's supporting information (SI-002); `count` is
        how many times that mutant was measured across plates.
        """
    )
    return


@app.cell
def _(data):
    singles = data.extract_single_mutants(data.load_si002())
    si002 = data.load_si002()
    wt_row = si002[si002["mutation"].isna()]
    wt_mean = float(wt_row["mean"].iloc[0])
    wt_n = int(wt_row["count"].iloc[0])
    return singles, wt_mean, wt_n


@app.cell
def _(data):
    from ired_88_research_copilot import data

    return (data,)


@app.cell
def _(mo, singles, wt_mean, wt_n):
    mo.md(
        f"""
        **The reference point.** The wild-type reference row
        (n = {wt_n:,} measurements spread across plates) has mean activity
        **{wt_mean:.3f}**. The median single mutant scores
        **{singles["mean"].median():.3f}** -- most mutations hurt, which is
        exactly what you expect from a folded enzyme.
        """
    )
    return


@app.cell
def _(alt, singles):
    heatmap = (
        alt.Chart(singles, title="Deep mutational scan of IRED-88 (activity)")
        .mark_rect()
        .encode(
            x=alt.X("pos:O", title="Sequence position"),
            y=alt.Y("mut_aa:O", title="Mutant residue", sort="descending"),
            color=alt.Color(
                "mean:Q",
                title="Activity (mean)",
                scale=alt.Scale(scheme="viridis"),
            ),
            tooltip=["mutation", "mean", "count"],
        )
        .properties(width=900, height=330)
    )
    heatmap
    return (heatmap,)


@app.cell
def _(alt, singles, wt_mean):
    top15 = singles.nlargest(15, "mean")
    top_chart = (
        alt.Chart(top15, title=f"Top 15 single mutants (WT reference = {wt_mean:.3f})")
        .mark_bar()
        .encode(
            x=alt.X("mutation:N", sort="-y", title="Mutation"),
            y=alt.Y("mean:Q", title="Activity (mean)"),
            color=alt.value("#4c78a8"),
            tooltip=["mutation", "mean", "count"],
        )
        .properties(width=700, height=280)
    )
    top_chart
    return (top15, top_chart)


@app.cell
def _(alt, pd, singles):
    by_position = (
        singles.groupby("pos")
        .agg(mean_activity=("mean", "mean"), n=("mutation", "count"))
        .reset_index()
    )
    position_chart = (
        alt.Chart(by_position, title="Per-position mean activity")
        .mark_line(point=True)
        .encode(
            x=alt.X("pos:Q", title="Sequence position"),
            y=alt.Y("mean_activity:Q", title="Mean activity at position"),
            tooltip=["pos", "mean_activity", "n"],
        )
        .properties(width=900, height=260)
    )
    boundaries = pd.DataFrame(
        {"pos": [12, 301], "label": ["first resolved", "last resolved"]}
    )
    rules = (
        alt.Chart(boundaries)
        .mark_rule(color="gray", strokeDash=[4, 4])
        .encode(x="pos:Q", tooltip=["label:N"])
    )
    position_chart + rules
    return (by_position, position_chart, rules)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Answer to Q1

        - The two strongest single mutants are **A296I** (mean 0.712,
          measured 7 times) and **S220T** (mean 0.678, measured 685 times --
          it was clearly re-measured heavily as the lead hit). Both beat the
          median mutant by >20x.
        - Beneficial positions are **scattered across the whole sequence**:
          hot positions appear near the N-terminus (6, 26, 57), mid-sequence
          (154-177, 212, 218-220, 243-247), and at the very C-terminal end
          (296, 302-304).
        - Positions 302-304 -- the last three residues of the protein -- have
          mean activities of 0.126 / 0.177 / 0.170, several-fold above the
          0.031 median. Remember that: the next notebook shows what the
          crystal structure can and cannot see.
        """
    )
    return


if __name__ == "__main__":
    app.run()
