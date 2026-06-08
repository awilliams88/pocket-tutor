from __future__ import annotations

# Gradio CSS overrides create a distinct chalkboard tutoring interface.
CUSTOM_CSS = """
body, .gradio-container {
    background-color: #000000 !important;
    color: #e5e7eb !important;
    font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
}

#pt-header {
    text-align: center;
    margin: 0 auto 0.65rem auto;
    padding: 0.35rem 0 0.65rem 0;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}
#pt-header h1 {
    color: #a7f3d0 !important;
    font-size: 2.7rem !important;
    font-weight: 750 !important;
    letter-spacing: 0 !important;
    margin-bottom: 0.35rem !important;
}
#pt-header p {
    color: #d1d5db !important;
    font-size: 1.08rem !important;
    margin: 0 !important;
}
#pt-kicker {
    width: fit-content;
    max-width: 92%;
    margin: 0 auto 1.5rem auto;
    padding: 0.7rem 1.6rem !important;
    background-color: rgba(22, 101, 52, 0.22) !important;
    border: 1px solid rgba(167, 243, 208, 0.24) !important;
    border-radius: 8px !important;
    text-align: center;
    color: #dcfce7 !important;
}

.pt-main-grid, .pt-plan-grid, .pt-workbench-grid, .pt-example-grid, .pt-control-row {
    gap: 1rem !important;
    align-items: stretch !important;
}
.pt-main-grid > .form, .pt-main-grid > .row, .pt-main-grid > div,
.pt-plan-grid > .form, .pt-plan-grid > .row, .pt-plan-grid > div,
.pt-workbench-grid > .form, .pt-workbench-grid > .row, .pt-workbench-grid > div,
.pt-example-grid > .form, .pt-example-grid > .row, .pt-example-grid > div {
    display: flex !important;
    flex-wrap: wrap !important;
    gap: 1rem !important;
}
.pt-input-panel, .pt-capture-panel, .pt-analysis-section, .pt-examples-section {
    background-color: #050505 !important;
    border: 1px solid rgba(167, 243, 208, 0.14) !important;
    border-radius: 8px !important;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.42) !important;
    padding: 1.15rem !important;
}
.pt-analysis-section, .pt-examples-section {
    margin-top: 1rem !important;
}
.pt-input-panel, .pt-capture-panel {
    flex: 1 1 330px !important;
}
.pt-input-panel h3, .pt-capture-panel h3, .pt-analysis-section h3, .pt-examples-section h3 {
    color: #f9fafb !important;
    margin: 0 0 0.75rem 0 !important;
}

.pt-control-title {
    margin-top: 0.9rem !important;
    margin-bottom: 0.35rem !important;
    color: #bbf7d0 !important;
}

#pt-question-input textarea, .pt-log-box textarea {
    background-color: #010101 !important;
    color: #f8fafc !important;
    border: 1px solid rgba(167, 243, 208, 0.22) !important;
    border-radius: 8px !important;
    line-height: 1.5 !important;
}
.pt-image-input, .pt-audio-input {
    border-radius: 8px !important;
    overflow: hidden !important;
}
.pt-run-btn {
    background: linear-gradient(135deg, #16a34a 0%, #22c55e 100%) !important;
    color: #04110d !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 750 !important;
    min-height: 50px !important;
}
.pt-run-btn:hover {
    opacity: 0.9 !important;
}
.pt-teach-btn {
    margin-top: 0.35rem !important;
}

.pt-output-card {
    min-width: 0 !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}
.pt-card-grid .block {
    flex: 1 1 280px !important;
    min-width: 0 !important;
}
.pt-output-card textarea {
    background-color: #010101 !important;
    color: #f8fafc !important;
    border-radius: 8px !important;
    font-size: 0.98rem !important;
    line-height: 1.5 !important;
    padding: 0.85rem !important;
    overflow-wrap: anywhere !important;
}
.pt-problem-card textarea { border: 1px solid rgba(134, 239, 172, 0.48) !important; }
.pt-knowns-card textarea { border: 1px solid rgba(250, 204, 21, 0.48) !important; }
.pt-strategy-card textarea { border: 1px solid rgba(96, 165, 250, 0.48) !important; }
.pt-steps-card textarea { border: 1px solid rgba(167, 139, 250, 0.48) !important; }
.pt-check-card textarea { border: 1px solid rgba(34, 197, 94, 0.48) !important; }
.pt-hint-card textarea { border: 1px solid rgba(251, 146, 60, 0.48) !important; }
.pt-parent-card textarea { border: 1px solid rgba(244, 114, 182, 0.48) !important; }

.pt-example-card {
    flex: 1 1 245px !important;
    background-color: #010101 !important;
    border: 1px solid rgba(167, 243, 208, 0.12) !important;
    border-radius: 8px !important;
    padding: 0.85rem !important;
}
.pt-example-copy {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}
.pt-example-head {
    display: flex;
    justify-content: space-between;
    gap: 0.8rem;
    color: #ecfccb;
    font-weight: 700;
}
.pt-example-head strong {
    color: #86efac;
    white-space: nowrap;
}
.pt-example-copy p {
    color: #d1fae5;
    margin: 0;
    line-height: 1.45;
}
.pt-example-btn {
    border-radius: 8px !important;
}
#pt-links {
    text-align: center;
    margin-top: 1rem;
    color: #bbf7d0 !important;
}
"""
