# Secure MCP Auditor: Verifiable AI Infrastructure 🛡️

## Overview
This project engineers a high-performance security and audit layer for LLM agents using the **Model Context Protocol (MCP)**. It addresses the critical challenge of AI hallucinations and logic sabotage by providing a verifiable "Fact-Check" layer that monitors tool-calling in real-time.

## 🚀 Core Project: Fact-Check Auditor
The repository features a specialized Python-based verification engine that intercepts AI-generated data and validates it against local ground-truth specifications.

### Key Technical Achievements
* **Logic Sabotage Detection:** Achieved a **100% detection rate** for budget variances and risk-level escalations during LLM orchestration.
* **High-Performance Verification:** Optimized auditing workflows to perform checks with **<100ms latency**, ensuring security without compromising user experience.
* **Forensic Traceability:** Implemented a persistent, immutable logging architecture (`audit_history.log`) for post-incident review and system observability.

## 🛠️ MCP Infrastructure & Setup
The system utilizes a Secure File System MCP Server to enable Claude to interact with local directories under a strict sandboxed environment.

## 📂 Project Structure
* `src/`: Core Python logic, including the `FactCheckAuditor` and `FileScanner`.
* `logs/`: Verifiable audit reports and forensic history logs.
* `config/`: Source specifications and project ground-truth data.
