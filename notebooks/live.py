# /// script
# requires-python = ">=3.10,<3.15"
#
# [tool.marimo-studio]
# default = "html-report"
#
# [tool.marimo-studio.cells]
# cell-1 = {ref = "cell:v1:2a8b2735feef7a97f2d8db1eef4043c6ce862e96336ce30dbd3d8abce84906c9:2a8b2735feef7a97f2d8db1eef4043c6ce862e96336ce30dbd3d8abce84906c9:0"}
# cell-2 = {ref = "cell:v1:d6429cfebe85d8e99aeed3fba5a4fae4b965750c4bd0cbc4b7b827eb2f65d26a:2d77ad5e08efc0e5005db011d352df1c1d3bca9b7aeda1204957d515ffcba966:0"}
# cell-3 = {ref = "cell:v1:18a34f32fdbf48a6292258bff12f8cc387536db205f7a204d71d608850dec042:4c0ffcbe429b06cdee68843040b9c9fa75b09c5f533390b766268d3379626add:0"}
# cell-4 = {ref = "cell:v1:0019d2eabf2d0ef6b5628cba65ee26c3afa2d663b9f3c2c311cf879188f5727b:610b3703d35a12a6861159d9b0ac11e24a5f657245aeab911485448861a0e809:0"}
# cell-23 = {ref = "cell:v1:4696318d454b65a1e86844ec35b2060e617704a8d10638784b47a3cdc6ac1343:66884c743c1f33d55869f0b7f2d2c681088d3a2b378a4489433ab7acdfb0a993:0"}
# cell-31 = {ref = "cell:v1:c9e9518351500489e7d005a74cd8187f870f863ca522639f849fbb0b12bf10fd:05853763f5a3acb2f3fc37cbc8fdb79573649c3b8f56d17abfbea2f34d3789b3:0"}
# cell-40 = {ref = "cell:v1:25b39802ab627c4f9df3e0746e7fdfc274f58f47f99945cb3dce5daa4c2b8503:2630ce9fb740de61aaa4272a2634983f4d6b5122b3eaa31601d99820cf7d3d51:0"}
# cell-41 = {ref = "cell:v1:f80ee31a67f512a573f52f5a26c94f96ca730038b92b467f461604bad746d339:8e9a20463745435be3f11993178838f6fe62dd770f0a4640e13164b0f1090780:0"}
# cell-46 = {ref = "cell:v1:daedd44cdc1f02c45ad944ab40142c70a46bdeea99c5edcccc3a0b5206c2daad:087634887b3ac91a2463a59e3806bd9c46bb86b4a071ff9bf9d53c173041cfee:3"}
# cell-47 = {ref = "cell:v1:a7b47099d4c32246fa010c4ce24676161ec9f1027200b3337eb5320eb7c34582:2ddb645a7a435e4e928d6e2a0fbd3720f7e5ea86b0b3cd4c8f9d55ee40aab7fa:0"}
# cell-48 = {ref = "cell:v1:d0e5856554db6ca1cc65f219cb3669f217eb96a762d883c58e764adab6c63315:9a8342da04ecad2a46f2f7faad632947e6781f67ecc4258afbcd58318365e25a:0"}
# cell-56 = {ref = "cell:v1:daedd44cdc1f02c45ad944ab40142c70a46bdeea99c5edcccc3a0b5206c2daad:087634887b3ac91a2463a59e3806bd9c46bb86b4a071ff9bf9d53c173041cfee:4"}
# cell-57 = {ref = "cell:v1:97c79d85b5763bf573725dc9431a5b60823d45dbd6fb345b1bc07c58194ac5db:849826c3727bfd6685ecd87fa274044bd309ac01cc7cd67ed1a71b1fe02dcaae:0"}
# cell-58 = {ref = "cell:v1:26ee6a94600435b2094847e8dc8dad48ef01dda198a0ada2a77f2fcba5ec97f7:713a94ecec1fdc06d50e663f18d46d46abbb81ef8c43ffd87fab703673b4db90:0"}
# cell-65 = {ref = "cell:v1:daedd44cdc1f02c45ad944ab40142c70a46bdeea99c5edcccc3a0b5206c2daad:087634887b3ac91a2463a59e3806bd9c46bb86b4a071ff9bf9d53c173041cfee:5"}
# cell-17 = {ref = "cell:v1:daedd44cdc1f02c45ad944ab40142c70a46bdeea99c5edcccc3a0b5206c2daad:087634887b3ac91a2463a59e3806bd9c46bb86b4a071ff9bf9d53c173041cfee:0"}
# cell-25 = {ref = "cell:v1:daedd44cdc1f02c45ad944ab40142c70a46bdeea99c5edcccc3a0b5206c2daad:087634887b3ac91a2463a59e3806bd9c46bb86b4a071ff9bf9d53c173041cfee:1"}
# cell-27 = {ref = "cell:v1:7fbfe34b51ee2ba892826b654295154f2aa60f9ad7a55bc5d78aa3666d197c5b:7887e2ffff96b19073607362a077e5568ff060d2228b1f1229ec615ebfe980d7:0"}
# cell-33 = {ref = "cell:v1:daedd44cdc1f02c45ad944ab40142c70a46bdeea99c5edcccc3a0b5206c2daad:087634887b3ac91a2463a59e3806bd9c46bb86b4a071ff9bf9d53c173041cfee:2"}
# ///

import marimo

__generated_with = "0.25.0"
app = marimo.App(width="medium")


@app.cell
def imports():
    import marimo as mo

    from ired_88_research_copilot import data, theme

    theme.apply()
    return data, mo, theme


@app.cell(hide_code=True)
def _(mo, theme):
    mo.md(f"""
    <div style="background:linear-gradient(135deg, {theme.PRIMARY} 0%, #134e4a 100%);
                border-radius:16px; padding:28px 32px; color:white;">
    <div style="font-size:13px; letter-spacing:2px; opacity:0.85;
                text-transform:uppercase;">AI as a Research Co-Pilot · Live demo</div>
    <h1 style="margin:10px 0 6px 0; font-size:34px; line-height:1.15;">
    The IRED-88 Research Copilot</h1>
    <div style="font-size:15px; opacity:0.92;">
    One enzyme, four data modalities, one question ladder -- in a single repo.</div>
    </div>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    An enzyme-engineering campaign produced a deep mutational scan, an
    enantioselectivity table, a 1.9 A crystal structure, and a set of
    engineered variants. Around it sits a small **knowledge base** of six
    papers. This demo runs the round-trip between all four modalities --
    and asks one question on the way:

    > #### Where do activity-improving mutations of the enzyme IRED-88 come from -- and could we have seen them coming?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Q1 -- Which single mutations improve IRED-88's activity?
    """)
    return


@app.cell(hide_code=True)
def q1_conversion_question(mo):
    mo.md(r"""
    ## What is in the conversion deep mutational scan?

    Substrate conversion and enantioselectivity were measured as
    separate screens. The next cell loads only the conversion screen
    (paper SI-002). The enantioselectivity table (SI-003) stays unloaded.
    """)
    return


@app.cell
def load_conversion(data):
    conversion = data.load_si002()
    conversion
    return (conversion,)


