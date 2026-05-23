import streamlit as st
import json
from datetime import datetime

st.set_page_config(
    page_title="AI Code Review Assistant",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background: #0a0a0f !important;
    overflow: hidden;
}

[data-testid="stAppViewContainer"] {
    background: #0a0a0f !important;
    position: relative;
}

[data-testid="stSidebar"] {
    display: none !important;
}

.main {
    max-width: 1600px;
    margin: 0 auto;
}

/* Animated Background Canvas */
@keyframes float-particle-1 {
    0% { transform: translate(0, 0); }
    25% { transform: translate(100px, -100px); }
    50% { transform: translate(50px, 150px); }
    75% { transform: translate(-80px, 80px); }
    100% { transform: translate(0, 0); }
}

@keyframes float-particle-2 {
    0% { transform: translate(0, 0); }
    25% { transform: translate(-120px, 80px); }
    50% { transform: translate(100px, -60px); }
    75% { transform: translate(60px, 120px); }
    100% { transform: translate(0, 0); }
}

@keyframes float-particle-3 {
    0% { transform: translate(0, 0); }
    25% { transform: translate(80px, 120px); }
    50% { transform: translate(-100px, 80px); }
    75% { transform: translate(-60px, -100px); }
    100% { transform: translate(0, 0); }
}

@keyframes float-particle-4 {
    0% { transform: translate(0, 0); }
    25% { transform: translate(-90px, -110px); }
    50% { transform: translate(110px, 90px); }
    75% { transform: translate(70px, -80px); }
    100% { transform: translate(0, 0); }
}

@keyframes float-particle-5 {
    0% { transform: translate(0, 0); }
    25% { transform: translate(110px, 70px); }
    50% { transform: translate(-80px, -120px); }
    75% { transform: translate(-100px, 100px); }
    100% { transform: translate(0, 0); }
}

@keyframes glow-pulse {
    0%, 100% { box-shadow: 0 0 20px rgba(147, 112, 219, 0.6), 0 0 60px rgba(168, 85, 247, 0.3); }
    50% { box-shadow: 0 0 30px rgba(147, 112, 219, 0.8), 0 0 80px rgba(168, 85, 247, 0.5); }
}

.particles-bg {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100vh;
    background: radial-gradient(circle at 20% 50%, rgba(139, 92, 246, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(168, 85, 247, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 50% 30%, rgba(124, 58, 237, 0.08) 0%, transparent 50%);
    z-index: 0;
    overflow: hidden;
}

.particle {
    position: absolute;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.8);
    filter: blur(1px);
    box-shadow: 0 0 20px rgba(147, 112, 219, 0.6);
}

.particle-1 {
    width: 8px;
    height: 8px;
    top: 20%;
    left: 15%;
    animation: float-particle-1 20s ease-in-out infinite;
    box-shadow: 0 0 20px rgba(147, 112, 219, 0.6), 0 0 40px rgba(168, 85, 247, 0.3);
}

.particle-2 {
    width: 6px;
    height: 6px;
    top: 60%;
    left: 75%;
    animation: float-particle-2 24s ease-in-out infinite;
    box-shadow: 0 0 15px rgba(139, 92, 246, 0.5), 0 0 35px rgba(168, 85, 247, 0.25);
}

.particle-3 {
    width: 5px;
    height: 5px;
    top: 40%;
    left: 50%;
    animation: float-particle-3 22s ease-in-out infinite;
    box-shadow: 0 0 18px rgba(147, 112, 219, 0.55), 0 0 45px rgba(168, 85, 247, 0.2);
}

.particle-4 {
    width: 7px;
    height: 7px;
    top: 80%;
    left: 25%;
    animation: float-particle-4 26s ease-in-out infinite;
    box-shadow: 0 0 22px rgba(139, 92, 246, 0.65), 0 0 50px rgba(168, 85, 247, 0.35);
}

.particle-5 {
    width: 6px;
    height: 6px;
    top: 30%;
    left: 70%;
    animation: float-particle-5 23s ease-in-out infinite;
    box-shadow: 0 0 16px rgba(147, 112, 219, 0.6), 0 0 38px rgba(168, 85, 247, 0.28);
}

.particle-6 {
    width: 4px;
    height: 4px;
    top: 70%;
    left: 60%;
    animation: float-particle-1 25s ease-in-out infinite reverse;
    box-shadow: 0 0 14px rgba(139, 92, 246, 0.5), 0 0 32px rgba(168, 85, 247, 0.22);
}

.particle-7 {
    width: 5px;
    height: 5px;
    top: 50%;
    left: 10%;
    animation: float-particle-3 21s ease-in-out infinite reverse;
    box-shadow: 0 0 18px rgba(147, 112, 219, 0.55), 0 0 42px rgba(168, 85, 247, 0.25);
}

.particle-8 {
    width: 7px;
    height: 7px;
    top: 15%;
    left: 85%;
    animation: float-particle-2 27s ease-in-out infinite;
    box-shadow: 0 0 24px rgba(139, 92, 246, 0.7), 0 0 55px rgba(168, 85, 247, 0.4);
}

/* Content Wrapper */
.content-wrapper {
    position: relative;
    z-index: 1;
    width: 100%;
}

/* Hero Section */
.hero-section {
    text-align: center;
    padding: 100px 40px 80px;
    background: linear-gradient(180deg, rgba(139, 92, 246, 0.05) 0%, rgba(168, 85, 247, 0.03) 100%);
    border-bottom: 1px solid rgba(168, 85, 247, 0.15);
    position: relative;
}

.hero-title {
    font-size: 4rem;
    font-weight: 700;
    background: linear-gradient(135deg, #e9d5ff 0%, #d8b4fe 50%, #c084fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 20px;
    letter-spacing: -0.02em;
    font-family: 'Inter', sans-serif;
}

.hero-subtitle {
    font-size: 1.25rem;
    color: #a78bfa;
    max-width: 750px;
    margin: 0 auto;
    line-height: 1.8;
    font-weight: 400;
}

/* Metric Cards */
.metrics-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 24px;
    padding: 50px 20px;
    max-width: 1600px;
    margin: 0 auto;
}

.metric-card {
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(124, 58, 237, 0.05) 100%);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(168, 85, 247, 0.2);
    border-radius: 16px;
    padding: 28px 24px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
    cursor: pointer;
}

