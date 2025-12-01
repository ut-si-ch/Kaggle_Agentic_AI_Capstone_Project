# agents/resume_agent.py
# Specialized agent for resume parsing, JD matching, and ATS optimization

import os
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types
from google.adk.tools import load_memory # <-- ADD the working tool
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field # Using Pydantic for structured output schema (Day 2 best practice)


# --- Configuration (Consistency with runner.py) ---
retry_config = types.HttpRetryOptions(
    attempts=5,        # Maximum retry attempts
    exp_base=7,        # Delay multiplier
    initial_delay=1,
    http_status_codes=[3-6], # <-- CRITICAL FIX: Ensure status codes are listed here
)

# --- Define Structured Output Schema (Demonstrates Day 2/Day 4 advanced capabilities) ---

# Define the structured output format the LLM must return after analysis
class ResumeAnalysisResult(BaseModel):
    """
    Structured analysis containing the match score, required edits, and skill gap assessment.
    This ensures the output is machine-readable for downstream agents or evaluation metrics.
    """
    match_score: int = Field(..., description="Percentage score (0-100) indicating resume fit against the JD.")
    required_skills_found: List[str] = Field(..., description="List of essential skills from the JD found in the resume.")
    skill_gaps_flagged: List[str] = Field(..., description="List of critical skills missing from the resume based on the JD.")
    suggested_rewrite_summary: str = Field(..., description="A short summary of the key changes needed for ATS optimization.")
    ats_risk_flags: List[str] = Field(..., description="Flags common ATS risks (e.g., non-standard fonts, tables, dense text).")


# --- Define Internal Tools (The Hands) ---

# NOTE: In a real system, these would use external libraries (PyPDF2, Docx) or APIs.

def parse_resume(resume_text: str, jd_text: str) -> str:
    """
    Parses a user's resume (from long-term memory) and a Job Description (JD) text.
    It performs initial keyword extraction and structure checking against the JD.

    Args:
        resume_text: The full text content of the user's current resume.
        jd_text: The full text content of the target Job Description.

    Returns:
        A structured JSON summary of extracted experience, education, and skills.
    """
    # Simulation: In production, this output is crucial for the main agent's reasoning.
    return f"ANALYSIS_SUCCESS: Extracted skills from JD: Python, SQL, Cloud. Extracted skills from Resume: Python, Excel, R."


def generate_ats_friendly_document(analysis: ResumeAnalysisResult, resume_content: str, document_type: str = "resume") -> str:
    """
    Generates a final, clean, ATS-compliant resume or cover letter based on the analysis.
    This tool should only be called AFTER the main agent has produced a final analysis.

    Args:
        analysis: The ResumeAnalysisResult object defining the required edits.
        resume_content: The original content to be rewritten.
        document_type: 'resume' or 'cover_letter'.

    Returns:
        The content of the final, tailored document (Markdown or plaintext format).
    """
    return f"GENERATED_DOCUMENT: Successfully generated the ATS-friendly {document_type} using keywords and a clean format."


# --- Agent Definition (The Brain) ---

resume_agent = LlmAgent(
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    name="ResumeTailorAgent",
    description="A specialized agent for optimizing resumes and generating ATS-friendly documents by matching user skills against specific job descriptions.",
    instruction=f"""
    You are the Resume Tailor Agent. Your mission is to maximize the user's chance of passing automated HR systems (ATS).

    CRITICAL BEHAVIOR:
    1. Retrieval: ALWAYS use the '{load_memory}' tool first to retrieve the user's current resume (long-term memory item: user:resume).
    2. Analysis: Use the 'parse_resume' tool to compare the retrieved resume against the user-provided Job Description (JD).
    3. Scrutiny: After parsing, your final answer MUST adhere strictly to the JSON schema of the ResumeAnalysisResult class. You must calculate a match score and identify critical skill gaps.
    4. Action: You MUST call the 'generate_ats_friendly_document' tool only if the user confirms the suggested changes are acceptable.
    5. Constraint: You MUST use the provided tools to handle data and analysis. Do not hallucinate data.
    """,
    tools=[
        load_memory, # <-- CRITICAL FIX: Use the functional reactive memory tool  # Proactive memory retrieval (Day 3)
        parse_resume,    # Custom tool (Day 2)
        generate_ats_friendly_document, # Custom tool (Day 2)
    ],
    # Enforce structured output for evaluation clarity (Day 4)
    #response_schema=ResumeAnalysisResult,
    #is_a2a_server=False,
)

print("Resume Tailor Agent module loaded.")