@app.cell(hide_code=True)
def q1_conversion_finding(mo):
    mo.md(r"""
    ## SI-002 holds 11,305 conversion measurements, stored as a fraction

    `mean` is the batch-adjusted conversion, from 0.0005 to 0.847.
    `ratio` is the unadjusted conversion fraction and spans nearly the
    same range. Wild type is the unlabeled row: mean 0.156, from 458
    measurements, which is 15.6% conversion on a percentage scale.
    4,720 rows are strict single mutants. This table has no
    enantiomeric-excess column.
    """)
    return


@app.cell(hide_code=True)
def q1_heatmap_question(mo):
    mo.md(r"""
    ## Where do high and low conversion values sit among side-chain classes?

    Each rectangle is one single mutant from the conversion screen.
    Color is a square-root scale of batch-adjusted conversion, `mean`,
    so differences among the many low values stay visible.
    Mutant residues are grouped by side-chain property and ordered
    alphabetically within each group.
    From top to bottom the groups are acidic (D, E), basic (H, K, R),
    polar uncharged (C, N, Q, S, T, Y), and nonpolar
    (A, F, G, I, L, M, P, V, W).
    A white seam between groups is about two fifths the height of a cell,
    so it reads as a divider rather than a missing residue.
    """)
    return


@app.cell(hide_code=True)
def dms_activity_heatmap(conversion, data, theme):
    import altair as alt
    import pandas as pd

    cell_span = 100
    group_gap = 40
    aa_groups = [
        ("Acidic", ["D", "E"]),
        ("Basic", ["H", "K", "R"]),
        ("Polar", ["C", "N", "Q", "S", "T", "Y"]),
        ("Nonpolar", ["A", "F", "G", "I", "L", "M", "P", "V", "W"]),
    ]

    aa_center = {}
    aa_group_name = {}
    group_label_y = []
    cursor = 0
    for group_index, (group_name, letters) in enumerate(aa_groups):
        group_start = cursor
        for letter in letters:
            aa_center[letter] = cursor
            aa_group_name[letter] = group_name
            cursor += cell_span
        group_mid = (group_start + cursor - cell_span) / 2
        group_label_y.append({"group": group_name, "y": group_mid})
        if group_index < len(aa_groups) - 1:
            cursor += group_gap

    singles = data.extract_single_mutants(conversion)
    singles = singles[singles["mut_aa"].isin(aa_center)].copy()
    singles["aa_group"] = singles["mut_aa"].map(aa_group_name)
    singles["x0"] = singles["pos"] - 0.5
    singles["x1"] = singles["pos"] + 0.5
    singles["y0"] = singles["mut_aa"].map(
        lambda letter: aa_center[letter] - cell_span / 2
    )
    singles["y1"] = singles["mut_aa"].map(
        lambda letter: aa_center[letter] + cell_span / 2
    )

    y_domain = [-cell_span / 2, max(aa_center.values()) + cell_span / 2]
    y_scale = alt.Scale(domain=y_domain, reverse=True)
    label_expr = (
        "{"
        + ",".join(f"'{center}':'{letter}'" for letter, center in aa_center.items())
        + "}[format(datum.value,'.0f')]"
    )
    mean_max = float(singles["mean"].max())

    heatmap_rects = (
        alt.Chart(singles)
        .mark_rect()
        .encode(
            x=alt.X(
                "x0:Q",
                title="Sequence position",
                scale=alt.Scale(domain=[1.5, 304.5], nice=False),
                axis=alt.Axis(
                    values=[50, 100, 150, 200, 250, 300],
                    grid=False,
                    labelExpr="format(datum.value, '.0f')",
                ),
            ),
            x2="x1:Q",
            y=alt.Y(
                "y0:Q",
                title=None,
                scale=y_scale,
                axis=alt.Axis(
                    values=list(aa_center.values()),
                    labelExpr=label_expr,
                    grid=False,
                    domain=False,
                    tickSize=2,
                    labelPadding=2,
                ),
            ),
            y2="y1:Q",
            color=alt.Color(
                "mean:Q",
                title="Mean conversion (square-root scale)",
                scale=alt.Scale(
                    type="sqrt",
                    domain=[0, mean_max],
                    range=["#d7e8e5", "#7fcdc4", theme.PRIMARY, "#134e4a"],
                ),
                legend=alt.Legend(orient="bottom"),
            ),
            tooltip=[
                alt.Tooltip("mutation:N", title="Mutant"),
                alt.Tooltip("pos:Q", title="Position", format=".0f"),
                alt.Tooltip("mut_aa:N", title="Mutant residue"),
                alt.Tooltip("aa_group:N", title="Side-chain group"),
                alt.Tooltip("mean:Q", title="Mean conversion", format=".3f"),
                alt.Tooltip("count:Q", title="Measurements", format=".0f"),
            ],
        )
        .properties(width=860, height=440)
    )

    group_labels = (
        alt.Chart(pd.DataFrame(group_label_y))
        .mark_text(
            align="right",
            baseline="middle",
            dx=-4,
            fontSize=11,
            color=theme.MUTED,
        )
        .encode(
            y=alt.Y("y:Q", scale=y_scale, axis=None),
            text="group:N",
        )
        .properties(width=78, height=440)
    )

    dms_heatmap = (
        alt.hconcat(group_labels, heatmap_rects, spacing=0)
        .resolve_scale(y="shared")
        .properties(title="Single-mutant conversion by position and mutant residue")
        .configure_view(strokeWidth=0)
    )
    dms_heatmap
    return alt, pd, singles


@app.cell(hide_code=True)
def heatmap_top_positions(mo):
    heatmap_lead = mo.md(
        r"""
    The darkest cells are single substitutions in different classes: A296I (0.712, nonpolar), S220T (0.678, polar), and H154V (0.583, nonpolar).
    """
    )
    heatmap_lead
    return


@app.cell(hide_code=True)
def q1_heatmap_finding(mo):
    mo.md(r"""
    ## High conversion is sparse, and it is not confined to one side-chain class

    The median single mutant has mean conversion 0.031, against 0.156 for
    wild type. 11.6% of single mutants sit above wild type.
    Group medians rise from acidic (0.014) to basic (0.022), nonpolar (0.032),
    and polar uncharged (0.040).
    Proline is the pale row, with median 0.003.
    Aspartate and arginine are also low (median 0.011).
    Methionine, valine, serine, isoleucine, and alanine sit near 0.05.

    The darkest cells are single substitutions in different classes:
    A296I (0.712, nonpolar), S220T (0.678, polar), and H154V (0.583, nonpolar).
    Positions 156, 243, 212, and 159 have the highest median conversion
    across the substitutions measured there.

    White rectangles are unmeasured pairs.
    Position 249 is an empty column: no single mutant was measured.
    The horizontal seams between groups are narrower than those empty cells.

    Color is on a square-root scale.
    On a linear scale from 0 to 0.71, the median would fall at about 4% of
    the color range, and the row differences above would collapse into one tint.
    """)
    return