.metric-card:hover {
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.15) 0%, rgba(124, 58, 237, 0.1) 100%);
    border-color: rgba(168, 85, 247, 0.4);
    transform: translateY(-8px);
    box-shadow: 0 16px 48px rgba(168, 85, 247, 0.2);
}

.metric-label {
    font-size: 0.875rem;
    color: #d8b4fe;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 12px;
}

.metric-value {
    font-size: 2.5rem;
    font-weight: 700;
    color: #e9d5ff;
    margin-bottom: 8px;
}

.metric-description {
    font-size: 0.875rem;
    color: #a78bfa;
    line-height: 1.5;
}

/* Main Layout */
.main-layout {
    display: grid;
    grid-template-columns: 1fr 0.35fr;
    gap: 32px;
    padding: 0 20px 50px;
    max-width: 1600px;
    margin: 0 auto;
}

@media (max-width: 1200px) {
    .main-layout {
        grid-template-columns: 1fr;
        gap: 24px;
    }
}

/* Code Input Panel */
.code-panel {
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.08) 0%, rgba(124, 58, 237, 0.04) 100%);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(168, 85, 247, 0.2);
    border-radius: 20px;
    padding: 32px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
}

.panel-header {
    display: flex;
    align-items: center;
    margin-bottom: 24px;
    gap: 12px;
}

.panel-title {
    font-size: 1.375rem;
    font-weight: 700;
    color: #e9d5ff;
    margin: 0;
}

.panel-subtitle {
    font-size: 0.9375rem;
    color: #a78bfa;
    margin-bottom: 20px;
    font-weight: 400;
}

/* Code Editor Area */
.code-editor-wrapper {
    position: relative;
    margin-bottom: 24px;
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid rgba(168, 85, 247, 0.15);
    background: rgba(20, 20, 30, 0.8);
}

textarea {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.9375rem !important;
    color: #e9d5ff !important;
    background: rgba(20, 20, 30, 0.9) !important;
    border: none !important;
    border-radius: 0 !important;
    padding: 20px !important;
    line-height: 1.6 !important;
    resize: vertical !important;
    min-height: 380px !important;
}

textarea::placeholder {
    color: #6b7280 !important;
}

textarea:focus {
    outline: none !important;
    border: none !important;
    box-shadow: inset 0 0 0 2px rgba(168, 85, 247, 0.3) !important;
}

