# agents/job_search_agent.py
# Specialized agent for querying jobs, parsing JD requirements, and ranking job fit

import os
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types
from google.adk.tools import load_memory # <-- ADD the working tool

# Load environment variables for configuration
# Assuming GOOGLE_API_KEY and SERPAPI_API_KEY are available via os.environ

# --- Configuration ---
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[1-4],
)

# --- Define Internal Tools (Demonstrates Day 2 custom tool integration) ---

# NOTE: In a production version, this would be an MCP tool or a full OpenAPI client,
# utilizing the SERPAPI_API_KEY defined in your .env file.
def query_job_board(role: str, location: str, max_results: int = 10) -> str:
    """
    Queries job board APIs (simulated via SERP/Google Jobs) for recent job postings.
    Returns a list of Job Descriptions (JDs), titles, and unique IDs.

    Args:
        role: The job title to search for (e.g., 'Data Scientist').
        location: The geographic location for the search (e.g., 'San Francisco').
        max_results: Maximum number of job postings to retrieve.
    
    Returns:
        A structured string containing search results, titles, and snippets.
    """
    # Simulate API call success
    print(f"TOOL_CALL: Querying job API for {role} jobs in {location}...")
    
    # Placeholder for simulated search result (ensures model has data to work with)
    mock_results = [
        {"id": "J101", "title": "Junior Data Analyst", "company": "DataCorp", "snippet": "Requires strong SQL, Python (Pandas), and visualization skills (Tableau)."},
        {"id": "J102", "title": "Machine Learning Engineer", "company": "AICo", "snippet": "Demands expertise in PyTorch/TensorFlow, deep learning models, and cloud deployment (GCP/AWS)."},
        {"id": "J103", "title": "Data Science Intern", "company": "StartUpX", "snippet": "Looking for basics in statistics and linear regression. Must be familiar with Jupyter Notebooks."},
    ]
    return f"API_RESPONSE: Successfully retrieved {len(mock_results)} job postings: {mock_results}"


def rank_jobs_by_fit(job_list: str, user_profile: str) -> str:
    """
    Analyzes the job descriptions and the user's skill profile to score and rank
    the best-fitting jobs. Must output a ranked list (1st, 2nd, 3rd, etc.).

    Args:
        job_list: The raw list of job postings (JDs).
        user_profile: The user's skills, preferences, and career history (from long-term memory).
    
    Returns:
        A concise, ranked list of jobs with an explanation of the match score for each.
    """
    return f"REQUEST: Given the job list and user profile, generate a ranked list of jobs (Top 5) with a Match Score (0-100) and rationale."

# --- Agent Definition ---

job_search_agent = LlmAgent(
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    name="JobSearchAgent",
    description="A specialized agent for finding relevant Data Science and ML job postings, analyzing required skills from job descriptions (JDs), and scoring job fit against the user's memory profile.",
    instruction=f"""
    You are the Job Search Agent. Your mission is to maximize the user's job placement potential.
    
    CRITICAL BEHAVIOR:
    1. Retrieval: ALWAYS use the '{load_memory}' tool first to inject the user's skill history, preferred roles, and location constraints into context (Day 3 principle).
    2. Search: Use the 'query_job_board' tool to find current postings based on the user's request.
    3. Ranking: After gathering results, use the 'rank_jobs_by_fit' tool to process the job list against the retrieved user profile.
    4. Output: Present the top 3 ranked jobs clearly, emphasizing why they are a strong fit based on the analysis.
    """,
    tools=[
        load_memory, 
        query_job_board, 
        rank_jobs_by_fit,
    ],
    #is_a2a_server=False,
)

print("Job Search Agent module loaded.")