# runner.py
# Main execution script for the Agentic Data Science Agent (Capstone Project)

import asyncio
import os
import uuid
from dotenv import load_dotenv

# Windows SSL fix
import sys
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Core ADK Imports (LlmAgent from agents, AgentTool from tools)
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService, InMemorySessionService
from google.adk.memory import InMemoryMemoryService # Simulating Memory Bank for local use
from google.adk.tools import AgentTool # Corrected import path
from google.adk.tools import load_memory # <-- ADD the working tool
from google.genai import types

# Import Custom Tools (needed to define tool catalog for agents)
from tools.web_tools import search_current_trends, query_live_job_listings
from tools.file_tools import load_user_resume, save_artifact

# Import Specialized Agents
from agents.ds_tutor_agent import ds_tutor_agent
from agents.research_agent import research_agent
from agents.job_search_agent import job_search_agent
from agents.resume_agent import resume_agent
from agents.coach_agent import coach_agent

# --- 1. Configuration and Setup ---

# Load environment variables (API keys)
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found. Please check your .env file.")

# Global Configuration
APP_NAME = "Agentic Data Science Agent"
USER_ID = "DS_Candidate_123"
MODEL = "gemini-2.5-pro" 

# Model Configuration (Retry Options - Day 4 concept)
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[3-6],
)

# --- 2. Define Root Orchestrator Agent ---

# The Root Agent manages the workflow (Day 1 Orchestration)
root_orchestrator = LlmAgent(
    name="CareerCoPilotRootAgent",
    model=Gemini(model=MODEL, retry_options=retry_config),
    instruction="""
    You are the Career Co-Pilot Root Orchestrator. Your mission is to guide a Data Science candidate to job placement readiness.
    
    You must execute tasks in a logical sequence, delegating specialized work to the appropriate sub-agent tools:
    1. If the user asks about concepts or skills, use the 'ds_tutor_agent'.
    2. If the user asks about market trends or data, use the 'research_agent'.
    3. If the user uploads a resume or asks for tailoring/optimization, use the 'resume_agent'.
    4. If the user needs job searching, ranking, or application support, use the 'job_search_agent'.
    5. If the user needs to practice high-stakes narratives (like explaining a layoff gap), use the 'coach_agent'.
    
    Always aggregate the results and provide a final, cohesive answer.
    """,
    # Agents are wrapped in AgentTool for local A2A delegation (Day 5 concept)
    tools=[
        AgentTool(agent=ds_tutor_agent),
        AgentTool(agent=research_agent),
        AgentTool(agent=job_search_agent),
        AgentTool(agent=resume_agent),
        AgentTool(agent=coach_agent),
        # Custom file tools are also available for saving/loading artifacts
        load_user_resume, 
        save_artifact,
        load_memory, # <-- CRITICAL FIX: Use the functional reactive memory tool
    ],
)

# --- 3. Initialize Services (Day 3 Sessions & Memory) ---

# Use InMemorySessionService for conversation history in this local demo
session_service = InMemorySessionService()

# Use InMemoryMemoryService to simulate persistent knowledge storage 
# In production, this would be Vertex AI Memory Bank [7, 8]
memory_service = InMemoryMemoryService()

# Create the main Runner
runner = Runner(
    agent=root_orchestrator,
    app_name=APP_NAME,
    session_service=session_service,
    memory_service=memory_service, # Memory service provided to runner
)

# --- 4. Execution Loop ---

async def run_mission(mission_query: str):
    """Orchestrates the full multi-agent mission."""
    
    # Generate a unique session ID for the execution
    session_id = f"mission_{uuid.uuid4().hex[:8]}"
    
    print(f"\n{'='*70}")
    print(f"🚀 Starting Mission: '{mission_query}'")
    print(f"🔗 Session ID: {session_id}")
    print(f"{'='*70}")
    
    # Create session 
    # Must use the App Name configured in your system.
    await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=session_id
    )
    
    query_content = types.Content(role="user", parts=[types.Part(text=mission_query)])
    
    # Run the orchestrator asynchronously
    print("\n[AGENT EXECUTION TRACE] (Observability Enabled)")
    
    try:
        # The runner handles the sequencing of agents and tools (Orchestration [6], [7])
        async for event in runner.run_async(
            user_id=USER_ID, session_id=session_id, new_message=query_content
        ):
            if event.content and event.content.parts:
                
                # **CRITICAL FIX: Safely extract text from the list of content parts.**
                # This handles structured parts (like function calls [8]) that do not have a .text attribute.
                text_parts = [
                    p.text for p in event.content.parts 
                    if hasattr(p, 'text') and p.text is not None and p.text != "None"
                ]
                full_text = ' '.join(text_parts).strip()
                
                # Check for the final response event
                if event.is_final_response() and full_text:
                    print(f"\n[FINAL RESPONSE] > {full_text}")
                
                # Print intermediate text events (thoughts, partial responses) for tracing
                elif full_text:
                    # Logs and Traces provide the narrative of actions (Day 4 [9])
                    print(f"[EVENT] > {full_text}")
    
    except Exception as e:
        # This final safeguard prevents an unhandled exception during A2A delegation 
        # from crashing the entire network transport layer (SSL Fatal Error).
        print(f"\n[FATAL EXECUTION ERROR CAUGHT]: An unhandled exception occurred during the agent run: {e}")
        # Note: If this prints, you must examine the agent's tool inputs or outputs 
        # (Day 2b LRO tool patterns [10]) for serialization issues.
                
    print(f"\n{'='*70}\nMission Completed.")

if __name__ == "__main__":
    # Example Mission demonstrating full orchestration:
    mission = (
        "I was recently laid off and need a pitch to explain the gap. "
        "Also, review my resume against the 'Senior Data Analyst' role requirements. "
        "What are the top three skills I should highlight?"
    )
    
    # Note: LROs (Long-Running Operations) requiring human input in coach_agent 
    # must be manually handled by checking events, as detailed in Day 2b [9].
    # For this synchronous demo, we rely on the agent completing a simple task.
    
    # Replace the direct asyncio.run() call:
    # asyncio.run(run_mission(mission))

    # With the graceful shutdown wrapper:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        # Run your agent logic until it completes
        loop.run_until_complete(run_mission(mission))
    finally:
        # Clean up generators gracefully
        loop.run_until_complete(loop.shutdown_asyncgens())
        # Close the event loop
        loop.close()