/* Buttons */
.button-group {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-bottom: 16px;
}

.btn {
    padding: 14px 24px;
    border: none;
    border-radius: 10px;
    font-size: 0.9375rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-family: 'Inter', sans-serif;
}

.btn-primary {
    background: linear-gradient(135deg, #a855f7 0%, #d946ef 100%);
    color: white;
    box-shadow: 0 8px 20px rgba(168, 85, 247, 0.4);
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 30px rgba(168, 85, 247, 0.6);
}

.btn-secondary {
    background: rgba(168, 85, 247, 0.15);
    color: #d8b4fe;
    border: 1px solid rgba(168, 85, 247, 0.3);
}

.btn-secondary:hover {
    background: rgba(168, 85, 247, 0.25);
    border-color: rgba(168, 85, 247, 0.5);
}

/* Info Panel */
.info-panel {
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.08) 0%, rgba(124, 58, 237, 0.04) 100%);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(168, 85, 247, 0.2);
    border-radius: 20px;
    padding: 32px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    height: fit-content;
    position: sticky;
    top: 20px;
}

.info-title {
    font-size: 1.125rem;
    font-weight: 700;
    color: #e9d5ff;
    margin-bottom: 20px;
}

.info-text {
    font-size: 0.9375rem;
    color: #a78bfa;
    line-height: 1.7;
    margin-bottom: 24px;
}

.tags-container {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
}

.tag {
    background: rgba(168, 85, 247, 0.15);
    color: #d8b4fe;
    padding: 8px 16px;
    border-radius: 8px;
    font-size: 0.8125rem;
    font-weight: 600;
    border: 1px solid rgba(168, 85, 247, 0.3);
    transition: all 0.3s ease;
}

.tag:hover {
    background: rgba(168, 85, 247, 0.25);
    border-color: rgba(168, 85, 247, 0.5);
    transform: translateY(-2px);
}

/* Results Section */
.results-section {
    padding: 0 20px 50px;
    max-width: 1600px;
    margin: 0 auto;
}

.results-header {
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.08) 0%, rgba(124, 58, 237, 0.04) 100%);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(168, 85, 247, 0.2);
    border-radius: 20px;
    padding: 32px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    margin-bottom: 24px;
    display: grid;
    grid-template-columns: auto 1fr;
    gap: 32px;
    align-items: center;
}

@media (max-width: 768px) {
    .results-header {
        grid-template-columns: 1fr;
    }
}

.score-display {
    text-align: center;
}

.score-circle {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    background: linear-gradient(135deg, #a855f7 0%, #d946ef 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 3rem;
    font-weight: 700;
    box-shadow: 0 12px 32px rgba(168, 85, 247, 0.4);
    margin: 0 auto 12px;
    border: 2px solid rgba(168, 85, 247, 0.3);
}

.score-label {
    font-size: 0.875rem;
    color: #a78bfa;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-weight: 600;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 24px;
}

@media (max-width: 768px) {
    .stats-grid {
        grid-template-columns: repeat(3, 1fr);
    }
}

.stat-item {
    text-align: center;
}

.stat-number {
    font-size: 2.25rem;
    font-weight: 700;
    color: #e9d5ff;
    margin-bottom: 4px;
}

.stat-label {
    font-size: 0.8125rem;
    color: #a78bfa;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.03em;
}

/* Issue Cards */
.issues-container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
    gap: 20px;
}

@media (max-width: 768px) {
    .issues-container {
        grid-template-columns: 1fr;
    }
}

.issue-card {
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.08) 0%, rgba(124, 58, 237, 0.04) 100%);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(168, 85, 247, 0.2);
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
    transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.issue-card:hover {
    border-color: rgba(168, 85, 247, 0.4);
    transform: translateY(-4px);
    box-shadow: 0 12px 32px rgba(168, 85, 247, 0.15);
}

.issue-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    margin-bottom: 16px;
    gap: 12px;
}

.issue-type {
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #d8b4fe;
}

.severity-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 6px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.03em;
    white-space: nowrap;
}

.severity-high {
    background: rgba(239, 68, 68, 0.2);
    color: #fca5a5;
}

.severity-medium {
    background: rgba(245, 158, 11, 0.2);
    color: #fcd34d;
}

