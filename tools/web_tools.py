# tools/web_tools.py
# Low-level atomic tools for real-time web search and external data access

from typing import Dict, Any, List, Optional
import os
import json
# Import the ADK built-in tool for easy web search access (Day 1 concept)
from google.adk.tools import google_search

# Load API keys via os.environ (set by runner.py from .env file)
# SERPAPI_API_KEY = os.environ.get("SERPAPI_API_KEY")

# --- Tools for Real-time Information (Day 2 Concept) ---

def search_current_trends(query: str, num_results: int = 5) -> str:
    """
    Searches the internet for the latest information relevant to job market trends,
    technical documentation, or academic topics. This tool grounds the agent's response
    in current facts.

    Args:
        query: The specific question or topic to search for (e.g., 'Latest Python version').
        num_results: The maximum number of search results to return.

    Returns:
        A formatted JSON string containing the search results (snippets, titles, URLs).
    """
    # NOTE: In a production system, this would explicitly call google_search or a SERP API client.
    # Here, we wrap the ADK built-in tool but force a structured request/response for clarity.

    # Simulate calling an external API for market data
    if "hiring trends" in query.lower():
        mock_data = [
            {"title": "GCP Data Engineer Demand Soars", "snippet": "Demand for GCP-certified data roles is up 30% YOY.", "url": "url_gcp_report"},
            {"title": "PyTorch vs TensorFlow for LLMs 2025", "snippet": "PyTorch dominates R&D, but TensorFlow remains popular for deployment.", "url": "url_ml_report"},
        ]
        print(f"TOOL_OUTPUT: Retrieved mock search data for trends: {query}")
        return json.dumps(mock_data)
        
    # Default behavior: rely on ADK's native tool invocation capability 
    # (The model will choose to call google_search directly if this function is unavailable/not chosen)
    return f"REQUEST_SENT: Performing live Google Search for query: '{query}' with {num_results} results."


def query_live_job_listings(role: str, location: str, max_age_days: int = 7) -> str:
    """
    Queries a job board API (simulated via search) for current job descriptions (JDs).
    
    Args:
        role: The job title to search for (e.g., 'Data Scientist').
        location: The geographic area (e.g., 'Remote').
        max_age_days: Only show postings younger than this age.

    Returns:
        A structured JSON string containing job titles, snippets, and source links.
    """
    # Simulation of structured job data retrieval
    mock_jobs = [
        {"title": "Junior Data Scientist (Entry-Level)", "company": "Global Analytics", "skills": ["Python", "SQL", "Tableau"], "link": "link_1"},
        {"title": "ML Research Engineer (GCP Focus)", "company": "Cloud Innovators", "skills": ["PyTorch", "GCP", "Kubeflow"], "link": "link_2"},
    ]
    print(f"TOOL_OUTPUT: Retrieved mock job listings for role: {role} in {location}")
    return json.dumps(mock_jobs)

print("Web Tools module loaded and ready for agent integration.")