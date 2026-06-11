---
base_model: openbmb/MiniCPM-V-4.6
library_name: peft
pipeline_tag: image-text-to-text
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
Space. The production app uses OpenBMB MiniCPM-V-4.6 for typed questions,
worksheet images, and transcribed microphone input through one dedicated
vision-language runtime.

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

- Base model: `openbmb/MiniCPM-V-4.6`
- Method: QLoRA with 4-bit NF4 quantization
- Hardware: Modal NVIDIA A10G
- Training data: 16 structured tutoring examples plus 7 schema-aligned follow-up turns
- Sequence length: 1536 tokens
- Runtime pairing: the same MiniCPM-V base model used by the Pocket Tutor Space

## Validation

The adapter is smoke-tested on Modal against every structured training example
and follow-up turn. The smoke test fails if any of the seven production UI
sections fall back to default placeholder text.

## Limitations

This model can make mistakes and should not be used to cheat on graded work. It
is designed to teach process and reasoning, not replace a teacher.
