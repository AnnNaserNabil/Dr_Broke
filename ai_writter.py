import streamlit as st

# ✅ MUST BE FIRST Streamlit command
st.set_page_config(page_title="💔 ভিঞ্চ ঘগ", page_icon="💔", layout="wide")

from agno.agent import Agent
from agno.models.google import Gemini
from typing import Tuple
import logging

from agno.agent import Agent
from agno.models.google import Gemini
import streamlit as st
from typing import Tuple
import logging

# Logging setup
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# Get API key
api_key = st.secrets.get("GEMINI_API_KEY")

# Agent initializer
def initialize_agents(api_key: str) -> Tuple[Agent, Agent, Agent]:
    try:
        model = Gemini(id="gemini-2.0-flash-exp", api_key=api_key)

        idea_agent = Agent(
            model=model,
            name="Idea Agent",
            instructions=[
                "Generate a goof story, Sci-fi innovation, psychic-quantum themes.",
                "Craft stories for teenage readers who love fantasy, action, sci-fi.",
                "গল্পটা অবশ্যই বাংলায় লিখবে।"
            ],
            markdown=True
        )

        writer_agent = Agent(
            model=model,
            name="Writer Agent",
            instructions=[
                "Write emotionally powerful, plot-driven stories with a real-world hook.",
                "গল্পটা অবশ্যই বাংলায় লিখবে।"
            ],
            markdown=True
        )

        poet_agent = Agent(
            model=model,
            name="Poet Agent",
            instructions=[
                "Write imaginative, relatable poetry with surreal themes.",
                "গল্পটা অবশ্যই বাংলায় লিখবে।"
            ],
            markdown=True
        )

        return idea_agent, writer_agent, poet_agent
    except Exception as e:
        st.error(f"Error initializing agents: {str(e)}")
        return None, None, None

# 🎨 Custom CSS
st.markdown("""
<style>
    body {
        background-color: #F8F8FF;
    }
    .title-style {
        font-size: 50px;
        color: #3F51B5;
        text-align: center;
        font-weight: bold;
        padding: 10px 0;
    }
    .section-header {
        font-size: 24px;
        color: #444;
        margin-top: 30px;
        border-left: 5px solid #FF6F61;
        padding-left: 10px;
    }
    .story-box {
        background-color: #F0F4FF;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .footer {
        text-align: center;
        font-size: 14px;
        color: #888;
        margin-top: 40px;
    }
    .stButton>button {
        background-color: #FF6F61;
        color: white;
        border-radius: 8px;
        height: 3em;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Page config
st.set_page_config(page_title="💔 ভিঞ্চ ঘগ", page_icon="💔", layout="wide")

# 🎬 Title and Header
st.markdown("<div class='title-style'>💔 ভিঞ্চ ঘগ</div>", unsafe_allow_html=True)
st.markdown("### কোন সময়ে হারালে মনে হয় উড়ছি আকাশে")

# 📝 Input Section
st.markdown("<div class='section-header'>🧠 সময় কিংবা স্থানের বাইরে চলে যেতে থাকি নিরন্তর</div>", unsafe_allow_html=True)
user_input = st.text_area("কেমন গল্প পড়তে চাচ্ছেন আজ?", height=150, placeholder="যে গল্পের শেষ নেই...")

# 👉 Button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    clicked = st.button("ঘুরে আসি 💝", type="primary")

# 💡 Process if clicked
if clicked:
    if not api_key:
        st.error("❌ API Key missing! Please add it to `.streamlit/secrets.toml` as GEMINI_API_KEY.")
    else:
        agents = initialize_agents(api_key)
        if all(agents):
            idea_agent, writer_agent, poet_agent = agents
            if user_input:
                try:
                    with st.spinner("🤗 প্রথম গল্প..."):
                        idea_prompt = f"User's message: {user_input}\nProvide a story."
                        idea = idea_agent.run(message=idea_prompt)
                        st.markdown("<div class='section-header'>🤗 শুরু করা যাক তাহলে</div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='story-box'>{idea.content}</div>", unsafe_allow_html=True)

                    with st.spinner("✍️ দাঁড়াও দাঁড়াও দাঁড়াও..."):
                        writer_prompt = f"User's feelings: {user_input}\n Write a noir style story."
                        written = writer_agent.run(message=writer_prompt)
                        st.markdown("<div class='section-header'>✍️ এমন হলে কেমন হয়</div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='story-box'>{written.content}</div>", unsafe_allow_html=True)

                    with st.spinner("📅 সাথে একটা ঝিলিমিলি কবিতা..."):
                        poet_prompt = f"Based on: {user_input}\nWrite a surreal poem."
                        poem = poet_agent.run(message=poet_prompt)
                        st.markdown("<div class='section-header'>📅 কবিতার গান</div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='story-box'>{poem.content}</div>", unsafe_allow_html=True)

                except Exception as e:
                    logger.error(f"Error: {str(e)}")
                    st.error("⚠️ বিশ্লেষণের সময় ত্রুটি ঘটেছে।")
            else:
                st.warning("অনুগ্রহ করে আপনার অনুভূতি লিখুন।")
        else:
            st.error("⚠️ Agent গুলো ঠিকমতো চালু হয়নি। API key চেক করুন।")

# 🎉 Footer
st.markdown("<div class='footer'>Made with ❤️ by Ann Naser Nabil | 🎨 Be Creative With Prompt</div>", unsafe_allow_html=True)
