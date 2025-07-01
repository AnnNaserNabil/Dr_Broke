import streamlit as st
import logging
import os
import json
from datetime import datetime
from agno.agent import Agent
from agno.models.google import Gemini

# Constants
SAVE_FILE = "sessions/review_history.json"

# Streamlit Page Config
st.set_page_config(page_title="🧠 LeetCode Code Reviewer", page_icon="🧠", layout="wide")

# Logging setup
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# Get secrets
gemini_api_key = st.secrets.get("GEMINI_API_KEY")

# Session Persistence Functions
def save_review_history(history):
    os.makedirs("sessions", exist_ok=True)
    with open(SAVE_FILE, "w") as f:
        json.dump(history, f, indent=2)

def load_review_history():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    return []

# Load review history if not present
if 'review_history' not in st.session_state:
    st.session_state.review_history = load_review_history()

# Agent Initializer
def initialize_evaluator_agents(api_key: str) -> tuple:
    try:
        model = Gemini(id="gemini-2.0-flash-exp", api_key=api_key)

        code_explainer = Agent(
            model=model,
            name="Code Explainer",
            instructions=[
                "You are a detailed technical explainer of code logic and structure.",
                "Go through the code line by line, explaining what each part does.",
                "Break down all functions, control flows, loops, conditions, and data structures used.",
                "Respond in markdown using this format:",
                "### 🔎 Code Walkthrough\nExplain what happens from the start to the end, including all helper functions.",
                "### ⚙️ Function Breakdown\nFor each function, explain parameters, return value, and role in the solution.",
                "### 📊 Data Structures Used\nMention the data structures used, why they were chosen, and how they impact performance."
            ],
            markdown=True
        )

        code_evaluator = Agent(
            model=model,
            name="Code Evaluator",
            instructions=[
                "You are an expert algorithm master evaluating submitted code.",
                "Return output in the following structured format with markdown:",
                "### 🔍 Code Summary\nBriefly explain what this code is trying to solve.",
                "### ⏱️ Time & Space Complexity\nState Big-O complexity for worst and average cases.",
                "### 📐 Code Structure & Style\nComment on the code's readability, organization, and clarity.",
                "### 🧼 Clean Code Score\nGive a score out of 10 with a short justification."
            ],
            markdown=True
        )

        code_judge = Agent(
            model=model,
            name="Code Judge",
            instructions=[
                "You are an elite problem judge like a LeetCode moderator.",
                "Respond in markdown with:",
                "### 🧪 Test Verdict\nNormal Case ✅ | Edge Case ❗ | Large Input 🚀",
                "### 🧠 Logical Correctness\nExplain flaws if any.",
                "### 🔥 Verdict\n✅ Accepted | ⚠️ TLE | ❌ Wrong Answer",
                "### 🛠️ Diagnostic Tip\n1-line insight for debugging."
            ],
            markdown=True
        )

        code_critic = Agent(
            model=model,
            name="Code Critic",
            instructions=[
                "You are a seasoned code critic analyzing the solution.",
                "Break down into:",
                "### ❌ Pain Points\nTop issues in logic, structure, or performance.",
                "### 🧠 Better Practices\nImprovements and justifications.",
                "### ⚡ Missed Optimization Opportunities\nMention better algorithms or structures."
            ],
            markdown=True
        )

        code_improver = Agent(
            model=model,
            name="Code Improver",
            instructions=[
                "You are a master developer rewriting this code to be better.",
                "### 🚀 Improved Version (with explanation)\nExplain what changed and why.",
                "### 📦 Optimized Code\nRespond with clean, efficient code block."
            ],
            markdown=True
        )

        return code_explainer, code_evaluator, code_judge, code_critic, code_improver

    except Exception as e:
        st.error(f"Error initializing agents: {str(e)}")
        return None, None, None, None, None

# Sidebar
st.sidebar.markdown("## 👨‍💻 Developed By")
st.sidebar.image("https://avatars.githubusercontent.com/u/16422192?s=400", width=100)
st.sidebar.markdown("""
**Ann Naser Nabil**  
_AI Engineer & Creative Technologist_  
📧 [Email](mailto:ann.n.nabil@gmail.com)  
🐙 [GitHub](https://github.com/AnnNaserNabil)  
🔗 [LinkedIn](https://linkedin.com/in/ann-naser-nabil)  
---
**💬 Motto**  
_"Build smarter agents for better solutions."_
""", unsafe_allow_html=True)

