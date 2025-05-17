from agno.agent import Agent
from agno.models.google import Gemini
from agno.media import Image as AgnoImage
from agno.tools.duckduckgo import DuckDuckGoTools
import streamlit as st
from typing import List
import logging
from pathlib import Path
import tempfile
import os

# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# Get API key from Streamlit secrets
api_key = st.secrets.get("GEMINI_API_KEY")

# Agent initializer
def initialize_agents(api_key: str) -> tuple[Agent, Agent, Agent, Agent]:
    try:
        model = Gemini(id="gemini-2.0-flash-exp", api_key=api_key)

        idea_agent = Agent(
            model=model,
            name="Idea Agent",
            instructions=[
                 "You are a story crafter that:",
                "1. Generate a random story in mind",
                "2. Makes Stories of Sci fi World with new innovation",
                "3. Binds the sci fi quantum world with psychic world",
                "4. Generate a random Story plot with meanning and deep emotion",
                "5. Story of a super hero born from own device of understanding of the time and space of events",
                "Craft stories for teen aged readers for fantasy, action, sci fi lovers"
                "গল্পটা অবশ্যই বাংলায় লিখবে, হুমায়ুন আহমেদের মত করে।।"
            ],
            markdown=True
        )

        writer_agent = Agent(
            model=model,
            name="Writer Agent",
            instructions=[
                "You are a story writer that comines:",
                "1. Original Emotions with people",
                "2. strirr the mind of the readers with plot twist",
                "3. Writting stories with progressive buildings",
                "4. Making real world be connected with the stories hooking pattern",
                "Building up the story with an succesfull arc"
                "গল্পটা অবশ্যই বাংলায় লিখবে, হুমায়ুন আহমেদের মত করে।"
            ],
            markdown=True
        )

        poet_agent = Agent(
            model=model,
            name="Poet Agent",
            instructions=[
               "You are a poet that:",
                "1. works with poetic words",
                "2. writes the most casual characters story",
                "3. Makes the story relatable",
                "4. WRites with great imagination",
                "Make the reading experience engaging"
                "গল্পটা অবশ্যই বাংলায় লিখবে, হুমায়ুন আহমেদের মত করে।।"
            ],
            markdown=True
        )



        return idea_agent, writer_agent, poet_agent
    except Exception as e:
        st.error(f"Error initializing agents: {str(e)}")
        return None, None, None, None

# Streamlit UI
st.set_page_config(page_title="💔 ভিঞ্চ ঘগ", page_icon="💔", layout="wide")

# Header
st.title("💔 ভিঞ্চ ঘগ")
st.markdown("### কোন সময়ে হারালে মনে হয় উড়ছি আকাশে")

# Input fields
col1, col2 = st.columns(2)

with col1:
    st.subheader("সময় কিংবা স্থানের বাইরে চলে যেতে থাকি নিরন্তর")
    user_input = st.text_area("কেমন গল্প পড়তে চাচ্ছেন আজ?", height=150, placeholder="যে গল্পের শেষ নেই...")

with col2:
    st.subheader("স্ক্রিনশট পড়ে কথা গুলো বুঝতে চাইলে")
    uploaded_files = st.file_uploader(" স্ক্রিনশট এড করো", type=["jpg", "jpeg", "png"], accept_multiple_files=True, key="screenshots")
    if uploaded_files:
        for file in uploaded_files:
            st.image(file, caption=file.name, use_container_width=True)

# Image processing
def process_images(files) -> List[AgnoImage]:
    processed_images = []
    for file in files:
        try:
            temp_path = os.path.join(tempfile.gettempdir(), f"temp_{file.name}")
            with open(temp_path, "wb") as f:
                f.write(file.getvalue())
            agno_image = AgnoImage(filepath=Path(temp_path))
            processed_images.append(agno_image)
        except Exception as e:
            logger.error(f"Error processing image {file.name}: {str(e)}")
    return processed_images

# Submit button
if st.button(" তবে চলুন ঘুরে আসি আজ এই ক্ষণে 💝", type="primary"):
    if not api_key:
        st.error("❌ API Key missing in secrets! Please add it to `.streamlit/secrets.toml` as GEMINI_API_KEY.")
    else:
        agents = initialize_agents(api_key)
        if all(agents):
            idea_agent, writer_agent, poet_agent = agents
            if user_input or uploaded_files:
                try:
                    all_images = process_images(uploaded_files) if uploaded_files else []

                    with st.spinner("🤗 নিয়ে আসছি একটা পুটী গল্প..."):
                        therapist_prompt = f"""User's message: {user_input}\nProvide a story based on the response."""
                        response = idea_agent.run(message=therapist_prompt, images=all_images)
                        st.subheader("🤗 শুরু করা যাক তাহলে ")
                        st.markdown(response.content)

                    with st.spinner("✍️ দাঁড়াও দাঁড়াও দাঁড়াও..."):
                        closure_prompt = f"""User's feelings: {user_input}\n Write another ending of the previous story."""
                        response = writer_agent.run(message=closure_prompt, images=all_images)
                        st.subheader("✍️ এমন হলে কেমন হয় ")
                        st.markdown(response.content)

                    with st.spinner("📅 সাথে একটা ঝিলিমিলি কবিতা..."):
                        routine_prompt = f"""Based on: {user_input}\nCreate a 7-day recovery plan."""
                        response = poet_agent.run(message=routine_prompt, images=all_images)
                        st.subheader("📅 কবিতার গান")
                        st.markdown(response.content)

                 

                except Exception as e:
                    logger.error(f"Error during analysis: {str(e)}")
                    st.error("An error occurred during analysis. Please check the logs for details.")
            else:
                st.warning("Please share your feelings or upload screenshots to get help.")
        else:
            st.error("Failed to initialize agents. Please check your API key.")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>Made with ❤️ by Ann Naser Nabil</p>
        <p>Heal thyself my love</p>
    </div>
""", unsafe_allow_html=True)
