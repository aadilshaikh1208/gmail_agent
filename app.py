import streamlit as st
from dotenv import load_dotenv
from langchain import hub
from langgraph.prebuilt import create_react_agent
from langchain_google_community.gmail.utils import (
    build_resource_service,
    get_gmail_credentials,
)
from langchain_google_community import GmailToolkit
from langchain.chat_models import init_chat_model

load_dotenv()

st.set_page_config(page_title="Gmail Agent", layout="wide")

# --- Enhanced Custom CSS for modern styling (fixed version) ---
CUSTOM_CSS = """
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

:root{
  --bg: #0f1724;
  --card: #111827;
  --card-hover: #1f2937;
  --muted: #94a3b8;
  --accent: #7c3aed;
  --accent-light: #8b5cf6;
  --success: #10b981;
  --warning: #f59e0b;
  --text-primary: #e6eef8;
  --text-secondary: #cbd5e1;
  --border: rgba(255,255,255,0.06);
  --glass-bg: rgba(255,255,255,0.05);
  --glass-border: rgba(255,255,255,0.1);
  --shadow-soft: 0 4px 24px rgba(0,0,0,0.15);
  --shadow-medium: 0 8px 32px rgba(0,0,0,0.2);
  --shadow-hard: 0 12px 48px rgba(0,0,0,0.3);
}

/* Global App Background + Typography */
html, body, .stApp {
  background: linear-gradient(180deg, #071028 0%, #0f1724 100%) !important;
  font-family: 'Inter', sans-serif !important; 
  color: var(--text-primary) !important;
}

.stApp > .main .block-container {
  padding-top: 1rem !important;
  max-width: 95% !important;
}

h1, h2, h3, .big-title { 
  color: var(--text-primary);
  font-weight: 700;
  letter-spacing: -0.02em;
}

/* Modern Compact Header Styling */
.main-header {
  background: linear-gradient(135deg, var(--accent) 0%, #4f46e5 100%);
  padding: 1rem 2rem;
  border-radius: 12px;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: var(--shadow-medium);
  border: 1px solid var(--glass-border);
  backdrop-filter: blur(20px);
  position: relative;
  overflow: hidden;
}

.main-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 50%);
  pointer-events: none;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
  z-index: 1;
}

.header-logo {
  width: 40px;
  height: 40px;
  background: rgba(255,255,255,0.2);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  backdrop-filter: blur(10px);
}

.header-title {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
  background: linear-gradient(45deg, #ffffff, #e2e8f0);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.header-subtitle {
  font-size: 0.85rem;
  opacity: 0.8;
  margin: 0;
  font-weight: 400;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 1rem;
  z-index: 1;
}

.header-badge {
  background: rgba(16, 185, 129, 0.2);
  color: var(--success);
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  border: 1px solid rgba(16, 185, 129, 0.3);
  backdrop-filter: blur(10px);
}

/* Enhanced Buttons with Modern Design */
.stButton button, button[kind="primary"] {
  background: linear-gradient(135deg, var(--accent) 0%, var(--accent-light) 100%) !important;
  border: none !important;
  color: white !important;
  padding: 14px 28px !important;
  border-radius: 14px !important;
  font-weight: 600 !important;
  font-size: 16px !important;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
  box-shadow: var(--shadow-soft) !important;
  width: 100% !important;
  position: relative !important;
  overflow: hidden !important;
  backdrop-filter: blur(10px) !important;
}

.stButton button::before {
  content: '' !important;
  position: absolute !important;
  top: 0 !important;
  left: -100% !important;
  width: 100% !important;
  height: 100% !important;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent) !important;
  transition: left 0.6s !important;
}

.stButton button:hover::before {
  left: 100% !important;
}

.stButton button:hover {
  transform: translateY(-3px) !important;
  box-shadow: var(--shadow-medium) !important;
  background: linear-gradient(135deg, var(--accent-light) 0%, var(--accent) 100%) !important;
}

.stButton button:active {
  transform: translateY(-1px) !important;
}

/* Enhanced Input & Textarea with Focus States */
input[type="text"], textarea {
  background: var(--glass-bg) !important;
  color: var(--text-primary) !important;
  border: 2px solid var(--border) !important;
  padding: 16px 20px !important;
  border-radius: 14px !important;
  font-size: 16px !important;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
  font-family: 'Inter', sans-serif !important;
  backdrop-filter: blur(10px) !important;
  box-shadow: inset 0 2px 4px rgba(0,0,0,0.1) !important;
}

input[type="text"]:focus, textarea:focus {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 4px rgba(124, 58, 237, 0.15), inset 0 2px 4px rgba(0,0,0,0.1) !important;
  background: rgba(255,255,255,0.08) !important;
  transform: translateY(-1px) !important;
}

input[type="text"]::placeholder, textarea::placeholder {
  color: var(--muted) !important;
  opacity: 0.7 !important;
}

/* Advanced Section Card with Glassmorphism */
.section-card {
  background: linear-gradient(145deg, var(--glass-bg), rgba(255,255,255,0.02));
  padding: 28px;
  border-radius: 20px;
  box-shadow: var(--shadow-soft);
  border: 1px solid var(--glass-border);
  backdrop-filter: blur(20px);
  margin-bottom: 1.5rem;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.section-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--accent), transparent);
  opacity: 0.5;
}

.section-card:hover {
  background: linear-gradient(145deg, rgba(255,255,255,0.08), rgba(255,255,255,0.04));
  border-color: var(--glass-border);
  transform: translateY(-2px);
  box-shadow: var(--shadow-medium);
}

/* Modern Output Section Design */
.output-section {
  background: linear-gradient(145deg, rgba(0,0,0,0.5), rgba(0,0,0,0.3));
  padding: 24px;
  border-radius: 16px;
  border: 1px solid rgba(255,255,255,0.08);
  margin-bottom: 1.2rem;
  backdrop-filter: blur(12px);
  position: relative;
  transition: all 0.3s ease;
}

.output-section:hover {
  border-color: rgba(255,255,255,0.12);
  background: linear-gradient(145deg, rgba(0,0,0,0.6), rgba(0,0,0,0.4));
}

.output-section h4 {
  margin: 0 0 16px 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: 10px;
  padding-bottom: 8px;
  border-bottom: 1px solid rgba(255,255,255,0.05);
}

/* Enhanced Output Box with Better Typography */
.output-box {
  background: linear-gradient(145deg, rgba(0,0,0,0.7), rgba(0,0,0,0.5));
  padding: 20px;
  border-radius: 12px;
  color: var(--text-primary);
  font-family: 'SF Mono', 'Monaco', 'Cascadia Code', 'Roboto Mono', monospace;
  font-size: 14px;
  line-height: 1.6;
  max-height: 380px;
  overflow-y: auto;
  border: 1px solid rgba(255,255,255,0.08);
  white-space: pre-wrap;
  word-wrap: break-word;
  scrollbar-width: thin;
  scrollbar-color: var(--accent) rgba(255,255,255,0.05);
  box-shadow: inset 0 2px 8px rgba(0,0,0,0.3);
  transition: all 0.3s ease;
}

.output-box:hover {
  border-color: rgba(255,255,255,0.12);
}

/* Interactive Highlighted Outputs */
.tool-output {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(16, 185, 129, 0.08));
  border-left: 4px solid var(--success);
  padding: 16px;
  margin: 12px 0;
  border-radius: 8px;
  font-size: 13px;
  transition: all 0.3s ease;
  border: 1px solid rgba(16, 185, 129, 0.2);
}

.tool-output:hover {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(16, 185, 129, 0.1));
  transform: translateX(4px);
}

.agent-output {
  background: linear-gradient(135deg, rgba(124, 58, 237, 0.15), rgba(124, 58, 237, 0.08));
  border-left: 4px solid var(--accent);
  padding: 16px;
  margin: 12px 0;
  border-radius: 8px;
  font-size: 13px;
  transition: all 0.3s ease;
  border: 1px solid rgba(124, 58, 237, 0.2);
}

.agent-output:hover {
  background: linear-gradient(135deg, rgba(124, 58, 237, 0.2), rgba(124, 58, 237, 0.1));
  transform: translateX(4px);
}

.stream-output {
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.15), rgba(245, 158, 11, 0.08));
  border-left: 4px solid var(--warning);
  padding: 16px;
  margin: 12px 0;
  border-radius: 8px;
  font-size: 13px;
  transition: all 0.3s ease;
  border: 1px solid rgba(245, 158, 11, 0.2);
}

.stream-output:hover {
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.2), rgba(245, 158, 11, 0.1));
  transform: translateX(4px);
}

/* Footer with Better Styling */
.small-muted { 
  color: var(--muted); 
  font-size: 13px;
  text-align: center;
  margin-top: 3rem;
  opacity: 0.7;
  padding: 1rem;
  border-top: 1px solid rgba(255,255,255,0.05);
  font-weight: 400;
}

/* Enhanced Compose Section */
.compose-section {
  background: linear-gradient(135deg, rgba(124, 58, 237, 0.12) 0%, rgba(79, 70, 229, 0.08) 100%);
  border: 1px solid rgba(124, 58, 237, 0.2);
}

.status-indicator {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.3), rgba(16, 185, 129, 0.2));
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  color: var(--success);
  margin-bottom: 1.2rem;
  border: 1px solid rgba(16, 185, 129, 0.3);
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.2);
}

/* Modern Scrollbar Design */
.output-box::-webkit-scrollbar {
  width: 8px;
}

.output-box::-webkit-scrollbar-track {
  background: rgba(255,255,255,0.05);
  border-radius: 10px;
}

.output-box::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, var(--accent), var(--accent-light));
  border-radius: 10px;
  border: 1px solid rgba(255,255,255,0.1);
}

.output-box::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(135deg, var(--accent-light), var(--accent));
}

/* Responsive Design Improvements */
@media (max-width: 768px) {
  .main-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .header-right {
    justify-content: center;
  }
  
  .section-card {
    padding: 20px;
    margin-bottom: 1rem;
  }
  
  .output-section {
    padding: 16px;
  }
  
  .output-box {
    max-height: 250px;
    padding: 16px;
  }
}

/* Loading Animation */
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.processing {
  animation: pulse 2s infinite;
}

/* Subtle Animations for Better UX */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.section-card, .output-section {
  animation: fadeIn 0.6s ease-out;
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# --- Modern Compact Header ---
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
        <div class="header-badge">🟢 Ready</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Initialize Gmail agent automatically ---
scopes = ["https://mail.google.com/"]
credentials = get_gmail_credentials(
    token_file="token.json",
    scopes=scopes,
    client_secrets_file="credentials.json",
)
api_resource = build_resource_service(credentials=credentials)
toolkit = GmailToolkit(api_resource=api_resource)
tools = toolkit.get_tools()

llm = init_chat_model("google_genai:gemini-2.0-flash")
instructions = """You are an intelligent Gmail Assistant and personal email manager with the highest standards of accuracy and reliability.

