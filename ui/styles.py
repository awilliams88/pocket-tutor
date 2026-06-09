from __future__ import annotations

# CSS is grouped by visible app area so the design is easy to adjust.
CUSTOM_CSS = """
/* Page */
body {
    background: radial-gradient(circle at top, #111827 0%, #060816 52%, #02040b 100%) !important;
    color: #e5e7eb !important;
    font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
}

.gradio-container {
    background: radial-gradient(circle at top, #111827 0%, #060816 52%, #02040b 100%) !important;
    color: #e5e7eb !important;
    font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
}

.gradio-container .block {
    background: transparent !important;
}

.gradio-container .panel {
    background: transparent !important;
}

.gradio-container .form {
    background: transparent !important;
}

.gradio-container .row {
    background: transparent !important;
}

.gradio-container .wrap {
    background: transparent !important;
}

/* Header */
#pt-header {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    margin: 0 auto 0.75rem auto;
    padding: 0.35rem 0 0.75rem 0;
    text-align: center;
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
    max-width: 90%;
    margin: 0 auto 2rem auto;
    padding: 0.75rem 2.25rem !important;
    background: transparent !important;
    border: 2px solid oklch(70.4% 0.14 182.503) !important;
    box-shadow: none !important;
    text-align: center;
    color: #c7d2fe !important;
    font-size: 1.1rem !important;
    line-height: 1.6 !important;
    border-radius: 40px !important;
}

/* Main layout */
.pt-main-grid {
    align-items: stretch !important;
    gap: 1rem !important;
}

.pt-main-grid > .form {
    align-self: stretch !important;
}

.pt-main-grid > .block {
    align-self: stretch !important;
}

.pt-main-grid > div {
    align-self: stretch !important;
}

.pt-input-panel {
    background: linear-gradient(180deg, rgba(15, 23, 42, 0.96) 0%, rgba(12, 18, 35, 0.92) 100%) !important;
    border: 1px solid rgba(96, 165, 250, 0.18) !important;
    border-radius: 10px !important;
    box-shadow: 0 10px 24px rgba(0, 0, 0, 0.42) !important;
    display: flex !important;
    flex-direction: column !important;
    height: 100% !important;
    padding: 1.15rem !important;
}

.pt-input-panel h3 {
    color: #f8fafc !important;
    margin: 0 0 0.75rem 0 !important;
}

.pt-capture-panel {
    background: linear-gradient(180deg, rgba(15, 23, 42, 0.96) 0%, rgba(12, 18, 35, 0.92) 100%) !important;
    border: 1px solid rgba(96, 165, 250, 0.18) !important;
    border-radius: 10px !important;
    box-shadow: 0 10px 24px rgba(0, 0, 0, 0.42) !important;
    display: flex !important;
    flex-direction: column !important;
    height: 100% !important;
    padding: 1.15rem !important;
}

.pt-capture-panel h3 {
    color: #f8fafc !important;
    margin: 0 0 0.75rem 0 !important;
}

/* Question inputs */
#pt-question-input textarea {
    background: rgba(8, 15, 30, 0.96) !important;
    border: 1px solid rgba(103, 232, 249, 0.20) !important;
    border-radius: 10px !important;
    color: #f8fafc !important;
    line-height: 1.5 !important;
}

.pt-image-input {
    border-radius: 10px !important;
    overflow: hidden !important;
}

.pt-audio-input {
    border-radius: 10px !important;
    overflow: hidden !important;
}

.pt-run-btn {
    background: linear-gradient(135deg, #22c55e 0%, #14b8a6 100%) !important;
    border: none !important;
    border-radius: 10px !important;
    color: #04111a !important;
    font-weight: 760 !important;
    margin: 0.5rem auto 0 auto !important;
}

.pt-run-btn:hover {
    opacity: 0.92 !important;
}

.pt-teach-btn {
    margin-top: 0.35rem !important;
}

/* Teaching controls */
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
    color: #f8fafc !important;
    margin: 0 0 0.65rem 0 !important;
}

.pt-teach-btn {
    align-self: center !important;
    margin-top: 0.35rem !important;
    width: fit-content !important;
}

.pt-teach-btn button {
    min-width: 0 !important;
    padding: 0.78rem 1.35rem !important;
    width: fit-content !important;
}

/* Grade radio */
#pt-grade-control {
    background: transparent !important;
    border: none !important;
    border-radius: 0 !important;
    padding: 0 !important;
}

fieldset#pt-grade-control span[data-testid="block-info"] {
    background: transparent !important;
    color: #f8fafc !important;
    display: inline-block !important;
    margin-bottom: 0.65rem !important;
    padding: 0 !important;
    width: fit-content !important;
}

#pt-grade-control .wrap {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    display: flex !important;
    gap: 0.45rem !important;
}

#pt-grade-control .container {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

#pt-grade-control .input-container {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

#pt-grade-control label {
    background: rgba(15, 23, 42, 0.98) !important;
    border: 1px solid rgba(96, 165, 250, 0.18) !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
    cursor: pointer !important;
    flex: 1 1 auto !important;
    text-align: center !important;
}

#pt-grade-control label:has(input:checked) {
    background: rgba(14, 165, 233, 0.18) !important;
    border-color: rgba(103, 232, 249, 0.48) !important;
    color: #f8fafc !important;
}

/* Help mode radio */
#pt-mode-control {
    background: transparent !important;
    border: none !important;
    border-radius: 0 !important;
    padding: 0 !important;
}

fieldset#pt-mode-control span[data-testid="block-info"] {
    background: transparent !important;
    color: #f8fafc !important;
    display: inline-block !important;
    margin-bottom: 0.65rem !important;
    padding: 0 !important;
    width: fit-content !important;
}

#pt-mode-control .wrap {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    display: flex !important;
    gap: 0.45rem !important;
}

#pt-mode-control .container {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

#pt-mode-control .input-container {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

#pt-mode-control label {
    background: rgba(15, 23, 42, 0.98) !important;
    border: 1px solid rgba(96, 165, 250, 0.18) !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
    cursor: pointer !important;
    flex: 1 1 auto !important;
    text-align: center !important;
}

#pt-mode-control label:has(input:checked) {
    background: rgba(14, 165, 233, 0.18) !important;
    border-color: rgba(103, 232, 249, 0.48) !important;
    color: #f8fafc !important;
}

/* Results */
.pt-results-section {
    margin-top: 1rem !important;
    width: 100% !important;
}

.pt-analysis-section {
    background: linear-gradient(180deg, rgba(15, 23, 42, 0.96) 0%, rgba(12, 18, 35, 0.92) 100%) !important;
    border: 1px solid rgba(96, 165, 250, 0.18) !important;
    border-radius: 10px !important;
    box-shadow: 0 10px 24px rgba(0, 0, 0, 0.42) !important;
    padding: 1.15rem !important;
    width: 100% !important;
}

.pt-analysis-section h3 {
    color: #f8fafc !important;
    margin: 0 0 0.75rem 0 !important;
}

.pt-plan-grid {
    display: grid !important;
    grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr)) !important;
    gap: 1rem !important;
    align-items: stretch !important;
}

.pt-plan-grid > .form,
.pt-plan-grid > .block,
.pt-plan-grid > div,
.pt-workbench-grid > .form,
.pt-workbench-grid > .block,
.pt-workbench-grid > div {
    align-self: stretch !important;
    max-width: none !important;
    min-width: 0 !important;
    width: auto !important;
}

.pt-workbench-grid {
    display: grid !important;
    grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr)) !important;
    gap: 1rem !important;
    align-items: stretch !important;
}

/* Output text boxes */
.pt-output-card {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

.pt-output-card .wrap {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

.pt-output-card .container {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

.pt-output-card .input-container {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

.pt-output-card .generating {
    background: rgba(30, 41, 59, 0.88) !important;
    color: #ccfbf1 !important;
    border: 1px solid rgba(94, 234, 212, 0.24) !important;
    border-radius: 10px !important;
}

.pt-output-card [class*="progress"] {
    background: rgba(30, 41, 59, 0.88) !important;
    color: #ccfbf1 !important;
    border: 1px solid rgba(94, 234, 212, 0.24) !important;
    border-radius: 10px !important;
}

.pt-output-card:has(.generating) {
    background: rgba(15, 23, 42, 0.72) !important;
}

.pt-output-card:has(.generating) textarea {
    background: rgba(30, 41, 59, 0.88) !important;
    border-color: rgba(94, 234, 212, 0.32) !important;
    color: #ccfbf1 !important;
}

.pt-output-card textarea {
    background: rgba(15, 23, 42, 0.96) !important;
    border-radius: 10px !important;
    color: #f8fafc !important;
    font-size: 0.98rem !important;
    line-height: 1.5 !important;
    overflow-wrap: anywhere !important;
    padding: 0.85rem !important;
}

.pt-problem-card textarea {
    border: 1px solid rgba(103, 232, 249, 0.30) !important;
}

.pt-knowns-card textarea {
    border: 1px solid rgba(56, 189, 248, 0.24) !important;
}

.pt-strategy-card textarea {
    border: 1px solid rgba(45, 212, 191, 0.24) !important;
}

.pt-steps-card textarea {
    border: 1px solid rgba(103, 232, 249, 0.22) !important;
}

.pt-check-card textarea {
    border: 1px solid rgba(34, 197, 94, 0.26) !important;
}

.pt-hint-card textarea {
    border: 1px solid rgba(251, 146, 60, 0.26) !important;
}

.pt-parent-card textarea {
    border: 1px solid rgba(244, 114, 182, 0.26) !important;
}

/* Examples */
.pt-examples-section {
    background: linear-gradient(180deg, rgba(15, 23, 42, 0.96) 0%, rgba(12, 18, 35, 0.92) 100%) !important;
    border: 1px solid rgba(96, 165, 250, 0.18) !important;
    border-radius: 10px !important;
    box-shadow: 0 10px 24px rgba(0, 0, 0, 0.42) !important;
    margin-top: 1rem !important;
    padding: 1.15rem !important;
    width: 100% !important;
}

.pt-examples-section h3 {
    color: #f8fafc !important;
    margin: 0 0 0.75rem 0 !important;
}

.pt-example-grid {
    display: grid !important;
    grid-template-columns: repeat(auto-fit, minmax(18rem, 1fr)) !important;
    align-items: stretch !important;
    gap: 1rem !important;
}

.pt-example-grid > .form,
.pt-example-grid > .block,
.pt-example-grid > div {
    align-self: stretch !important;
    max-width: none !important;
    min-width: 0 !important;
    width: auto !important;
}

.pt-example-card {
    background: rgba(15, 23, 42, 0.96) !important;
    border: 1px solid rgba(103, 232, 249, 0.16) !important;
    border-radius: 10px !important;
    padding: 0.9rem !important;
    display: flex !important;
    flex-direction: column !important;
    height: 100% !important;
}

.pt-example-copy {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    flex: 1 1 auto;
}

.pt-example-head {
    color: #67e8f9;
    display: flex;
    gap: 0.8rem;
    font-weight: 700;
    justify-content: space-between;
}

.pt-example-head strong {
    color: #34d399;
    white-space: nowrap;
}

.pt-example-copy p {
    color: #e5e7eb;
    line-height: 1.45;
    margin: 0;
}

.pt-example-btn {
    background: rgba(20, 184, 166, 0.12) !important;
    border: 1px solid rgba(103, 232, 249, 0.28) !important;
    border-radius: 8px !important;
    color: #99f6e4 !important;
    margin-top: auto !important;
}

.pt-example-btn:hover {
    background: rgba(20, 184, 166, 0.18) !important;
}

/* Footer */
#pt-links {
    color: #bae6fd !important;
    margin-top: 1rem;
    text-align: center;
}

/* Diagnostics */
.pt-diagnostics-section {
    background: linear-gradient(180deg, rgba(15, 23, 42, 0.96) 0%, rgba(12, 18, 35, 0.92) 100%) !important;
    border: 1px solid rgba(96, 165, 250, 0.18) !important;
    border-radius: 10px !important;
    box-shadow: 0 10px 24px rgba(0, 0, 0, 0.42) !important;
    margin-top: 1rem !important;
    padding: 0.85rem !important;
}

.pt-diagnostics-section .label-wrap {
    color: #e0f2fe !important;
}

.pt-diagnostics-section .wrap {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

.pt-diagnostics-section .block {
    background: transparent !important;
    box-shadow: none !important;
}

.pt-log-box textarea {
    background: rgba(8, 15, 30, 0.96) !important;
    border: 1px solid rgba(103, 232, 249, 0.20) !important;
    border-radius: 10px !important;
    color: #f8fafc !important;
    line-height: 1.5 !important;
}

/* Remove Gradio card chrome inside our own panels. */
.pt-input-panel .block {
    background: transparent !important;
    box-shadow: none !important;
}

.pt-capture-panel .block {
    background: transparent !important;
    box-shadow: none !important;
}

.pt-analysis-section .block {
    background: transparent !important;
    box-shadow: none !important;
}

.pt-workbench-section .block {
    background: transparent !important;
    box-shadow: none !important;
}

.pt-examples-section .block {
    background: transparent !important;
    box-shadow: none !important;
}
"""