@app.cell(hide_code=True)
def q1_marked_positions_question(mo):
    mo.md(r"""
    ## Which marked positions actually convert well?

    The boxes are coarse. S4 covers roughly positions 2-17, S1 covers 98-132,
    S2 covers 140-171, and S3 covers 194-240.
    The chart does not draw every position in those spans.
    It keeps the strongest position in each box, and the strongest positions
    that fall outside the boxes.
    An open point is the median substitution at that position.
    A filled point is the best substitution.
    The dashed line is wild type.
    """)
    return


@app.cell(hide_code=True)
def marked_position_dive(alt, conversion, pd, singles, theme):
    focus_positions = pd.DataFrame(
        [
            (6, "S4"),
            (118, "S1"),
            (154, "S2"),
            (156, "S2"),
            (175, "Outside"),
            (212, "S3"),
            (218, "S3"),
            (220, "S3"),
            (243, "Outside"),
            (296, "Outside"),
        ],
        columns=["pos", "mark"],
    )
    position_summary = singles.groupby("pos", as_index=False).agg(
        best_mean=("mean", "max"),
        median_mean=("mean", "median"),
    )
    best_mutation = singles.loc[
        singles.groupby("pos")["mean"].idxmax(), ["pos", "mutation"]
    ]
    focus_positions = focus_positions.merge(position_summary, on="pos").merge(
        best_mutation, on="pos"
    )
    focus_positions["label"] = (
        focus_positions["pos"].astype(str) + "  " + focus_positions["mutation"]
    )
    wt_conversion = float(conversion.loc[conversion["mutation"].isna(), "mean"].iloc[0])

    mark_color = alt.Color(
        "mark:N",
        title="Region",
        scale=alt.Scale(
            domain=["S4", "S1", "S2", "S3", "Outside"],
            range=[
                theme.PRIMARY,
                theme.DISTAL,
                theme.SECOND_SHELL,
                theme.ACTIVE_SITE,
                theme.INK,
            ],
        ),
        legend=alt.Legend(orient="bottom"),
    )
    position_axis = alt.Y(
        "label:N",
        sort=alt.SortField("best_mean", order="descending"),
        title=None,
    )
    conversion_axis = alt.X(
        "best_mean:Q",
        title="Conversion (mean)",
        scale=alt.Scale(domain=[0, 0.8]),
    )
    span = (
        alt.Chart(focus_positions)
        .mark_rule(strokeWidth=2, opacity=0.85)
        .encode(
            x="median_mean:Q",
            x2="best_mean:Q",
            y=position_axis,
            color=mark_color,
        )
    )
    median_point = (
        alt.Chart(focus_positions)
        .mark_point(filled=False, size=70)
        .encode(
            x="median_mean:Q",
            y=position_axis,
            color=mark_color,
            tooltip=[
                alt.Tooltip("pos:Q", title="Position", format=".0f"),
                alt.Tooltip("mutation:N", title="Best mutant"),
                alt.Tooltip("mark:N", title="Region"),
                alt.Tooltip("median_mean:Q", title="Median conversion", format=".3f"),
                alt.Tooltip("best_mean:Q", title="Best conversion", format=".3f"),
            ],
        )
    )
    best_point = (
        alt.Chart(focus_positions)
        .mark_point(filled=True, size=70)
        .encode(x=conversion_axis, y=position_axis, color=mark_color)
    )
    wild_type_rule = (
        alt.Chart(pd.DataFrame({"wt_conversion": [wt_conversion]}))
        .mark_rule(strokeDash=[5, 4], color=theme.MUTED)
        .encode(x="wt_conversion:Q")
    )
    position_dive = (wild_type_rule + span + median_point + best_point).properties(
        width=520,
        height=320,
        title=alt.Title(
            "Standout positions: median substitution and best substitution",
            subtitle="Dashed line is wild type. Open point is the median; filled point is the best mutant.",
        ),
    )
    position_dive
    return


@app.cell(hide_code=True)
def q1_marked_positions_finding(mo):
    mo.md(r"""
    ## S2 and S3 hold the strong positions. S1 and S4 are milder.

    Wild type is 0.156.

    In S2 (about 140-171), H154V reaches 0.583 and the median substitution
    at 154 is 0.165, just above wild type.
    Position 156 is a different kind of hit: A156G is 0.425, and the median
    substitution is 0.285, the highest median in this set.
    Positions 159 and 160, not drawn, match that pattern
    (medians 0.248 and 0.204).

    In S3 (about 194-240), S220T is 0.678, the second-best single mutant
    in the scan. A218L is 0.519.
    Position 212 has a high median (0.252) and a strong best mutant
    (I212K, 0.467).

    In S4 (about 2-17), position 6 is the early signal.
    S6C is 0.438 and the median substitution is 0.199, above wild type.
    The other positions in that box top out near 0.31.

    In S1 (about 98-132), position 118 is the one that holds up:
    median 0.199, best mutant D118M at 0.314.
    Position 127 is omitted because its best mutant is 0.333
    while its median is 0.008. One substitution there works.

    Outside the boxes, A296I at 296 is the best mutant in the scan (0.712),
    and the median at 296 is only 0.081.
    V175K (0.539) sits between S2 and S3, with a median of 0.022.
    L243D (0.501) is just past S3, and position 243 has a median of 0.283.
    """)
    return


@app.cell
def _():
    # top-15 single mutants, bar chart
    return


@app.cell
def _():
    # per-position mean activity, with lines at the crystal boundary (12, 301)
    return


