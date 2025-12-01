# init_memory.py
import os
from tools.memory_tools import save_memory  # adjust import if needed

# Path to your local resume file
RESUME_PATH = os.path.join("data", "resume.txt")

if not os.path.exists(RESUME_PATH):
    raise FileNotFoundError("resume.txt not found in /data folder")

# Read your resume
with open(RESUME_PATH, "r", encoding="utf-8") as f:
    resume_text = f.read()

# Save to long-term memory
save_memory("user:resume", resume_text)

print("✔ Resume successfully stored in long-term memory.")
print("Characters stored:", len(resume_text))
