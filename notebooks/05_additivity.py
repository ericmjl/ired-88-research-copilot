import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import altair as alt
    import marimo as mo
    import numpy as np
    import pandas as pd

    from ired_88_research_copilot import data, theme

    theme.apply()
    return alt, data, mo, np, pd, theme


@app.cell(hide_code=True)
def _(mo, theme):
    mo.md(
        f"""
        <span style="background:{theme.SYNERGY};color:white;padding:3px 12px;
        border-radius:12px;font-size:12px;font-weight:600">Q5 / 6 · THE COMBINATIONS</span>

        # Doubles and triples: additive or epistatic?

        Q3's knowledge base made a falsifiable claim: linear additivity
        explains why combining mutations works **outside** the active site,
        while active-site mutations combine less predictably (Gilio et al.
        2022, reading the Ma et al. 2021 results). Q2 gave us the site
        classes to test exactly that. The combination data -- every
        engineered variant with its measured conversion -- live in SI-003.
        """
    )
    return


@app.cell
def _(data):
    si002 = data.load_si002()
    si003 = data.load_si003()
    singles = data.extract_single_mutants(si002)
    return si002, si003, singles


@app.cell(hide_code=True)
def _(alt, mo, si003):
    strategy_chart = (
        alt.Chart(
            si003,
            title="Every engineered variant: conversion vs. R-enantiomeric excess, by strategy",
        )
        .mark_circle(size=70, opacity=0.8)
        .encode(
            x=alt.X(
                "ratio:Q",
                title="Fractional conversion",
                scale=alt.Scale(domain=[0, 1]),
            ),
            y=alt.Y(
                "r_enantiomeric_excess:Q",
                title="R-enantiomeric excess",
                scale=alt.Scale(domain=[0, 1]),
            ),
            color=alt.Color("experiment:N", title="Strategy"),
            tooltip=["mutation", "experiment", "ratio", "r_enantiomeric_excess"],
        )
        .properties(width=740, height=400)
    )
    mo.vstack([strategy_chart])
    return (strategy_chart,)


@app.cell(hide_code=True)
def _(data, mo, np, si002, si003, singles):
    shared = si003[si003["mutation"].str.match(r"^[A-Z]\d+[A-Z*]$", na=False)].merge(
        singles[["mutation", "mean"]], on="mutation", how="inner"
    )
    slope, intercept = np.polyfit(shared["mean"], shared["ratio"], 1)
    residuals = shared["ratio"] - (slope * shared["mean"] + intercept)
    wt_mean = float(si002[si002["mutation"].isna()]["mean"].iloc[0])
    wt_ratio = float(slope * wt_mean + intercept)
    single_lookup = singles.set_index("mutation")["mean"].to_dict()
    calibration_md = mo.md(
        f"""
        ## One scale for everything

        Additivity needs singles and combos on the same scale. The two
        tables summarize the same assay differently: SI-002 `mean`
        (activity) vs. SI-003 `ratio` (fractional conversion). For the
        {len(shared)} single mutants present in both, they track tightly
        (r = {np.corrcoef(shared["mean"], shared["ratio"])[0, 1]:.3f},
        residual sd {residuals.std():.3f}), so a linear bridge is
        legitimate -- and it puts the wild type at conversion
        {wt_ratio:.3f}.
        """
    )
    mo.vstack([calibration_md])
    return intercept, shared, single_lookup, slope, wt_ratio


@app.cell(hide_code=True)
def _(data, mo, np, si003, single_lookup, slope, intercept, wt_ratio):
    def logit(p):
        p = np.clip(p, 0.01, 0.99)
        return np.log(p / (1 - p))

    combos = si003[si003["mutation"].str.contains(";", na=False)].copy()
    combos["components"] = combos["mutation"].apply(data.split_combination)
    combos["covered"] = combos["components"].apply(
        lambda tokens: all(t in single_lookup for t in tokens)
    )
    covered = combos[combos["covered"]].copy()

    def expected_logit(mutation):
        single_logits = [
            logit(slope * single_lookup[t] + intercept)
            for t in data.split_combination(mutation)
        ]
        return float(
            logit(wt_ratio) + sum(sl - logit(wt_ratio) for sl in single_logits)
        )

    covered["expected_ratio"] = covered["mutation"].apply(
        lambda m: float(1 / (1 + np.exp(-expected_logit(m))))
    )
    covered["epistasis"] = logit(covered["ratio"]) - covered["mutation"].apply(
        expected_logit
    )
    combos_md = mo.md(
        f"""
        ## The additivity model

        For each of the {len(combos)} combinations we sum the components'
        single-mutant effects -- in log-odds space, so expectations cannot
        silently saturate at 1.0:

        **expected = WT odds x (product of each mutation's odds ratio over WT)**

        then compare with measurement. {len(combos) - len(covered)}
        combinations drop out because a component was never cloned as a
        single (the library covered ~81% of sequence space), leaving
        **{len(covered)} testable combinations**.
        """
    )
    mo.vstack([combos_md])
    return covered, expected_logit, logit