@app.cell
def _():
    # bonus if time: a position slider + per-mutant bar chart (the explorer)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Answer
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Q2 -- Are the beneficial positions where the structure says they should be?
    """)
    return


@app.cell(hide_code=True)
def q2_structure_question(mo):
    mo.md(r"""
    ## How should 7OG3 be colored: by activity, or by distance to NADP?

    PDB 7OG3 is the 1.9 Å crystal structure, with NADP bound in each chain.
    ATOM residue numbers are DMS positions. The crystal resolves positions 12-301.
    The dropdown colors both chains by the per-position mean of
    batch-adjusted conversion, or by the minimum distance from that residue to NADP.
    The same residue number gets the same color on chain A and chain B.
    Clicking a residue stores its position.
    """)
    return


@app.cell(hide_code=True)
def structure_viewer(mo, singles, theme):
    import anywidget
    import traitlets

    from ired_88_research_copilot import structure

    crystal = structure.load_crystal_structure()
    crystal_resnums = set(crystal.observed_resnums)
    activity_series = singles.groupby("pos")["mean"].mean()
    activity_by_residue = {
        str(int(pos)): round(float(value), 4)
        for pos, value in activity_series.items()
        if int(pos) in crystal_resnums
    }
    distance_by_residue = {}
    for resnum in crystal.observed_resnums:
        nadp_distance = structure.min_ligand_distance(crystal, resnum)
        if nadp_distance is not None:
            distance_by_residue[str(resnum)] = round(nadp_distance, 2)

    pdb_lines = []
    for pdb_line in (structure.EXTERNAL_DATA_DIR / "7OG3.pdb").read_text().splitlines():
        if pdb_line.startswith("ATOM"):
            pdb_lines.append(pdb_line)
        elif pdb_line.startswith("HETATM") and pdb_line[17:20].strip() == "NDP":
            pdb_lines.append(pdb_line)
    pdb_lines.append("END")
    cartoon_pdb = "\n".join(pdb_lines)
    activity_max = max(activity_by_residue.values())

    viewer_esm = """
    import * as molns from "https://esm.sh/3dmol@2.4.2";

    const $3Dmol = molns.createViewer ? molns : molns.default;

    function mix(start, end, fraction) {
      const left = parseInt(start.slice(1), 16);
      const right = parseInt(end.slice(1), 16);
      const channels = [16, 8, 0].map((shift) => {
        const a = (left >> shift) & 255;
        const b = (right >> shift) & 255;
        return Math.round(a + (b - a) * fraction);
      });
      return "#" + channels.map((v) => v.toString(16).padStart(2, "0")).join("");
    }

    function ramp(stops, fraction) {
      const x = Math.max(0, Math.min(1, fraction));
      let index = 0;
      while (index < stops.length - 2 && x > stops[index + 1][0]) index += 1;
      const [t0, c0] = stops[index];
      const [t1, c1] = stops[index + 1];
      const span = t1 - t0;
      return mix(c0, c1, span === 0 ? 0 : (x - t0) / span);
    }

    export default {
      render({ model, el }) {

        const nesRoot = el.getRootNode();
        const nesMount = nesRoot instanceof ShadowRoot ? nesRoot : document.head;
        if (!nesMount.querySelector("link[data-nes-css]")) {
          const nesFont = document.createElement("link");
          nesFont.rel = "stylesheet";
          nesFont.href = "https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap";
          const nesSheet = document.createElement("link");
          nesSheet.rel = "stylesheet";
          nesSheet.href = "https://unpkg.com/nes.css@2.3.0/css/nes.min.css";
          nesSheet.dataset.nesCss = "1";
          nesMount.prepend(nesFont, nesSheet);
        }
        const controller = new AbortController();
        const { signal } = controller;
        const palette = model.get("palette");
        const root = document.createElement("div");
        root.className = "nes-container is-rounded viewer-shell";

        const controls = document.createElement("div");
        controls.className = "viewer-controls";
        const colorLabel = document.createElement("span");
        colorLabel.textContent = "Color by";
        controls.append(colorLabel);
        const selectWrap = document.createElement("div");
        selectWrap.className = "nes-select";
        const select = document.createElement("select");
        select.innerHTML = `
          <option value="activity">Mean activity</option>
          <option value="distance">Distance to NADP</option>
        `;
        selectWrap.append(select);
        controls.append(selectWrap);

        const viewport = document.createElement("div");
        viewport.className = "viewer-stage";
        viewport.textContent = "Loading 3Dmol.js…";

        const legend = document.createElement("div");
        legend.className = "viewer-legend";
        const status = document.createElement("div");
        status.className = "viewer-status";
        status.textContent = "Click a residue to store its position.";

        root.append(controls, viewport, legend, status);
        el.replaceChildren(root);

        let viewer = null;

        function colorOf(atom) {
          const key = String(atom.resi);
          if (model.get("color_by") === "distance") {
            const distance = model.get("distance_by_residue")[key];
            if (distance == null) return palette.missing;
            return ramp(
              [
                [0, palette.near],
                [6 / 24, palette.shell],
                [12 / 24, palette.far],
                [1, palette.far],
              ],
              Number(distance) / 24,
            );
          }
          const activity = model.get("activity_by_residue")[key];
          if (activity == null) return palette.missing;
          const scaleMax = model.get("activity_max") || 1;
          return ramp(
            [
              [0, palette.low],
              [0.55, palette.mid],
              [1, palette.high],
            ],
            Number(activity) / scaleMax,
          );
        }

        function paintLegend() {
          const mode = model.get("color_by");
          if (mode === "distance") {
            legend.innerHTML = `
              <div style="height:12px; border:4px solid #212529; background:linear-gradient(to right, ${palette.near} 0%, ${palette.shell} 25%, ${palette.far} 50%, ${palette.far} 100%);"></div>
              <div style="display:flex; justify-content:space-between; margin-top:4px;">
                <span>0 Å</span><span>6 Å</span><span>12 Å</span><span>24 Å</span>
              </div>
              <div>Minimum distance from the residue to NADP. Red is the pocket.</div>
            `;
            return;
          }
          const scaleMax = Number(model.get("activity_max") || 0).toFixed(2);
          legend.innerHTML = `
            <div style="display:flex; gap:8px; align-items:center;">
              <div style="flex:1; height:12px; border:4px solid #212529; background:linear-gradient(to right, ${palette.low}, ${palette.mid}, ${palette.high});"></div>
              <div style="width:12px; height:12px; background:${palette.missing}; border:4px solid #212529;"></div>
              <span>no measurement</span>
            </div>
            <div style="display:flex; justify-content:space-between; margin-top:4px;">
              <span>0</span><span>${scaleMax}</span>
            </div>
            <div>Per-position mean of batch-adjusted conversion, on both chains.</div>
          `;
        }

        function applyColor() {
          if (!viewer) return;
          const colorfunc = (atom) => colorOf(atom);
          viewer.setStyle({ hetflag: false }, { cartoon: { colorfunc } });
          viewer.setStyle({ resn: "NDP" }, { stick: { radius: 0.18 } });
          viewer.render();
        }

        function showClicked(residue) {
          status.textContent = residue == null
            ? "Click a residue to store its position."
            : `Clicked residue ${residue}.`;
        }

        select.addEventListener("change", () => {
          model.set("color_by", select.value);
          model.save_changes();
          paintLegend();
          applyColor();
        }, { signal });

        model.on("change:color_by", () => {
          if (select.value !== model.get("color_by")) select.value = model.get("color_by");
          paintLegend();
          applyColor();
        });
        model.on("change:clicked_residue", () => showClicked(model.get("clicked_residue")));

        select.value = model.get("color_by") || "activity";
        paintLegend();
        showClicked(model.get("clicked_residue"));

        const api = $3Dmol && $3Dmol.createViewer ? $3Dmol : null;
        if (!api) {
          viewport.textContent = "3Dmol.js did not export createViewer.";
          model.set("load_error", "missing createViewer");
          model.save_changes();
          return () => controller.abort();
        }

        viewport.textContent = "";
        viewer = api.createViewer(viewport, { backgroundColor: "white" });
        viewer.addModel(model.get("pdb_text"), "pdb");
        viewer.setClickable({ hetflag: false }, true, (atom) => {
          if (!atom || atom.resi == null) return;
          model.set("clicked_residue", atom.resi);
          model.save_changes();
        });
        applyColor();
        requestAnimationFrame(() => {
          viewer.resize();
          viewer.zoomTo();
          viewer.render();
        });

        return () => {
          controller.abort();
          if (viewer) viewer.clear();
        };
      },
    };
    """

    viewer_css = """
    :host {
      display: block;
      font-family: "Press Start 2P", monospace;
      font-size: 10px;
      line-height: 1.6;
      color: #212529;
    }

    .viewer-shell.nes-container {
      margin: 0;
      background: #fff;
    }

    .viewer-controls {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 12px;
    }

    .viewer-controls .nes-select {
      flex: 0 1 340px;
      margin: 0;
    }

    .viewer-controls .nes-select select {
      font-family: "Press Start 2P", monospace;
      font-size: 10px;
      border-width: 4px;
      border-style: solid;
      border-color: #212529;
      border-radius: 0;
      background-color: #fff;
      color: #212529;
      padding: 0.5rem 0.6rem;
    }

    .viewer-stage {
      width: 100%;
      height: 460px;
      position: relative;
      background: #fff;
    }

    .viewer-legend,
    .viewer-status {
      margin-top: 12px;
      font-size: 10px;
      line-height: 1.7;
      color: #212529;
    }
    """

    class IredCartoonViewer(anywidget.AnyWidget):
        """Cartoon of both chains of PDB 7OG3, colored by activity or NADP distance.

        :param pdb_text: ATOM records plus NADP HETATM records.
        :param activity_by_residue: DMS position to per-position mean conversion.
        :param distance_by_residue: DMS position to minimum NADP distance, in Å.
        :param activity_max: Upper end of the activity color scale.
        :param color_by: ``activity`` or ``distance``.
        :param clicked_residue: Residue number from the last click, if any.
        """

        pdb_text = traitlets.Unicode("").tag(sync=True)
        activity_by_residue = traitlets.Dict().tag(sync=True)
        distance_by_residue = traitlets.Dict().tag(sync=True)
        activity_max = traitlets.Float(1.0).tag(sync=True)
        color_by = traitlets.Unicode("activity").tag(sync=True)
        clicked_residue = traitlets.Int(None, allow_none=True).tag(sync=True)
        palette = traitlets.Dict().tag(sync=True)
        load_error = traitlets.Unicode("").tag(sync=True)
        _esm = viewer_esm
        _css = viewer_css

    structure_viewer = IredCartoonViewer(
        pdb_text=cartoon_pdb,
        activity_by_residue=activity_by_residue,
        distance_by_residue=distance_by_residue,
        activity_max=float(activity_max),
        palette={
            "low": "#d7e8e5",
            "mid": theme.PRIMARY,
            "high": "#134e4a",
            "near": theme.ACTIVE_SITE,
            "shell": theme.SECOND_SHELL,
            "far": theme.DISTAL,
            "missing": theme.UNRESOLVED,
            "ink": theme.INK,
            "muted": theme.MUTED,
        },
    )
    get_clicked_residue, set_clicked_residue = mo.state(
        structure_viewer.clicked_residue
    )
    structure_viewer.observe(
        lambda event: set_clicked_residue(structure_viewer.clicked_residue),
        names=["clicked_residue"],
    )
    structure_viewer
    return anywidget, crystal, structure, traitlets


@app.cell(hide_code=True)
def q2_structure_finding(mo):
    mo.md(r"""
    ## Both chains are colored by one residue property at a time

    Mean activity on the 290 resolved positions runs from 0.001 to 0.294.
    Chain A and chain B share that color, because both use the DMS residue number.
    Position 249 is in the crystal and has no single-mutant measurement, so it stays grey.
    Distance is the minimum atom distance to NADP, from 2.5 Å to 24.1 Å
    (median 13.8 Å). The scale is red at the ligand, amber at 6 Å, and blue from 12 Å outward.
    A click writes that residue number to `clicked_residue` on the viewer.
    """)
    return


@app.cell
def q2_homolog_question(mo):
    mo.md(r"""
    ## Where do Ser220 and Ala296 sit on a reductive aminase homolog?

    S220T and A296I are the two strongest single mutants in this scan, with mean conversion 0.678 and 0.712.
    Gilio et al. 2022, in the knowledge base, place Ser220 at the mouth of the active-site cleft and credit S220T with raising the enantiomeric excess from 30% to 96%.
    A 2024 ACS Catalysis review names A296I among the top activity variants of this same scan.
    The notes in `kb/papers/` do not mention A296.
    Aleku et al. 2016, also in the knowledge base, contribute the AoIRED crystal 5FWN as a family reference. That structure already exists, so it is not the model folded here.
    The homolog with a sequence in this repo is BacRedAm, GenBank PZN88780.1, from Aleku et al. 2024.
    Xing et al. 2025 place IRED-88 Asn178 at BacRedAm Asp188.
    No experimental BacRedAm structure is deposited. The coordinates are the ESMFold prediction already saved from the public ESM Atlas endpoint.
    Chain A of 7OG3 and that prediction are superimposed on aligned Cα atoms.
    Red spheres mark Ser220 and its BacRedAm partner. The amber sphere marks Ala296.
    NADP from the crystal is shown as sticks.
    """)
    return


@app.cell(hide_code=True)
def homolog_overlay(anywidget, crystal, structure, theme, traitlets):
    import numpy as np

    ired_sequence = "".join(
        line.strip()
        for line in (structure.EXTERNAL_DATA_DIR / "ired88_wt.fasta")
        .read_text()
        .splitlines()
        if not line.startswith(">")
    )
    bac_sequence = "".join(
        line.strip()
        for line in (structure.EXTERNAL_DATA_DIR / "bacredam.fasta")
        .read_text()
        .splitlines()
        if not line.startswith(">")
    )
    bac_structure = structure.parse_pdb(
        structure.EXTERNAL_DATA_DIR / "bacredam_esmfold.pdb"
    )

    def align_sequences(query, target):
        match, mismatch, gap_penalty = 2, -1, -2
        n_query, n_target = len(query), len(target)
        scores = np.zeros((n_query + 1, n_target + 1))
        pointer = np.zeros((n_query + 1, n_target + 1), dtype=np.int8)
        for i in range(1, n_query + 1):
            scores[i, 0] = gap_penalty * i
            pointer[i, 0] = 2
        for j in range(1, n_target + 1):
            scores[0, j] = gap_penalty * j
            pointer[0, j] = 3
        for i in range(1, n_query + 1):
            for j in range(1, n_target + 1):
                substitution = match if query[i - 1] == target[j - 1] else mismatch
                diagonal = scores[i - 1, j - 1] + substitution
                up = scores[i - 1, j] + gap_penalty
                left = scores[i, j - 1] + gap_penalty
                best, direction = diagonal, 1
                if up > best:
                    best, direction = up, 2
                if left > best:
                    best, direction = left, 3
                scores[i, j] = best
                pointer[i, j] = direction
        i, j = n_query, n_target
        columns = []
        while i or j:
            direction = int(pointer[i, j])
            if i and j and direction == 1:
                columns.append((i, j))
                i -= 1
                j -= 1
            elif i and (direction == 2 or j == 0):
                columns.append((i, None))
                i -= 1
            else:
                columns.append((None, j))
                j -= 1
        columns.reverse()
        return columns

    alignment_columns = align_sequences(ired_sequence, bac_sequence)
    bac_of_ired = {
        ired_pos: bac_pos
        for ired_pos, bac_pos in alignment_columns
        if ired_pos is not None and bac_pos is not None
    }

    def alpha_carbon(parsed, resnum):
        coords, names = parsed.residues[resnum][1], parsed.residues[resnum][2]
        return coords[names.index("CA"), :3]

    ired_cloud = []
    bac_cloud = []
    for ired_pos, bac_pos in bac_of_ired.items():
        if ired_pos in crystal.residues and bac_pos in bac_structure.residues:
            ired_cloud.append(alpha_carbon(crystal, ired_pos))
            bac_cloud.append(alpha_carbon(bac_structure, bac_pos))
    ired_cloud = np.vstack(ired_cloud)
    bac_cloud = np.vstack(bac_cloud)
    ired_center = ired_cloud.mean(axis=0)
    bac_center = bac_cloud.mean(axis=0)
    covariance = (bac_cloud - bac_center).T @ (ired_cloud - ired_center)
    left, _singular, right = np.linalg.svd(covariance)
    sign = np.linalg.det(right.T @ left.T)
    rotation = right.T @ np.diag([1.0, 1.0, sign]) @ left.T

    def place_bac(coord):
        return rotation @ (coord - bac_center) + ired_center

    superposed = np.vstack([place_bac(coord) for coord in bac_cloud])
    _homolog_rmsd = float(np.sqrt(((superposed - ired_cloud) ** 2).sum(axis=1).mean()))
    _aligned_identity = sum(
        ired_sequence[ired_pos - 1] == bac_sequence[bac_pos - 1]
        for ired_pos, bac_pos in bac_of_ired.items()
    )
    bac220 = bac_of_ired[220]
    _ser220_shift = float(
        np.linalg.norm(
            place_bac(alpha_carbon(bac_structure, bac220)) - alpha_carbon(crystal, 220)
        )
    )
    _ala230_plddt = float(bac_structure.residues[bac220][1][0, 3] * 100)

    def transform_chain(text, chain_out):
        rewritten = []
        for line in text.splitlines():
            if not (line.startswith("ATOM") and line[21] == "A"):
                continue
            coord = np.array(
                [float(line[30:38]), float(line[38:46]), float(line[46:54])]
            )
            moved = place_bac(coord)
            coord_text = f"{moved[0]:8.3f}{moved[1]:8.3f}{moved[2]:8.3f}"
            rewritten.append(
                line[:21] + chain_out + line[22:30] + coord_text + line[54:]
            )
        return "\n".join(rewritten) + "\nEND\n"

    crystal_text = (structure.EXTERNAL_DATA_DIR / "7OG3.pdb").read_text()
    ired_pdb = (
        "\n".join(
            line
            for line in crystal_text.splitlines()
            if (line.startswith("ATOM") and line[21] == "A")
            or (
                line.startswith("HETATM")
                and line[21] == "A"
                and line[17:20].strip() in structure.LIGAND_RESNAMES
            )
        )
        + "\nEND\n"
    )
    bac_pdb = transform_chain(
        (structure.EXTERNAL_DATA_DIR / "bacredam_esmfold.pdb").read_text(),
        "B",
    )
    label_sites = {
        "S220": alpha_carbon(crystal, 220),
        "A230": place_bac(alpha_carbon(bac_structure, bac220)),
        "A296": alpha_carbon(crystal, 296),
    }

    overlay_esm = """
    function render({ model, el }) {

      const nesRoot = el.getRootNode();
      const nesMount = nesRoot instanceof ShadowRoot ? nesRoot : document.head;
      if (!nesMount.querySelector("link[data-nes-css]")) {
        const nesFont = document.createElement("link");
        nesFont.rel = "stylesheet";
        nesFont.href = "https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap";
        const nesSheet = document.createElement("link");
        nesSheet.rel = "stylesheet";
        nesSheet.href = "https://unpkg.com/nes.css@2.3.0/css/nes.min.css";
        nesSheet.dataset.nesCss = "1";
        nesMount.prepend(nesFont, nesSheet);
      }
      const palette = model.get("palette");
      const root = document.createElement("div");
      root.className = "nes-container is-rounded overlay-shell";
      root.innerHTML = `
        <p class="overlay-caption">
          Gray cartoon: IRED-88 chain A, PDB 7OG3. Blue cartoon: BacRedAm ESMFold, placed on IRED-88.
          Red spheres: Ser220 and BacRedAm ${model.get("bac_partner")}. Amber sphere: Ala296, which has no aligned BacRedAm residue.
          Gray sticks: NADP.
        </p>
        <div id="viewport" class="overlay-stage"></div>
      `;
      el.appendChild(root);
      const viewport = root.querySelector("#viewport");
      let viewer = null;
      const controller = new AbortController();

      async function start() {
        const molns = await import("https://esm.sh/3dmol@2.4.2");
        const api = molns.createViewer ? molns : molns.default;
        if (!api || !api.createViewer) {
          viewport.textContent = "3Dmol.js did not export createViewer.";
          return;
        }
        viewer = api.createViewer(viewport, { backgroundColor: "white" });
        viewer.addModel(model.get("ired_pdb"), "pdb");
        viewer.addModel(model.get("bac_pdb"), "pdb");
        viewer.setStyle({ model: 0, hetflag: false }, { cartoon: { color: palette.ired } });
        viewer.setStyle({ model: 1 }, { cartoon: { color: palette.bac, opacity: 0.85 } });
        viewer.addStyle({ model: 0, resi: 220 }, { sphere: { color: palette.site220, radius: 0.8 } });
        viewer.addStyle({ model: 1, resi: model.get("bac_resi") }, { sphere: { color: palette.site220, radius: 0.8 } });
        viewer.addStyle({ model: 0, resi: 296 }, { sphere: { color: palette.site296, radius: 0.8 } });
        viewer.addStyle({ model: 0, hetflag: true }, { stick: { radius: 0.15, color: palette.muted } });
        const labels = model.get("labels");
        for (const label of labels) {
          viewer.addLabel(label.text, {
            position: { x: label.x, y: label.y, z: label.z },
            backgroundColor: label.color,
            fontColor: "white",
            fontSize: 12,
            backgroundOpacity: 0.85,
          });
        }
        viewer.zoomTo({ resi: [220, 296, model.get("bac_resi")] });
        viewer.render();
      }
      start();
      return () => {
        controller.abort();
        if (viewer) viewer.clear();
      };
    }
    """

    overlay_css = """
    :host {
      display: block;
      font-family: "Press Start 2P", monospace;
      font-size: 10px;
      line-height: 1.6;
      color: #212529;
    }

    .overlay-shell.nes-container {
      margin: 0;
      background: #fff;
    }

    .overlay-caption {
      margin: 0 0 12px;
      font-size: 10px;
      line-height: 1.7;
    }

    .overlay-stage {
      width: 100%;
      height: 480px;
      position: relative;
      background: #fff;
    }
    """

    class HomologOverlay(anywidget.AnyWidget):
        """IRED-88 crystal superimposed on the BacRedAm ESMFold model.

        :param ired_pdb: Chain A of 7OG3, including NADP.
        :param bac_pdb: BacRedAm atoms transformed into the 7OG3 frame.
        :param bac_resi: BacRedAm residue aligned to IRED-88 position 220.
        :param bac_partner: Label for that BacRedAm residue.
        :param labels: Text and coordinates for the three highlighted sites.
        :param palette: Cartoon and sphere colors.
        """

        ired_pdb = traitlets.Unicode("").tag(sync=True)
        bac_pdb = traitlets.Unicode("").tag(sync=True)
        bac_resi = traitlets.Int(230).tag(sync=True)
        bac_partner = traitlets.Unicode("A230").tag(sync=True)
        labels = traitlets.List().tag(sync=True)
        palette = traitlets.Dict().tag(sync=True)
        _esm = overlay_esm
        _css = overlay_css

    homolog_overlay = HomologOverlay(
        ired_pdb=ired_pdb,
        bac_pdb=bac_pdb,
        bac_resi=int(bac220),
        bac_partner=f"{bac_sequence[bac220 - 1]}{bac220}",
        labels=[
            {
                "text": "S220",
                "x": float(label_sites["S220"][0]),
                "y": float(label_sites["S220"][1]),
                "z": float(label_sites["S220"][2]),
                "color": theme.ACTIVE_SITE,
            },
            {
                "text": f"{bac_sequence[bac220 - 1]}{bac220}",
                "x": float(label_sites["A230"][0]),
                "y": float(label_sites["A230"][1]),
                "z": float(label_sites["A230"][2]),
                "color": theme.ACTIVE_SITE,
            },
            {
                "text": "A296",
                "x": float(label_sites["A296"][0]),
                "y": float(label_sites["A296"][1]),
                "z": float(label_sites["A296"][2]),
                "color": theme.SECOND_SHELL,
            },
        ],
        palette={
            "ired": "#b7bcc4",
            "bac": theme.DISTAL,
            "site220": theme.ACTIVE_SITE,
            "site296": theme.SECOND_SHELL,
            "muted": theme.MUTED,
            "ink": theme.INK,
        },
    )
    homolog_overlay
    return (np,)


@app.cell
def q2_homolog_finding(mo):
    mo.md(r"""
    ## Ser220 aligns to BacRedAm Ala230; Ala296 is on an insertion

    The alignment recovers the published register: IRED-88 Asn178 pairs with BacRedAm Asp188.
    Over the 294 columns where both sequences have a residue, 44% of the amino acids match.
    Superposition of the 280 shared Cα atoms that are present in 7OG3 gives an RMSD of 3.05 Å.

    Ser220 pairs with BacRedAm Ala230. After the superposition those Cα atoms are 4.6 Å apart, and the residues on either side are mostly 4–5 Å apart. The sequences are in register there, and the backbones are shifted. Ala230 is predicted at pLDDT 96, so the offset is not a low-confidence coordinate.

    Ala296 has no BacRedAm partner. It is the first of five IRED-88 residues, 296–300 (AFKQP), that fall in a gap. The preceding stretch does overlay: positions 288–295 sit 0.8–2.9 Å from their BacRedAm partners, including Tyr294 paired with Val302 at 0.75 Å and the identical pair Glu295/Glu303 at 1.5 Å. The next shared column, Ser301, is 10.9 Å from BacRedAm Glu304. Relative to this homolog, the strongest activity mutation in the scan sits on a C-terminal insertion, and the chain does not return to the homolog's path immediately after it.

    No paper in the knowledge base, and none of the open reviews checked here, reports a mutation at the homologous position in another IRED. S220T is the mutation those reviews repeat. A296I is named when a review retells this scan, and it is otherwise quiet.
    """)
    return


@app.cell
def _():
    # per-position activity, colored by site class
    return


@app.cell
def _():
    # top-15 mutants annotated with site class + resolved status
    return


@app.cell
def _():
    # enrichment: site-class distribution of the top-50 positions vs. all
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Answer
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Q3 -- What does prior work already know about our top hits?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `kb/papers/` holds one markdown note per paper with YAML
    frontmatter. `kb.py` searches them programmatically.
    """)
    return


