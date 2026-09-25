"""Command-line interface for the IRED-88 research copilot."""

from __future__ import annotations

import typer

from ired_88_research_copilot import data, kb, structure

app = typer.Typer(help="IRED-88 research copilot CLI.")


@app.callback()
def callback() -> None:
    """IRED-88 research copilot command-line interface."""


@app.command()
def summary() -> None:
    """Print a one-screen summary of every data modality in the repo."""
    singles = data.extract_single_mutants(data.load_si002())
    notes = kb.load_all_notes()
    crystal = structure.load_crystal_structure()
    top = singles.nlargest(1, "mean")
    typer.echo(f"DMS single mutants measured : {len(singles)}")
    typer.echo(f"positions covered           : {singles['pos'].nunique()}")
    typer.echo(f"best mutant                 : {top['mutation'].iloc[0]}")
    typer.echo(f"KB notes                    : {len(notes)}")
    typer.echo(
        f"crystal residues observed   : {len(crystal.observed_resnums)} (chain A)"
    )


if __name__ == "__main__":
    app()
