# tools/memory_tools.py

import os
from google.adk.memory import InMemoryMemoryService

# Initialize a memory service instance (local DB)
memory_service = InMemoryMemoryService()

def save_memory(key: str, value: str):
    """Save a memory item under a specific key."""
    memory_service.save_memory(user_id="DS_Candidate_123", key=key, value=value)
    return f"Memory stored under key: {key}"

def load_memory(key: str):
    """Load a memory item by key."""
    memory_item = memory_service.load_memory(user_id="DS_Candidate_123", key=key)
    if memory_item:
        return memory_item
    return f"No memory found for key: {key}"
