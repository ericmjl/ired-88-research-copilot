"""Shared visual design system for the IRED-88 research copilot notebooks.

One palette, one altair theme, echoed across every figure so the notebook
series reads like a designed page rather than a code dump. Notebooks call
:func:`apply` once in their imports cell.
"""

from __future__ import annotations

#: Near-black ink for titles and axis labels.
INK = "#1f2430"
#: Muted grey for captions and de-emphasized marks.
MUTED = "#8a8f98"
#: Teal -- the primary series color and the demo's brand hue.
PRIMARY = "#0f766e"
#: Red -- active-site residues (< 6 A from NADP).
ACTIVE_SITE = "#d64550"
#: Amber -- second-shell residues (6-12 A from NADP).
SECOND_SHELL = "#eda63a"
#: Blue -- distal residues (> 12 A from NADP).
DISTAL = "#3b6ea5"
#: Grey -- positions with no experimental coordinates.
UNRESOLVED = "#b0b4bc"
#: Purple -- knowledge-base-derived annotations.
KB = "#7c5cbf"
#: Green -- synergy / favorable verdicts.
SYNERGY = "#2e8b57"

#: Site-class colors, keyed by :func:`ired_88_research_copilot.structure.site_class` output.
SITE_CLASS_COLORS = {
    "active_site": ACTIVE_SITE,
    "second_shell": SECOND_SHELL,
    "distal": DISTAL,
    "unresolved": UNRESOLVED,
}

#: Site classes in canonical display order.
SITE_CLASS_ORDER = ["active_site", "second_shell", "distal", "unresolved"]


def apply() -> None:
    """Register and enable the shared altair theme.

    Call once per notebook, in the imports cell. Safe to call repeatedly
    (re-registering an altair theme of the same name is a no-op).
    """
    import altair as alt

    alt.themes.register("ired88", _ired88_theme)
    alt.themes.enable("ired88")


def _ired88_theme() -> dict:
    """Build the altair theme config dictionary.

    :returns: An altair theme payload (a dict with a ``config`` key).
    """
    return {
        "config": {
            "title": {
                "fontSize": 14,
                "fontWeight": 600,
                "anchor": "start",
                "color": INK,
                "subtitleFontSize": 12,
                "subtitleColor": MUTED,
            },
            "axis": {
                "gridColor": "#e9eaee",
                "domainColor": "#c9ccd4",
                "tickColor": "#c9ccd4",
                "labelFontSize": 11,
                "titleFontSize": 12,
                "labelColor": INK,
                "titleColor": INK,
            },
            "legend": {
                "labelFontSize": 11,
                "titleFontSize": 11,
                "titleColor": INK,
                "labelColor": INK,
                "orient": "right",
            },
            "view": {"stroke": "transparent"},
            "range": {
                "category": [PRIMARY, ACTIVE_SITE, SECOND_SHELL, KB, DISTAL],
            },
            "bar": {"fill": PRIMARY},
            "line": {"stroke": PRIMARY},
            "point": {"filled": True, "size": 60},
        }
    }