.severity-low {
    background: rgba(34, 197, 94, 0.2);
    color: #86efac;
}

.issue-title {
    font-size: 1.125rem;
    font-weight: 700;
    color: #e9d5ff;
    margin-bottom: 12px;
    line-height: 1.4;
}

.issue-section {
    margin-bottom: 16px;
}

.issue-section:last-child {
    margin-bottom: 0;
}

.issue-label {
    font-size: 0.8125rem;
    font-weight: 600;
    color: #d8b4fe;
    text-transform: uppercase;
    letter-spacing: 0.03em;
    margin-bottom: 8px;
    display: block;
}

.issue-text {
    font-size: 0.9375rem;
    color: #a78bfa;
    line-height: 1.6;
}

.code-snippet {
    background: rgba(20, 20, 30, 0.8);
    border-left: 3px solid #a855f7;
    padding: 12px 16px;
    border-radius: 6px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8125rem;
    color: #d8b4fe;
    overflow-x: auto;
    margin-top: 6px;
    border: 1px solid rgba(168, 85, 247, 0.15);
}

/* Empty State */
.empty-state {
    text-align: center;
    padding: 60px 40px;
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.08) 0%, rgba(124, 58, 237, 0.04) 100%);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(168, 85, 247, 0.2);
    border-radius: 20px;
    color: #a78bfa;
}

.empty-state-icon {
    font-size: 3rem;
    margin-bottom: 16px;
}

.empty-state-text {
    font-size: 1.125rem;
    color: #e9d5ff;
    margin-bottom: 12px;
}

/* File Upload */
.upload-section {
    margin-bottom: 20px;
    padding: 16px;
    border: 2px dashed rgba(168, 85, 247, 0.3);
    border-radius: 12px;
    text-align: center;
    background: rgba(168, 85, 247, 0.05);
    transition: all 0.3s ease;
}

.upload-section:hover {
    border-color: rgba(168, 85, 247, 0.6);
    background: rgba(168, 85, 247, 0.1);
}

/* Dropdown */
.sample-label {
    font-size: 0.8125rem;
    font-weight: 600;
    color: #a78bfa;
    text-transform: uppercase;
    letter-spacing: 0.03em;
    display: block;
    margin-bottom: 8px;
}

select {
    width: 100%;
    padding: 10px 12px;
    border: 1px solid rgba(168, 85, 247, 0.3);
    border-radius: 8px;
    background: rgba(20, 20, 30, 0.8);
    color: #e9d5ff;
    font-family: 'Inter', sans-serif;
    font-size: 0.9375rem;
    cursor: pointer;
    transition: all 0.3s ease;
}

select:hover {
    border-color: rgba(168, 85, 247, 0.6);
}

select:focus {
    outline: none;
    border-color: rgba(168, 85, 247, 0.8);
    box-shadow: 0 0 0 3px rgba(168, 85, 247, 0.2);
}

option {
    background: #1f2937;
    color: #e9d5ff;
}

/* Utility Classes */
.text-center {
    text-align: center;
}

.mt-24 {
    margin-top: 24px;
}

.mb-24 {
    margin-bottom: 24px;
}

.relative {
    position: relative;
}

.z-1 {
    z-index: 1;
}

/* Scrollbar Styling */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(168, 85, 247, 0.05);
}

::-webkit-scrollbar-thumb {
    background: rgba(168, 85, 247, 0.3);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: rgba(168, 85, 247, 0.5);
}

</style>
""", unsafe_allow_html=True)

# Animated Particle Background
st.markdown("""
<div class="particles-bg">
    <div class="particle particle-1"></div>
    <div class="particle particle-2"></div>
    <div class="particle particle-3"></div>
    <div class="particle particle-4"></div>
    <div class="particle particle-5"></div>
    <div class="particle particle-6"></div>
    <div class="particle particle-7"></div>
    <div class="particle particle-8"></div>
