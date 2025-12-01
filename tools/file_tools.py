# tools/file_tools.py
# Low-level atomic tools for simulating file I/O (resume storage, output generation)

import os
import json
from typing import Dict, Any, Union, List

# --- Configuration: File Locations ---
# This path must be correct relative to the location where runner.py is executed.
RESUME_FILE_PATH = os.path.join("data", "resume.txt")
OUTPUT_DIR = "output"

# Ensure the output directory exists
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# --- Helper Data Structures (Simulating Persistent User Files/Memory - Day 3 Concept) ---
# NOTE: This dictionary simulates both long-term preferences and saved output artifacts.
MOCK_USER_FILES: Dict[str, str] = {
    # Mock data for demonstration purposes
    "user:resume:raw": "Placeholder resume content.",
    "user:preferences:location": "San Francisco, CA",
    "user:preferences:salary": "$120,000+",
    # Example preference stored for the Coach Agent (Long-Term Memory/Preferences - Day 3)
    "user:coaching:layoff_reason": "I was part of a major workforce reduction due to global economic slowdown in Q3 2024.",
}


# --- Tools for File/Data Interaction (Day 2 Concept) ---

def load_user_resume() -> Dict[str, Union[str, int]]:
    """
    [TOOL] Retrieves the full text content of the user's resume from the local filesystem.
    This replaces the mock data lookup to fix the file loading issue.
    
    Returns:
        A dictionary containing the status, content (full resume text), and character count.
    """
    if not os.path.exists(RESUME_FILE_PATH):
        return {
            "status": "error",
            "message": f"Resume file not found at {RESUME_FILE_PATH}.",
            "content": "",
            "char_count": 0
        }
    
    try:
        # Action: Read the actual file content from disk (Production I/O)
        with open(RESUME_FILE_PATH, "r", encoding="utf-8") as f:
            resume_content = f.read()
        
        if not resume_content or len(resume_content) < 32:
            return {
                "status": "warning",
                "message": "Resume file was read but appears to be empty or too short (<32 chars).",
                "content": "",
                "char_count": 0
            }
            
        return {
            "status": "success",
            "content": resume_content,
            "char_count": len(resume_content)
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to read resume file content: {str(e)}",
            "content": "",
            "char_count": 0
        }


def save_artifact(artifact_name: str, content: str) -> str:
    """
    [TOOL] Stores a generated document (e.g., tailored resume, final pitch, study plan)
    in the simulated output storage AND saves it locally for demonstration.
    
    This tool supports the ResumeTailorAgent and CoachAgent by finalizing deliverables.
    
    Args:
        artifact_name: Descriptive name for the saved file (e.g., 'Tailored_Resume_for_J102').
        content: The text content of the artifact.
        
    Returns:
        A confirmation message including the artifact name and content length.
    """
    # 1. Simulate saving to a file or database entry (using mock dictionary)
    MOCK_USER_FILES[f"artifact:{artifact_name}"] = content
    
    # 2. Save artifact to local 'output' directory (Production readiness/Demo artifact)
    output_filename = f"{artifact_name}.txt"
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"TOOL_OUTPUT: Saved artifact: {artifact_name} to {output_path}")
        return f"Artifact successfully saved: '{artifact_name}' ({len(content)} characters). Output saved to {output_path}"
    except Exception as e:
        return f"Artifact saved to mock storage, but local file save failed: {str(e)}"


def get_layoff_context(user_id: str = "ds_student_user") -> str:
    """
    [TOOL] Retrieves the user's specific context or preferred narrative regarding a layoff 
    or employment gap, used by the Coach Agent. (Day 3: Long-Term Memory/Preferences)
    
    Args:
        user_id: The ID of the user.
        
    Returns:
        The user's stored explanation for an employment gap.
    """
    # Note: This simulates retrieving 'preference' memory from long-term storage [5, 6].
    key = f"{user_id}:coaching:layoff_reason".replace("ds_student_user:", "")
    layoff_context = MOCK_USER_FILES.get(key, "User has no recorded layoff context.")
    print(f"TOOL_OUTPUT: Retrieved layoff context.")
    return layoff_context

print("File Tools module loaded and ready for agent integration.")