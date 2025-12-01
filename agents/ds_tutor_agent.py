# agents/ds_tutor_agent.py
# Specialized agent for Data Science Concept Tutoring and Skill Gap Analysis

import os
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types
from google.adk.tools import load_memory # <-- ADD the working tool

# Load environment variables for configuration
# Assuming GOOGLE_API_KEY is available via os.environ (loaded by runner.py)

# --- Configuration (Copied from runner.py for consistency) ---
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[18-21],
)

# --- Define Internal Tools (Demonstrates Day 2 custom tool integration) ---

def create_short_quiz(topic: str, num_questions: int = 3) -> str:
    """
    Generates a brief, multiple-choice quiz about a specific Data Science or Machine Learning topic
    to test the user's understanding.
    Args:
        topic: The ML/DS concept for the quiz (e.g., 'Gradient Descent').
        num_questions: The number of questions to generate (default is 3).
    Returns:
        A structured string containing the quiz questions and answers.
    """
    # NOTE: In a real system, this function would use an external API or code execution tool
    # to guarantee code examples and accurate questions. Here we rely on the LLM.
    return f"REQUEST: Generate a {num_questions}-question diagnostic quiz on the topic: {topic}. Output in Markdown format."

# --- Agent Definition (The Brain) ---

ds_tutor_agent = LlmAgent(
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    name="DataScienceTutorAgent",
    description="A specialized agent dedicated to teaching, quizzing, and diagnosing conceptual gaps in Data Science, Machine Learning, and technical interview topics.",
    instruction=f"""
    You are the Data Science Tutor Agent. Your goal is to ensure the user fully masters complex DS/ML concepts.
    
    CRITICAL BEHAVIOR:
    1. Retrieval: ALWAYS use the '{load_memory}' tool before responding to automatically load the user's recorded skill profile, study history, and known gaps from long-term memory.
    2. Teaching: Explain concepts clearly, providing code examples (when relevant), and adjust complexity based on the retrieved user skill level.
    3. Assessment: When asked to diagnose a skill or create practice problems, you MUST first use the 'create_short_quiz' tool. If the user asks for a study plan, generate a 2-week plan tailored to their known skill gaps.
    4. Conciseness: Keep core explanations under 400 words.
    """,
    tools=[
        create_short_quiz, # Day 2 custom function tool
        load_memory, # <-- Corrected tool name for memory access
    ],
    # Configuration to ensure agent is discoverable by the Orchestrator
    #is_a2a_server=False, # This agent is consumed internally by the orchestrator
)

print("DS Tutor Agent module loaded.")