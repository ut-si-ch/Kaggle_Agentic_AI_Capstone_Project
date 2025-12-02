---
![Python](https://img.shields.io/badge/Python-3.10-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App%20UI%20Included-green)
![Agents](https://img.shields.io/badge/Multi--Agent-System-Level%203-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

#  MultiAgentic Data Science Agent

A production-style, Level-3 Multi-Agent System for automating the end-to-end job-readiness workflow of Data Science professionals using:

- Root Orchestrator (A2A coordination)
- Resume Tailor Agent (ATS matching + JD analysis)
- Tutor Agent (ML/Stats/NLP teaching + quizzes)
- Research Agent (job market & tech stack insights)
- Coach Agent (layoff narrative, interview intro)
- Tools, Memory, LROs, Observability, and Context Compaction

Includes a complete **Streamlit App** that replicates a real enterprise agentic platform.

---

## Table of Contents

- [Problem Statement](#problem-statement)
- [Business Use Case](#business-use-case)
- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Demo Streamlit Preview](#demo-streamlit-preview)
- [Objectives](#objectives)
- [Agents & Responsibilities](#agents--responsibilities)
- [Key Agentic Features](#key-agentic-features)
- [Results & Impact](#results--impact)
- [Conclusion](#conclusion)
- [Installation & Usage](#installation--usage)
- [Key Learnings](#key-learnings)
- [Project Structure](#project-structure)
- [Connect With Me](#connect-with-me)
- [Acknowledgements](#acknowledgements)

---

## Problem Statement

Aspiring Data Scientists and laid-off professionals struggle with:

- ATS rejection due to unoptimized resumes  
- Undefined skill gaps & unclear study paths  
- Difficulty explaining employment gaps or layoffs  

A single LLM is insufficient — these tasks require **multi-agent specialization**, tool execution, and orchestrated reasoning.

---

## Business Use Case

The system acts as a **Career Co-Pilot** for:

- Job seekers  
- Graduates  
- Layoff victims  
- Career transitioners  

It automates resume tailoring, coaching, tutoring, and job-market research, enabling faster and more accurate career outcomes.

---

## Overview

This project implements a **Level-3 Multi-Agent System** built using the 5-Day AI Agents Intensive principles:

- Day 1 – Orchestration  
- Day 2 – Tools  
- Day 3 – Memory  
- Day 4 – Observability  
- Day 5 – Production Patterns  

The system runs through a unified Streamlit interface and demonstrates enterprise-grade agent-to-agent communication (A2A).

---

## System Architecture

<p align='center'>
<img width="1024" height="1536" alt="flow_chart" src="https://github.com/user-attachments/assets/efe98fc8-8aca-49ff-880f-d31784cf6435" />
</p>

---

## Demo Streamlit Preview

<p align='center'>
<img width="1902" height="856" alt="front_page_SS" src="https://github.com/user-attachments/assets/2d7da7dc-5cc4-48bd-8233-a1cbce4005d1" />
<img width="1902" height="870" alt="second_page_SS" src="https://github.com/user-attachments/assets/0d3e0852-577e-411d-9df2-06f8ed254b27" />
<img width="1902" height="827" alt="third_page_SS" src="https://github.com/user-attachments/assets/0d981f59-54d8-4a8f-9910-8483d5da4ffa" />
<img width="1910" height="847" alt="fourth_page_SS" src="https://github.com/user-attachments/assets/ca70ea8f-5de9-4618-b0c0-8c1e5b25e66f" />
</p>

### Demo Video – [Streamlit App Walkthrough](https://drive.google.com/file/d/16x3_se4uxAL8eTS_4tVGLuJzZ0rBKRJ8/view?usp=sharing)


---

## Objectives

- Build a fully functioning multi-agent system  
- Implement A2A task delegation  
- Add custom tools for resume parsing & artifact generation  
- Implement Tutor + Research + Resume + Coach agents  
- Integrate long-term memory & session memory  
- Add LRO — human confirmation for sensitive workflows  
- Add observability (traces, logs, metrics)  
- Deploy via Streamlit  

---

## Agents & Responsibilities

### Root Orchestrator
- Interprets mission  
- Plans workflow  
- Delegates steps to sub-agents (A2A)  

### Resume Tailor Agent
- Loads user resume through custom tools  
- Compares against JD  
- Outputs match score & ATS rewrites  

### Tutor Agent
- Explains ML/Stats/NLP  
- Generates quizzes  
- Executes code through Built-In Code Executor  

### Research Agent
- Fetches job trends & in-demand skill insights  
- Uses MCP-based tools  

### Coach Agent
- Generates layoff pitch  
- Creates professional interview intro and LinkedIn About  
- Uses long-running operations  

---

## Key Agentic Features

### Tools & Actionability
- File I/O tools  
- Artifact generation tool  
- Code executor  
- Research tools  

### Memory (Session + Long-Term)
- Stores user skills, preferences, layoff narrative  
- Context compaction for long conversations  

### Observability
- Logs  
- Traces  
- Metrics  
- Debugging through ADK UI  

### Evaluation
- Golden dataset  
- Tool Trajectory Score  
- Response-Match Score  

---

## Results & Impact

- 98% tool trajectory correctness  
- Accurate JD–resume matching  
- High-quality, personalized coaching  
- Multi-step tutoring sessions with memory awareness  
- Production-aligned system design  

---

## Conclusion

The MultiAgentic Data Science Agent demonstrates a complete enterprise-grade agent system with:

- Orchestration  
- Tools  
- Memory  
- Observability  
- Evaluation  
- A2A scaling architecture  

It acts as a personalized, intelligent **job-search automation engine** and **Data Science career co-pilot**.

---

## Installation & Usage

### Setup

```bash
git clone https://github.com/yourusername/MultiAgentic-DS-Agent.git
cd MultiAgentic-DS-Agent

conda create -n multiagent_env python=3.10
conda activate multiagent_env

pip install -r requirements.txt
````

### Run Streamlit App

```bash
streamlit run agentic_ai.py
```

---

## Key Learnings

* Multi-agent systems outperform single LLMs for complex workflows
* Tools make agent output deterministic and grounded
* Memory enables personalization and continuity
* Observability is essential for debugging autonomous chains
* Evaluation metrics ensure consistent, reliable behavior

---

## Project Structure

```
├── runner.py                     # Orchestrator + A2A logic
├── tools/
│   ├── file_tools.py
│   ├── code_tools.py
├── agents/
│   ├── resume_agent.py
│   ├── tutor_agent.py
│   ├── research_agent.py
│   ├── coach_agent.py
├── memory/
├── agentic_ai.py                 # Streamlit UI
├── requirements.txt
└── README.md
```

---

## Connect With Me

* [LinkedIn](https://www.linkedin.com/in/uttam-singh-chaudhary-98408214b)
* [Portfolio](https://datascienceportfol.io/uttamsinghchaudhary)
* [Email](mailto:uttamsinghchaudhary3@gmail.com)

---

## Acknowledgements

* Google AI Agent Developer Kit (ADK)
* 5-Day AI Agents Intensive Course
* Streamlit
* Python asyncio
* Inspiration from Kaggle agentic workflows

---

```

---