@app.cell
def _():
    # load all notes; show a small index table
    return


@app.cell
def _():
    # search: "S220 active site mouth stereoselectivity" -> show snippets
    return


@app.cell
def _():
    # search: "linear additivity combining mutations"
    return


@app.cell
def _():
    # search: "A296I" -- expect silence
    return


@app.cell
def _():
    # bonus if time: a live mo.ui.text query box wired to kb.search_notes
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Answer
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Q4 -- What does structure prediction see that the crystal cannot?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The crystal resolves 12-301. ESMFold predicted all 304 residues
    (B-factor column = pLDDT/100). Validate first, then read blind spots.
    """)
    return


@app.cell
def _():
    # load crystal + prediction; ca_rmsd and superposed_ca
    return


@app.cell
def _():
    # per-residue deviation: prediction vs. crystal (line chart)
    return


@app.cell
def _():
    # per-residue pLDDT (B-factor x 100), colored by crystal-resolved region
    return


@app.cell
def _():
    # where do the invisible residues (1-11, 302-304) sit? distance to NADP
    # in the crystal frame (superposition transform)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Answer
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Q5 -- Doubles and triples: additive or epistatic?
    """)
    return


@app.cell
def q5_epistasis_question(mo):
    mo.md(r"""
    ## Do doubles and triples of the best singles add, or fall short?

    The top 50 single mutants are ranked by batch-adjusted conversion (`mean`).
    The combinations are the doubles and triples whose every component is one of those 50.
    Measured conversion is `ratio`, a fraction from 0 to 1.
    On the shared variants, that column is the same number in SI-002 and SI-003.
    Wild type is 0.146.

    The first two panels are the earlier calculations, kept as a record.
    Arithmetic additivity sums the gains over wild type, and that sum can exceed 1.
    A conversion above 1 is not a possible measurement.
    Log-odds additivity sums the gains on the logit of conversion, then converts back to a fraction.

    The third panel follows the paper.
    Ma et al. treat conversion as a probability and take the unconverted fraction, `1 − conversion`.
    Independent effects multiply, so the sum is taken on `log(1 − conversion)`, then converted back to an expected conversion.
    That is a logarithm, not a logit.
    A point on the dashed line matches that panel's null.
    A point below it converts less than the null.
    """)
    return


