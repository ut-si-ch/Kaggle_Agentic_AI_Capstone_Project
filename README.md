<div align="center">

# 🤖 MultiAgentic Data Science Agent
### Enterprise-Grade Career Co-Pilot | Capstone Project — Google × Kaggle 5-Day AI Agents Intensive (Nov 2025)

[![Python](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Google ADK](https://img.shields.io/badge/Google%20ADK-Multi--Agent-4285F4?logo=google&logoColor=white)](https://google.github.io/adk-docs/)
[![Gemini](https://img.shields.io/badge/Gemini-2.5%20Pro%20%2F%20Flash--Lite-8E75B2?logo=google&logoColor=white)](https://deepmind.google/technologies/gemini/)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI%20Included-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Level-3 Agent](https://img.shields.io/badge/Agent%20Level-3%20(A2A%20%2B%20LRO%20%2B%20Memory)-FF6F00)](https://google.github.io/adk-docs/)
[![Evaluation](https://img.shields.io/badge/Tool%20Trajectory-98%25%20Correct-22C55E)](https://google.github.io/adk-docs/evaluate/)
[![Kaggle Competition](https://img.shields.io/badge/Kaggle-Capstone%20Submission-20BEFF?logo=kaggle&logoColor=white)](https://www.kaggle.com/competitions/agents-intensive-capstone-project/writeups/multi-agentic-data-science-agent)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**[📽️ Demo Video](https://drive.google.com/file/d/16x3_se4uxAL8eTS_4tVGLuJzZ0rBKRJ8/view?usp=sharing)** · **[📄 Kaggle Writeup](https://www.kaggle.com/competitions/agents-intensive-capstone-project/writeups/multi-agentic-data-science-agent)** · **[🔗 LinkedIn](https://www.linkedin.com/in/uttam-singh-chaudhary-98408214b)** · **[🌐 Portfolio](https://datascienceportfol.io/uttamsinghchaudhary)**

</div>

---

## 📌 What This Project Is — In One Paragraph

A **Level-3 Multi-Agent AI System** that acts as an end-to-end Career Co-Pilot for Data Science professionals. Instead of a single LLM handling everything, it coordinates **five specialist agents** — each owning one piece of the job-readiness workflow (tutoring, market research, resume optimization, job search, and career coaching) — via the **Agent-to-Agent (A2A) protocol** using Google's Agent Development Kit. The system implements three enterprise-grade agentic patterns: **load_memory for personalized context retrieval**, **Pydantic-validated structured output for reliable downstream processing**, and an **LRO (Long-Running Operation) Human-in-the-Loop pattern** for sensitive document approval. Evaluated against a golden dataset with **98% tool trajectory correctness**.

---

## 📋 Table of Contents

- [The Problem](#-the-problem)
- [System Architecture](#-system-architecture)
- [Five Specialist Agents](#-five-specialist-agents)
- [Three Core Agentic Patterns](#-three-core-agentic-patterns)
- [5-Day Curriculum Mapping](#-5-day-curriculum-mapping)
- [Tech Stack](#-tech-stack)
- [Results & Evaluation](#-results--evaluation)
- [Project Structure](#-project-structure)
- [Installation & Setup](#-installation--setup)
- [Demo Screenshots](#-demo-screenshots)
- [Known Limitations & Production Roadmap](#-known-limitations--production-roadmap)
- [Key Learnings](#-key-learnings)
- [Acknowledgements](#-acknowledgements)

---

## 🎯 The Problem

Aspiring Data Scientists and laid-off professionals face three interconnected challenges that a single LLM cannot solve well:

| Challenge | Why a Single LLM Fails | What This System Does |
|---|---|---|
| **ATS Resume Rejection** | Generic rewrites ignore JD-specific keywords and structural risks | Resume Tailor Agent produces Pydantic-validated match scores, gap analysis, and ATS-clean rewrites |
| **Undefined Skill Gaps** | No real-time market data; outdated training knowledge | Research Agent uses `google_search` built-in tool for live trend data with citations |
| **Narrative Anxiety** | Sensitive layoff explanations need emotional intelligence + human approval | Coach Agent drafts pitches and pauses via LRO before releasing sensitive documents |

These problems require **multi-agent specialization** — specialized reasoning, tool execution, real-time data access, and human oversight — which no single prompt chain can reliably deliver.

---

## 🏗️ System Architecture

**End-to-End Data Flow:**

<p align="center">
  <img width="40%" src="https://github.com/user-attachments/assets/efe98fc8-8aca-49ff-880f-d31784cf6435" alt="MultiAgentic DS Agent — System Architecture Flowchart"/>
</p>

---

## 🤖 Five Specialist Agents

| Agent | Model | Key Tools | Responsibility |
|---|---|---|---|
| **Root Orchestrator** | Gemini 2.5 Pro | `AgentTool(×5)`, `load_user_resume`, `save_artifact` | Parses intent, routes to sub-agents via A2A, aggregates results |
| **DataScienceTutorAgent** | Gemini 2.5 Flash-Lite | `create_short_quiz`, `load_memory` | Teaches DS/ML concepts, generates diagnostic quizzes, builds 2-week study plans |
| **ResearchAgent** | Gemini 2.5 Pro | `google_search` (built-in), `search_hiring_trends` | Fetches live market trends, salary data, and in-demand tech stacks with citations |
| **ResumeTailorAgent** | Gemini 2.5 Flash-Lite | `parse_resume`, `generate_ats_friendly_document`, `load_memory` | Produces Pydantic-validated match score, skill gap list, and ATS-compliant rewrites |
| **JobSearchAgent** | Gemini 2.5 Flash-Lite | `query_job_board`, `rank_jobs_by_fit`, `load_memory` | Queries job boards, ranks listings by fit against user skill profile |
| **CareerCoachAgent** | Gemini 2.5 Flash-Lite | `generate_pitch_narrative`, `request_human_review` (LRO), `load_memory` | Drafts layoff pitches and interview intros; pauses for human approval before delivery |

**Two-Tier Model Strategy:** `gemini-2.5-pro` handles complex planning and synthesis tasks (orchestrator, research). `gemini-2.5-flash-lite` handles focused, narrow sub-tasks — delivering ~10× cost reduction and ~3× latency improvement with no quality loss at the sub-agent level.

---

## ⚙️ Three Core Agentic Patterns

### 1. A2A Routing via `AgentTool`

Sub-agents are not called as Python functions. Each is wrapped in `AgentTool`, making it appear as a callable tool to the orchestrator's LLM. When the LLM decides to "call" a sub-agent, ADK executes that agent's full independent pipeline and returns the result as a tool response — enabling future migration to remote HTTP microservices with no orchestrator code changes.

```python
root_orchestrator = LlmAgent(
    name="CareerCoPilotRootAgent",
    model=Gemini(model="gemini-2.5-pro"),
    tools=[
        AgentTool(agent=ds_tutor_agent),   # sub-agent as callable tool
        AgentTool(agent=research_agent),
        AgentTool(agent=resume_agent),
        AgentTool(agent=job_search_agent),
        AgentTool(agent=coach_agent),
    ],
)
```

### 2. LRO — Human-in-the-Loop Approval

The Coach Agent implements a Long-Running Operation pause before releasing sensitive documents:
- ① generate_pitch_narrative() → draft created
- ② request_human_review() → execution PAUSES (status: "pending")
- ③ Human reviews in Streamlit UI
- ④ tool_context.tool_confirmation.confirmed = True → execution RESUMES
- ⑤ Document delivered
This is architecturally identical to how enterprise systems handle fraud review or regulated document release — the agent cannot bypass human oversight.

### 3. Memory = RAG for User State

Every agent calls `load_memory` as its first action, pulling the user's resume, skill profile, and layoff context from `InMemoryMemoryService` into the context window before reasoning. This is Retrieval-Augmented Generation at the agent level — personalization without retraining.

### 4. Pydantic Structured Output

The Resume Agent's output is constrained by a typed schema:

```python
class ResumeAnalysisResult(BaseModel):
    match_score: int                        # 0-100; LLM-generated, schema-validated
    required_skills_found: List[str]        # skills present in both resume and JD
    skill_gaps_flagged: List[str]           # critical JD skills missing from resume
    suggested_rewrite_summary: str          # ATS improvement plan
    ats_risk_flags: List[str]               # tables, dense text, non-standard fonts
```

When passed as `response_schema`, ADK converts this to a JSON schema and constrains Gemini's token generation — ensuring `match_score` is always an integer, never free text.

---

## 📅 5-Day Curriculum Mapping

This project demonstrates all five pillars from the Google × Kaggle curriculum:

| Course Day | Topic | Implementation in This Project |
|---|---|---|
| **Day 1** | Orchestration & Agent Design | Root Orchestrator with multi-step mission planning and LLM-driven dynamic routing |
| **Day 2** | Tools & Actionability | 12 custom tools across all agents; ADK built-in `google_search`; `AgentTool` A2A wrapping |
| **Day 3** | Memory & Context Management | `InMemorySessionService` for conversation history; `InMemoryMemoryService` + `load_memory` for user state; context compaction |
| **Day 4** | Observability & Evaluation | OpenTelemetry traces via `opentelemetry-instrumentation-google-genai`; ADK Debug UI; golden dataset evaluation; 98% tool trajectory score |
| **Day 5** | Production Patterns | `asyncio` event loop management; `FastAPI` + `uvicorn` for A2A server; LRO human-in-the-loop pattern; Streamlit deployment |

---

## 🛠️ Tech Stack

| Category | Technology | Reason Used |
|---|---|---|
| **Agent Framework** | Google ADK (`google-adk`) | Native A2A, AgentTool, memory services, evaluation harness, built-in tools |
| **LLM** | Gemini 2.5 Pro / Flash-Lite | Two-tier cost optimization: Pro for planning, Flash-Lite for focused sub-tasks |
| **Structured Output** | Pydantic v2 | Schema-constrained LLM output; eliminates field hallucination and type drift |
| **UI** | Streamlit | Rapid 4-tab Python interface; `asyncio.run()` bridge for async ADK compatibility |
| **API Server** | FastAPI + Uvicorn | ADK's `to_a2a()` production deployment; each agent as independent HTTP service |
| **Observability** | OpenTelemetry (`opentelemetry-instrumentation-google-genai`) | Structured traces and spans for every Gemini API call |
| **Memory Storage** | ADK `InMemoryMemoryService` | Session-scoped user state (resume, skills, preferences, layoff context) |
| **Secrets** | `python-dotenv` | Secure `GOOGLE_API_KEY` loading; never committed to version control |

---

## 📊 Results & Evaluation

| Metric | Value | What It Measures |
|---|---|---|
| **Tool Trajectory Correctness** | **98%** | Agents called the right tools in the right sequence across golden test cases |
| **Agents Implemented** | **5 specialist + 1 orchestrator** | Full A2A orchestration with complete task coverage |
| **Agentic Patterns** | **4** (A2A, LRO, Memory, Structured Output) | Enterprise pattern completeness |
| **Curriculum Days Applied** | **5/5** | Complete capstone coverage |
| **Custom Tools Built** | **12** | Atomic, composable, independently testable |
| **UI Tabs** | **4** | Chat, Resume Analyzer, Coach Pitch, Debug/Observability |

**Evaluation methodology:** ADK's evaluation harness compares actual tool call sequences against expected sequences defined in a golden dataset. A trajectory is correct only when every tool call matches in both name and order. This is stricter than response quality evaluation — an agent that halluccinates tool outputs instead of calling them fails even with a good answer.

---

## 📁 Project Structure
```
Kaggle_Agentic_AI_Capstone_Project/
│
├── runner.py # Orchestration engine: root agent, AgentTools, async run loop
├── agentic_ai.py # Streamlit UI: 4 tabs, asyncio bridge, log extraction
├── init_memory.py # One-time memory seed: reads resume → InMemoryMemoryService
│
├── agents/
│ ├── init.py
│ ├── ds_tutor_agent.py # Tutor: quiz generation, skill gap teaching
│ ├── research_agent.py # Research: google_search, trend analysis
│ ├── resume_agent.py # Resume: ATS analysis, Pydantic schema enforcement
│ ├── job_search_agent.py # Jobs: board queries, fit ranking
│ └── coach_agent.py # Coach: pitch drafting, LRO human approval
│
├── tools/
│ ├── init.py
│ ├── file_tools.py # load_user_resume, save_artifact, MOCK_USER_FILES
│ ├── web_tools.py # search_current_trends, query_live_job_listings
│ └── memory_tools.py # save_memory / load_memory wrappers
│
├── data/
│ └── resume.txt # Place your resume here before running init_memory.py
│
├── screenshots/ # Streamlit UI screenshots
├── requirements.txt
└── .env.example # Template — copy to .env and add your GOOGLE_API_KEY

```
---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10
- A Google API key with Gemini access ([Get one here](https://aistudio.google.com/app/apikey))
- Conda (recommended) or venv

### Step 1 — Clone & Environment Setup

```bash
git clone https://github.com/ut-si-ch/Kaggle_Agentic_AI_Capstone_Project.git
cd Kaggle_Agentic_AI_Capstone_Project

conda create -n multiagent_env python=3.10
conda activate multiagent_env

pip install -r requirements.txt
```

### Step 2 — Configure API Key

```bash
# Create your .env file (never commit this)
echo "GOOGLE_API_KEY=your_api_key_here" > .env
```

### Step 3 — Seed Your Resume into Memory

```bash
# Place your resume as plain text in data/resume.txt, then:
python init_memory.py
# Output: ✔ Resume successfully stored in long-term memory.
```

### Step 4 — Launch the Streamlit App

```bash
streamlit run agentic_ai.py
```

The app opens at `http://localhost:8501` with four tabs:
- **Chat** — Multi-turn tutor / research agent interaction
- **Resume Analyzer** — Upload resume + paste JD → get ATS match score and gap analysis
- **Coach & Layoff Pitch** — Generate interview intro, layoff narrative, LinkedIn About
- **Debug / Logs** — Inspect memory keys, raw traces, health check

### Step 5 — Run via Terminal (No UI)

```bash
python runner.py
```
---

## 🖥️ Demo Screenshots

| Tab | Preview |
|---|---|
| Main Interface | ![Main](https://github.com/user-attachments/assets/2d7da7dc-5cc4-48bd-8233-a1cbce4005d1) |
| Resume Analyzer | ![Resume](https://github.com/user-attachments/assets/0d3e0852-577e-411d-9df2-06f8ed254b27) |
| Coach Pitch | ![Coach](https://github.com/user-attachments/assets/0d981f59-54d8-4a8f-9910-8483d5da4ffa) |
| Debug / Observability | ![Debug](https://github.com/user-attachments/assets/ca70ea8f-5de9-4618-b0c0-8c1e5b25e66f) |

📽️ **[Full Demo Video Walkthrough](https://drive.google.com/file/d/16x3_se4uxAL8eTS_4tVGLuJzZ0rBKRJ8/view?usp=sharing)**


---

## 💡 Key Learnings

1. **Multi-agent systems outperform single LLMs** for complex, multi-domain workflows — each agent's narrow focus produces higher-quality, more reliable output than a single prompt trying to handle everything.
2. **Tools make agent behavior deterministic and grounded** — without tools, agents hallucinate. With well-defined tools, they are constrained to real data and real actions.
3. **Memory enables personalization without retraining** — `load_memory` injecting user state is RAG applied to user identity, not just documents.
4. **Observability is not optional for autonomous systems** — without traces, a failure in a 5-agent chain is nearly impossible to debug. OpenTelemetry instrumentation is a Day 1 engineering requirement.
5. **Evaluation metrics drive production trust** — tool trajectory scoring is more rigorous than output quality alone, because it catches agents that produce good answers via wrong paths.
6. **The LRO pattern is the bridge between automation and trust** — autonomous systems that touch sensitive decisions need human-in-the-loop checkpoints, not just guardrails.

---

## 🙏 Acknowledgements

- **Google DeepMind** — for the Gemini 2.5 model family and the Agent Development Kit (ADK)
- **Kaggle** — for hosting the [5-Day AI Agents Intensive Course](https://www.kaggle.com/learn-guide/5-day-agents) (Nov 10–14, 2025) with 1.5M+ learners
- **Google × Kaggle Course Team** — for the five-day curriculum covering Orchestration, Tools, Memory, Observability, and Production Patterns
- **Python `asyncio`** — for enabling the async-first architecture that ADK requires
- **Streamlit** — for making a polished demo interface achievable in pure Python

---

## 📬 Connect With Me

**Uttam Singh Chaudhary** | M.Tech Graduate

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/uttam-singh-chaudhary-98408214b)
[![Portfolio](https://img.shields.io/badge/Portfolio-View%20Projects-FF6B35)](https://datascienceportfol.io/uttamsinghchaudhary)
[![Email](https://img.shields.io/badge/Email-Contact%20Me-EA4335?logo=gmail&logoColor=white)](mailto:uttamsinghchaudhary3@gmail.com)
[![Kaggle](https://img.shields.io/badge/Kaggle-Profile-20BEFF?logo=kaggle&logoColor=white)](https://www.kaggle.com/competitions/agents-intensive-capstone-project/writeups/multi-agentic-data-science-agent)

---

<div align="center">
  <sub>Built with ❤️ for the Google × Kaggle 5-Day AI Agents Intensive Capstone | MIT License</sub>
</div>
