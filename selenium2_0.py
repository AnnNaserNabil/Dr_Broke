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
st.set_page_config(page_title="🕷️ AI Scraper Builder", page_icon="🕷️", layout="wide")

# Logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# API Key
gemini_api_key = st.secrets.get("GEMINI_API_KEY")

# Load/Save Functions
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

# Agent Initialization
def initialize_scraper_agent(api_key: str) -> Agent:
    try:
        model = Gemini(id="gemini-2.0-pro", api_key=api_key)
        return Agent(
            model=model,
            name="Smart Scraper Agent",
            instructions=[
                "You are an expert web scraper generator using Python + Selenium.",
                "You'll be given HTML (or a webpage dump) and a user-described goal.",
                "Your task is to understand what the user wants, identify correct DOM elements, and write a working scraper.",
                "",
                "**Always do the following:**",
                "1. Identify the target elements (e.g., links, prices, titles, etc.) even if not explicitly mentioned.",
                "2. Analyze the HTML and suggest the best tag/class/ID selectors.",
                "3. Generate clean Selenium code. Use BeautifulSoup optionally.",
                "",
                "**Output Format:**",
                "### 🧠 Inferred Task\nSummarize the user's goal and target elements.",
                "### 📋 Scraping Plan\nExplain your approach to selecting DOM elements.",
                "### 🔧 Selenium Code\nFull working Python code using Selenium.",
                "### ⚠️ Notes\nMention any JS rendering issues, login needs, or site-specific tricks."
            ],
            markdown=True
        )
    except Exception as e:
        st.error(f"❌ Agent init failed: {str(e)}")
        return None

# Sidebar
st.sidebar.markdown("## 🧠 Built by Ann Naser Nabil")
st.sidebar.image("https://avatars.githubusercontent.com/u/16422192?s=400", width=100)
st.sidebar.markdown("""
**AI Engineer & Web Automator**  
📧 [Email](mailto:ann.n.nabil@gmail.com)  
🐙 [GitHub](https://github.com/AnnNaserNabil)  
🔗 [LinkedIn](https://linkedin.com/in/ann-naser-nabil)  
""", unsafe_allow_html=True)

# Main Interface
st.title("🕷️ AI-Powered Selenium Scraper Builder")
st.markdown("Upload `.html` or `.txt` source, or paste HTML/DOM — describe your scraping goal and let AI do the rest!")

uploaded_file = st.file_uploader("📄 Upload Website Source Code", type=["html", "txt"])

source_html = ""
if uploaded_file:
    try:
        source_html = uploaded_file.read().decode("utf-8", errors="ignore")
        st.success(f"✅ Loaded: {uploaded_file.name}")
    except Exception as e:
        st.error(f"❌ Could not read file: {e}")

# Manual input fallback
if not source_html:
    source_html = st.text_area("🌐 Or Paste HTML/Visible DOM", height=200, placeholder="Paste raw HTML or page source here...")

# Free-form goal input
scrape_goal = st.text_area("🎯 What do you want to scrape?", height=150, placeholder="e.g., I want product names, prices and ratings from this page.")

# Optional: sample URL
url_sample = st.text_input("🔗 Sample URL (optional)", placeholder="https://example.com/products")

# Build Scraper
if st.button("🛠️ Build Smart Scraper", type="primary"):
    if not gemini_api_key:
        st.error("❌ Gemini API Key is missing.")
    elif not source_html or not scrape_goal:
        st.warning("⚠️ Please provide both HTML content and a scraping goal.")
    else:
        agent = initialize_scraper_agent(gemini_api_key)
        if agent:
            full_prompt = f"""
You are a Selenium scraper builder.

Here is the page's raw HTML or DOM:
