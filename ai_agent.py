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

        therapist_agent = Agent(
            model=model,
            name="Therapist Agent",
            instructions=[
                "তুমি একজন সহানুভূতিশীল থেরাপিস্ট। তোমার কাজ হলো:",
                "১। মনোযোগ দিয়ে শুনে অনুভূতিগুলোর প্রতি সহানুভূতি প্রকাশ করা",
                "২। হালকা ও মজার রসিকতার মাধ্যমে মানসিক চাপ কমানো",
                "৩। নিজের সম্পর্কের অভিজ্ঞতা থেকে relatable গল্প শেয়ার করা",
                "৪। সান্ত্বনা ও সাহস জোগানোর মতো কথা বলা",
                "৫। ব্যবহারকারীর লেখা এবং ছবির আবেগ বিশ্লেষণ করা",
                "উত্তর শুধুমাত্র বাংলা ভাষায় দাও। সহানুভূতির সাথে কথা বলো।"
            ],
            markdown=True
        )

        closure_agent = Agent(
            model=model,
            name="Closure Agent",
            instructions=[
                "তুমি একজন আবেগিক ক্লোজার বিশেষজ্ঞ। তোমার কাজ হলো:",
                "১। অপাঠানো আবেগময় বার্তা লেখায় সাহায্য করা",
                "২। কাঁচা এবং সততার সাথে আবেগ প্রকাশের সুযোগ তৈরি করা",
                "৩। বার্তাগুলো সুন্দরভাবে হেডিং সহ সাজিয়ে উপস্থাপন করা",
                "৪। মন থেকে বিদায় জানানোর প্রক্রিয়া ও সহায়ক অভ্যাসের পরামর্শ দেওয়া",
                "উত্তর অবশ্যই বাংলা ভাষায় দেবে। হৃদয়ের গভীরতা ও আন্তরিকতা বজায় রেখো।"
            ],
            markdown=True
        )

        routine_planner_agent = Agent(
            model=model,
            name="Routine Planner Agent",
            instructions=[
                "তুমি একজন রিকভারি রুটিন পরিকল্পক। তোমার দায়িত্ব হলো:",
                "১। ৭ দিনের রিকভারি চ্যালেঞ্জ তৈরি করা",
                "২। প্রতিদিনের মজার ও যত্নমূলক কাজের তালিকা দেওয়া",
                "৩। সোশ্যাল মিডিয়া ডিটক্সের কার্যকরী উপায় দেওয়া",
                "৪। মন ভালো করার মতো প্লেলিস্ট সাজানো",
                "উত্তর সবসময় বাংলায় দাও। বাস্তবসম্মত ও অনুপ্রেরণামূলক পরিকল্পনা তৈরি করো।"
            ],
            markdown=True
        )

        brutal_honesty_agent = Agent(
            model=model,
            name="Brutal Honesty Agent",
            tools=[DuckDuckGoTools()],
            instructions=[
                "তুমি একজন নির্মমভাবে সত্যান্বেষী বিশ্লেষক। তোমার কাজ:",
                "১। সম্পর্ক ভেঙে যাওয়ার খোলামেলা ও অকপট বিশ্লেষণ দেওয়া",
                "২। কেন সম্পর্কটা কাজ করেনি, সেটা বাস্তবভাবে বোঝানো",
                "৩। চিন্তাভাবনা উদ্দীপক এবং কঠোর কিন্তু গঠনমূলক ভাষায় কথা বলা",
                "৪। সামনে এগিয়ে যাওয়ার জন্য কার্যকরী পরামর্শ দেওয়া",
                "উত্তর সবসময় বাংলা ভাষায় হওয়া উচিত। কোনো ধরনের সাজসজ্জা বা চিনি মেশানো কথা নয়।"
            ],
            markdown=True
        )

        return therapist_agent, closure_agent, routine_planner_agent, brutal_honesty_agent
    except Exception as e:
        st.error(f"Error initializing agents: {str(e)}")
        return None, None, None, None

# Streamlit UI
st.set_page_config(page_title="💔 Breakup Recovery Squad", page_icon="💔", layout="wide")

# Header
st.title("💔 ড. ব্রোক")
st.markdown("### মন খারাপ? নিজের কথা বলো শুনি\nমন খারাপের কথা গুলো লিখে জানালে আমি হয়ত একটা মনের কথা শুনতে পারব")

# Input fields
col1, col2 = st.columns(2)

with col1:
    st.subheader("মনের কথা লিখুন")
    user_input = st.text_area("কেমন আছো? কি হয়েছে আজ?", height=150, placeholder="আমাকে জানাতে পারো...")

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
if st.button("নিজের কাছে ফিরে আসো 💝", type="primary"):
    if not api_key:
        st.error("❌ API Key missing in secrets! Please add it to `.streamlit/secrets.toml` as GEMINI_API_KEY.")
    else:
        agents = initialize_agents(api_key)
        if all(agents):
            therapist_agent, closure_agent, routine_planner_agent, brutal_honesty_agent = agents
            if user_input or uploaded_files:
                try:
                    all_images = process_images(uploaded_files) if uploaded_files else []

                    with st.spinner("🤗 তোমাকে নিয়ে ভাবছি..."):
                        therapist_prompt = f"""User's message: {user_input}\nProvide a compassionate response."""
                        response = therapist_agent.run(message=therapist_prompt, images=all_images)
                        st.subheader("🤗 তোমার কথা শুনে যা বুঝলাম")
                        st.markdown(response.content)

                    with st.spinner("✍️ তোমাকে নিয়ে ভেবে যা পেলাম..."):
                        closure_prompt = f"""User's feelings: {user_input}\nHelp write unsent messages and provide closure tips."""
                        response = closure_agent.run(message=closure_prompt, images=all_images)
                        st.subheader("✍️ আসলে এই সময়ে যা করতে পারো")
                        st.markdown(response.content)

                    with st.spinner("📅 এই সময়ে যা যা করতে পারো তাই নিয়ে ভাবলাম..."):
                        routine_prompt = f"""Based on: {user_input}\nCreate a ৭-day recovery plan."""
                        response = routine_planner_agent.run(message=routine_prompt, images=all_images)
                        st.subheader("📅 যেভাবে ফিরে আসবে")
                        st.markdown(response.content)

                    with st.spinner("💪 একটা বাস্তবসম্মত প্ল্যান দিচ্ছি..."):
                        honesty_prompt = f"""Situation: {user_input}\nGive brutally honest but constructive advice."""
                        response = brutal_honesty_agent.run(message=honesty_prompt, images=all_images)
                        st.subheader("💪 মন খারাপ না করে হাসো ")
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
        <p>Made with ❤️ by আন্‌ নাসের নাবিল</p>
        <p>ইউ শ্যল ওভারকাম</p>
    </div>
""", unsafe_allow_html=True)
