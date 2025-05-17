from agno.agent import Agent
from agno.models.google import Gemini
import streamlit as st
from typing import Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# Get API key from Streamlit secrets
api_key = st.secrets.get("GEMINI_API_KEY")

# Agent initializer
def initialize_agents(api_key: str) -> Tuple[Agent, Agent, Agent]:
    try:
        model = Gemini(id="gemini-2.0-flash-exp", api_key=api_key)

        idea_agent = Agent(
            model=model,
            name="Idea Agent",
            instructions=[
                "You are a story crafter that:",
                "1. Generate a goof story",
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

# Streamlit UI setup
st.set_page_config(page_title="💔 ভিঞ্চ ঘগ", page_icon="💔", layout="wide")

st.title("💔 ভিঞ্চ ঘগ")
st.markdown("### কোন সময়ে হারালে মনে হয় উড়ছি আকাশে")

# Input fields
st.subheader("সময় কিংবা স্থানের বাইরে চলে যেতে থাকি নিরন্তর")
user_input = st.text_area("কেমন গল্প পড়তে চাচ্ছেন আজ?", height=150, placeholder="যে গল্পের শেষ নেই...")

# Submit button
if st.button("ঘুরে আসি 💝", type="primary"):
    if not api_key:
        st.error("❌ API Key missing in secrets! Please add it to `.streamlit/secrets.toml` as GEMINI_API_KEY.")
    else:
        agents = initialize_agents(api_key)
        if all(agents):
            idea_agent, writer_agent, poet_agent = agents
            if user_input:
                try:
                    with st.spinner("🤗 প্রথম গল্প..."):
                        idea_prompt = f"""User's message: {user_input}\nProvide a story based on the response."""
                        response = idea_agent.run(message=idea_prompt)
                        st.subheader("🤗 শুরু করা যাক তাহলে")
                        st.markdown(response.content)

                    with st.spinner("✍️ দাঁড়াও দাঁড়াও দাঁড়াও..."):
                        writer_prompt = f"""User's feelings: {user_input}\n Write a noir style story."""
                        response = writer_agent.run(message=writer_prompt)
                        st.subheader("✍️ এমন হলে কেমন হয়")
                        st.markdown(response.content)

                    with st.spinner("📅 সাথে একটা  কবিতা..."):
                        poet_prompt = f"""Based on: {user_input}\nWrite some poetry that are surreal."""
                        response = poet_agent.run(message=poet_prompt)
                        st.subheader("📅 কবিতার গান")
                        st.markdown(response.content)

                except Exception as e:
                    logger.error(f"Error during analysis: {str(e)}")
                    st.error("⚠️ বিশ্লেষণের সময় ত্রুটি ঘটেছে। অনুগ্রহ করে লগ চেক করুন।")
            else:
                st.warning("অনুগ্রহ করে আপনার অনুভূতি লিখুন।")
        else:
            st.error("⚠️ Agent গুলো ঠিকমতো চালু হয়নি। API key চেক করুন।")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>Made with ❤️ by Ann Naser Nabil</p>
        <p>🎨 Be Creative With Prompt </p>
    </div>
""", unsafe_allow_html=True)
