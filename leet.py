import streamlit as st

# ✅ MUST be the first Streamlit command
st.set_page_config(page_title="🧠 LeetCode Solver", page_icon="🧠", layout="wide")

from agno.agent import Agent
from agno.models.google import Gemini
from agno.media import Image as AgnoImage
from typing import List
import logging
import tempfile
import os

# Setup logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# Get API key securely
api_key = st.secrets.get("GEMINI_API_KEY")

# Agent initializer
def initialize_agents(api_key: str) -> tuple:
    try:
        model = Gemini(id="gemini-2.0-flash-exp", api_key=api_key)

        problem_analyzer = Agent(
            model=model,
            name="Problem Analyzer",
            instructions=[
                "You are a LeetCode problem analyzer that:",
                "1. Breaks down the problem statement into clear components",
                "2. Identifies the problem type (Array, String, Tree, Graph, DP, etc.)",
                "3. Extracts key constraints and requirements",
                "4. Identifies edge cases to consider",
                "5. Determines the expected time/space complexity",
                "Always respond in Bengali and English mixed format for better understanding.",
                "Start with a brief summary, then provide detailed analysis."
            ],
            markdown=True
        )

        problem_explainer = Agent(
            model=model,
            name="Problem Explainer",
            instructions=[
                "You are a coding mentor that explains LeetCode problems in depth:",
                "1. Use simple analogies and real-world examples",
                "2. Break down complex concepts into digestible parts",
                "3. Provide step-by-step walkthrough of examples",
                "4. Explain why certain approaches work better than others",
                "5. Help users understand the intuition behind the solution",
                "Use a mix of Bengali and English for clarity.",
                "Focus on building conceptual understanding, not just code."
            ],
            markdown=True
        )

        solution_architect = Agent(
            model=model,
            name="Solution Architect",
            instructions=[
                "You are a coding expert that provides multiple solution approaches:",
                "1. Present solutions from brute force to optimal",
                "2. Provide clean, well-commented code in Python/Java/C++",
                "3. Explain time and space complexity for each approach",
                "4. Show the evolution of thinking from naive to optimal",
                "5. Include code snippets with detailed explanations",
                "Code comments should be in English, explanations in Bengali-English mix.",
                "Always provide at least 2-3 different approaches when possible."
            ],
            markdown=True
        )

        problem_solver_mentor = Agent(
            model=model,
            name="Problem Solver Mentor",
            instructions=[
                "You are a competitive programming mentor that teaches problem-solving mindset:",
                "1. Provide strategic thinking patterns for similar problems",
                "2. Teach when to use specific data structures and algorithms",
                "3. Share debugging techniques and optimization strategies",
                "4. Give advice on how to approach unknown problems",
                "5. Provide tips for interview preparation and competitive programming",
                "6. Share insights on recognizing problem patterns",
                "Mix Bengali and English for better connection with learners.",
                "Focus on developing algorithmic thinking and problem-solving intuition."
            ],
            markdown=True
        )

        return problem_analyzer, problem_explainer, solution_architect, problem_solver_mentor
    except Exception as e:
        st.error(f"Error initializing agents: {str(e)}")
        return None, None, None, None

# UI
st.markdown("# 🧠 LeetCode Solver")
st.markdown("### Advanced Problem Solving Assistant")
st.markdown("---")

# Sidebar: Developer Info
st.sidebar.markdown("## 👨‍💻 Developed By")
st.sidebar.image("https://avatars.githubusercontent.com/u/16422192?s=400&u=64cc1f0c21d7b8fcb54ca59ef9fe50dcca771209&v=4", width=100)

st.sidebar.markdown("""
**Ann Naser Nabil**  
_AI Researcher & Creative Technologist_

📧 [Email](mailto:ann.n.nabil@gmail.com)  
🐙 [GitHub](https://github.com/AnnNaserNabil)  
🔗 [LinkedIn](https://linkedin.com/in/ann-naser-nabil)  

---

**💬 Motto**  
_"Building intelligent AI agents for problem solving."_
""", unsafe_allow_html=True)

