from agno.agent import Agent
from agno.models.google import Gemini
from agno.media import Image as AgnoImage
from agno.tools.duckduckgo import DuckDuckGoTools
import streamlit as st
from typing import List, Optional
import logging
from pathlib import Path
import tempfile
import os
হচ্ছে
# Configure logging for errors only
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

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


# Set page config and UI elements
st.set_page_config(
    page_title="💔 Breakup Recovery Squad",
    page_icon="💔",
    layout="wide"
)



# Sidebar for API key input
with st.sidebar:
    st.header("🔑 API Configuration")

    if "api_key_input" not in st.session_state:
        st.session_state.api_key_input = ""
        
    api_key = st.text_input(
        "Enter your Gemini API Key",
        value=st.session_state.api_key_input,
        type="password",
        help="Get your API key from Google AI Studio",
        key="api_key_widget"  
    )

    if api_key != st.session_state.api_key_input:
        st.session_state.api_key_input = api_key
    
    if api_key:
        st.success("API Key provided! ✅")
    else:
        st.warning("Please enter your API key to proceed")
        st.markdown("""
        To get your API key:
        1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
        2. Enable the Generative Language API in your [Google Cloud Console](https://console.developers.google.com/apis/api/generativelanguage.googleapis.com)
        """)

# Main content
st.title("💔 ড. ব্রোক")
st.markdown("""
    ### মন খারাপ? নিজের কথা বলো শুনি
    মন খারাপের কথা গুলো লিখে জানালে আমি হয়ত একটা মনের কথা শুনতে পারব
""")

# Input section
col1, col2 = st.columns(2)

with col1:
    st.subheader("মনের কথা লিখুন")
    user_input = st.text_area(
                    "কেমন আছেন? কি হয়েছে আজ?",
        height=150,
        placeholder=" আমাকে জানাতে পারেন কিন্তু..."
    )
    
with col2:
    st.subheader(" স্ক্রিনশট পড়ে কথা গুলো বুঝুন")
    uploaded_files = st.file_uploader(
                    " চাইলে স্ক্রিনশট এখানে দিতে পারেন",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
        key="screenshots"
    )
    
    if uploaded_files:
        for file in uploaded_files:
            st.image(file, caption=file.name, use_container_width=True)

# Process button and API key check
if st.button("নিজের কাছে ফিরে আসুন 💝", type="primary"):
    if not st.session_state.api_key_input:
        st.warning("Please enter your API key in the sidebar first!")
    else:
        therapist_agent, closure_agent, routine_planner_agent, brutal_honesty_agent = initialize_agents(st.session_state.api_key_input)
        
        if all([therapist_agent, closure_agent, routine_planner_agent, brutal_honesty_agent]):
            if user_input or uploaded_files:
                try:
                    st.header("যা করতে পারেন এই সময়ে")
                    
                    def process_images(files):
                        processed_images = []
                        for file in files:
                            try:
                                temp_dir = tempfile.gettempdir()
                                temp_path = os.path.join(temp_dir, f"temp_{file.name}")
                                
                                with open(temp_path, "wb") as f:
                                    f.write(file.getvalue())
                                
                                agno_image = AgnoImage(filepath=Path(temp_path))
                                processed_images.append(agno_image)
                                
                            except Exception as e:
                                logger.error(f"Error processing image {file.name}: {str(e)}")
                                continue
                        return processed_images
                    
                    all_images = process_images(uploaded_files) if uploaded_files else []
                    
                    # Therapist Analysis
                    with st.spinner("🤗 Getting empathetic support..."):
                        therapist_prompt = f"""
                        Analyze the emotional state and provide empathetic support based on:
                        User's message: {user_input}
                        
                        Please provide a compassionate response with:
                        1. Validation of feelings
                        2. Gentle words of comfort
                        3. Relatable experiences
                        4. Words of encouragement
                        """
                        
                        response = therapist_agent.run(
                            message=therapist_prompt,
                            images=all_images
                        )
                        
                        st.subheader("🤗 Emotional Support")
                        st.markdown(response.content)
                    
                    # Closure Messages
                    with st.spinner("✍️ Crafting closure messages..."):
                        closure_prompt = f"""
                        Help create emotional closure based on:
                        User's feelings: {user_input}
                        
                        Please provide:
                        1. Template for unsent messages
                        2. Emotional release exercises
                        3. Closure rituals
                        4. Moving forward strategies
                        """
                        
                        response = closure_agent.run(
                            message=closure_prompt,
                            images=all_images
                        )
                        
                        st.subheader("✍️ Finding Closure")
                        st.markdown(response.content)
                    
                    # Recovery Plan
                    with st.spinner("📅 Creating your recovery plan..."):
                        routine_prompt = f"""
                        Design a 7-day recovery plan based on:
                        Current state: {user_input}
                        
                        Include:
                        1. Daily activities and challenges
                        2. Self-care routines
                        3. Social media guidelines
                        4. Mood-lifting music suggestions
                        """
                        
                        response = routine_planner_agent.run(
                            message=routine_prompt,
                            images=all_images
                        )
                        
                        st.subheader("📅 যেভাবে ফিরে আসবেন ")
                        st.markdown(response.content)
                    
                    # Honest Feedback
                    with st.spinner("💪 একটা বাস্তবসম্মত প্ল্যান দিচ্ছি..."):
                        honesty_prompt = f"""
                        Provide honest, constructive feedback about:
                        Situation: {user_input}
                        
                        Include:
                        1. Objective analysis
                        2. Growth opportunities
                        3. Future outlook
                        4. Actionable steps
                        """
                        
                        response = brutal_honesty_agent.run(
                            message=honesty_prompt,
                            images=all_images
                        )
                        
                        st.subheader("💪 বাস্তবে যা ")
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
        <p>Made with ❤️ by the Breakup Recovery Squad</p>
        <p>Share your recovery journey with #BreakupRecoverySquad</p>
    </div>
""", unsafe_allow_html=True)
