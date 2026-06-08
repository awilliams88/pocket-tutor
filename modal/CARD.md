---
base_model: openbmb/MiniCPM3-4B
library_name: peft
pipeline_tag: text-generation
language:
- en
tags:
- peft
- lora
- qlora
- tutoring
- education
- multimodal
- build-small-hackathon
---

# Pocket Tutor Socratic LoRA

Pocket Tutor Socratic LoRA is a QLoRA adapter trained for the Pocket Tutor
Space. The production app uses OpenBMB vision-language input when available and
falls back to this compact MiniCPM text adapter for typed or transcribed
homework questions.

## Intended Use

- Explaining homework from photos, typed questions, or microphone input
- Producing concise Socratic hints and step-by-step support
- Helping parents ask better guiding questions
- Refusing requests to cheat on active tests or exams

## Output Format

The adapter is trained on the current production UI format:

```text
=== PROBLEM READ ===
=== KNOWNS ===
=== STRATEGY ===
=== WORKED STEPS ===
=== CHECK ===
=== NEXT HINT ===
=== PARENT NOTE ===
```

## Training Recipe

- Base model: `openbmb/MiniCPM3-4B`
- Method: QLoRA with 4-bit NF4 quantization
- Hardware: Modal NVIDIA A10G
- Training data: synthetic app-format tutoring examples and short follow-up turns
- Sequence length: 1536 tokens
- Runtime pairing: OpenBMB MiniCPM-V for image context plus adapter-backed text tutoring

## Limitations

This model can make mistakes and should not be used to cheat on graded work. It
is designed to teach process and reasoning, not replace a teacher.
