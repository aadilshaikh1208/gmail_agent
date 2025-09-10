import uuid
import html
import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_google_community import GmailToolkit
from langchain_google_community.gmail.utils import (
    build_resource_service,
    get_gmail_credentials,
)
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

# =========================================================
# ✅ Environment
# =========================================================
load_dotenv()


# =========================================================
# 🏷️ Loading Css file
# =========================================================


def load_css(file_name: str):
    """Load a CSS file and inject into Streamlit"""
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css("style.css")

# =========================================================
# 🏷️ Header Section
# =========================================================

st.set_page_config(page_title="Gmail Agent", layout="wide")
st.markdown("""
<div class="main-header">
    <div class="header-left">
        <div class="header-logo">📧</div>
        <div>
            <h1 class="header-title">Gmail Agent</h1>
            <p class="header-subtitle">AI-Powered Email Assistant</p>
        </div>
    </div>
    <div class="header-right">
        <div class="header-badge">🟢 Agent Ready</div>
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# 📧 Gmail API Setup
# =========================================================


@st.cache_resource
def init_gmail_tools_cached():
    return init_gmail_tools()


@st.cache_resource
def init_agent_cached(_tools):
    llm = init_chat_model("google_genai:gemini-2.0-flash")
    return create_react_agent(
        llm,
        _tools,
        prompt=instructions,
        checkpointer=st.session_state.checkpointer,
    )


def init_gmail_tools():
    """Initialize Gmail API service and return toolkit tools."""
    scopes = ["https://mail.google.com/"]
    credentials = get_gmail_credentials(
        token_file="token.json",
        scopes=scopes,
        client_secrets_file="credentials.json",
    )
    api_resource = build_resource_service(credentials=credentials)
    return GmailToolkit(api_resource=api_resource).get_tools()


# =========================================================
# 🧠 Memory & Agent Setup
# =========================================================

def init_agent():
    """Create or retrieve the Gmail agent with memory persistence."""
    if "checkpointer" not in st.session_state:
        st.session_state.checkpointer = MemorySaver()

    if "thread_id" not in st.session_state:
        st.session_state.thread_id = f"gmail_agent_session_{uuid.uuid4()}"

    if "agent_executor" not in st.session_state:
        tools = init_gmail_tools_cached()
        st.session_state.agent_executor = init_agent_cached(tools)

    return st.session_state.agent_executor


# =========================================================
# 📋 Loading Agent Instructions
# =========================================================
def load_instructions(file_name: str) -> str:
    """Load assistant instructions from file"""
    with open(file_name, "r") as f:
        return f.read()


# Load instructions once
instructions = load_instructions("instructions.txt")

# =========================================================
# 🖼️ UI Layout
# =========================================================
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("✉️ Compose / Ask")

    if "example_query" not in st.session_state:
        st.session_state.example_query = ""

    # Store latest query safely
    if "last_query" not in st.session_state:
        st.session_state.last_query = ""

    def handle_send():
        st.session_state.last_query = st.session_state.example_query.strip()
        st.session_state.example_query = ""  

    example_query = st.text_area(
        "Type your query here",
        key='example_query',
        height=160,
        placeholder="e.g., 'Show me my latest 5 emails' or 'Draft an email to john@example.com about the meeting'",
    )

    run_button = st.button("🚀 Send Query", on_click=handle_send)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    # Agent Response Section
    st.markdown("""
    <div class="output-section"><h4>🤖 Agent Response</h4>
    """, unsafe_allow_html=True)
    agent_output_box = st.empty()
    agent_output_box.markdown(
        "<div class='output-box'>Ready to process your query...</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# 🚀 Query Execution
# =========================================================
if run_button:
    try:
        query = st.session_state.last_query

        if not query:
            st.warning("⚠️ Please enter a query before sending.")

        else:
            agent_executor = init_agent()

            # Initialize output containers
            final_response = None

            agent_output_box.markdown(
                "<div class='output-box processing'>🔄 Processing your request...</div>",
                unsafe_allow_html=True,
            )

            # Stream events
            events = agent_executor.stream(
                {"messages": [("user", query)]},
                config={"configurable": {
                    "thread_id": st.session_state.thread_id}},
                stream_mode="values",
            )
            for event in events:
                messages = event.get("messages", [])
                if not messages:
                    continue

                last_message = messages[-1]
                message_content = getattr(
                    last_message, "content", str(last_message))
                message_type = getattr(
                    last_message, "__class__", type(last_message)).__name__

                if "Tool" in message_type:
                    continue

                elif "AI" in message_type:
                    if message_content and message_content.strip():   # ✅ only if not empty
                        safe_content = html.escape(str(message_content))
                        final_response = safe_content
                        agent_output_box.markdown(
                            f"<div class='output-box'>{final_response}</div>",
                            unsafe_allow_html=True,
                        )

            # Ensure final response is displayed
            if not final_response:
                agent_output_box.markdown(
                    "<div class='output-box'>✅ Task completed. Check tool calls for details.</div>",
                    unsafe_allow_html=True,
                )

    except Exception as e:
        agent_output_box.markdown(
            f"<div class='output-box'>❌ Error: {str(e)}</div>",
            unsafe_allow_html=True,
        )

# =========================================================
# 📌 Footer
# =========================================================
st.markdown("---")
st.markdown(
    "<div class='small-muted'>Built By Aadil Shaikh </div>",
    unsafe_allow_html=True,
)
