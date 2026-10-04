# Re-evaluating Released Vision-Language-Action Checkpoints on the RoboBenchMart Retail Benchmark: Octo and π₀.₅

This project contains the LaTeX source for the candidate's dissertation, an independent re-evaluation of the Octo and π₀.₅ checkpoints released with the RoboBenchMart benchmark (arXiv:2511.10276).

## Build

Compile `main.tex` with XeLaTeX/BibTeX, for example:

```text
latexmk -xelatex main.tex
```

The output is written to `build/main.pdf` (see `.latexmkrc`). Tectonic 0.16.9 (`tectonic main.tex --keep-logs`) also works.

## Data sources

All experiment numbers come from the evaluation records in the project repository
[SaladMike/RoboBenchMart_dissertation](https://github.com/SaladMike/RoboBenchMart_dissertation):

- `results/octo-2026-09-28/` — Octo, 42 configurations × 30 episodes
- `results/pi05-2026-10-02/` — π₀.₅, 42 configurations × 30 episodes

Each directory holds `success_rates.csv`, `episode_outcomes.csv`, `artifact_manifest.csv` and `log_manifest.csv`. Videos are stored in Git LFS. Upstream figures quoted in Chapter 5 are taken from arXiv:2511.10276v2.

Files under `tools/rerun/`, `tools/data/` and the `make_*_figure.py` scripts belong to an earlier draft and are no longer used by the dissertation.

## Required before submission

- Fill the red fields in `dissertation-metadata.tex`.
- Replace the provisional declaration pages with the current NTU EEE wording, and update the signature dates.
- Disclose AI assistance truthfully under the rules applicable to the submission.
- Check the upstream values in Table 5.3 against the arXiv PDF.

The generated PDF is a review draft, not a submission-ready signed copy.
