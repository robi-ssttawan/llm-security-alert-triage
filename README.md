# 🛡️ LLM-Powered Security Alert Triage System

An automated Security Operations Center (SOC) alert triage system powered by LLMs and mapped to the **MITRE ATT&CK** framework. Built to mitigate alert fatigue for security analysts by converting raw security logs into structured, actionable JSON insights in real-time.

---

## 🌟 Key Features
- **Automated Log Parsing:** Analyzes raw unstructured log data (SSH Brute Force, SQL Injection, Phishing Executables, System Logs, etc.).
- **Dynamic Severity Scoring:** Automatically evaluates incident criticalities (`Low`, `Medium`, `High`, `Critical`).
- **MITRE ATT&CK Mapping:** Maps log events directly to MITRE Technique IDs (e.g., `T1110 - Brute Force`, `T1190 - Exploit Public-Facing Application`).
- **Actionable Remediation Advice:** Provides concise, prioritized response steps for SOC analysts.
- **Interactive Web Dashboard:** Clean UI powered by Streamlit with interactive sample prompt switching and raw JSON inspection.

---

## 🛠️ Tech Stack
- **Core Language:** Python 3.10+
- **Frontend Dashboard:** Streamlit
- **LLM Orchestration:** `g4f` / Multi-provider Inference Engine
- **Data Exchange Format:** Structured JSON

---

## 📸 Dashboard Preview

> *Masukkan screenshot dashboard Streamlit kamu di sini untuk tampilan optimal!*

---

## 🚀 Getting Started & Installation

### Prerequisites
- Python 3.10 or higher
- Git installed on your local machine

### Step-by-Step Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/robi-ssttawan/llm-security-alert-triage.git
cd llm-security-alert-triage
