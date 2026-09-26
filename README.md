# IRED-88 Research Copilot

A single repo where **DMS data, a literature knowledge base, a crystal
structure, and structure prediction** answer one scientific question
together, in marimo notebooks.

Built as the live demo for the "AI as a Research Co-Pilot" course (UMass
Chan Medical School, Week 3): it picks up where John Damask's session on
personal knowledge bases hands off -- here, a knowledge base is not just
read by an agent, it is *used in the analysis loop* alongside the data.

Made with care by Eric Ma (@ericmjl). The underlying data are public
(supporting information of the anchor paper below); the DMS dataset is
Eric's own from his Novartis days.

## The overarching question

> **Where do activity-improving mutations of the enzyme IRED-88 come from --
> and could we have seen them coming by combining DMS data, structure,
> prediction, and literature?**

## The question ladder

| # | Notebook | Question | Leans on |
|---|----------|----------|----------|
| Q1 | [`notebooks/01_dms_activity_map.py`](notebooks/01_dms_activity_map.py) | Which single mutations improve activity, and where do they sit along the sequence? | DMS table (paper SI-002) |
| Q2 | [`notebooks/02_structure_context.py`](notebooks/02_structure_context.py) | Are the beneficial positions where the structure says they should be? | DMS + PDB 7OG3 |
| Q3 | [`notebooks/03_knowledge_base.py`](notebooks/03_knowledge_base.py) | What does prior work already know about the top hits? | `kb/papers/*.md` |
| Q4 | [`notebooks/04_structure_prediction.py`](notebooks/04_structure_prediction.py) | What does prediction see that the crystal cannot? | ESMFold + 7OG3 |
| Q5 | [`notebooks/05_additivity.py`](notebooks/05_additivity.py) | Doubles and triples of top mutations: additive or epistatic? (Does the KB's claim survive the data?) | SI-003 combos + SI-002 singles + site classes |
| Q6 | [`notebooks/06_masked_recovery.py`](notebooks/06_masked_recovery.py) | If the DMS had a hole where the literature matters, would we have noticed? | everything |

Presenting live? [`notebooks/live/`](notebooks/live) holds empty skeleton twins
of every analysis notebook -- same questions, no code -- to build up on
stage, with the filled versions above as the answer key.

Start at [`notebooks/00_overarching_question.py`](notebooks/00_overarching_question.py).

## The four modalities

| Modality | Where | Notes |
|----------|-------|-------|
| DMS + ee data | `data/raw/` | 4,720 single mutants measured (81% of sequence space), plus enantioselectivity for every strategy in the campaign |
| Knowledge base | `kb/` | six paper notes with YAML frontmatter; programmatic search via `ired_88_research_copilot/kb.py` |
| Crystal structure | `data/external/7OG3.pdb` | IRED-88 + NADP, 1.9 A, resolves residues 12-301 |
| Structure prediction | `data/external/ired88_esmfold.pdb` | ESMFold, all 304 residues; regenerate with `scripts/predict_structure_esmfold.py` |

Helper code lives in `ired_88_research_copilot/` (`data.py`, `structure.py`,
`kb.py`), with tests in `tests/`.

## Run it

```bash
pixi install
pixi run marimo edit notebooks/
```

or, without touching the environment:

```bash
uvx marimo edit --sandbox notebooks/
```

Regenerate the structure prediction (needs network):

```bash
uv run scripts/predict_structure_esmfold.py
```

## Anchor citation

> Ma, E. J.; Siirola, E.; Moore, C.; et al. **Machine-Directed Evolution of
> an Imine Reductase for Activity and Stereoselectivity.** *ACS Catal.* 2021,
> *11* (20), 12433-12445. DOI:
> [10.1021/acscatal.1c02786](https://pubs.acs.org/doi/abs/10.1021/acscatal.1c02786)

Crystal structure: PDB [7OG3](https://www.rcsb.org/structure/7OG3)
(1.90 A, deposited with the paper). Use the bundled data for demos and
teaching; cite the paper for any external use of the raw tables.

## Notes for agents (and humans)

- 7OG3 numbers ATOM records by **wild-type protein position** (PDB residue
  number = DMS position); the 21-residue expression tag appears only in
  SEQRES. See `ired_88_research_copilot/structure.py`.
- The crystal resolves positions **12-301**; positions **1-11** and
  **302-304** have no coordinates.
- ESMFold's PDB output stores **pLDDT/100** in the B-factor column.
- Repo conventions live in [AGENTS.md](AGENTS.md).