@app.cell(hide_code=True)
def top50_epistasis(
    alt,
    conversion,
    crystal,
    data,
    np,
    pd,
    singles,
    structure,
    theme,
):
    top_mutations = set(singles.nlargest(50, "mean")["mutation"])
    single_ratio = singles.set_index("mutation")["ratio"].to_dict()
    position_of = singles.set_index("mutation")["pos"].to_dict()
    wt_ratio = float(conversion.loc[conversion["mutation"].isna(), "ratio"].iloc[0])
    ligand_distance = {
        resnum: structure.min_ligand_distance(crystal, resnum)
        for resnum in crystal.observed_resnums
    }

    def logit(fraction):
        bounded = np.clip(fraction, 1e-4, 1 - 1e-4)
        return np.log(bounded / (1 - bounded))

    def expit(log_odds):
        return 1 / (1 + np.exp(-log_odds))

    def where_mutations_sit(parts):
        classes = [
            structure.site_class(ligand_distance.get(int(position_of[part])))
            for part in parts
        ]
        if "unresolved" in classes:
            return "includes unresolved"
        if "active_site" in classes:
            return "includes active site"
        if all(site == "distal" for site in classes):
            return "all distal"
        return "includes second shell"

    variant_table = data.load_si003().copy()
    variant_table["parts"] = variant_table["mutation"].map(data.split_combination)
    variant_table["n_mut"] = variant_table["parts"].map(len)
    top_combinations = variant_table[variant_table["n_mut"].isin([2, 3])].copy()
    top_combinations = top_combinations[
        top_combinations["parts"].map(
            lambda parts: all(part in top_mutations for part in parts)
        )
    ].copy()

    expectation_rows = []
    for combo in top_combinations.itertuples(index=False):
        component_ratios = np.array([single_ratio[part] for part in combo.parts])
        arithmetic = wt_ratio + np.sum(component_ratios - wt_ratio)
        log_odds = expit(
            logit(wt_ratio) + np.sum(logit(component_ratios) - logit(wt_ratio))
        )
        order = "double" if combo.n_mut == 2 else "triple"
        location = where_mutations_sit(combo.parts)
        expectation_rows.append(
            {
                "mutation": combo.mutation,
                "order": order,
                "location": location,
                "observed": combo.ratio,
                "model": "Arithmetic",
                "expected": arithmetic,
            }
        )
        expectation_rows.append(
            {
                "mutation": combo.mutation,
                "order": order,
                "location": location,
                "observed": combo.ratio,
                "model": "Log-odds",
                "expected": log_odds,
            }
        )
        unconverted = np.clip(1 - component_ratios, 1e-4, 1 - 1e-4)
        wt_unconverted = float(np.clip(1 - wt_ratio, 1e-4, 1 - 1e-4))
        log_unconverted = np.log(wt_unconverted) + np.sum(
            np.log(unconverted) - np.log(wt_unconverted)
        )
        expectation_rows.append(
            {
                "mutation": combo.mutation,
                "order": order,
                "location": location,
                "observed": combo.ratio,
                "model": "Log of unconverted",
                "expected": 1 - np.exp(log_unconverted),
            }
        )
    combination_expectations = pd.DataFrame(expectation_rows)

    location_color = alt.Color(
        "location:N",
        title="Where the mutations sit",
        scale=alt.Scale(
            domain=[
                "all distal",
                "includes second shell",
                "includes unresolved",
            ],
            range=[theme.DISTAL, theme.SECOND_SHELL, theme.UNRESOLVED],
        ),
    )
    diagonal_frame = pd.DataFrame({"expected": [0.0, 1.0], "observed": [0.0, 1.0]})

    def expectation_panel(model_name, x_max):
        subset = combination_expectations[
            combination_expectations["model"] == model_name
        ]
        panel_points = (
            alt.Chart(subset)
            .mark_circle(size=70, opacity=0.9)
            .encode(
                x=alt.X(
                    "expected:Q",
                    title="Additive expectation",
                    scale=alt.Scale(domain=[0, x_max]),
                ),
                y=alt.Y(
                    "observed:Q",
                    title="Measured conversion",
                    scale=alt.Scale(domain=[0, 1]),
                ),
                color=location_color,
                shape=alt.Shape("order:N", title="Combination"),
                tooltip=[
                    alt.Tooltip("mutation:N", title="Combination"),
                    alt.Tooltip("order:N", title="Order"),
                    alt.Tooltip("location:N", title="Location"),
                    alt.Tooltip("expected:Q", title="Expected", format=".3f"),
                    alt.Tooltip("observed:Q", title="Measured", format=".3f"),
                ],
            )
        )
        diagonal = (
            alt.Chart(diagonal_frame)
            .mark_line(strokeDash=[4, 4], color=theme.MUTED)
            .encode(x="expected:Q", y="observed:Q")
        )
        return (diagonal + panel_points).properties(
            width=220, height=260, title=model_name
        )

    epistasis_chart = alt.hconcat(
        expectation_panel("Arithmetic", 1.6),
        expectation_panel("Log-odds", 1.6),
        expectation_panel("Log of unconverted", 1.0),
        spacing=24,
    ).resolve_scale(color="shared", shape="shared")
    epistasis_chart
    return


