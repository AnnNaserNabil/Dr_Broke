import streamlit as st

# ✅ MUST be the first Streamlit command
st.set_page_config(page_title="👩‍🎨 ভিঞ্চ গখ", page_icon="👩‍🎨", layout="wide")

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

        idea_agent = Agent(
            model=model,
            name="Idea Agent",
            instructions=[
                "You are a story crafter that:",
                "1. Generate a good plot based story without intro",
                "2. Make story of related genre",
                "3. Bind the story with sci-fi world",
                "4. Generate a random story plot with meaning and deep emotion",
                "5. Story of something new",
                "Craft stories for teenage readers who love fantasy, action, sci-fi.",
                "গল্পটা অবশ্যই বাংলায় লিখবে। মডার্ন ন্যারেটিভে, নামের ক্ষেত্রে জনপ্রিয় নাম ব্যাবহার করতে পারো"
            ],
            markdown=True
        )

        writer_agent = Agent(
            model=model,
            name="Writer Agent",
            instructions=[
                "You are a short story writer that combines:",
                "1. Original emotions with people",
                "2. Stir the minds of readers with plot twists",
                "3. Write stories with progressive development",
                "4. Connect the real world with the story’s hook",
                "5. Build the story with a successful arc and ending",
                "গল্পটা অবশ্যই বাংলায় লিখবে কোনো রকম ইন্ট্রো ছাড়া।"
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
st.markdown("# 👩‍🎨 ভিঞ্চ গখ")
st.markdown("### রাইটার এজেন্ট")
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
_"Building intelligent AI agents."_
""", unsafe_allow_html=True)

# Input field
st.subheader("আমি গল্প বলি সময়েরর শেষ দিকের")
user_input = st.text_area("কেমন গল্প পড়তে চান আজ?", height=150, placeholder="যে গল্পের শেষ নেই...")

# Button
if st.button("গল্প শোনাও 💝", type="primary"):
    if not api_key:
        st.error("❌ API Key missing! Add it to `.streamlit/secrets.toml` as GEMINI_API_KEY.")
    elif not user_input.strip():
        st.warning("অনুগ্রহ করে অনুভূতি লিখুন।")
    else:
        idea_agent, writer_agent, poet_agent = initialize_agents(api_key)
        if all([idea_agent, writer_agent, poet_agent]):
            try:
                images = []  # Define empty list for now unless you plan to add image input later

                with st.spinner("🤗 এটা প্রথম গল্প ..."):
                    response = idea_agent.run(message=f"User's message: {user_input}", images=images)
                    st.subheader("🤗 শুরু করা যাক তাহলে")
                    st.markdown(response.content)

                with st.spinner("✍️ গল্প এগোচ্ছে অন্য কোথাও..."):
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
            st.error("⚠️ Agent গুলো চালু হয়নি। API key সঠিক কিনা দেখুন।")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray'>
    <p>Made with ❤️ by <b>Ann Naser Nabil</b></p>
    <p>🎨 Be Creative With Prompt </p>
</div>
""", unsafe_allow_html=True)
