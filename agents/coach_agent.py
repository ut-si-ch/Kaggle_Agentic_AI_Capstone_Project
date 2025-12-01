# agents/coach_agent.py
# Specialized agent for sensitive career coaching (pitches, narratives, LRO approval)

import os
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types
from google.adk.tools import load_memory # <-- ADD the working tool
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.function_tool import FunctionTool
from typing import Dict, Any

# --- Configuration (Consistency with runner.py) ---
retry_config = types.HttpRetryOptions(
    attempts=5, 
    exp_base=7, 
    initial_delay=1,
    http_status_codes=[3-6],
)

# --- Define Internal Tools (Demonstrates Day 2b LRO Pattern) ---

def generate_pitch_narrative(topic: str, context: str) -> str:
    """
    Generates a professional, emotionally intelligent narrative for a sensitive topic, 
    such as explaining a resume gap, a layoff, or an interview failure.
    
    Args:
        topic: The sensitive topic (e.g., 'Layoff explanation', 'Interview failure rationale').
        context: Summarized user history and job context (from memory retrieval).
        
    Returns:
        The generated draft narrative.
    """
    # NOTE: The LLM will use this tool definition to format the draft.
    return f"DRAFT_NARRATIVE: Analyzing context ({len(context)} chars) to craft a high-stakes pitch on: {topic}."


def request_human_review(document_type: str, document_draft: str, tool_context: ToolContext) -> Dict[str, Any]:
    """
    PAUSES the agent workflow to request human confirmation/approval before proceeding 
    with a sensitive or high-stakes operation (LRO pattern, Day 2b).
    
    Args:
        document_type: The type of document requiring review (e.g., 'Layoff Pitch').
        document_draft: The complete text of the sensitive document draft.
        tool_context: ADK context provided automatically, used to manage pause/resume.
        
    Returns:
        Status dictionary (pending, approved, or rejected).
    """
    
    # SCENARIO 1: Check if the tool is resuming from a pause (Day 2b, Section 3.2)
    if tool_context.tool_confirmation:
        if tool_context.tool_confirmation.confirmed:
            return {"status": "approved", "message": f"Human approved the {document_type}. Final document delivered."}
        else:
            return {"status": "rejected", "message": f"Human rejected the {document_type}. Please revise the plan."}

    # SCENARIO 2: If this is the first call, request confirmation and PAUSE (Day 2b, Section 3.2)
    tool_context.request_confirmation(
        hint=f"⚠️ High-stakes document created: {document_type}. Requires review before delivery.",
        payload={"document_type": document_type, "draft_start": document_draft[:50]}
    )
    
    # ADK sends 'pending' status and pauses execution
    return {"status": "pending", "message": f"Draft created for {document_type}. Awaiting human approval."}


# --- Agent Definition (The Brain) ---

coach_agent = LlmAgent(
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    name="CareerCoachAgent",
    description="A specialized agent providing pitch coaching for interviews, managing sensitive career narratives (e.g., layoffs), and implementing human-in-the-loop approval for high-stakes actions.",
    instruction=f"""
    You are the Career Coach Agent. Your mission is to build user confidence and prepare them for sensitive conversations.

    CRITICAL BEHAVIOR:
    1. Retrieval: ALWAYS use the '{load_memory}' tool first to retrieve the user's career history, sensitive notes (like layoff reasons, past review comments), and known skill gaps (Day 3 principle).
    2. Drafting: Use the 'generate_pitch_narrative' tool to create the initial draft pitch or narrative.
    3. Approval: After creating a sensitive document (like a layoff pitch, or final resume), you MUST IMMEDIATELY use the 'request_human_review' tool. Do NOT release the final document until approval status is 'approved'.
    4. Task: If the user asks for mock interview practice, simulate a 5-minute scenario and score their response (LLM-as-a-Judge approach).
    """,
    tools=[
        load_memory, # <-- Corrected tool name for memory access  # Proactive memory retrieval (Day 3)
        FunctionTool(generate_pitch_narrative), # Custom tool (Day 2)
        FunctionTool(request_human_review), # Custom LRO tool (Day 2b)
    ],
    #is_a2a_server=False,
)

print("Career Coach Agent module loaded.")