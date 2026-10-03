# A Vision-Language-Action Benchmark for Mobile Manipulation in Retail Environments

This project contains the LaTeX source for the candidate's dissertation on evaluating vision-language-action models for mobile manipulation in retail environments.

## 本轮两模型评测对照

[旧论文实验与 Octo、π₀.₅ 新评测的详细对照及正文替换清单](docs/EXPERIMENT_REPLACEMENT_zh.md)。原始汇总数据与逐配置并列表见 [data/reproduced-2026-10-02](data/reproduced-2026-10-02)。论文 LaTeX 正文尚未按新结果改写。

## Build

Compile `main.tex` with XeLaTeX/BibTeX, or with Tectonic 0.16.9:

```text
tectonic main.tex --keep-logs
```

## Required before submission

- Fill the red fields in `dissertation-metadata.tex`.
- Replace the provisional declaration pages with the current NTU EEE wording.
- Disclose AI assistance truthfully under the rules applicable to the submission.
- Verify every experiment number against the final paper, dataset and code revision.

The generated PDF is a review draft, not a submission-ready signed copy.
