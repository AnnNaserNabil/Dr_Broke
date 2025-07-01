import streamlit as st
import json
from datetime import datetime
from typing import Dict, Any
import requests
import logging

# MUST be the first Streamlit command
st.set_page_config(page_title="🧠 LeetCode Code Reviewer", page_icon="🧠", layout="wide")

from agno.agent import Agent
from agno.models.google import Gemini

# Setup logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# Get API keys securely from Streamlit secrets
gemini_api_key = st.secrets.get("GEMINI_API_KEY")
google_docs_api_key = st.secrets.get("GOOGLE_DOCS_API_KEY")
google_doc_id = st.secrets.get("GOOGLE_DOC_ID")  # The ID of your target Google Doc

class GoogleDocsMCPServer:
    """MCP Server for Google Docs integration"""
    
    def __init__(self, api_key: str, doc_id: str):
        self.api_key = api_key
        self.doc_id = doc_id
        self.base_url = "https://docs.googleapis.com/v1/documents"
        
    def append_to_document(self, content: str) -> bool:
        """Append content to the Google Doc"""
        try:
            # First, get the document to find the end index
            get_url = f"{self.base_url}/{self.doc_id}"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.get(get_url, headers=headers)
            if response.status_code != 200:
                logger.error(f"Failed to get document: {response.text}")
                return False
                
            doc_data = response.json()
            end_index = doc_data['body']['content'][-1]['endIndex'] - 1
            
            # Prepare the batch update request
            update_url = f"{self.base_url}/{self.doc_id}:batchUpdate"
            
            requests_payload = [
                {
                    "insertText": {
                        "location": {"index": end_index},
                        "text": content
                    }
                }
            ]
            
            payload = {"requests": requests_payload}
            
            response = requests.post(update_url, headers=headers, json=payload)
            
            if response.status_code == 200:
                return True
            else:
                logger.error(f"Failed to update document: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error appending to Google Doc: {str(e)}")
            return False
    
    def save_review_session(self, session_data: Dict[str, Any]) -> bool:
        """Save a complete review session to Google Doc"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            content = f"""
{'='*80}
🧠 LEETCODE CODE REVIEW SESSION - {timestamp}
{'='*80}

📋 PROBLEM STATEMENT:
{session_data['problem']}

💻 SUBMITTED CODE ({session_data['language']}):
```{session_data['language'].lower()}
{session_data['code']}
```

🏷️ DIFFICULTY: {session_data['difficulty']}

{'='*50} AI ANALYSIS {'='*50}

🔍 CODE EVALUATION:
{session_data['evaluation']}

⚖️ JUDGEMENT VERDICT:
{session_data['judgement']}

🕵️ CRITIC ANALYSIS:
{session_data['criticism']}

🚀 IMPROVED SOLUTION:
{session_data['improvement']}

📖 CODE EXPLANATION:
{session_data['explanation']}

{'='*80}
END OF SESSION
{'='*80}

"""
            return self.append_to_document(content)
            
        except Exception as e:
            logger.error(f"Error saving review session: {str(e)}")
            return False

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

# Google Docs Integration Section
st.sidebar.markdown("---")
st.sidebar.markdown("## 📄 Google Docs Integration")
save_to_docs = st.sidebar.checkbox("💾 Save to Google Docs", value=True)
if save_to_docs:
    if google_docs_api_key and google_doc_id:
        st.sidebar.success("✅ Google Docs configured")
    else:
        st.sidebar.error("❌ Missing Google Docs configuration")
        st.sidebar.markdown("Add `GOOGLE_DOCS_API_KEY` and `GOOGLE_DOC_ID` to secrets")

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

    if not gemini_api_key:
        st.error("❌ Gemini API Key not found. Please add `GEMINI_API_KEY` to `.streamlit/secrets.toml`.")
    elif not user_problem or not user_code:
        st.warning("Please provide both the problem statement and your code.")
    else:
        code_evaluator, code_judge, code_critic, code_improver, code_explainer = initialize_evaluator_agents(gemini_api_key)

        if all([code_evaluator, code_judge, code_critic, code_improver, code_explainer]):
            full_context = f"Problem:\n{user_problem}\n\nCode:\n```{language}\n{user_code}\n```"
            
            # Initialize session data for Google Docs
            session_data = {
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

            # Save to Google Docs if enabled
            if save_to_docs and google_docs_api_key and google_doc_id:
                with st.spinner("💾 Saving to Google Docs..."):
                    try:
                        mcp_server = GoogleDocsMCPServer(google_docs_api_key, google_doc_id)
                        if mcp_server.save_review_session(session_data):
                            st.success("✅ Successfully saved review session to Google Docs!")
                        else:
                            st.error("❌ Failed to save to Google Docs. Check your configuration.")
                    except Exception as e:
                        st.error(f"❌ Error saving to Google Docs: {str(e)}")

        else:
            st.error("⚠️ Failed to initialize agents. Please check your configuration.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray'>
    <p>Made with ❤️ by <b>Ann Naser Nabil</b></p>
    <p>🧠 Master Problem Solving with AI Agents</p>
    <p>💾 All sessions automatically saved to Google Docs</p>
</div>
""", unsafe_allow_html=True)