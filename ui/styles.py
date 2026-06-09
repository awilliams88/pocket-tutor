from __future__ import annotations

# Gradio CSS overrides create a distinct chalkboard tutoring interface.
CUSTOM_CSS = """
body, .gradio-container {
    background: radial-gradient(circle at top, #111827 0%, #060816 52%, #02040b 100%) !important;
    color: #e5e7eb !important;
    font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
}

.gradio-container .block,
.gradio-container .panel,
.gradio-container .form,
.gradio-container .row,
.gradio-container .wrap {
    background: transparent !important;
}

#pt-header {
    text-align: center;
    margin: 0 auto 0.75rem auto;
    padding: 0.35rem 0 0.75rem 0;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}
#pt-header h1 {
    color: #a7f3d0 !important;
    font-size: 2.85rem !important;
    font-weight: 760 !important;
    letter-spacing: 0 !important;
    margin-bottom: 0.35rem !important;
}
#pt-header p {
    color: #cbd5e1 !important;
    font-size: 1.08rem !important;
    margin: 0 !important;
}
#pt-kicker {
    width: fit-content;
    max-width: 92%;
    margin: 0 auto 1.35rem auto;
    padding: 0.72rem 1.6rem !important;
    background: rgba(14, 165, 233, 0.10) !important;
    border: 1px solid rgba(103, 232, 249, 0.22) !important;
    border-radius: 10px !important;
    text-align: center;
    color: #e0f2fe !important;
}

.pt-main-grid, .pt-plan-grid, .pt-workbench-grid, .pt-example-grid {
    gap: 1rem !important;
}
.pt-input-panel, .pt-capture-panel, .pt-analysis-section, .pt-examples-section, .pt-workbench-section {
    background: linear-gradient(180deg, rgba(15, 23, 42, 0.96) 0%, rgba(12, 18, 35, 0.92) 100%) !important;
    border: 1px solid rgba(96, 165, 250, 0.18) !important;
    border-radius: 10px !important;
    box-shadow: 0 10px 24px rgba(0, 0, 0, 0.42) !important;
    padding: 1.15rem !important;
}
.pt-analysis-section, .pt-workbench-section, .pt-examples-section {
    width: 100% !important;
    margin-top: 1rem !important;
}
.pt-input-panel h3, .pt-capture-panel h3, .pt-analysis-section h3, .pt-examples-section h3 {
    color: #f8fafc !important;
    margin: 0 0 0.75rem 0 !important;
}

.pt-control-title {
    margin-top: 0.9rem !important;
    margin-bottom: 0.35rem !important;
    color: #7dd3fc !important;
}

.pt-control-stack {
    gap: 0.9rem !important;
}

.pt-control-card {
    background: rgba(17, 24, 39, 0.92) !important;
    border: 1px solid rgba(96, 165, 250, 0.16) !important;
    border-radius: 10px !important;
    padding: 0.9rem !important;
}
.pt-control-card h3 {
    margin: 0 0 0.65rem 0 !important;
    color: #f8fafc !important;
}

fieldset#pt-grade-control span[data-testid="block-info"],
fieldset#pt-mode-control span[data-testid="block-info"] {
    display: inline-block !important;
    width: fit-content !important;
    color: #f8fafc !important;
    background: transparent !important;
    padding: 0 !important;
    margin-bottom: 0.65rem !important;
}

#pt-grade-control,
#pt-mode-control {
    background: transparent !important;
    border: none !important;
    border-radius: 0 !important;
    padding: 0 !important;
}
#pt-grade-control .wrap,
#pt-mode-control .wrap,
#pt-grade-control .container,
#pt-mode-control .container,
#pt-grade-control .input-container,
#pt-mode-control .input-container {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}
#pt-grade-control .wrap,
#pt-mode-control .wrap {
    display: flex !important;
    gap: 0.45rem !important;
}
#pt-grade-control label,
#pt-mode-control label {
    flex: 1 1 auto !important;
    background: rgba(15, 23, 42, 0.98) !important;
    border: 1px solid rgba(96, 165, 250, 0.18) !important;
    border-radius: 8px !important;
    text-align: center !important;
    color: #e2e8f0 !important;
    cursor: pointer !important;
}
#pt-grade-control label:has(input:checked),
#pt-mode-control label:has(input:checked) {
    background: rgba(14, 165, 233, 0.18) !important;
    border-color: rgba(103, 232, 249, 0.48) !important;
    color: #f8fafc !important;
}
#pt-question-input textarea, .pt-log-box textarea {
    background: rgba(8, 15, 30, 0.96) !important;
    color: #f8fafc !important;
    border: 1px solid rgba(103, 232, 249, 0.20) !important;
    border-radius: 10px !important;
    line-height: 1.5 !important;
}
.pt-image-input, .pt-audio-input {
    border-radius: 10px !important;
    overflow: hidden !important;
}
.pt-run-btn {
    background: linear-gradient(135deg, #22c55e 0%, #14b8a6 100%) !important;
    color: #04111a !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 760 !important;
    margin: 0.5rem auto 0 auto !important;
}
.pt-run-btn:hover {
    opacity: 0.92 !important;
}
.pt-teach-btn {
    margin-top: 0.35rem !important;
}

.pt-output-card {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}
.pt-output-card textarea {
    background: rgba(15, 23, 42, 0.96) !important;
    color: #f8fafc !important;
    border-radius: 10px !important;
    font-size: 0.98rem !important;
    line-height: 1.5 !important;
    padding: 0.85rem !important;
    overflow-wrap: anywhere !important;
}
.pt-problem-card textarea { border: 1px solid rgba(103, 232, 249, 0.30) !important; }
.pt-knowns-card textarea { border: 1px solid rgba(56, 189, 248, 0.24) !important; }
.pt-strategy-card textarea { border: 1px solid rgba(45, 212, 191, 0.24) !important; }
.pt-steps-card textarea { border: 1px solid rgba(103, 232, 249, 0.22) !important; }
.pt-check-card textarea { border: 1px solid rgba(34, 197, 94, 0.26) !important; }
.pt-hint-card textarea { border: 1px solid rgba(251, 146, 60, 0.26) !important; }
.pt-parent-card textarea { border: 1px solid rgba(244, 114, 182, 0.26) !important; }

.pt-example-card {
    background: rgba(15, 23, 42, 0.96) !important;
    border: 1px solid rgba(103, 232, 249, 0.16) !important;
    border-radius: 10px !important;
    padding: 0.9rem !important;
    display: flex !important;
    flex-direction: column !important;
}
.pt-example-copy {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    flex: 1 1 auto;
}
.pt-example-head {
    display: flex;
    justify-content: space-between;
    gap: 0.8rem;
    color: #67e8f9;
    font-weight: 700;
}
.pt-example-head strong {
    color: #34d399;
    white-space: nowrap;
}
.pt-example-copy p {
    color: #e5e7eb;
    margin: 0;
    line-height: 1.45;
}
.pt-example-btn {
    border-radius: 8px !important;
    background: rgba(20, 184, 166, 0.12) !important;
    color: #99f6e4 !important;
    border: 1px solid rgba(103, 232, 249, 0.28) !important;
    margin-top: auto !important;
}
.pt-example-btn:hover {
    background: rgba(20, 184, 166, 0.18) !important;
}
#pt-links {
    text-align: center;
    margin-top: 1rem;
    color: #bae6fd !important;
}

.pt-input-panel .block,
.pt-capture-panel .block,
.pt-analysis-section .block,
.pt-workbench-section .block,
.pt-examples-section .block {
    background: transparent !important;
    box-shadow: none !important;
}
"""
