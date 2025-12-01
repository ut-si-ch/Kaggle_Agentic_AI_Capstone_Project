
import os
import io
import re
import asyncio
import contextlib
from pathlib import Path
from typing import Tuple, Any, Dict

import streamlit as st

# Windows event loop policy fix (helps avoid the "Event loop is closed" / SSL errors)
if os.name == "nt":
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except Exception:
        pass

# Import your project runner and tools
# runner.run_mission should be an async coroutine that prints logs to stdout
import runner

# Import the mock storage from your tools so we can inject uploaded resume text
from tools.file_tools import MOCK_USER_FILES

# -------------------------
# Helper utilities
# -------------------------

def run_async_and_capture_stdout(coro) -> Tuple[str, Exception]:
    """
    Run an async coroutine and capture stdout into a string buffer.
    Returns tuple (captured_text, exception_or_None).
    Uses asyncio.run() so it runs synchronously from Streamlit.
    """
    buf = io.StringIO()
    exc = None
    try:
        with contextlib.redirect_stdout(buf):
            asyncio.run(coro)
    except Exception as e:
        # capture exception message in buffer too so user can see
        buf.write(f"\n[ERROR] Exception while running mission: {e}\n")
        exc = e
    return buf.getvalue(), exc

def extract_final_response(raw_output: str) -> Tuple[str, str]:
    """
    Extracts the main assistant final message from the raw printed logs.
    Heuristics:
    - Look for lines like "[FINAL RESPONSE] > ..." (ADK style)
    - Otherwise, take the portion between the last header line and "Mission Completed."
    Returns (final_text, rest_logs)
    """
    final_text = ""
    rest = raw_output

    # Pattern 1: [FINAL RESPONSE] > ...
    m = re.search(r"\[FINAL RESPONSE\]\s*> ?(.*?)(?:\n={3,}|\n\[|$)", raw_output, re.S)
    if m:
        final_text = m.group(1).strip()
        # remove that part from rest
        rest = raw_output.replace(m.group(0), "")
        return final_text, rest

    # Pattern 2: Use "FINAL RESPONSE" block or "Mission Completed." boundaries
    # Try to capture any block after "AGENT EXECUTION TRACE" and before "Mission Completed."
    m2 = re.search(r"(?:\n\n)?(.*?)\n+==+[\s\S]*?Mission Completed\.", raw_output)

    if m2:
        # fallback: take last chunk
        final_text = m2.group(1).strip()
        rest = raw_output.replace(m2.group(0), "")
        return final_text, rest

    # Otherwise, search for obvious candidate: last non-empty text chunk
    lines = [ln for ln in raw_output.splitlines() if ln.strip()]
    if lines:
        final_text = "\n".join(lines[-15:]) # last up-to-15 lines
        return final_text.strip(), rest
    
    return final_text, rest

# --- NOTE: Removed chat_bubble and sanitize_for_html functions ---

# -------------------------
# Streamlit layout and session state
# -------------------------

st.set_page_config(page_title="MultiAgentic Data Science Agent", layout="wide") 
st.title("MultiAgentic Data Science Agent — Submission Demo") 
st.markdown(
"""
This **Level 3 Multi-Agent System** orchestrates specialized agents (Tutor, Research, Coach, Tailor) 
to make Data Science professionals placement-ready. It demonstrates mastery of A2A, LRO, and Memory systems.
"""
)

# Sidebar
with st.sidebar:
    st.header("Session & Controls")
    user_id = st.text_input("User ID", value=st.session_state.get("user_id", "DS_Candidate_123"))
    st.session_state["user_id"] = user_id
    st.text("Model (from runner):")
    st.caption("Configured in your runner.py")
    st.markdown("---")
    st.markdown("**Important**: Ensure `runner.py` and `.env` are configured (GOOGLE_API_KEY).")
    
    if st.button("Clear chat history"):
        st.session_state["chat_history"] = []

# init chat history if missing
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [] # list of dicts: {"sender":"user"|"agent","text":..., "raw":...}

# Tabs (Note: st.tabs returns a list/sequence)
tabs = st.tabs(["Chat (Multi-Turn)", "Resume Analyzer", "Coach & Layoff Pitch", "Debug / Logs"])

# -------------------------
# TAB 1: Multi-turn Chat (Index 0)
# -------------------------

