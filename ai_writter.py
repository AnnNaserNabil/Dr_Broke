import streamlit as st

# ✅ MUST be the first Streamlit command
st.set_page_config(page_title="💔 ভিঞ্চ গখ", page_icon="💔", layout="wide")

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

# Dummy image processor
def process_images(files) -> List[AgnoImage]:
    images = []
    for file in files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
            tmp_file.write(file.read())
            images.append(AgnoImage(path=tmp_file.name))
    return images

# Agent initializer
def initialize_agents(api_key: str) -> tuple:
    try:
        model = Gemini(id="gemini-2.0-flash-exp", api_key=api_key)

        idea_agent = Agent(
            model=model,
            name="Idea Agent",
            instructions=[
                "You are a story crafter that:",
                "1. Generate a good story",
                "2. Make stories of Sci-fi World with new innovation",
                "3. Bind the sci-fi quantum world with the psychic world",
                "4. Generate a random story plot with meaning and deep emotion",
                "5. Story of a superhero born from their own understanding of time and space",
                "Craft stories for teenage readers who love fantasy, action, sci-fi.",
                "গল্পটা অবশ্যই বাংলায় লিখবে।"
            ],
            markdown=True
        )

        writer_agent = Agent(
            model=model,
            name="Writer Agent",
            instructions=[
                "You are a story writer that combines:",
                "1. Original emotions with people",
                "2. Stir the minds of readers with plot twists",
                "3. Write stories with progressive development",
                "4. Connect the real world with the story’s hook",
                "5. Build the story with a successful arc",
                "গল্পটা অবশ্যই বাংলায় লিখবে।"
            ],
            markdown=True
        )

        poet_agent = Agent(
            model=model,
            name="Poet Agent",
            instructions=[
                "You are a poet that:",
                "1. Works with poetic words",
                "2. Writes about casual characters",
                "3. Makes the story relatable",
                "4. Writes with great imagination",
                "5. Makes the reading experience engaging",
                "গল্পটা অবশ্যই বাংলায় লিখবে।"
            ],
            markdown=True
        )

        return idea_agent, writer_agent, poet_agent
    except Exception as e:
        st.error(f"Error initializing agents: {str(e)}")
        return None, None, None

# UI
st.markdown("# 💔 ভিঞ্চ গখ")
st.markdown("###  এজেন্ট ভায়োলেট")
st.markdown("---")

# Sidebar
st.sidebar.title("🎒 আপনার সঙ্গী")
st.sidebar.markdown("আপনি চাইলে একটি ছবি আপলোড করতে পারেন")

uploaded_files = st.sidebar.file_uploader("📷 ছবি দিন (ঐচ্ছিক)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# Input field
st.subheader("সময় কিংবা স্থানের বাইরে চলে যেতে থাকি নিরন্তর")
user_input = st.text_area("কেমন গল্প পড়তে চাচ্ছেন আজ?", height=150, placeholder="যে গল্পের শেষ নেই...")

# Button
if st.button("ঘুরে আসি 💝", type="primary"):
    if not api_key:
        st.error("❌ API Key missing! Add it to `.streamlit/secrets.toml` as GEMINI_API_KEY.")
    else:
        idea_agent, writer_agent, poet_agent = initialize_agents(api_key)
        if all([idea_agent, writer_agent, poet_agent]):
            if user_input or uploaded_files:
                try:
                    images = process_images(uploaded_files) if uploaded_files else []

                    with st.spinner("🤗 প্রথম গল্প তৈরি হচ্ছে..."):
                        response = idea_agent.run(message=f"User's message: {user_input}", images=images)
                        st.subheader("🤗 শুরু করা যাক তাহলে")
                        st.markdown(response.content)

                    with st.spinner("✍️ গল্প এগোচ্ছে..."):
                        response = writer_agent.run(message=f"User's feelings: {user_input}", images=images)
                        st.subheader("✍️ এমন হলে কেমন হয়")
                        st.markdown(response.content)

                    with st.spinner("📅 সাথে একটা কবিতা..."):
                        response = poet_agent.run(message=f"Based on: {user_input}", images=images)
                        st.subheader("📅 কবিতার গান")
                        st.markdown(response.content)

                except Exception as e:
                    logger.error(f"Processing error: {str(e)}")
                    st.error("⚠️ বিশ্লেষণের সময় ত্রুটি ঘটেছে। লগ চেক করুন।")
            else:
                st.warning("অনুগ্রহ করে অনুভূতি লিখুন বা ছবি দিন।")
        else:
            st.error("⚠️ Agent গুলো চালু হয়নি। API key সঠিক কিনা দেখুন।")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray'>
    <p>Made with ❤️ by <b>Ann Naser Nabil</b></p>
    <p>🎨 Creative Prompt Writing Enabled</p>
</div>
""", unsafe_allow_html=True)
