import streamlit as st
import logging
from datetime import datetime
from agno.agent import Agent
from agno.models.google import Gemini

# Streamlit Page Config
st.set_page_config(page_title="🧠 LeetCode Code Reviewer", page_icon="🧠", layout="wide")

# Logging setup
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# Get secrets
gemini_api_key = st.secrets.get("GEMINI_API_KEY")

# Initialize history if not exists
if 'review_history' not in st.session_state:
    st.session_state.review_history = []

# Agent Initializer
def initialize_evaluator_agents(api_key: str) -> tuple:
    try:
        model = Gemini(id="gemini-2.0-flash-exp", api_key=api_key)

        code_evaluator = Agent(
            model=model,
            name="Code Evaluator",
            instructions=[
                "You are an expert algorithm master evaluating submitted code.",
                "Return output in the following structured format with markdown:",
                "### 🔍 Code Summary\nBriefly explain what this code is trying to solve.",
                "### ⏱️ Time & Space Complexity\nState Big-O complexity for worst and average cases.",
                "### 📐 Code Structure & Style\nComment on the code's readability, organization, and clarity.",
                "### 🧼 Clean Code Score\nGive a score out of 10 with a short justification.",
                "Write in a clear, professional tone. No fluff. Always assume the user is technically sharp but looking to improve."
            ],
            markdown=True
        )

        code_judge = Agent(
            model=model,
            name="Code Judge",
            instructions=[
                "You are an elite problem judge like a LeetCode competition moderator.",
                "Given the problem and code, simulate these steps and report in markdown:",
                "### 🧪 Test Verdict\nList different categories: Normal Case ✅ | Edge Case ❗ | Large Input 🚀",
                "### 🧠 Logical Correctness\nDoes the logic break anywhere? Explain clearly.",
                "### 🔥 Verdict\nUse: ✅ Accepted | ⚠️ TLE | ❌ Wrong Answer | 🧠 Needs Optimization",
                "### 🛠️ Diagnostic Tip\nOne brief insight for debugging or performance.",
                "Respond concisely but insightfully. Make it feel like a code review by a senior judge."
            ],
            markdown=True
        )

        code_critic = Agent(
            model=model,
            name="Code Critic",
            instructions=[
                "You are a seasoned code critic analyzing the pain points of a solution.",
                "Break down your response into:",
                "### ❌ Pain Points\n- List the top 2-3 issues in the logic, structure, or performance.",
                "### 🧠 Better Practices\n- Recommend improvements with brief justification.",
                "### ⚡ Missed Optimization Opportunities\n- Mention if a better algorithm or structure was possible.",
                "Use bullets, bold key terms, and make it practical for the coder to improve immediately."
            ],
            markdown=True
        )

        code_improver = Agent(
            model=model,
            name="Code Improver",
            instructions=[
                "You are a master developer rewriting this code to be faster, cleaner, and more elegant.",
                "Respond with:",
                "### 🚀 Improved Version (with explanation)\nBriefly explain what changed and why.",
                "### 📦 Optimized Code\nRespond with a well-commented, clean, efficient code block in the specified language.",
                "Use best practices. Avoid overengineering. Think like you're training someone to ace Google interviews."
            ],
            markdown=True
        )

        code_explainer = Agent(
            model=model,
            name="Code Explainer",
            instructions=[
                "You are a detailed technical explainer of code logic and structure.",
                "Go through the code line by line, explaining what each part does.",
                "Break down all functions, control flows, loops, conditions, and data structures used.",
                "Your explanation must be thorough and educational, like a senior engineer mentoring a junior.",
                "Respond in markdown using this format:",
                "### 🔎 Code Walkthrough\nExplain what happens from the start to the end, including all helper functions.",
                "### ⚙️ Function Breakdown\nFor each function, explain parameters, return value, and role in the solution.",
                "### 📊 Data Structures Used\nMention the data structures used, why they were chosen, and how they impact performance.",
                "Be precise and technical, avoid oversimplifying. Use code snippets where needed to clarify."
            ],
            markdown=True
        )

        return code_evaluator, code_judge, code_critic, code_improver, code_explainer

    except Exception as e:
        st.error(f"Error initializing agents: {str(e)}")
        return None, None, None, None, None


