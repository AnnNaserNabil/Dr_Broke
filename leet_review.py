import streamlit as st

# MUST be the first Streamlit command
st.set_page_config(page_title="🧠 LeetCode Code Reviewer", page_icon="🧠", layout="wide")

from agno.agent import Agent
from agno.models.google import Gemini
import logging

# Setup logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# Get API key securely from Streamlit secrets
api_key = st.secrets.get("GEMINI_API_KEY")

# Agent Initializer
def initialize_evaluator_agents(api_key: str) -> tuple:
    try:
        model = Gemini(id="gemini-2.0-flash-exp", api_key=api_key)

        code_evaluator = Agent(
            model=model,
            name="Code Evaluator",
            instructions=[
                "You are a code evaluator for LeetCode problems.",
                "Your role is to analyze the submitted solution code and provide:",
                "1. Summary of what the code is doing",
                "2. Time and space complexity analysis",
                "3. Whether the code follows best practices and clean coding principles",
                "4. Comments on readability and structure",
                "Respond in markdown using clear sections."
            ],
            markdown=True
        )

        code_judge = Agent(
            model=model,
            name="Code Judge",
            instructions=[
                "You are a competitive programming judge evaluating LeetCode solutions.",
                "Given a problem statement and the solution code, perform:",
                "1. Test the code against different input scenarios (normal, edge, large inputs)",
                "2. Report performance concerns or failures",
                "3. Identify if the logic breaks in any edge cases",
                "4. Give a final verdict: Accept / TLE / Wrong Answer / Needs Optimization",
                "Respond in markdown with a verdict and analysis."
            ],
            markdown=True
        )

        code_critic = Agent(
            model=model,
            name="Code Critic",
            instructions=[
                "You are a code reviewer identifying inefficiencies or problems.",
                "1. Spot redundant logic, bad practices, or inefficient patterns",
                "2. Highlight missing edge case handling",
                "3. Identify better algorithm choices",
                "Respond using markdown with clear headings: Drawbacks, Suggestions"
            ],
            markdown=True
        )

        code_improver = Agent(
            model=model,
            name="Code Improver",
            instructions=[
                "You are an expert developer rewriting the solution to be cleaner and more efficient.",
                "1. Optimize time and space complexity",
                "2. Use cleaner syntax, better data structures",
                "3. Output fully working code with comments",
                "Respond with explanation followed by the rewritten code block."
            ],
            markdown=True
        )

        return code_evaluator, code_judge, code_critic, code_improver

    except Exception as e:
        st.error(f"Error initializing agents: {str(e)}")
        return None, None, None, None


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
st.markdown("### Upload your solved LeetCode problem & get AI reviews")

# Input
st.text_area("📝 Problem Statement", key="problem", height=200, placeholder="Paste the full problem statement here.")
st.text_area("💻 Your Code", key="code", height=250, placeholder="Paste your code here.")
language = st.selectbox("Preferred Language", ["Python", "Java", "C++", "JavaScript"])
difficulty = st.selectbox("Difficulty Level", ["Easy", "Medium", "Hard", "Unknown"])

if st.button("🚀 Review My Code", type="primary"):
    user_problem = st.session_state.problem.strip()
    user_code = st.session_state.code.strip()

    if not api_key:
        st.error("❌ API Key not found. Please add `GEMINI_API_KEY` to `.streamlit/secrets.toml`.")
    elif not user_problem or not user_code:
        st.warning("Please provide both the problem statement and your code.")
    else:
        code_evaluator, code_judge, code_critic, code_improver = initialize_evaluator_agents(api_key)

        if all([code_evaluator, code_judge, code_critic, code_improver]):
            full_context = f"Problem:\n{user_problem}\n\nCode:\n```{language}\n{user_code}\n```"

            with st.spinner("🔍 Evaluating Code..."):
                eval_response = code_evaluator.run(message=full_context)
                st.subheader("🔍 Code Evaluation")
                st.markdown(eval_response.content)

            with st.spinner("⚖️ Judging Code Performance..."):
                judge_response = code_judge.run(message=full_context)
                st.subheader("⚖️ Judgement Verdict")
                st.markdown(judge_response.content)

            with st.spinner("🕵️ Analyzing Drawbacks..."):
                critic_response = code_critic.run(message=full_context)
                st.subheader("🕵️ Critic Analysis")
                st.markdown(critic_response.content)

            with st.spinner("🚀 Rewriting Optimized Code..."):
                improve_response = code_improver.run(message=full_context)
                st.subheader("🚀 Improved Solution")
                st.markdown(improve_response.content)
        else:
            st.error("⚠️ Failed to initialize agents. Please check your configuration.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray'>
    <p>Made with ❤️ by <b>Ann Naser Nabil</b></p>
    <p>🧠 Master Problem Solving with AI Agents</p>
</div>
""", unsafe_allow_html=True)
