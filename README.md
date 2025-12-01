# 🚀 Agentic Data Science Agent: Career Co-Pilot

## Project Overview

The **Agentic Data Science Agent** is a multi-agent system designed to guide aspiring data scientists from learning concepts to achieving job placement readiness. It addresses the critical challenges in the current job market: skill mismatch, difficulty parsing job descriptions (JDs), passing Applicant Tracking Systems (ATS), and navigating sensitive career transitions (like explaining layoffs) [7].

This system is built using the **Agent Development Kit (ADK)** and demonstrates mastery of all core concepts from the 5-Day AI Agents Intensive Course with Google. It is submitted under the **Enterprise Agents** track [4].

## Core Value Proposition

This agent system serves as an automated career co-pilot that coordinates five specialized agents to perform complex, multi-step workflows [8]:
1.  **Diagnosis and Tutoring** (via `ds_tutor_agent`)
2.  **Market Intelligence and Research** (via `research_agent`)
3.  **Targeted Job Search and Ranking** (via `job_search_agent`)
4.  **Resume and Cover Letter Optimization** (via `resume_agent`)
5.  **High-Stakes Pitch Coaching** (via `coach_agent`)

## 🛠️ Technical Architecture & Required Features

The system follows a **Hierarchical Multi-Agent System** design (Level 3/4 Taxonomy [9]), ensuring **modularity** and specialization [10].

### 1. Multi-Agent System (Day 1 / Day 5 A2A)
A **Root Orchestrator** (`runner.py`) acts as the central manager, analyzing the user's mission and delegating tasks sequentially or in parallel to five distinct, specialized sub-agents [11]. The sub-agents are integrated using the **AgentTool** pattern, which is the local application of the **Agent2Agent (A2A) Protocol** [12, 13].

### 2. Tools and Interoperability (Day 2 / MCP)
The agents rely on both built-in and custom, atomic tools [14]:
*   **Built-in Tools:** `google_search` and `BuiltInCodeExecutor` (for reliable calculations/practice problems) [15, 16].
*   **Custom Tools:** Functions for job querying, resume parsing (`tools/file_tools.py`), and job ranking (`job_search_agent.py`) [17].
*   **Code-as-Tool:** The `coach_agent` and `resume_agent` rely on Python functions to handle file I/O operations (simulating document reading/saving) [18].

### 3. Long-Running Operations (LRO / Day 2b)
The `coach_agent` implements the LRO pattern for sensitive tasks, such as finalizing a layoff pitch or submitting a tailored resume. This ensures **Human-in-the-Loop (HITL)** oversight by requiring explicit confirmation from the user before proceeding with a high-stakes action [19]. This uses the `ToolContext.request_confirmation()` mechanism to pause and resume agent execution [20, 21].

### 4. Sessions and Long-Term Memory (Day 3)
The system is **stateful** and personalized:
*   **Sessions:** Managed by `DatabaseSessionService` (configured in `runner.py`) to maintain conversation history and tool results across a single interaction [22].
*   **Long-Term Memory:** Utilizes ADK’s memory pattern (`preload_memory` tool) to store persistent knowledge, such as the user's skill profile, past applications, and career preferences, ensuring **cross-session recall** [23, 24]. This proactive memory retrieval is critical for the `job_search_agent` to accurately rank job fit [25].

### 5. Observability and Evaluation (Day 4)
The architecture includes robust quality assurance mechanisms [26]:
*   **Observability:** The system is designed to emit **Logs** (single events), **Traces** (the sequential narrative of agent reasoning and tool choices), and **Metrics** (success rates/latency) [27]. This allows for debugging why an agent chooses a certain path (Trajectory) [28].
*   **Evaluation:** The system can be tested against **Golden Datasets** using the **LLM-as-a-Judge** framework to measure metrics like **Response Match Score** and **Tool Trajectory Score** [29, 30].

## 🏗️ Project Structure

The project is modularized into distinct directories for clarity and maintainability:

CapstoneAgentProject/ ├── agents/                  # Specialized Agents (Tutor, Research, Coach, etc.) │   ├── ds_tutor_agent.py │   ├── research_agent.py │   ├── job_search_agent.py │   ├── resume_agent.py │   └── coach_agent.py ├── tools/                   # Atomic, Low-Level Utility Functions (File I/O, Web Search) │   ├── file_tools.py │   └── web_tools.py ├── .env                     # Configuration file (securely stores API keys, excluded from source control) ├── runner.py                # Main Orchestrator and Runner initialization ├── requirements.txt         # Project dependencies └── README.md                # This document

## Setup and Installation

1.  **Environment:** Ensure you have Python 3.9+ and pip installed. Create a virtual environment (`conda create -n agentcapstone python=3.10`).
2.  **Clone/Create:** Create the directory structure above and populate the files.
3.  **Dependencies:** Install all required libraries using the `requirements.txt` file (to be generated next).
4.  **API Keys:** Create a `.env` file containing your `GOOGLE_API_KEY` and `SERPAPI_API_KEY` (as discussed during the process, your manual saving of `.env` was correct). **Do not commit this file.**
5.  **Execution:** Run the main orchestrator script: `python runner.py`.