# Add helpful information in sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("""
## 🎯 How to Use
1. **Paste the LeetCode problem** (title + description)
2. **Click "Solve করো"** to get comprehensive analysis
3. **Study each agent's response** step by step
4. **Practice the concepts** mentioned

## 📚 What You'll Get
- 🔍 **Problem Analysis**
- 📖 **Deep Explanation**  
- 💻 **Multiple Solutions**
- 🧠 **Solving Strategies**
""")

# Input field
st.subheader("LeetCode Problem দাও, সমাধান নিয়ে যাও")
user_input = st.text_area(
    "LeetCode problem statement পেস্ট করুন:", 
    height=200, 
    placeholder="""Example:
Two Sum
Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.

Example 1:
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1]."""
)

# Additional options
col1, col2 = st.columns(2)
with col1:
    difficulty = st.selectbox("Difficulty Level:", ["Easy", "Medium", "Hard", "Unknown"])
with col2:
    preferred_language = st.selectbox("Preferred Language:", ["Python", "Java", "C++", "JavaScript"])

# Button
if st.button("Solve করো 🚀", type="primary"):
    if not api_key:
        st.error("❌ API Key missing! Add it to `.streamlit/secrets.toml` as GEMINI_API_KEY.")
    elif not user_input.strip():
        st.warning("অনুগ্রহ করে LeetCode problem statement দিন।")
    else:
        problem_analyzer, problem_explainer, solution_architect, problem_solver_mentor = initialize_agents(api_key)
        if all([problem_analyzer, problem_explainer, solution_architect, problem_solver_mentor]):
            try:
                problem_context = f"Problem: {user_input}\nDifficulty: {difficulty}\nPreferred Language: {preferred_language}"

                # Problem Analysis Phase
                with st.spinner("🔍 Problem analyze করছি..."):
                    response = problem_analyzer.run(message=problem_context)
                    st.subheader("🔍 Problem Analysis")
                    st.markdown(response.content)
                    st.markdown("---")

                # Problem Explanation Phase
                with st.spinner("📖 Problem explain করছি..."):
                    response = problem_explainer.run(message=f"Explain this problem in depth: {problem_context}")
                    st.subheader("📖 Deep Problem Understanding")
                    st.markdown(response.content)
                    st.markdown("---")

                # Solution Architecture Phase
                with st.spinner("💻 Multiple solutions তৈরি করছি..."):
                    response = solution_architect.run(message=f"Provide multiple solution approaches for: {problem_context}")
                    st.subheader("💻 Solution Approaches")
                    st.markdown(response.content)
                    st.markdown("---")

                # Problem Solving Mentorship Phase
                with st.spinner("🧠 Problem solving strategies দিচ্ছি..."):
                    response = problem_solver_mentor.run(message=f"Provide problem-solving insights and strategies for: {problem_context}")
                    st.subheader("🧠 Problem Solver's Mindset")
                    st.markdown(response.content)

            except Exception as e:
                logger.error(f"Processing error: {str(e)}")
                st.error("⚠️ Analysis এর সময় ত্রুটি ঘটেছে। দয়া করে আবার চেষ্টা করুন।")
        else:
            st.error("⚠️ Agent গুলো initialize হয়নি। API key সঠিক কিনা দেখুন।")

# Tips section
st.markdown("---")
st.markdown("## 💡 Pro Tips")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **🎯 Problem Approach**
    - Read the problem twice
    - Understand constraints
    - Think of edge cases
    - Start with brute force
    """)

with col2:
    st.markdown("""
    **🔧 Optimization Strategy**
    - Identify bottlenecks
    - Use appropriate data structures
    - Consider time vs space tradeoffs
    - Think of mathematical shortcuts
    """)

with col3:
    st.markdown("""
    **🚀 Best Practices**
    - Write clean, readable code
    - Add meaningful comments
    - Test with examples
    - Practice similar problems
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray'>
    <p>Made with ❤️ by <b>Ann Naser Nabil</b></p>
    <p>🧠 Master Problem Solving with AI Agents</p>
</div>
""", unsafe_allow_html=True)