with tabs[0]: 
    st.subheader("Tutor / Research Agent — Multi-Turn Chat")
    st.write("Use this tab to interact with the **Tutor Agent** (conceptual quizzes) or the **Research Agent** (market trends).")

    # Display chat history in simple windows/text blocks
    history_box = st.container()
    with history_box:
        for msg in st.session_state["chat_history"]:
            sender = msg["sender"].capitalize()
            # Use st.expander or st.markdown for simple display without custom HTML styling
            if sender == 'User':
                st.markdown(f"**👤 You:** {msg['text']}")
            else:
                st.info(msg['text'], icon="🧠")
            st.markdown("---")

    # Input row
    col1, col2 = st.columns([1, 2])
    with col1:
        user_message = st.text_area("You:", key="user_input", height=90, placeholder="Ask the Tutor Agent about A/B testing, gradient boosting, or request a quick quiz...")
    with col2:
        chosen_agent = st.selectbox("Target Agent", options=["ds_tutor_agent", "research_agent"], index=0)
        send_btn = st.button("Send", key="send_button")

    if send_btn and user_message.strip():
        # append user message to history
        st.session_state["chat_history"].append({"sender": "user", "text": user_message})

        # build mission for a chat continuation style:
        mission = (
            f"[CHAT_TO_AGENT] agent:{chosen_agent}\n" 
            f"User ID: {user_id}\n"
            f"Task: {user_message}\n\n"
            "Please respond concisely and include steps or examples as required."
        )

        # run the orchestrator and capture raw output synchronously
        with st.spinner("Running orchestrator and delegating task..."):
            raw_out, exc = run_async_and_capture_stdout(runner.run_mission(mission))
        
        final_text, rest_logs = extract_final_response(raw_out)

        # If the agent returned nothing helpful, show friendly diagnostic
        if not final_text.strip():
            # include either raw_out or a friendly message
            if exc is not None:
                final_text = f"[Agent error] {str(exc)}\n\n(See Debug logs tab for raw output.)"
            else:
                # try to show some last lines of raw output
                final_text = "(No final response detected.)\n\nRaw logs preview:\n" + "\n".join(raw_out.splitlines()[-12:])

        # append agent reply and keep raw logs attached
        st.session_state["chat_history"].append({"sender": "agent", "text": final_text, "raw": raw_out})

        # Rerun to display updated history and clear input
        st.rerun()

# -------------------------
# TAB 2: Resume Analyzer (Index 1)
# -------------------------

with tabs[1]:
    st.subheader("Resume Analyzer & ATS Feedback (File I/O Demo)")
    st.info("Demonstrates custom **File I/O Tools** and **Structured Output (ATS Score)**.")
    
    st.write("Upload resume (.txt preferred). Resume text will be stored in the agent's mock memory and analyzed against a pasted Job Description (JD).")
    
    uploaded_file = st.file_uploader("Upload resume file (.txt, .pdf, .docx)", type=["txt", "pdf", "docx"])
    jd_text = st.text_area("Paste Target Job Description (JD) here:", height=200)
    
    analyze_btn = st.button("Analyze Resume vs JD", key="analyze_resume")

    if analyze_btn:
        if not uploaded_file:
            st.warning("Please upload a resume file first.")
        elif not jd_text.strip():
            st.warning("Please paste the Job Description to compare against.")
        else:
            filename = uploaded_file.name.lower()
            try:
                if filename.endswith(".txt"):
                    resume_text = uploaded_file.read().decode("utf-8", errors="ignore")
                else:
                    resume_bytes = uploaded_file.read()
                    # Simple decode fallback for non-text files
                    resume_text = resume_bytes.decode("utf-8", errors="ignore")
                st.info("Non-txt upload: text extraction may be imperfect. Using raw text extraction.")

            except Exception as e:
                resume_text = f"[ERROR extracting upload: {e}]"

            # Inject into mock memory used by tools.file_tools
            MOCK_USER_FILES["user:resume:raw"] = resume_text
            st.success("Resume uploaded successfully to mock storage (ADK Memory Tool ready).")

            mission = (
                "TASK: resume_review\n"
                f"User ID: {user_id}\n"
                "Action: Ask ResumeTailorAgent to analyze the user's resume (from memory/file tools) against the following Job Description and return a structured summary (match score, top missing skills, suggested rewrites).\n\n"
                "Job Description:\n"
                f"{jd_text}\n\n"
                "Please produce a concise ATS score summary and suggested ATS-friendly rewrite snippets."
            )

            with st.spinner("Analyzing resume (calling ResumeTailorAgent via orchestrator)..."):
                raw_out, exc = run_async_and_capture_stdout(runner.run_mission(mission))

            final_text, rest_logs = extract_final_response(raw_out)

            # show cleaned answer in a simple text area
            st.markdown("**ATS Analysis Result:**")
            st.text_area("ATS Analysis Result", value=final_text or "(No final parsed response)", height=250)

            st.markdown("**Raw logs (hidden by default)**")
            if st.checkbox("Show raw logs for this analysis", key="show_resume_raw"):
                st.code(raw_out)

            # Offer follow-up action if we got analysis: generate ATS resume
            if final_text and ("Match Score" in final_text or "match score" in final_text.lower()):
                if st.button("Generate ATS-friendly Resume (based on suggestions)"):
                    follow_mission = (
                        "TASK: generate_ats\n"
                        f"User ID: {user_id}\n"
                        "Action: Ask ResumeTailorAgent to produce an ATS-friendly resume document given the prior analysis and user's resume in memory. Output only the generated document text."
                    )

                    with st.spinner("Generating ATS-friendly resume..."):
                        raw_out2, exc2 = run_async_and_capture_stdout(runner.run_mission(follow_mission))
                        final_text2, rest2 = extract_final_response(raw_out2)

                    st.markdown("**Generated ATS Resume (preview):**")
                    st.text_area("ATS Resume", value=final_text2 or raw_out2, height=350)