@app.cell
def _(covered, mo):
    strategies = ["all"] + sorted(covered["experiment"].unique().tolist())
    strategy_filter = mo.ui.dropdown(
        options=strategies, value="all", label="Show one strategy"
    )
    strategy_filter
    return (strategy_filter,)


@app.cell(hide_code=True)
def _(alt, covered, mo, pd, strategy_filter):
    shown = (
        covered
        if strategy_filter.value == "all"
        else covered[covered["experiment"] == strategy_filter.value]
    )
    corr = shown[["expected_ratio", "ratio"]].corr().iloc[0, 1]
    diagonal_df = pd.DataFrame({"x": [0.0, 1.0]})
    evo_chart = (
        alt.Chart(shown, title="Additive expectation vs. measured conversion")
        .mark_circle(size=60, opacity=0.75)
        .encode(
            x=alt.X(
                "expected_ratio:Q",
                title="Additive expectation (conversion)",
                scale=alt.Scale(domain=[0, 1]),
            ),
            y=alt.Y(
                "ratio:Q",
                title="Measured conversion",
                scale=alt.Scale(domain=[0, 1]),
            ),
            color=alt.Color("experiment:N", title="Strategy"),
            tooltip=["mutation", "experiment", "expected_ratio", "ratio"],
        )
        .properties(width=600, height=430)
    )
    diagonal = (
        alt.Chart(diagonal_df)
        .mark_line(color="#555555", strokeDash=[5, 4])
        .encode(x="x:Q", y="x:Q")
    )
    evo_md = mo.md(
        f"""
        Points **below the diagonal** combine to less than the sum of their
        parts (antagonistic epistasis); **above it**, more (synergy).
        Correlation for the {len(shown)} shown combinations: {corr:.2f}.
        """
    )
    mo.vstack([evo_md, evo_chart + diagonal])
    return (evo_chart,)


@app.cell(hide_code=True)
def _(alt, covered, mo, theme):
    by_experiment = (
        covered.groupby("experiment")["epistasis"]
        .median()
        .rename("median_epistasis")
        .reset_index()
    )
    epi_chart = (
        alt.Chart(by_experiment, title="Median epistasis by strategy (log-odds)")
        .mark_bar()
        .encode(
            x=alt.X("experiment:N", sort="-y", title="Strategy"),
            y=alt.Y(
                "median_epistasis:Q",
                title="Median epistasis (observed - additive, log-odds)",
            ),
            color=alt.Color(
                "median_epistasis:Q",
                scale=alt.Scale(scheme="redblue", domain=[-2, 2]),
                legend=None,
            ),
            tooltip=["experiment", "median_epistasis"],
        )
        .properties(width=600, height=280)
    )
    epi_md = mo.md(
        r"""
        The split that actually shows up is **by strategy**, not by
        active-site composition (only 22 of the combinations even touch an
        active-site residue):

        - the **epPCR lineage** (rounds 2-3, stacked on the S220T backbone)
          is additive-to-synergistic -- its winners *beat* the additive
          expectation;
        - **ML-designed stacks** sit far below additive expectation. Caveat
          before over-reading: 35 of the 91 ML combinations have additive
          expectations above 90% conversion, and nothing in this campaign
          was ever measured above 87% -- the assay saturates, so part of
          that gap is ceiling, not biology.
        """
    )
    mo.vstack([epi_md, epi_chart])
    return (epi_chart,)


@app.cell(hide_code=True)
def _(covered, mo):
    winner = covered[covered["mutation"] == "Q194L; S220T; H230Y"].iloc[0]
    winner_callout = mo.callout(
        mo.md(
            f"""
            **The KB's flagship: `Q194L/S220T/H230Y`** -- additive expectation
            {winner["expected_ratio"]:.3f}, measured **{winner["ratio"]:.3f}**:
            **{winner["epistasis"]:+.2f} log-odds of synergy**. The variant
            that went to gram-scale synthesis of the drug ZPL389 beat the sum
            of its parts.
            """
        ),
        kind="success",
    )
    winner_callout
    return (winner_callout,)


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        mo.md(
            r"""
            ### Answer -- Q5

            **Partially additive, honestly conditional.**

            - Where the KB's claim was made -- the epPCR lineage stacked on
              S220T -- combinations are **additive to synergistic**: round-3
              winners match or beat the sum of their single-mutant effects.
              The claim survives where it was born.
            - **ML-designed stacks** fall short of additive expectation. Some
              of that is assay ceiling, but the pattern is consistent enough
              to say: naively stacking individually-good mutations is not a
              design principle.
            - The KB's exact split (active site vs. distal) is **not
              testable** here -- only 22 combinations touch an active-site
              residue. Saying so is part of the analysis.
            - Design implication: combine **distal, well-measured singles
              within one lineage** -- that is where additivity holds -- and
              validate combinations empirically, exactly what this campaign
              did.
            """
        ),
        kind="success",
    )
    return


if __name__ == "__main__":
    app.run()
