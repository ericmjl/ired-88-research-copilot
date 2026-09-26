import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import altair as alt
    import marimo as mo
    import numpy as np
    import pandas as pd

    from ired_88_research_copilot import data, structure

    return alt, data, mo, np, pd, structure


@app.cell
def _(mo):
    mo.md(
        r"""
        # Q5 -- Doubles and triples: additive or epistatic?

        Q3's knowledge base made a falsifiable claim: linear additivity
        explains why combining mutations works **outside** the active site,
        while active-site mutations combine less predictably (Gilio et al.
        2022, reading the Ma et al. 2021 results). Q2 gave us the site
        classes to test exactly that.

        The campaign's combination data live in SI-003: every engineered
        variant (multi-mutant strings like `Q194L; S220T; H230Y`) with its
        measured conversion (`ratio`) and enantioselectivity.
        """
    )
    return


@app.cell
def _(data):
    si003 = data.load_si003()
    si002 = data.load_si002()
    singles = data.extract_single_mutants(si002)
    return si002, si003, singles


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
    mo.vstack(
        [
            mo.md(
                r"""
                ## The combination data

                310 engineered variants, tagged by the strategy that produced
                them: epPCR rounds 1-3, ML-guided, structure-guided
                mutagenesis (SGM), Low-N, fragment library. This is where
                doubles and triples live.
                """
            ),
            strategy_chart,
        ]
    )
    return (strategy_chart,)


@app.cell
def _(mo, np, si002, si003, singles):
    shared = si003[si003["mutation"].str.match(r"^[A-Z]\d+[A-Z*]$", na=False)].merge(
        singles[["mutation", "mean"]], on="mutation", how="inner"
    )
    slope, intercept = np.polyfit(shared["mean"], shared["ratio"], 1)
    residuals = shared["ratio"] - (slope * shared["mean"] + intercept)
    wt_mean = float(si002[si002["mutation"].isna()]["mean"].iloc[0])
    wt_ratio = slope * wt_mean + intercept
    single_lookup = singles.set_index("mutation")["mean"].to_dict()

    mo.md(
        f"""
        ## One scale for everything

        Additivity needs singles and combos on the same scale. The two
        tables report different summaries of the same assay: SI-002
        `mean` (activity) and SI-003 `ratio` (fractional conversion). For
        the {len(shared)} single mutants present in both, they track each
        other tightly (r = {np.corrcoef(shared["mean"], shared["ratio"])[0, 1]:.3f}),
        so a linear bridge is legitimate:

        **ratio = {slope:.3f} x mean + {intercept:+.4f}**
        (residual sd {residuals.std():.3f}), putting the wild type at
        conversion {wt_ratio:.3f}.
        """
    )
    return intercept, shared, slope, single_lookup, wt_mean, wt_ratio


@app.cell
def _(alt, intercept, mo, pd, shared, slope):
    calib_chart = (
        alt.Chart(shared, title="Scale bridge: SI-002 activity vs. SI-003 conversion")
        .mark_circle(size=45, opacity=0.7)
        .encode(
            x=alt.X("mean:Q", title="SI-002 activity (mean)"),
            y=alt.Y("ratio:Q", title="Fractional conversion"),
            tooltip=["mutation", "mean", "ratio"],
        )
        .properties(width=450, height=350)
    )
    fit_df = pd.DataFrame({"mean": [0.0, 0.9]})
    fit_df["ratio"] = slope * fit_df["mean"] + intercept
    fit_line = alt.Chart(fit_df).mark_line(color="red").encode(x="mean:Q", y="ratio:Q")
    mo.vstack(
        [
            mo.md(r"""The bridge, eyeball-checked against the shared singles:"""),
            calib_chart + fit_line,
        ]
    )
    return (calib_chart,)


