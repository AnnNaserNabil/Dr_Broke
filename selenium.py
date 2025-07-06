import streamlit as st
import logging
import os
import json
from datetime import datetime
from agno.agent import Agent
from agno.models.google import Gemini

# Constants
SAVE_FILE = "sessions/scraper_history.json"

# Streamlit Page Config
st.set_page_config(page_title="🕷️ Selenium Scraper Builder", page_icon="🕷️", layout="wide")

# Logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# Get API key
gemini_api_key = st.secrets.get("GEMINI_API_KEY")

# Load/Save Session Functions
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

# Initialize Agent
def initialize_scraper_agent(api_key: str) -> Agent:
    try:
        model = Gemini(id="gemini-2.0-pro", api_key=api_key)
        agent = Agent(
            model=model,
            name="Scraper Agent",
            instructions=[
                "You are an expert web scraper builder using Python and Selenium.",
                "The user will give you the HTML source or partial code of a webpage, and a goal (like 'scrape all titles and links').",
                "You must return:",
                "### 📋 Scraping Plan\nExplain what parts of the DOM you will target.",
                "### 🔧 Selenium Code\nGive working Python code using Selenium and optionally BeautifulSoup.",
                "### ⚠️ Notes\nAdd any issues (e.g., dynamic content, login required)."
            ],
            markdown=True
        )
        return agent
    except Exception as e:
        st.error(f"❌ Error initializing agent: {str(e)}")
        return None

# Sidebar
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
st.markdown("### Paste the webpage source and describe your scraping goal.")

source_html = st.text_area("🌐 Website Source Code", height=200, placeholder="Paste HTML source or visible DOM content here.")
scrape_goal = st.text_area("🎯 What do you want to scrape?", height=150, placeholder="e.g., Extract all product names and prices.")

url_sample = st.text_input("🔗 Sample URL (optional)", placeholder="https://example.com/products")

if st.button("🛠️ Build Scraper", type="primary"):
    if not gemini_api_key:
        st.error("❌ Gemini API Key not found in secrets.")
    elif not source_html or not scrape_goal:
        st.warning("Please provide both source code and scraping instructions.")
    else:
        scraper_agent = initialize_scraper_agent(gemini_api_key)

        if scraper_agent:
            full_prompt = f"""You're building a Selenium scraper.
URL (optional): {url_sample if url_sample else 'N/A'}

🧩 HTML Source:
{source_html}

🎯 Goal:
{scrape_goal}
"""
            with st.spinner("🤖 Thinking and building scraper..."):
                result = scraper_agent.run(message=full_prompt).content
                st.subheader("📦 Generated Scraper")
                st.markdown(result)
                
                session_data = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "source": source_html,
                    "goal": scrape_goal,
                    "url": url_sample,
                    "result": result
                }
                st.session_state.scraper_history.append(session_data)
                save_scraper_history(st.session_state.scraper_history)
        else:
            st.error("⚠️ Agent initialization failed.")

# View Past Sessions
if st.button("📂 Load Saved Sessions"):
    st.session_state.scraper_history = load_scraper_history()
    st.success("Loaded saved scraper sessions.")

if st.session_state.scraper_history:
    st.markdown("## 🕰️ Previous Scraper Sessions")
    for session in reversed(st.session_state.scraper_history):
        with st.expander(f"📁 {session['timestamp']} — Goal: {session['goal'][:40]}..."):
            st.markdown(f"### 🔗 URL (if provided):\n{session['url']}")
            st.markdown(f"### 🌐 Source Snippet\n```html\n{session['source'][:500]}...\n```")
            st.markdown(f"### 📋 Generated Code\n{session['result']}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray'>
    <p>Built with 🧠 for fast automation by <b>Ann Naser Nabil</b></p>
</div>
""", unsafe_allow_html=True)