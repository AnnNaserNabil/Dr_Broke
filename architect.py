import streamlit as st

# ✅ MUST be the first Streamlit command
st.set_page_config(
    page_title="🚀 Senior Dev AI Assistant", 
    page_icon="🚀", 
    layout="wide",
    initial_sidebar_state="expanded"
)

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

# Agent initializer with expertly crafted prompts
def initialize_agents(api_key: str) -> tuple:
    try:
        model = Gemini(id="gemini-2.0-flash-exp", api_key=api_key)

        senior_developer = Agent(
            model=model,
            name="Senior Software Developer",
            instructions=[
                "You are a seasoned Senior Software Developer with 10+ years of experience across multiple technologies and domains.",
                "Your expertise includes:",
                "1. **Code Architecture & Design**: Design scalable, maintainable, and robust software solutions",
                "2. **Best Practices**: Apply SOLID principles, design patterns, clean code practices",
                "3. **Technology Stack**: Deep knowledge of modern frameworks, databases, cloud services",
                "4. **Code Review**: Identify potential issues, security vulnerabilities, performance bottlenecks",
                "5. **Technical Leadership**: Guide junior developers, make architectural decisions",
                "",
                "When answering:",
                "- Provide production-ready code examples with comprehensive error handling",
                "- Explain the reasoning behind architectural choices",
                "- Consider scalability, maintainability, and performance implications",
                "- Suggest testing strategies and deployment considerations",
                "- Include security best practices and potential pitfalls",
                "- Reference industry standards and proven patterns",
                "",
                "Always structure responses with: Problem Analysis → Solution Design → Implementation → Best Practices → Next Steps"
            ],
            markdown=True
        )

        ai_agent_architect = Agent(
            model=model,
            name="AI Agent Architect",
            instructions=[
                "You are an expert AI Agent Architect specializing in designing intelligent agent systems and multi-agent architectures.",
                "Your core competencies:",
                "1. **Agent Design Patterns**: Single agents, multi-agent systems, hierarchical architectures",
                "2. **LLM Integration**: Prompt engineering, model selection, context management, token optimization",
                "3. **Agent Orchestration**: Workflow design, agent communication, task delegation, state management",
                "4. **AI Frameworks**: LangChain, AutoGen, CrewAI, Semantic Kernel, custom agent frameworks",
                "5. **Production Deployment**: Scalable agent systems, monitoring, error handling, fallback strategies",
                "",
                "Approach each problem by:",
                "- Analyzing the use case and identifying agent requirements",
                "- Designing appropriate agent roles and responsibilities",
                "- Creating detailed prompt templates and persona definitions",
                "- Planning inter-agent communication and data flow",
                "- Recommending suitable frameworks and implementation patterns",
                "- Addressing scalability, reliability, and cost optimization",
                "",
                "Structure responses as: Use Case Analysis → Agent Architecture → Implementation Strategy → Framework Recommendations → Deployment Considerations"
            ],
            markdown=True
        )

        system_designer = Agent(
            model=model,
            name="System Design Expert",
            instructions=[
                "You are a Principal System Design Engineer with expertise in building large-scale distributed systems.",
                "Your specializations include:",
                "1. **Scalability Design**: Horizontal/vertical scaling, load balancing, caching strategies",
                "2. **Distributed Systems**: Microservices, service mesh, event-driven architecture, message queues",
                "3. **Database Design**: SQL/NoSQL selection, sharding, replication, consistency models",
                "4. **Cloud Architecture**: AWS/GCP/Azure services, serverless, containerization, orchestration",
                "5. **Performance & Reliability**: Monitoring, observability, fault tolerance, disaster recovery",
                "",
                "For each system design question:",
                "- Start with requirements gathering and constraint analysis",
                "- Break down the system into core components and services",
                "- Design data models and storage solutions",
                "- Plan API design and communication patterns",
                "- Address scalability bottlenecks and failure scenarios",
                "- Estimate capacity, costs, and performance metrics",
                "- Create detailed architectural diagrams and documentation",
                "",
                "Response format: Requirements Analysis → High-Level Design → Detailed Components → Data Flow → Scalability & Reliability → Implementation Roadmap"
            ],
            markdown=True
        )

        opensource_contributor = Agent(
            model=model,
            name="Open Source AI Contributor",
            instructions=[
                "You are an experienced Open Source AI Contributor and maintainer with deep knowledge of the AI/ML ecosystem.",
                "Your expertise covers:",
                "1. **Project Contribution**: Finding suitable projects, understanding codebases, making meaningful contributions",
                "2. **AI/ML Libraries**: TensorFlow, PyTorch, Hugging Face, scikit-learn, OpenAI APIs, LangChain",
                "3. **Community Engagement**: Writing documentation, creating tutorials, mentoring newcomers",
                "4. **Project Maintenance**: Code review, issue triage, release management, community building",
                "5. **AI Ethics & Best Practices**: Responsible AI development, bias detection, model evaluation",
                "",
                "When providing guidance:",
                "- Recommend specific projects aligned with user's interests and skill level",
                "- Explain contribution workflows and community etiquette",
                "- Suggest ways to add value through code, documentation, or community support",
                "- Share insights on building reputation and network in the AI community",
                "- Provide practical steps for getting started with contributions",
                "- Discuss trends and opportunities in the AI open source ecosystem",
                "",
                "Structure advice as: Goal Assessment → Project Recommendations → Contribution Strategy → Skill Development → Community Engagement → Long-term Growth"
            ],
            markdown=True
        )

        return senior_developer, ai_agent_architect, system_designer, opensource_contributor
    except Exception as e:
        st.error(f"Error initializing agents: {str(e)}")
        return None, None, None, None

# Main UI
st.markdown("# 🚀 Senior Software Developer AI Assistant")
st.markdown("### Your AI-Powered Technical Mentor & Architect")
st.markdown("Get expert guidance on software development, AI agent architecture, system design, and open-source contributions.")
st.markdown("---")

# Sidebar: Developer Info
st.sidebar.markdown("## 🧑‍💻 Enhanced By")
st.sidebar.image("https://avatars.githubusercontent.com/u/16422192?s=400&u=64cc1f0c21d7b8fcb54ca59ef9fe50dcca771209&v=4", width=100)

st.sidebar.markdown("""
**Ann Naser Nabil**  
_AI Researcher & Creative Technologist_

📧 [Email](mailto:ann.n.nabil@gmail.com)  
🐙 [GitHub](https://github.com/AnnNaserNabil)  
🔗 [LinkedIn](https://linkedin.com/in/ann-naser-nabil)  

---

**💫 Vision**  
_"Empowering developers with intelligent AI agents for advanced problem solving."_
""", unsafe_allow_html=True)

# Sidebar: How to Use
st.sidebar.markdown("---")
st.sidebar.markdown("""
## 🎯 How to Use This System

### 1. **Choose Your Expert**
Select the appropriate AI agent based on your question type

### 2. **Describe Your Challenge**
Provide detailed context about your software development question

### 3. **Get Expert Analysis**
Receive comprehensive guidance from specialized AI agents

### 4. **Apply the Insights**
Implement the recommendations in your projects

## 🔧 What Each Agent Provides

**🏗️ Senior Developer**
- Code architecture & design
- Best practices & patterns
- Technology recommendations
- Code review insights

**🤖 AI Agent Architect**  
- Multi-agent system design
- LLM integration strategies
- Agent orchestration patterns
- Production deployment

**🏢 System Designer**
- Distributed system architecture
- Scalability solutions
- Database design
- Cloud infrastructure

**🌟 Open Source Contributor**
- Project recommendations
- Contribution strategies
- Community engagement
- Skill development paths
""")

# Question Type Selection
st.subheader("🎯 Select Your Question Type")
question_type = st.selectbox(
    "Choose the type of guidance you need:",
    [
        "Software Development & Architecture",
        "AI Agent System Design",
        "System Design & Scalability",
        "Open Source AI Contribution",
        "Comprehensive Analysis (All Experts)"
    ]
)

# Input field
st.subheader("📝 Describe Your Challenge")
user_input = st.text_area(
    "Provide detailed information about your software development question:", 
    height=200, 
    placeholder="""Examples:

🏗️ Software Development:
"I need to design a microservices architecture for an e-commerce platform that handles 1M+ users. What are the key components and how should they communicate?"

🤖 AI Agent Architecture:
"I want to build a multi-agent system for automated customer support. How should I design the agent roles and orchestrate their interactions?"

🏢 System Design:
"Design a real-time chat application that can scale to support millions of concurrent users. What database, caching, and messaging solutions would you recommend?"

🌟 Open Source:
"I'm a machine learning engineer looking to contribute to AI open source projects. Which projects should I focus on and how can I make meaningful contributions?"
"""
)

# Additional context options
col1, col2, col3 = st.columns(3)
with col1:
    tech_stack = st.multiselect(
        "Technology Stack:", 
        ["Python", "JavaScript/Node.js", "Java", "Go", "Rust", "C++", "React", "Angular", "Vue.js", "Django", "FastAPI", "Spring Boot", "Docker", "Kubernetes", "AWS", "GCP", "Azure"]
    )
with col2:
    complexity_level = st.selectbox("Complexity Level:", ["Beginner", "Intermediate", "Advanced", "Expert"])
with col3:
    project_scale = st.selectbox("Project Scale:", ["Personal/Small", "Startup/Medium", "Enterprise/Large", "Global Scale"])

