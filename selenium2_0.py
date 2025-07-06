# ... (all previous imports remain the same)
# Constants
SAVE_FILE = "sessions/scraper_history.json"

# Streamlit Page Config
st.set_page_config(page_title="🕷️ Selenium Scraper Builder", page_icon="🕷️", layout="wide")

# Logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# API Key
gemini_api_key = st.secrets.get("GEMINI_API_KEY")

# Load/Save Functions (no change)
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
        agent = Agent(
            model=model,
            name="Scraper Agent",
            instructions=[
                "You are an expert web scraper builder using Python and Selenium.",
                "You will receive a goal and HTML source code (either full or partial).",
                "Follow these steps strictly when replying:",
                "",
                "**1. Analyze Structure**: Read the HTML input and understand the DOM tree structure.",
                "**2. Locate Elements**: Identify which tags or classes/IDs to target to extract user-specified content (like links, product names, etc).",
                "**3. Extract Using Selenium**: Generate robust Python code using Selenium to extract the required elements.",
                "**4. Use Best Practices**: Handle dynamic content, page loads, and edge cases where needed.",
                "",
                "Return your output in this format:",
                "### 📋 Scraping Plan\nExplain DOM targets and logic.",
                "### 🔧 Selenium Code\nFull working script using Selenium (use BeautifulSoup optionally).",
                "### ⚠️ Notes\nMention JS rendering issues, login requirements, or alternatives if any."
            ],
            markdown=True
        )
        return agent
    except Exception as e:
        st.error(f"❌ Error initializing agent: {str(e)}")
        return None

# Sidebar — unchanged
st.sidebar.markdown("## 🔧 Built by Ann Naser Nabil")
st.sidebar.image("https://avatars.githubusercontent.com/u/16422192?s=400", width=100)
st.sidebar.markdown("""
**AI Engineer & Web Automator**  
📧 [Email](mailto:ann.n.nabil@gmail.com)  
🐙 [GitHub](https://github.com/AnnNaserNabil)  
🔗 [LinkedIn](https://linkedin.com/in/ann-naser-nabil)  
""", unsafe_allow_html=True)

# Main Interface
st.title("🕷️ AI-Powered Selenium Scraper Builder")
st.markdown("### Upload a `.html` or `.txt` file, or paste the HTML source, and describe your scraping goal.")

uploaded_file = st.file_uploader("📄 Upload Website Source Code (.html or .txt)", type=["txt", "html"])

source_html = ""
if uploaded_file is not None:
    try:
        file_bytes = uploaded_file.read()
        source_html = file_bytes.decode("utf-8", errors="ignore")
        st.success(f"✅ File '{uploaded_file.name}' uploaded and processed successfully.")
    except Exception as e:
        st.error(f"❌ Error reading file: {str(e)}")

# Fallback to manual input
if not source_html:
    source_html = st.text_area("🌐 Or Paste Website Source Code", height=200, placeholder="Paste HTML source or visible DOM content here.")

# Text input for goal
scrape_goal = st.text_area("🎯 What do you want to scrape?", height=150, placeholder="e.g., Extract all product names and prices.")

# Element selection
element_types = st.multiselect(
    "🔍 What type(s) of elements do you want to scrape?",
    ["Links (anchor tags)", "Text content", "Images", "Buttons", "Tables", "Lists"],
    default=["Links (anchor tags)", "Text content"]
)

url_sample = st.text_input("🔗 Sample URL (optional)", placeholder="https://example.com/products")

if st.button("🛠️ Build Scraper", type="primary"):
    if not gemini_api_key:
        st.error("❌ Gemini API Key not found in secrets.")
    elif not source_html or not scrape_goal:
        st.warning("Please provide both source code and scraping instructions.")
    else:
        scraper_agent = initialize_scraper_agent(gemini_api_key)

        if scraper_agent:
            elements_str = ", ".join(element_types)
            full_prompt = f"""You're building a Selenium scraper.
URL (optional): {url_sample if url_sample else 'N/A'}

🧩 HTML Source:
{source_html}

🎯 Goal:
{scrape_goal}

🔍 Elements to scrape: {elements_str}
"""
            with st.spinner("🤖 Thinking and building scraper..."):
                result = scraper_agent.run(message=full_prompt).content
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
            st.error("⚠️ Agent initialization failed.")

# Past Sessions
if st.button("📂 Load Saved Sessions"):
    st.session_state.scraper_history = load_scraper_history()
    st.success("Loaded saved scraper sessions.")

if st.session_state.scraper_history:
    st.markdown("## 🕰️ Previous Scraper Sessions")
    for session in reversed(st.session_state.scraper_history):
        with st.expander(f"📁 {session['timestamp']} — Goal: {session['goal'][:40]}..."):
            st.markdown(f"### 🔗 URL (if provided):\n{session['url']}")
            st.markdown(f"### 🌐 Source Snippet\n```html\n{session['source']}\n```")
            st.markdown(f"### 📋 Generated Code\n{session['result']}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray'>
    <p>Built with 🧠 for fast automation by <b>Ann Naser Nabil</b></p>
</div>
""", unsafe_allow_html=True)