@app.cell
def _(data, mo, np, si003, single_lookup, slope, intercept, wt_ratio):
    def logit(p):
        p = np.clip(p, 0.01, 0.99)
        return np.log(p / (1 - p))

    combos = si003[si003["mutation"].str.contains(";", na=False)].copy()
    combos["components"] = combos["mutation"].apply(data.split_combination)
    combos["covered"] = combos["components"].apply(
        lambda toks: all(t in single_lookup for t in toks)
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
    mo.md(
        f"""
        ## The additivity model

        For each of the {len(combos)} combinations we sum the components'
        single-mutant effects (on the bridged conversion scale, in log-odds
        space so expectations cannot silently saturate at 1.0):

        **expected = WT x (product of each mutation's odds ratio over WT)**

        then compare with what was actually measured. {len(combos) - len(covered)}
        combinations are dropped because at least one component was never
        cloned as a single mutant (the library covered ~81% of sequence
        space), leaving **{len(covered)} testable combinations**.
        """
    )
    return covered, expected_logit, logit


@app.cell
def _(alt, covered, mo, pd):
    corr = covered[["expected_ratio", "ratio"]].corr().iloc[0, 1]
    evo_chart = (
        alt.Chart(covered, title="Additive expectation vs. measured conversion")
        .mark_circle(size=55, opacity=0.75)
        .encode(
            x=alt.X("expected_ratio:Q", title="Additive expectation (conversion)"),
            y=alt.Y("ratio:Q", title="Measured conversion"),
            color=alt.Color("experiment:N", title="Strategy"),
            tooltip=["mutation", "experiment", "expected_ratio", "ratio"],
        )
        .properties(width=560, height=430)
    )
    diagonal_df = pd.DataFrame({"x": [0.0, 1.0]})
    diagonal = (
        alt.Chart(diagonal_df)
        .mark_line(color="black", strokeDash=[4, 4])
        .encode(x="x:Q", y="x:Q")
    )
    mo.vstack(
        [
            mo.md(
                f"""
                Points below the diagonal combine to **less** than the sum of
                their parts (antagonistic epistasis); above it, **more**
                (synergy). Correlation here: {corr:.2f} -- additive
                expectation is informative but far from the whole story.
                """
            ),
            evo_chart + diagonal,
        ]
    )
    return (evo_chart,)


@app.cell
def _(alt, covered, mo):
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
                title="Median epistasis (log-odds, observed - additive)",
            ),
            color=alt.Color(
                "median_epistasis:Q", title="Median", scale=alt.Scale(scheme="redblue")
            ),
            tooltip=["experiment", "median_epistasis"],
        )
        .properties(width=560, height=300)
    )
    mo.vstack(
        [
            mo.md(
                r"""
                The split that actually shows up in this data is **by
                strategy**, not by active-site composition (only 22 of the
                combinations even touch an active-site residue):

                - the **epPCR lineage** (rounds 2-3, built on the S220T
                  backbone) is additive-to-synergistic -- the winners beat
                  the additive expectation;
                - **ML-designed stacks** sit far below additive expectation.
                  Caveat before over-reading that: 35 of the 91 ML
                  combinations have additive expectations above 90%
                  conversion, and no measured variant in this campaign ever
                  exceeded 87% -- the assay itself saturates, so some of
                  that gap is ceiling, not biology.
                """
            ),
            epi_chart,
        ]
    )
    return (epi_chart,)


@app.cell
def _(covered, mo):
    winner = covered[covered["mutation"] == "Q194L; S220T; H230Y"].iloc[0]
    mo.md(
        f"""
        The KB's flagship, **Q194L/S220T/H230Y**: additive expectation
        {winner["expected_ratio"]:.3f}, measured {winner["ratio"]:.3f} --
        **{winner["epistasis"]:+.2f} log-odds of synergy**. The variant that
        went to gram-scale synthesis beat the sum of its parts.
        """
    )
    return (winner,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Answer to Q5

        **Partially additive, honestly conditional.**

        - Where the KB's claim was made -- the epPCR lineage stacked on
          S220T -- combinations are **additive to synergistic**: round-3
          winners match or beat the sum of their single-mutant effects.
          The claim survives where it was born.
        - The **ML-designed stacks** fall short of additive expectation.
          Some of that gap is assay ceiling (expectations above 90%
          conversion are unmeasurable), but the pattern is consistent
          enough to say: naively stacking individually-good mutations is
          not a design principle.
        - The KB's specific split (active site vs. distal) is **not
          testable** in this dataset -- only 22 combinations touch an
          active-site residue. That is a real limitation, and saying so is
          part of the analysis.
        - Design implication: combine **distal, well-measured singles in
          one lineage** (that is where additivity holds), and validate
          combinations empirically -- which is exactly what the campaign
          did.
        """
    )
    return


if __name__ == "__main__":
    app.run()