# Process button
if st.button("🚀 Get Expert Analysis", type="primary"):
    if not api_key:
        st.error("❌ API Key missing! Add it to `.streamlit/secrets.toml` as GEMINI_API_KEY.")
    elif not user_input.strip():
        st.warning("Please provide a detailed description of your challenge.")
    else:
        senior_developer, ai_agent_architect, system_designer, opensource_contributor = initialize_agents(api_key)
        if all([senior_developer, ai_agent_architect, system_designer, opensource_contributor]):
            try:
                # Prepare context
                context = f"""
                Question: {user_input}
                Question Type: {question_type}
                Tech Stack: {', '.join(tech_stack) if tech_stack else 'Not specified'}
                Complexity Level: {complexity_level}
                Project Scale: {project_scale}
                """

                # Route to appropriate agent(s)
                if question_type == "Software Development & Architecture":
                    with st.spinner("🏗️ Senior Developer analyzing your challenge..."):
                        response = senior_developer.run(message=context)
                        st.subheader("🏗️ Senior Software Developer Analysis")
                        st.markdown(response.content)

                elif question_type == "AI Agent System Design":
                    with st.spinner("🤖 AI Agent Architect designing your system..."):
                        response = ai_agent_architect.run(message=context)
                        st.subheader("🤖 AI Agent Architecture Recommendations")
                        st.markdown(response.content)

                elif question_type == "System Design & Scalability":
                    with st.spinner("🏢 System Designer creating architecture..."):
                        response = system_designer.run(message=context)
                        st.subheader("🏢 System Design & Architecture")
                        st.markdown(response.content)

                elif question_type == "Open Source AI Contribution":
                    with st.spinner("🌟 Open Source Expert providing guidance..."):
                        response = opensource_contributor.run(message=context)
                        st.subheader("🌟 Open Source Contribution Strategy")
                        st.markdown(response.content)

                else:  # Comprehensive Analysis
                    # Senior Developer Analysis
                    with st.spinner("🏗️ Senior Developer analyzing..."):
                        response = senior_developer.run(message=context)
                        st.subheader("🏗️ Senior Developer Perspective")
                        st.markdown(response.content)
                        st.markdown("---")

                    # AI Agent Architect Analysis
                    with st.spinner("🤖 AI Agent Architect designing..."):
                        response = ai_agent_architect.run(message=context)
                        st.subheader("🤖 AI Agent Architecture Insights")
                        st.markdown(response.content)
                        st.markdown("---")

                    # System Designer Analysis
                    with st.spinner("🏢 System Designer architecting..."):
                        response = system_designer.run(message=context)
                        st.subheader("🏢 System Design Recommendations")
                        st.markdown(response.content)
                        st.markdown("---")

                    # Open Source Contributor Guidance
                    with st.spinner("🌟 Open Source Expert advising..."):
                        response = opensource_contributor.run(message=context)
                        st.subheader("🌟 Open Source Strategy")
                        st.markdown(response.content)

            except Exception as e:
                logger.error(f"Processing error: {str(e)}")
                st.error("⚠️ An error occurred during analysis. Please try again.")
        else:
            st.error("⚠️ Agents failed to initialize. Please check your API key.")

# Expert Tips Section
st.markdown("---")
st.markdown("## 🎓 Expert Development Tips")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    **🏗️ Software Architecture**
    - Start with requirements analysis
    - Apply SOLID principles
    - Design for testability
    - Consider future scalability
    - Document architectural decisions
    """)

with col2:
    st.markdown("""
    **🤖 AI Agent Systems**
    - Define clear agent roles
    - Design robust communication
    - Implement error handling
    - Plan for context management
    - Monitor agent performance
    """)

with col3:
    st.markdown("""
    **🏢 System Design**
    - Understand trade-offs
    - Plan for failure scenarios
    - Design for observability
    - Consider data consistency
    - Estimate capacity needs
    """)

with col4:
    st.markdown("""
    **🌟 Open Source**
    - Start with documentation
    - Follow project guidelines
    - Engage with community
    - Build relationships
    - Share knowledge actively
    """)

# Resources Section
st.markdown("---")
st.markdown("## 📚 Recommended Resources")

tab1, tab2, tab3, tab4 = st.tabs(["📖 Books", "🌐 Websites", "🎥 Courses", "🛠️ Tools"])

with tab1:
    st.markdown("""
    ### Essential Reading
    - **Clean Code** by Robert Martin
    - **System Design Interview** by Alex Xu
    - **Designing Data-Intensive Applications** by Martin Kleppmann
    - **The Pragmatic Programmer** by Hunt & Thomas
    - **Building Microservices** by Sam Newman
    """)

with tab2:
    st.markdown("""
    ### Key Websites
    - **High Scalability** - System design case studies
    - **AWS Architecture Center** - Cloud design patterns
    - **Google Cloud Architecture** - Scalable solutions
    - **GitHub Explore** - Trending open source projects
    - **Papers We Love** - Academic research papers
    """)

with tab3:
    st.markdown("""
    ### Learning Platforms
    - **Coursera** - Software Engineering courses
    - **Udemy** - System design interviews
    - **Pluralsight** - Advanced development topics
    - **edX** - Computer science fundamentals
    - **YouTube** - Tech talks and tutorials
    """)

with tab4:
    st.markdown("""
    ### Development Tools
    - **Draw.io** - System architecture diagrams
    - **Postman** - API testing and documentation
    - **Docker** - Containerization platform
    - **Kubernetes** - Container orchestration
    - **Terraform** - Infrastructure as code
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray'>
    <p>🚀 <b>Senior Software Developer AI Assistant</b></p>
    <p>Enhanced by <b>Ann Naser Nabil</b> | Powered by Advanced AI Agents</p>
    <p>💡 <i>Elevating software development through intelligent collaboration</i></p>
</div>
""", unsafe_allow_html=True)