# -------------------------
# TAB 3: Coach & Layoff Pitch (Index 2)
# -------------------------

with tabs[2]:
    st.subheader("Coach Agent: Layoff Pitch & Interview Prep")
    st.warning("This task involves sensitive, high-stakes communication. It demonstrates the **Long-Running Operation (LRO)** pattern: outputs require human review before finalization.")

    st.write("Enter your professional context. The CoachAgent will draft sensitive narratives (interview pitch, LinkedIn About).")
    
    context = st.text_area("Your role & layoff context (1-4 short paragraphs):", height=180)
    requested_item = st.selectbox("Generate:", options=["Layoff pitch (short)", "LinkedIn About", "Interview intro (30s)"])
    generate_btn = st.button("Generate Pitch / Draft", key="generate_coach")

    if generate_btn:
        if not context.strip():
            st.warning("Please enter your role + layoff context to generate a personalized pitch.")
        else:
            mission = (
                f"TASK: coach_pitch\nUser ID: {user_id}\n"
                "Action: Ask CoachAgent to draft a sensitive, professional narrative based on the user's context.\n\n"
                f"Requested: {requested_item}\n\nUser Context:\n{context}\n\n"
                "Please create a compassionate, professional, and concise draft suitable for interviews and LinkedIn. This may require human approval if deemed high-stakes."
            )

            with st.spinner("Generating pitch via CoachAgent (may include LRO pause)..."):
                raw_out, exc = run_async_and_capture_stdout(runner.run_mission(mission))

            final_text, rest_logs = extract_final_response(raw_out)

            # If agent didn't produce a final text, show short diagnostics
            if not final_text:
                final_text = "(No final response detected; check Debug / Logs for raw output.)"

            # Present as a roomy, wrapped text area with no horizontal scrollbar
            st.markdown("**Draft produced by Coach / Orchestrator:**")
            st.text_area("Generated Draft", value=final_text, height=300)

            if st.checkbox("Show raw logs for this draft", key="show_coach_raw"):
                st.code(raw_out)

# -------------------------
# TAB 4: Debug / Logs (Index 3)
# -------------------------

with tabs[3]: 
    st.subheader("Debug / Diagnostics (Observability Demo)")
    st.write("Inspect tool memory and run basic health checks to demonstrate **Day 4 Observability** principles.")

    # Retrieve memory keys check (demonstrates custom tools/memory integration)
    try:
        if st.button("Show MOCK_USER_FILES keys"):
            st.write(list(MOCK_USER_FILES.keys()))
    except NameError:
        st.error("MOCK_USER_FILES object not found (check `tools/file_tools.py` import).")


    if st.button("Run a health check mission"):
        mission = "TASK: health_check\nAction: Please respond with 'OK' from the orchestrator."
        with st.spinner("Running health check..."):
            raw_out, exc = run_async_and_capture_stdout(runner.run_mission(mission))
        st.code(raw_out)

    st.markdown(
"""
**Common issues & tips**
- If you see `503 UNAVAILABLE` or `model overloaded`: your Gemini API or account quota is rate-limited. Try later or reduce parallel calls.
- If you see function-calling errors like `Tool use with function calling is unsupported`, Gemini's function-calling mode or ADK tool config may be incompatible with your local setup.
- Use the "Show raw logs" checkboxes in other tabs to inspect full agent execution traces and tool calls.
"""
    )

    st.caption("Do not commit your .env file or API keys to GitHub. See README for deployment & submission instructions.")
