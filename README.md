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

**Pocket Tutor** is a private, multimodal homework coach for students and parents. It accepts a worksheet photo, a typed question, or microphone input, then returns a compact tutoring plan: what the problem is asking, known information, a strategy, worked steps, a quality check, the next hint, and a parent support note.

The app runs on a dedicated OpenBMB MiniCPM-V vision-language model inside the Hugging Face Space runtime. There is no external answer API, so the tutoring flow stays local to the Space and follows the same production output structure used during fine-tuning.

Pocket Tutor is a tutoring tool, not a cheating tool. Requests for active tests or exams should be redirected toward study guidance instead of direct answers.

### Links

- **Demo**: pending final recording
- **Social Post**: pending final LinkedIn post
- **GitHub Repo**: [awilliams88/pocket-tutor](https://github.com/awilliams88/pocket-tutor)
- **Hugging Face Space**: [build-small-hackathon/pocket-tutor](https://huggingface.co/spaces/build-small-hackathon/pocket-tutor)
- **Fine-tuned Model**: [build-small-hackathon/pocket-tutor-minicpmv-socratic](https://huggingface.co/build-small-hackathon/pocket-tutor-minicpmv-socratic)

## Hackathon Alignment

| Requirement | Pocket Tutor implementation |
|---|---|
| Gradio Space in `build-small-hackathon` | `build-small-hackathon/pocket-tutor` |
| Track | Backyard AI |
| Sponsor focus | OpenBMB MiniCPM-V multimodal tutoring |
| Merit targets | Off-Brand, Best Agent, Well-Tuned, Off the Grid |
| Multimodal input | Image upload/webcam, typed question, microphone transcript |
| Fine-tuning | Modal QLoRA adapter trained on app-format Socratic tutoring examples |

## What It Does

Write or upload a homework prompt, then let Pocket Tutor break it into the same structured response used by the model and UI:

| Section | Description |
|---|---|
| **Problem Read** | What the problem is asking |
| **Knowns** | Relevant facts extracted from the prompt or image |
| **Strategy** | The most useful method for solving it |
| **Worked Steps** | Compact step-by-step reasoning |
| **Check** | A quick correctness check |
| **Next Hint** | A Socratic follow-up hint |
| **Parent Note** | A short note for a parent or helper |

The app supports:

- worksheet photo input
- typed homework questions
- microphone-based question capture
- short, structured tutoring answers
- refusal of active test or exam solving

## Fine-Tuned Model

The inference engine uses a QLoRA-adapted version of [`openbmb/MiniCPM-V-4.6`](https://huggingface.co/openbmb/MiniCPM-V-4.6), trained specifically for the Pocket Tutor output format.

**Why fine-tune instead of only prompting?**
The base model is general-purpose. Fine-tuning teaches it the exact tutoring voice, the section layout, the refusal style, and the compact Socratic coaching pattern expected by the app. That makes the output more consistent than prompt-only steering.

**Training details:**
- Method: QLoRA with 4-bit NF4 quantization
- Hardware: Modal A10G
- Dataset: 16 structured tutoring examples plus 5 short follow-up coaching examples
- Output format: current production UI sections, not an older seed format
- Coverage: math, science, reading, writing, statistics, blurry image recovery, parent notes, and cheat-refusal examples
- Runtime pairing: the same MiniCPM-V base model used by the Space

The fine-tuned LoRA adapter is published at [`build-small-hackathon/pocket-tutor-minicpmv-socratic`](https://huggingface.co/build-small-hackathon/pocket-tutor-minicpmv-socratic) and is loaded automatically on top of the base model at startup.

## Inference Architecture

```
User Input (photo, text, or mic transcript)
        │
        ▼
┌─────────────────────┐
│    Gradio UI        │  ui/layout.py — dark classroom dashboard
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Analyzer           │  core/analyzer.py — prompt construction & dispatch
└──────────┬──────────┘
           │
     ┌─────┴──────┐
     ▼            ▼
┌─────────┐  ┌──────────┐
│Inference│  │  Parser  │  core/inference.py — model execution
│ Engine  │  │  Engine  │  core/parser.py — section splitting
└────┬────┘  └──────────┘
     │
     └── Space runtime: MiniCPM-V base model + LoRA adapter via `PeftModel`
```

**Inference priority:**
1. Dedicated multimodal model on the Space runtime with the fine-tuned adapter.
2. If model execution fails, return a deterministic tutoring scaffold instead of silently failing.
3. Do not route homework text to a separate answer API.

## Local Development

**Setup:**
```bash
./run.sh setup
```

**Run locally:**
```bash
./run.sh app
```

**Quality checks**:
```bash
./run.sh verify
```

**Smoke tests**:
```bash
modal run modal/smoke.py
python scripts/smoke_space.py
```

The Modal smoke test loads the production base model and LoRA adapter on Modal
and checks the returned section contract directly. The Space smoke test calls
the deployed Gradio API endpoint and verifies that `Check`, `Next Hint`, and
`Parent Note` are generated by the model instead of falling back to the default
placeholder text.

## Codebase

### Root
| File | Purpose |
|---|---|
| `app.py` | Hugging Face Spaces entry point |

### `env/` - App infrastructure
| File | Purpose |
|---|---|
| `env/config.py` | Central constants - model IDs, repo URLs, limits |
| `env/runtime.py` | Env var loader and asyncio cleanup patch |

### `core/` - Business logic
| File | Purpose |
|---|---|
| `core/analyzer.py` | Tutoring orchestrator and model dispatch |
| `core/inference.py` | Lazy model loader and local inference |
| `core/parser.py` | Output section splitter |

### `ui/` - Presentation
| File | Purpose |
|---|---|
| `ui/layout.py` | Gradio layout, components, and event wiring |
| `ui/styles.py` | Custom chalkboard CSS and component styling |

### `modal/` - Remote fine-tuning
| File | Purpose |
|---|---|
| `modal/tune.py` | QLoRA fine-tuning orchestrator |
| `modal/dataset.py` | Tutoring dataset and prompt builders |
| `modal/CARD.md` | Hugging Face model card for the LoRA adapter |

## Tech Stack

- **Model**: `openbmb/MiniCPM-V-4.6` + custom LoRA adapter (`build-small-hackathon/pocket-tutor-minicpmv-socratic`)
- **Fine-tuning**: QLoRA via `peft` + `trl` SFTTrainer on Modal A10G
- **Inference**: `transformers` + `peft` + `accelerate`
- **UI**: Gradio 6 with custom CSS
- **Hosting**: Hugging Face Spaces
- **Sponsor**: [OpenBMB](https://github.com/OpenBMB)

## Safety

Pocket Tutor is designed to teach reasoning, not help students cheat. It should redirect active test and exam requests toward study guidance and worked practice.

## Training Data

The Modal dataset includes math, science, reading, writing, statistics, blurry image recovery, parent-note coaching, and explicit cheating refusal examples. The training target is the current production UI format, not an earlier seed format.
