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


@app.cell
def _(mo, theme):
    mo.md(
        f"""
        <span style="background:{theme.PRIMARY};color:white;padding:3px 12px;
        border-radius:12px;font-size:12px;font-weight:600">Q1 / 6 · THE DATA</span>

        # Which single mutations improve IRED-88?

        The deep mutational scan measured nearly all ~6,000 possible single
        mutants of the 304-residue enzyme. `mean` is the batch-adjusted
        activity (paper SI-002); `count` is how many times that mutant was
        measured across plates.
        """
    )
    return


@app.cell
def _(data, structure):
    singles = data.extract_single_mutants(data.load_si002())
    si002 = data.load_si002()
    wt_mean = float(si002[si002["mutation"].isna()]["mean"].iloc[0])
    wt_n = int(si002[si002["mutation"].isna()]["count"].iloc[0])
    median_mean = float(singles["mean"].median())
    best = singles.nlargest(1, "mean").iloc[0]
    crystal = structure.load_crystal_structure()
    distances = {
        resnum: structure.min_ligand_distance(crystal, resnum)
        for resnum in crystal.observed_resnums
    }
    return best, distances, median_mean, singles, wt_mean, wt_n


@app.cell
def _(best, median_mean, mo, wt_mean, wt_n):
    stat_row = mo.hstack(
        [
            mo.stat(
                value=f"{wt_mean:.3f}",
                label="wild type",
                caption=f"reference row, n={wt_n:,}",
            ),
            mo.stat(
                value=f"{median_mean:.3f}", label="median mutant", caption="most hurt"
            ),
            mo.stat(
                value=f"{best['mean']:.3f}",
                label=f"best mutant ({best['mutation']})",
                caption="21x the median",
            ),
        ],
        justify="space-between",
    )
    stat_row
    return (stat_row,)


@app.cell(hide_code=True)
def _(alt, mo, singles):
    heatmap = (
        alt.Chart(
            singles,
            title="The deep mutational scan: activity of every measured single mutant",
        )
        .mark_rect()
        .encode(
            x=alt.X("pos:O", title="Sequence position").axis(labels=False, ticks=False),
            y=alt.Y("mut_aa:O", title="Mutant residue", sort="descending"),
            color=alt.Color(
                "mean:Q",
                title="Activity",
                scale=alt.Scale(scheme="viridis"),
                legend=alt.Legend(orient="left"),
            ),
            tooltip=[alt.Tooltip("mutation", title="Mutant"), "mean", "count"],
        )
        .properties(width=860, height=340)
    )
    mo.vstack([heatmap])
    return (heatmap,)


@app.cell(hide_code=True)
def _(alt, singles, theme, wt_mean):
    top15 = singles.nlargest(15, "mean")
    top_chart = (
        alt.Chart(
            top15, title=f"Top 15 single mutants -- wild type sits at {wt_mean:.3f}"
        )
        .mark_bar()
        .encode(
            x=alt.X("mutation:N", sort="-y", title=None),
            y=alt.Y("mean:Q", title="Activity"),
            color=alt.condition(
                "datum.mean > 0.6", alt.value(theme.PRIMARY), alt.value("#9fb8c8")
            ),
            tooltip=["mutation", "mean", "count"],
        )
        .properties(width=720, height=260)
    )
    top_chart
    return (top_chart, top15)


@app.cell(hide_code=True)
def _(alt, mo, pd, singles, theme):
    by_position = (
        singles.groupby("pos")
        .agg(mean_activity=("mean", "mean"), n=("mutation", "count"))
        .reset_index()
    )
    boundary_df = pd.DataFrame(
        {
            "pos": [12, 301],
            "label": ["first residue in crystal", "last residue in crystal"],
        }
    )
    position_chart = (
        alt.Chart(
            by_position,
            title="Per-position mean activity -- note the peaks at both ends",
        )
        .mark_line(point=True, color=theme.PRIMARY)
        .encode(
            x=alt.X("pos:Q", title="Sequence position"),
            y=alt.Y("mean_activity:Q", title="Mean activity at position"),
            tooltip=["pos", "mean_activity", "n"],
        )
        .properties(width=860, height=240)
    )
    boundaries = (
        alt.Chart(boundary_df)
        .mark_rule(color=theme.MUTED, strokeDash=[5, 4])
        .encode(x="pos:Q", tooltip=["label:N"])
    )
    mo.vstack([position_chart + boundaries])
    return (position_chart,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Explore it yourself

        Drag through positions and watch the 19 possible mutations at each.
        Try position **220** -- the DMS's most-replicated lead -- and
        position **296**, buried in the tail the crystal cannot see.
        """
    )
    return


@app.cell
def _(mo):
    position_slider = mo.ui.slider(
        start=2, stop=304, value=220, label="Sequence position", show_value=True
    )
    position_slider
    return (position_slider,)


@app.cell(hide_code=True)
def _(alt, distances, mo, position_slider, singles, structure, theme):
    pos_selected = position_slider.value
    at_position = singles[singles["pos"] == pos_selected].sort_values("mut_aa")
    explorer_chart = (
        alt.Chart(
            at_position,
            title=f"Position {pos_selected}: activity of each mutant residue",
        )
        .mark_bar()
        .encode(
            x=alt.X("mut_aa:N", title="Mutant residue", sort=None),
            y=alt.Y("mean:Q", title="Activity", scale=alt.Scale(domain=[0, 0.8])),
            color=alt.Color(
                "mean:Q",
                scale=alt.Scale(scheme="viridis"),
                legend=None,
            ),
            tooltip=["mutation", "mean", "count"],
        )
        .properties(width=640, height=240)
    )
    explorer_note = mo.callout(
        mo.md(
            f"""
            Position {pos_selected} is
            **{structure.site_class(distances.get(pos_selected))}** in the
            crystal structure. Best mutation here:
            **{at_position.nlargest(1, "mean")["mutation"].iloc[0]}**
            (mean {at_position["mean"].max():.3f}).
            """
        ),
        kind="neutral",
    )
    mo.vstack([explorer_note, explorer_chart])
    return (explorer_chart,)


@app.cell
def _(mo):
    mo.callout(
        mo.md(
            r"""
            ### Answer -- Q1

            - The two strongest single mutants are **A296I** (mean 0.712,
              measured 7 times) and **S220T** (mean 0.678, measured **685**
              times -- clearly re-measured heavily as the lead hit). Both
              beat the median mutant by >20x.
            - Beneficial positions are **scattered across the whole
              sequence**: near the N-terminus (6, 26, 57), mid-sequence
              (154-177, 212, 218-220, 243-247), and at the very C-terminal
              end (296, 302-304).
            - Positions **302-304** -- the last three residues -- average
              0.126 / 0.177 / 0.170 against a 0.031 median. Remember them:
              Q2 shows what the crystal structure cannot see there.
            """
        ),
        kind="success",
    )
    return


if __name__ == "__main__":
    app.run()
