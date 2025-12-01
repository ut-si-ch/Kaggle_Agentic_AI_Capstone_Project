# agents/research_agent.py
# Specialized agent for finding current market data and authoritative documents

import os
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types
# Using a built-in tool that utilizes Google Search for real-time information (Day 1, Day 2 concept)
from google.adk.tools import google_search

# Load environment variables for configuration
# Assuming GOOGLE_API_KEY is available via os.environ

# --- Configuration (Copied from runner.py for consistency) ---
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[6-9],
)

# --- Define Agent Tools (The Hands) ---

# We define a custom tool to handle the structured output requirement for market trends.
# NOTE: This uses the google_search tool internally, but forces the LLM to structure the output.
def search_hiring_trends(query: str, years: int = 1) -> str:
    """
    Searches the internet for the latest Data Science hiring trends, required tech stacks,
    and salary benchmarks over the last 'years' period. Returns a report structured as a list of findings.
    Args:
        query: The specific job role or trend to search for (e.g., 'Python vs R for DS 2024').
        years: The number of recent years the data should cover (default is 1).
    Returns:
        A formatted report summarizing market trends with citations (URLs if available).
    """
    # The agent's instruction will guide the internal Google Search call and summarization.
    return f"REQUEST: Find top 5 recent hiring trends and skill demands in Data Science for the query: '{query}' over the last {years} year(s). Must include links/citations."

# --- Agent Definition (The Brain) ---

research_agent = LlmAgent(
    model=Gemini(model="gemini-2.5-pro", retry_options=retry_config),
    name="ResearchAgent",
    description="A specialized research assistant that queries real-time data sources (Google Search, SERP APIs) to find the latest industry trends, hiring demands, salary data, and authoritative documents.",
    instruction="""
    You are the Research Agent. Your goal is to provide up-to-date, reliable, and grounded information to the Root Orchestrator.
    
    CRITICAL BEHAVIOR:
    1. Grounding: ALWAYS use the 'google_search' tool for external or current information requests (Day 2 principle).
    2. Structuring: When generating a report on hiring trends, ALWAYS use the 'search_hiring_trends' tool request format to guide the output.
    3. Output: Always include clear citations (e.g., source URLs and dates) for factual claims, adhering to Day 4 quality and grounding best practices.
    4. Delegation: If the user asks a question about general DS concepts or code practice, state clearly that the task belongs to the Tutor Agent.
    """,
    tools=[
        google_search, # Built-in tool (Day 1 concept)
        search_hiring_trends, # Custom tool (Day 2 concept)
    ],
    # Configuration to ensure agent is discoverable by the Orchestrator (A2A setup)
    #is_a2a_server=False, 
)

print("Research Agent module loaded.")