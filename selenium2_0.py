import streamlit as st
import logging
import os
import json
from datetime import datetime
from agno.agent import Agent
from agno.models.google import Gemini

# Constants
SAVE_FILE = "sessions/scraper_history.json"

# Streamlit Config
st.set_page_config(page_title="🕷️ AI Scraper Builder", page_icon="🕷️", layout="wide")

# Logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# Load API Key
gemini_api_key = st.secrets.get("GEMINI_API_KEY")

# Save and Load Functions
def save_scraper_history(history):
    os.makedirs("sessions", exist_ok=True)
    with open(SAVE_FILE, "w") as f:
        json.dump(history, f, indent=2)

def load_scraper_history():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    return []

if "scraper_history" not in st.session_state:
    st.session_state.scraper_history = load_scraper_history()

# Initialize Scraper Agent
def initialize_scraper_agent(api_key: str) -> Agent:
    try:
        model = Gemini(id="gemini-2.0-flash", api_key=api_key)
        return Agent(
            model=model,
            name="Smart Scraper Agent",
            instructions=[
                "You are an expert web scraper generator using Python + Selenium.",
                "You'll be given HTML (or a webpage dump) and a user-described goal.",
                "Your task is to understand what the user wants, identify correct DOM elements, and write a working scraper.",
                "**Always do the following:**",
                "1. Identify the target elements (e.g., links, prices, titles, etc.) even if not explicitly mentioned.",
                "2. Analyze the HTML and suggest the best tag/class/ID selectors.",
                "3. Generate clean Selenium code. Use BeautifulSoup optionally.",
                "**Output Format:**",
                "### 🧠 Inferred Task\nSummarize the user's goal and target elements.",
                "### 📋 Scraping Plan\nExplain your approach to selecting DOM elements.",
                "### 🔧 Selenium Code\nFull working Python code using Selenium.",
                "### ⚠️ Notes\nMention any JS rendering issues, login needs, or site-specific tricks."
            ],
            markdown=True
        )
    except Exception as e:
        st.error(f"❌ Error initializing agent: {str(e)}")
        return None

# Sidebar Info
st.sidebar.markdown("## 🔧 Built by Ann Naser Nabil")
st.sidebar.image("https://avatars.githubusercontent.com/u/16422192?s=400", width=100)
st.sidebar.markdown("""
**AI Engineer & Web Automator**  
📧 [Email](mailto:ann.n.nabil@gmail.com)  
🐙 [GitHub](https://github.com/AnnNaserNabil)  
🔗 [LinkedIn](https://linkedin.com/in/ann-naser-nabil)  
""", unsafe_allow_html=True)

# Main UI
st.title("🕷️ AI-Powered Selenium Scraper Builder")
st.markdown("Upload an `.html` or `.txt` file, or paste the page source. Then describe what you want to scrape. The AI will build the code for you!")

uploaded_file = st.file_uploader("📄 Upload Website Source Code (.html or .txt)", type=["txt", "html"])

source_html = ""
if uploaded_file:
    try:
        source_html = uploaded_file.read().decode("utf-8", errors="ignore")
        st.success(f"✅ File '{uploaded_file.name}' uploaded successfully.")
    except Exception as e:
        st.error(f"❌ Error reading file: {str(e)}")

# Manual input fallback
if not source_html:
    source_html = st.text_area("🌐 Or Paste Website Source Code", height=200, placeholder="Paste raw HTML or DOM content here...")

# User input: Goal
scrape_goal = st.text_area("🎯 What do you want to scrape?", height=150, placeholder="e.g., Product names and prices from the product listing.")

# Optional URL
url_sample = st.text_input("🔗 Sample URL (optional)", placeholder="https://example.com/products")

# Build button
if st.button("🛠️ Build Smart Scraper", type="primary"):
    if not gemini_api_key:
        st.error("❌ Gemini API Key not found.")
    elif not source_html or not scrape_goal:
        st.warning("⚠️ Please provide both HTML source and scraping goal.")
    else:
        agent = initialize_scraper_agent(gemini_api_key)
        if agent:
            # Escape triple backticks using tags to avoid SyntaxError
            html_display = f"[START HTML]\n{source_html[:4000]}\n[END HTML]"
            prompt = f"""You are a Selenium scraper builder.

Below is a section of the HTML source code of the page:
{html_display}

User's scraping goal:
"{scrape_goal}"

Sample URL (if provided): {url_sample if url_sample else "N/A"}

Please infer what to scrape, explain your logic, and return a working Selenium scraper.
"""
            with st.spinner("🤖 Generating scraping logic..."):
                result = agent.run(message=prompt).content
                st.subheader("📦 Generated Scraper")
                st.markdown(result)

                session_data = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "source": source_html[:1000],
                    "goal": scrape_goal,
                    "url": url_sample,
                    "result": result
                }
                st.session_state.scraper_history.append(session_data)
                save_scraper_history(st.session_state.scraper_history)
        else:
            st.error("⚠️ Could not initialize the agent.")

# Load past sessions
if st.button("📂 Load Saved Sessions"):
    st.session_state.scraper_history = load_scraper_history()
    st.success("✅ Loaded previous sessions.")

# Display history
if st.session_state.scraper_history:
    st.markdown("## 🕰️ Previous Scraper Sessions")
    for session in reversed(st.session_state.scraper_history):
        with st.expander(f"📁 {session['timestamp']} — Goal: {session['goal'][:40]}..."):
            st.markdown(f"### 🔗 URL:\n{session['url']}")
            st.markdown(f"### 🌐 Source Snippet\n```html\n{session['source']}\n```")
            st.markdown(f"### 📋 Generated Code\n{session['result']}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray'>
    <p>Built with 🧠 by <b>Ann Naser Nabil</b></p>
</div>
""", unsafe_allow_html=True)