@app.cell
def q5_epistasis_finding(mo):
    mo.md(r"""
    ## The paper adds `log(1 − conversion)`, and these combinations still fall short

    Ma et al., ACS Catalysis 2021, "Linear Additivity of Mutations," state that a fraction converted can be treated as a probability, that independent mutational effects multiply, and that additivity is then visible in the log of the fraction unconverted.
    Figure 3b plots that unconverted fraction against the prediction from each mutant's unconverted fraction.
    The complement in the recollection matches the paper.
    The transform in the paper is `log(1 − conversion)`, not the logit of that quantity.
    `logit(1 − conversion)` equals `−logit(conversion)`, so adding on that scale and converting back to a conversion reproduces the log-odds panel.

    None of the top 50 singles is within 6 Å of NADP.
    The best active-site single is A127V, rank 60, with mean 0.333.
    Distal means more than 12 Å from NADP.
    Second shell means 6–12 Å.
    Thirty-nine combinations are built only from the top 50: 9 doubles and 30 triples.

    On the paper's scale, expected conversion stays inside 0 to 1.
    For these 39 it runs from 0.579 to 0.907.
    Measured conversion is more than 0.05 below that expectation for 30 combinations, within 0.05 for 7, and more than 0.05 above it for 2.
    The median difference is −0.25.
    The two above the null are Y177W; A218M (measured 0.840, expected 0.649) and L189M; A218L (measured 0.767, expected 0.695).
    Doubles fall short by a median of 0.13. Triples fall short by a median of 0.27.

    All-distal combinations have a median difference of −0.19 (n = 11).
    Combinations that include a second-shell mutation have a median difference of −0.21 (n = 18).
    Under this null, the shortfall is smaller than on the two earlier scales, and a few combinations sit on the line, but the typical double or triple of these top singles still converts less than the additive prediction.
    """)
    return