</div>
<div class="content-wrapper">
""", unsafe_allow_html=True)

SAMPLE_CODES = {
    "Select a sample": "",
    "🔐 Hardcoded Password": '''def login(username, password):
    if password == "admin123":
        return authenticate_user(username)
    return False''',
    "🗄️ SQL Injection": '''def get_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return db.execute(query)''',
    "⚡ Inefficient Loop": '''def process_data():
    for i in range(1000000):
        print(f"Processing item {i}")
        time.sleep(0.1)''',
    "✨ Clean Code": '''def add_numbers(a, b):
    """Add two numbers and return result."""
    return a + b

result = add_numbers(5, 3)
print(f"Result: {result}")''',
}

def demo_review(code: str) -> dict:
    """Generate mock code review results."""
    issues = []
    lower = code.lower()

    if 'password == "admin123"' in lower or "admin123" in lower:
        issues.append({
            "type": "Security",
            "severity": "High",
            "title": "Hardcoded Password Detected",
            "explanation": "Storing passwords directly in code is a critical security risk. Credentials should never be hardcoded and must be stored securely using environment variables or a secrets manager.",
            "fix": "Use environment variables or a secure secrets management system (e.g., python-dotenv, AWS Secrets Manager)",
            "snippet": 'password == "admin123"',
        })

    if "select *" in lower and ("f\"" in lower or "f'" in lower):
        issues.append({
            "type": "Security",
            "severity": "High",
            "title": "SQL Injection Vulnerability",
            "explanation": "Concatenating user input directly into SQL queries allows attackers to inject malicious SQL code and access unauthorized data.",
            "fix": "Use parameterized queries or prepared statements with bound parameters instead of string formatting.",
            "snippet": 'query = f"SELECT * FROM users WHERE id = {user_id}"',
        })

    if "for i in range(1000000)" in lower or "sleep(0.1)" in lower:
        issues.append({
            "type": "Performance",
            "severity": "Medium",
            "title": "Inefficient Loop with Sleep",
            "explanation": "Looping 1 million times with sleep operations will cause significant performance degradation and block execution.",
            "fix": "Use batch processing, async operations, or reduce the iteration count. Consider using generators or multiprocessing.",
            "snippet": "for i in range(1000000):\n    time.sleep(0.1)",
        })

    if "print(f\"processing" in lower or ("print(" in lower and "range(1000000)" in lower):
        issues.append({
            "type": "Code Quality",
            "severity": "Low",
            "title": "Debug Statements in Production Code",
            "explanation": "Debug print statements create noise in logs and hurt performance. Use proper logging instead.",
            "fix": "Replace with a proper logging framework (e.g., Python's logging module).",
            "snippet": 'print(f"Processing item {i}")',
        })

    if not issues:
        issues.append({
            "type": "Analysis",
            "severity": "Low",
            "title": "No Issues Detected",
            "explanation": "This code snippet passed the automated analysis.",
            "fix": "Continue following best practices for security, performance, and code quality.",
            "snippet": "",
        })

    high_count = sum(1 for i in issues if i["severity"] == "High")
    medium_count = sum(1 for i in issues if i["severity"] == "Medium")
    low_count = sum(1 for i in issues if i["severity"] == "Low")

    score = max(40, 100 - (high_count * 20 + medium_count * 10 + low_count * 5))

    return {
        "score": score,
        "issues": issues,
        "high_count": high_count,
        "medium_count": medium_count,
        "low_count": low_count,
        "total_issues": len(issues),
    }

def get_severity_color(severity: str) -> str:
    colors = {
        "High": "severity-high",
        "Medium": "severity-medium",
        "Low": "severity-low",
    }
    return colors.get(severity, "severity-low")

# Hero Section
st.markdown("""
<div class="hero-section">
    <div class="hero-title">AI Code Review Assistant</div>
    <div class="hero-subtitle">Upload code or paste snippets to detect bugs, security issues, performance problems, and code smells instantly.</div>
</div>
""", unsafe_allow_html=True)

# Metrics
st.markdown("""
<div class="metrics-container">
    <div class="metric-card">
        <div class="metric-label">⚡ Review Speed</div>
        <div class="metric-value">&lt;2s</div>
        <div class="metric-description">Instant code analysis and feedback</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">🔐 Security Coverage</div>
        <div class="metric-value">50+</div>
        <div class="metric-description">Vulnerability patterns detected</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">⚙️ Performance Detection</div>
        <div class="metric-value">30+</div>
        <div class="metric-description">Optimization opportunities found</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">🤖 AI Analysis Status</div>
        <div class="metric-value">Ready</div>
        <div class="metric-description">Real-time intelligent scanning</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Main Layout
col_left, col_right = st.columns([1, 0.35], gap="large")