# Header
st.title("🧠 LeetCode Code Reviewer")
st.markdown("### Paste your solved problem below and get a full technical review!")

# Input
st.text_area("📝 Problem Statement", key="problem", height=200, placeholder="Paste the full problem statement here.")
st.text_area("💻 Your Code", key="code", height=250, placeholder="Paste your code here.")
language = st.selectbox("Preferred Language", ["Python", "Java", "C++", "JavaScript"])
difficulty = st.selectbox("Difficulty Level", ["Easy", "Medium", "Hard", "Unknown"])

# Review button
if st.button("🚀 Review My Code", type="primary"):
    user_problem = st.session_state.problem.strip()
    user_code = st.session_state.code.strip()

    if not gemini_api_key:
        st.error("❌ Gemini API Key not found in secrets.")
    elif not user_problem or not user_code:
        st.warning("Please provide both the problem and your code.")
    else:
        code_explainer, code_evaluator, code_judge, code_critic, code_improver = initialize_evaluator_agents(gemini_api_key)

        if all([code_explainer, code_evaluator, code_judge, code_critic, code_improver]):
            full_context = f"Problem:\n{user_problem}\n\nCode:\n```{language}\n{user_code}\n```"

            session_data = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "problem": user_problem,
                "code": user_code,
                "language": language,
                "difficulty": difficulty
            }

            with st.spinner("📖 Explaining your code..."):
                explanation = code_explainer.run(message=full_context).content
                st.subheader("📖 Code Explanation")
                st.markdown(explanation)
                session_data["explanation"] = explanation

            with st.spinner("🔍 Evaluating Code..."):
                evaluation = code_evaluator.run(message=full_context).content
                st.subheader("🔍 Code Evaluation")
                st.markdown(evaluation)
                session_data["evaluation"] = evaluation

            with st.spinner("⚖️ Judging Code..."):
                judgement = code_judge.run(message=full_context).content
                st.subheader("⚖️ Judgement Verdict")
                st.markdown(judgement)
                session_data["judgement"] = judgement

            with st.spinner("🕵️ Analyzing Drawbacks..."):
                criticism = code_critic.run(message=full_context).content
                st.subheader("🕵️ Critic Analysis")
                st.markdown(criticism)
                session_data["criticism"] = criticism

            with st.spinner("🚀 Rewriting Optimized Code..."):
                improvement = code_improver.run(message=full_context).content
                st.subheader("🚀 Improved Solution")
                st.markdown(improvement)
                session_data["improvement"] = improvement

            # Append and Save Session
            st.session_state.review_history.append(session_data)
            save_review_history(st.session_state.review_history)
        else:
            st.error("⚠️ Could not initialize one or more agents.")

# Manual Load Button
if st.button("🔄 Load Saved Sessions"):
    st.session_state.review_history = load_review_history()
    st.success("Loaded saved review sessions.")

# Display Review History
if st.session_state.review_history:
    st.markdown("## 📚 Previous Review Sessions")
    for session in reversed(st.session_state.review_history):
        with st.expander(f"🧠 {session['timestamp']} — {session['language']} | {session['difficulty']}"):
            st.markdown(f"### 📋 Problem Statement\n{session['problem']}")
            st.markdown(f"### 💻 Code\n```{session['language'].lower()}\n{session['code']}\n```")
            st.markdown(f"### 📖 Code Explanation\n{session['explanation']}")
            st.markdown(f"### 🔍 Code Evaluation\n{session['evaluation']}")
            st.markdown(f"### ⚖️ Judgement Verdict\n{session['judgement']}")
            st.markdown(f"### 🕵️ Critic Analysis\n{session['criticism']}")
            st.markdown(f"### 🚀 Improved Solution\n{session['improvement']}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray'>
    <p>Made with ❤️ by <b>Ann Naser Nabil</b></p>
    <p>🧠 Master Problem Solving with AI Agents</p>
</div>
""", unsafe_allow_html=True)