## 🎯 CORE MISSION
Your primary responsibility is to help users manage their Gmail efficiently while maintaining absolute precision in every action, especially when handling sensitive operations like sending emails.

## 🔒 CRITICAL SAFETY PROTOCOLS

### Email Sending - MANDATORY VERIFICATION STEPS:
1. **ALWAYS** confirm recipient email addresses before sending
2. **VERIFY** the intended recipient matches the user's request exactly

## 🚀 CAPABILITIES & RESPONSIBILITIES

### Email Management:
- **READ & ANALYZE**: Fetch, parse, and summarize emails with context
- **SEARCH & FILTER**: Find emails by sender, subject, date, keywords, or labels
- **ORGANIZE**: Help categorize, label, and manage email organization
- **PRIORITIZE**: Identify urgent/important emails and suggest actions

### Email Composition:
- **DRAFT**: Create professional, contextually appropriate email content
- **PERSONALIZE**: Adapt tone and style based on recipient relationship
- **OPTIMIZE**: Suggest subject lines and improve email effectiveness
- **TEMPLATE**: Create reusable email templates for common scenarios

### Workflow Automation:
- **BATCH OPERATIONS**: Handle multiple emails efficiently
- **FOLLOW-UPS**: Track and remind about pending email responses
- **SCHEDULING**: Help plan email sending at optimal times
- **INTEGRATION**: Connect email actions with calendar and task management

