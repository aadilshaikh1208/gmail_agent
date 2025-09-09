# 📧 Gmail Agent — Modern UI with Streamlit + LangChain

An **AI-powered Gmail Assistant** built with **Streamlit, LangChain, and Google Gmail API**.  
This app lets you **interact with your Gmail inbox**, compose and send emails, and automate email workflows with a modern, interactive UI.  

---

## ✨ Features
- 🔐 **Secure Gmail API integration** with OAuth2 (`credentials.json` + `token.json`)  
- 🤖 **LangChain-powered agent** using Google Gemini (`google_genai:gemini-2.0-flash`)  
- 📬 Fetch, read, and manage your Gmail inbox  
- 📝 Draft and send emails with natural language commands  
- 🖥️ **Streamlit modern UI** with responsive design, animations, and interactive output sections  
- 🧠 **Persistent conversation memory** using LangGraph MemorySaver — remembers past queries in the same session
- 📡 Real-time streaming of agent responses, tool calls, and event logs  
- 🎨 Custom CSS with **dashboard-like design** for professional feel  

---

## 🛠️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/aadilshaikh1208/gmail_agent.git
cd email-agent
```

### 2. Create and activate a virtual environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## 🔑 Setup Gmail API Credentials

### Step 1: Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **Gmail API** for your project

### Step 2: Create OAuth 2.0 Credentials
1. Go to **Credentials** in the Google Cloud Console
2. Click **+ CREATE CREDENTIALS** → **OAuth client ID**
3. Choose **Desktop application** as the application type
4. Download the `credentials.json` file
5. Place the `credentials.json` file in your project root directory

### Step 3: First-time Authentication
- On first run, you'll be redirected to authenticate with Google
- This generates a `token.json` file automatically for future use
- Grant the necessary Gmail permissions

---

## ⚙️ Environment Setup

### Required API Keys
Create a `.env` file in your project root:
```env
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

Get your Google Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey).

---

## ▶️ Running the App

### Start the Streamlit application:
```bash
streamlit run app.py
```

Then open your browser and navigate to: `http://localhost:8501`

---

## 🧑‍💻 Usage Examples

Type natural language queries like:

### 📬 **Reading Emails**
- `"Show me my last 5 emails"`
- `"Find emails from john@example.com"`
- `"Search emails with subject 'Invoice'"`
- `"Show unread messages"`

### 📝 **Composing Emails**
- `"Draft an email to sarah@company.com about tomorrow's meeting"`
- `"Send a thank you email to the team"`
- `"Compose a follow-up email for the client"`

### 🔍 **Email Management**
- `"Mark all emails from newsletter@company.com as read"`
- `"Find emails received last week"`
- `"Show emails with attachments"`

### 📊 **Interactive Output Sections**
Watch real-time responses in three sections:
1. 🤖 **Agent Response** - AI assistant's natural language response
2. 🛠️ **Tool Calls & Messages** - Technical execution details
3. 📡 **Live Stream Logs** - Real-time streaming of processing steps

---

## 📂 Project Structure

```
📦 email-agent/
 ┣ 📜 app.py               # Main Streamlit application
 ┣ 📜 requirements.txt     # Python dependencies
 ┣ 📜 credentials.json     # Gmail API credentials (from Google Cloud)
 ┣ 📜 token.json           # Auto-generated after first auth
 ┣ 📜 .env                 # Environment variables (API keys)
 ┣ 📜 README.md            # This documentation
 ┗ 📜 .gitignore           # Git ignore file
```


---

## ⚡ Tech Stack

| Component | Technology |
|-----------|------------|
| **Frontend** | Streamlit |
| **LLM Framework** | LangChain |
| **AI Model** | Google Gemini 2.0 Flash |
| **Email API** | Gmail API |
| **Authentication** | OAuth 2.0 |
| **Styling** | Custom CSS |


---

## 🔒 Security & Privacy

- **OAuth 2.0**: Secure authentication with Google
- **Local Storage**: Credentials stored locally (`token.json`)
- **API Scopes**: Limited to necessary Gmail permissions only
- **No Data Storage**: Email content is not permanently stored


---

## 🚀 Advanced Features

### Custom CSS Styling
The app includes modern dashboard-like styling with:
- Responsive design
- Dark/light mode support
- Smooth animations
- Professional color scheme

### Real-time Streaming
- Live tool execution logs
- Streaming agent responses
- Interactive progress indicators


## 🐛 Troubleshooting

### Common Issues:

**1. "credentials.json not found"**
```bash
# Make sure you downloaded credentials.json from Google Cloud Console
# Place it in the project root directory
```

**2. "Authentication failed"**
```bash
# Delete token.json and re-authenticate
rm token.json
streamlit run app.py
```

**3. "API quota exceeded"**
```bash
# Check your Google Cloud Console quotas
# Gmail API has daily limits
```

**4. "Module not found"**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