@app.cell
def _():
    # scale bridge: singles in BOTH tables -> linear fit mean -> ratio
    # (WT reference row comes from SI-002)
    return


@app.cell
def _():
    # combos: split_combination, keep only fully-covered combinations
    return


@app.cell
def _():
    # additive expectation in log-odds space:
    # expected logit = logit(WT) + sum(logit(single) - logit(WT))
    # epistasis = logit(observed) - expected logit
    return


@app.cell
def _():
    # expected vs observed scatter with a diagonal, colored by strategy
    return


@app.cell
def _():
    # median epistasis by experiment (bar chart); watch for assay ceiling
    return


@app.cell
def _():
    # bonus if time: a strategy dropdown filtering the expected-vs-observed scatter
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Answer
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Q6 -- If the DMS had a hole where the literature matters, would we have noticed?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Punch a hole in the DMS at exactly the positions the KB talks
    about -- extracted programmatically, no hardcoding -- then ask the
    other three modalities to nominate what the data lost.
    """)
    return


@app.cell
def _():
    # kb.extract_mutation_positions(notes) -> the mask set
    # data.mask_positions(singles, positions) -> the blinded dataset
    return


@app.cell
def _():
    # blinded per-position activity with bands over the masked positions
    return


@app.cell
def _():
    # recovery attempt 1: site classes of the masked positions (structure)
    return


@app.cell
def _():
    # recovery attempt 2: prediction-vs-crystal deviation, masked positions highlighted
    return


@app.cell
def _():
    # recovery attempt 3: KB search (acknowledge the circularity!)
    return


@app.cell
def _():
    # unmask and score: best single + rank per masked position
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Answer
    """)
    return


if __name__ == "__main__":
    app.run()