# Sidebar Developer Info
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
st.markdown("### Upload your solved LeetCode problem & get AI reviews")

# Input Fields
st.text_area("📝 Problem Statement", key="problem", height=200, placeholder="Paste the full problem statement here.")
st.text_area("💻 Your Code", key="code", height=250, placeholder="Paste your code here.")
language = st.selectbox("Preferred Language", ["Python", "Java", "C++", "JavaScript"])
difficulty = st.selectbox("Difficulty Level", ["Easy", "Medium", "Hard", "Unknown"])

# Run Button
if st.button("🚀 Review My Code", type="primary"):
    user_problem = st.session_state.problem.strip()
    user_code = st.session_state.code.strip()

    if not gemini_api_key:
        st.error("❌ Gemini API Key not found. Please add `GEMINI_API_KEY` to `.streamlit/secrets.toml`.")
    elif not user_problem or not user_code:
        st.warning("Please provide both the problem statement and your code.")
    else:
        code_evaluator, code_judge, code_critic, code_improver, code_explainer = initialize_evaluator_agents(gemini_api_key)

        if all([code_evaluator, code_judge, code_critic, code_improver, code_explainer]):
            full_context = f"Problem:\n{user_problem}\n\nCode:\n```{language}\n{user_code}\n```"

            session_data = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "problem": user_problem,
                "code": user_code,
                "language": language,
                "difficulty": difficulty,
                "evaluation": "",
                "judgement": "",
                "criticism": "",
                "improvement": "",
                "explanation": ""
            }

            with st.spinner("🔍 Evaluating Code..."):
                eval_response = code_evaluator.run(message=full_context)
                st.subheader("🔍 Code Evaluation")
                st.markdown(eval_response.content)
                session_data["evaluation"] = eval_response.content

            with st.spinner("⚖️ Judging Code Performance..."):
                judge_response = code_judge.run(message=full_context)
                st.subheader("⚖️ Judgement Verdict")
                st.markdown(judge_response.content)
                session_data["judgement"] = judge_response.content

            with st.spinner("🕵️ Analyzing Drawbacks..."):
                critic_response = code_critic.run(message=full_context)
                st.subheader("🕵️ Critic Analysis")
                st.markdown(critic_response.content)
                session_data["criticism"] = critic_response.content

            with st.spinner("🚀 Rewriting Optimized Code..."):
                improve_response = code_improver.run(message=full_context)
                st.subheader("🚀 Improved Solution")
                st.markdown(improve_response.content)
                session_data["improvement"] = improve_response.content

            with st.spinner("📖 Explaining Code..."):
                explainer_response = code_explainer.run(message=full_context)
                st.subheader("📖 Code Explanation")
                st.markdown(explainer_response.content)
                session_data["explanation"] = explainer_response.content

            # Save to session history
            st.session_state.review_history.append(session_data)

        else:
            st.error("⚠️ Failed to initialize agents. Please check your configuration.")

# Display Review History
if st.session_state.review_history:
    st.markdown("## 📚 Previous Review Sessions")
    for session in reversed(st.session_state.review_history):
        with st.expander(f"🧠 Review at {session['timestamp']} — {session['language']} | {session['difficulty']}"):
            st.markdown(f"### 📋 Problem Statement\n{session['problem']}")
            st.markdown(f"### 💻 Submitted Code\n```{session['language'].lower()}\n{session['code']}\n```")
            st.markdown(f"### 🔍 Code Evaluation\n{session['evaluation']}")
            st.markdown(f"### ⚖️ Judgement Verdict\n{session['judgement']}")
            st.markdown(f"### 🕵️ Critic Analysis\n{session['criticism']}")
            st.markdown(f"### 🚀 Improved Solution\n{session['improvement']}")
            st.markdown(f"### 📖 Code Explanation\n{session['explanation']}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray'>
    <p>Made with ❤️ by <b>Ann Naser Nabil</b></p>
    <p>🧠 Master Problem Solving with AI Agents</p>
    <p>📚 Review history is saved during this session</p>
</div>
""", unsafe_allow_html=True)