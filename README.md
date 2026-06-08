---
title: Pocket Tutor
emoji: 🎒
colorFrom: green
colorTo: yellow
sdk: gradio
sdk_version: 6.17.3
app_file: app.py
python_version: "3.12"
short_description: Photo-first homework coaching for students and parents
pinned: false
tags:
- build-small-hackathon
- backyard-ai
- openbmb
- off-brand
- best-agent
- multimodal
- off-the-grid
- modal
- well-tuned
---

# Pocket Tutor

Pocket Tutor is a multimodal homework coach for students and parents. It accepts
a worksheet photo, a typed question, or microphone input, then returns a compact
tutoring plan: what the problem is asking, known information, a strategy, worked
steps, a quality check, the next hint, and a parent support note.

## Model Plan

- Primary model: `openbmb/MiniCPM-V-4.6` for image + text tutoring
- Text fallback: `openbmb/MiniCPM3-4B`
- Speech input: `openai/whisper-small` local transcription
- Fine-tuned adapter: `build-small-hackathon/pocket-tutor-minicpmv-socratic`
- Training: Modal A10G QLoRA on current app-format tutoring examples
- Parameter cap: every planned model is under the 32B hackathon limit

The app does not call an external answer API. If local model execution is still
loading or unavailable, it returns a deterministic tutoring scaffold instead of
silently failing.

## Hackathon Alignment

| Requirement | Pocket Tutor implementation |
|---|---|
| Gradio Space in `build-small-hackathon` | `build-small-hackathon/pocket-tutor` |
| Track | Backyard AI |
| Sponsor focus | OpenBMB MiniCPM-V multimodal tutoring |
| Merit targets | Off-Brand, Best Agent, Well-Tuned |
| Multimodal input | Image upload/webcam, typed question, microphone transcript |
| Fine-tuning | Modal QLoRA adapter trained on app-format Socratic tutoring examples |
| Demo/social links | Add final demo video and social post links after recording |

## Links

- GitHub Repo: https://github.com/awilliams88/pocket-tutor
- Hugging Face Space: https://huggingface.co/spaces/build-small-hackathon/pocket-tutor
- Fine-tuned Model: https://huggingface.co/build-small-hackathon/pocket-tutor-minicpmv-socratic
- Demo Video: pending final recording
- Social Post: pending final post

## Local Development

```bash
./run.sh setup
./run.sh app
./run.sh verify
```

## Codebase

| Path | Purpose |
|---|---|
| `app.py` | Hugging Face Spaces entry point |
| `env/` | Runtime patches, constants, model IDs, links |
| `core/` | Prompt orchestration, speech transcription, inference, parsing |
| `ui/` | Gradio layout, examples, custom chalkboard CSS |
| `modal/` | Modal QLoRA training job, synthetic dataset, adapter card |

## Safety

Pocket Tutor is meant to teach reasoning, not help students cheat. Requests for
active tests or exams should be redirected toward study guidance.

## Training Data

The Modal dataset includes math, science, reading, writing, statistics, blurry
image recovery, follow-up confusion, and explicit cheating refusal examples. The
training target is the current production UI format, not an earlier seed format.