## 🎨 COMMUNICATION STYLE

### Professional & Friendly:
- Be conversational yet professional in all interactions
- Provide clear, actionable responses with specific steps
- Use appropriate technical terminology while remaining accessible
- Show enthusiasm for helping while maintaining reliability


## 📋 RESPONSE STRUCTURE

### For Complex Tasks:
1. **ACKNOWLEDGE** the request clearly
2. **OUTLINE** the steps you'll take
3. **EXECUTE** with real-time updates

### For Email Actions:
1. **PREPARE** the email content/action
2. **PRESENT** for user review
3. **EXECUTE** only after approval
4. **CONFIRM** successful completion

## 🎯 SUCCESS METRICS
- **ZERO** emails sent to wrong recipients
- **100%** accuracy in following user instructions
- **PROACTIVE** error prevention and suggestion of improvements
- **EFFICIENT** task completion with minimal back-and-forth

"""

agent_executor = create_react_agent(llm, tools, prompt=instructions)

# --- Main layout ---
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("<div class='section-card compose-section'>",
                unsafe_allow_html=True)
    st.markdown("<div class='status-indicator'>🟢 Agent Ready</div>",
                unsafe_allow_html=True)
    st.subheader("✉️ Compose / Ask")

    instruction_text = st.text_area(
        "System Instructions (optional)",
        value=instructions,
        height=120,
        help="Customize the agent's behavior and instructions"
    )

    example_query = st.text_area(
        "Type your query here",
        height=160,
        placeholder="e.g., 'Show me my latest 5 emails' or 'Draft an email to john@example.com about the meeting'"
    )

    run_button = st.button("🚀 Send Query")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)

    # Agent Response Section
    st.markdown("""
    <div class="output-section">
        <h4>🤖 Agent Response</h4>
    """, unsafe_allow_html=True)
    agent_output_box = st.empty()
    agent_output_box.markdown(
        "<div class='output-box'>Ready to process your query...</div>",
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # Tool Calls Section
    st.markdown("""
    <div class="output-section">
        <h4>🛠️ Tool Calls & Messages</h4>
    """, unsafe_allow_html=True)
    tools_output_box = st.empty()
    tools_output_box.markdown(
        "<div class='output-box'>Tool interactions will appear here...</div>",
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# --- Run agent and stream responses ---
if run_button:
    base_prompt = hub.pull("langchain-ai/openai-functions-template")
    prompt = base_prompt.partial(instructions=instruction_text)

    # Initialize output containers
    tools_text = ""
    final_response = ""

    # Update initial states
    agent_output_box.markdown(
        "<div class='output-box processing'>🔄 Processing your request...</div>",
        unsafe_allow_html=True
    )
    tools_output_box.markdown(
        "<div class='output-box processing'>🔄 Waiting for tool calls...</div>",
        unsafe_allow_html=True
    )

    # Stream events
    events = agent_executor.stream(
        {"messages": [("user", example_query)]},
        stream_mode="values",
    )

    for event in events:
        # Extract messages
        messages = event.get("messages", [])
        if messages:
            last_message = messages[-1]
            message_content = getattr(
                last_message, "content", str(last_message))
            message_type = getattr(
                last_message, "__class__", type(last_message)).__name__

            import html
            # Categorize messages
            if "Tool" in message_type:
                safe_content = html.escape(str(message_content))
                tools_text += f"🔧 [{message_type}]\n{safe_content}\n\n"
                tools_output_box.markdown(
                    f"<div class='output-box'>{tools_text}</div>",
                    unsafe_allow_html=True
                )

            # When rendering AI responses
            elif "AI" in message_type:
                safe_content = html.escape(str(message_content))
                final_response = safe_content
                agent_output_box.markdown(
                    f"<div class='output-box'>{final_response}</div>",
                    unsafe_allow_html=True
                )

    # Ensure final response is displayed
    if final_response:
        agent_output_box.markdown(
            f"<div class='output-box'>{final_response}</div>",
            unsafe_allow_html=True
        )
    else:
        agent_output_box.markdown(
            "<div class='output-box'>✅ Task completed. Check tool calls for details.</div>",
            unsafe_allow_html=True
        )

# --- Footer ---
st.markdown("---")
st.markdown(
    "<div class='small-muted'>Built with Streamlit · Uses credentials.json & token.json from working directory</div>",
    unsafe_allow_html=True,
)