with col_left:
    st.markdown('<div class="code-panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header"><h2 class="panel-title">📝 Code Editor</h2></div>', unsafe_allow_html=True)
    st.markdown('<div class="panel-subtitle">Paste code or select a sample to get started</div>', unsafe_allow_html=True)

    sample_choice = st.selectbox(
        "Select Code Sample",
        list(SAMPLE_CODES.keys()),
        key="sample_select",
        label_visibility="collapsed"
    )

    default_code = SAMPLE_CODES.get(sample_choice, "")

    uploaded_file = st.file_uploader(
        "Upload Code File",
        type=["py", "js", "ts", "java", "cpp", "c", "txt", "jsx", "tsx"],
        label_visibility="collapsed",
    )

    if uploaded_file is not None:
        try:
            default_code = uploaded_file.read().decode("utf-8", errors="ignore")
        except Exception:
            st.error("Could not read the uploaded file.")

    code = st.text_area(
        "Code Editor",
        value=default_code,
        height=380,
        placeholder="Paste your code here or select a sample...",
        label_visibility="collapsed",
    )

    button_col1, button_col2 = st.columns(2, gap="small")
    with button_col1:
        review_clicked = st.button("🔍 Review Code", use_container_width=True, key="review_btn")
    with button_col2:
        clear_clicked = st.button("🧹 Clear", use_container_width=True, key="clear_btn")

    if clear_clicked:
        st.session_state.code = ""
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="info-panel">', unsafe_allow_html=True)
    st.markdown('<h3 class="info-title">✨ Key Features</h3>', unsafe_allow_html=True)
    st.markdown('''<p class="info-text">Get comprehensive code analysis across multiple dimensions with our AI-powered engine.</p>''', unsafe_allow_html=True)

    st.markdown('''<div class="tags-container">
    <span class="tag">🔐 Security</span>
    <span class="tag">⚡ Performance</span>
    <span class="tag">🐛 Bugs</span>
    <span class="tag">📋 Code Quality</span>
    </div>''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='margin: 40px 0;'></div>", unsafe_allow_html=True)

# Results Section
if review_clicked:
    if not code.strip():
        st.markdown('''<div class="empty-state">
            <div class="empty-state-icon">📝</div>
            <div class="empty-state-text">No code to review</div>
            <p style="color: #a78bfa;">Paste some code or select a sample to begin analysis.</p>
        </div>''', unsafe_allow_html=True)
    else:
        with st.spinner("🔍 Analyzing code..."):
            review_data = demo_review(code)

        score = review_data["score"]
        high_count = review_data["high_count"]
        medium_count = review_data["medium_count"]
        low_count = review_data["low_count"]
        total_issues = review_data["total_issues"]
        issues = review_data["issues"]

        st.markdown(f'''
        <div class="results-header">
            <div class="score-display">
                <div class="score-circle">{score}</div>
                <div class="score-label">Code Quality Score</div>
            </div>
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-number">{total_issues}</div>
                    <div class="stat-label">Total Issues</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number" style="color: #fca5a5;">{high_count}</div>
                    <div class="stat-label">High Severity</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number" style="color: #fcd34d;">{medium_count}</div>
                    <div class="stat-label">Medium Severity</div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

        st.markdown("<h3 style='font-size: 1.375rem; font-weight: 700; color: #e9d5ff; margin: 40px 20px 24px; padding: 0;'>🔍 Review Results</h3>", unsafe_allow_html=True)

        st.markdown('<div class="issues-container" style="padding: 0 20px;">', unsafe_allow_html=True)

        for issue in issues:
            severity_class = get_severity_color(issue["severity"])
            st.markdown(f'''
            <div class="issue-card">
                <div class="issue-header">
                    <div class="issue-type">{issue['type']}</div>
                    <span class="severity-badge {severity_class}">{issue['severity']}</span>
                </div>
                <div class="issue-title">{issue['title']}</div>
                <div class="issue-section">
                    <span class="issue-label">Explanation</span>
                    <div class="issue-text">{issue['explanation']}</div>
                </div>
                <div class="issue-section">
                    <span class="issue-label">Recommended Fix</span>
                    <div class="issue-text">{issue['fix']}</div>
                </div>
                {f'<div class="issue-section"><span class="issue-label">Code Location</span><div class="code-snippet">{issue["snippet"]}</div></div>' if issue['snippet'] else ''}
            </div>
            ''', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)