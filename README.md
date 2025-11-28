# AutoResearcher AI – Autonomous Internet Research Agent

**AI-powered web crawling + LLM summarization + GitHub automation.**

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18.2-61DAFB)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688)](https://fastapi.tiangolo.com/)

---

## 🎯 Problem Statement

People waste **hours** searching, reading, and summarizing information from the internet. Students, researchers, and developers constantly:
- Jump across multiple tabs and websites
- Manually gather sources and copy-paste content
- Clean and structure messy text
- Write summaries from scratch
- Lose track of sources and references

This process is **slow, repetitive, and prone to errors**. Naive LLM queries often hallucinate or miss critical sources, while manual research is exhausting and time-consuming.

## 💡 Solution

**AutoResearcher AI** automates the entire research workflow end-to-end:

✅ **Crawl** any website or topic using Apify's powerful web scraper  
✅ **Clean** and normalize extracted text automatically  
✅ **Summarize** content using multi-provider LLM (Groq/OpenAI/Gemini)  
✅ **Export** results into clean Markdown research reports  
✅ **Commit** reports directly to GitHub repositories (optional)  
✅ **Review** PRs automatically with CodeRabbit integration  

No more manual copy-pasting. No more lost sources. Just instant, comprehensive research reports.

---

## ✨ Key Features

### 🔍 **Universal Query Support**
- Research any **topic** or **URL**
- Automatic detection of input type
- DuckDuckGo search integration for topics

### 🕷️ **Advanced Web Scraping**
- **Hybrid Crawler** - DuckDuckGo Lite for fast, free results
- **Apify Ready** - Architecture designed for Apify Actor integration
- **Smart Extraction** - Removes ads, scripts, and clutter
- **Multi-Source** - Aggregates data from top 5 search results

### 🤖 **Multi-Provider AI**
- **Groq** (Default - Free tier)
- **OpenAI** (GPT-3.5/GPT-4)
- **Google Gemini** (Gemini Pro/Flash)
- Graceful fallbacks if no API keys

### 📊 **Comprehensive Output**
- **AI Summary** - Key insights highlighted
- **Cleaned Text** - Normalized content
- **Raw Data** - Original crawl results
- **Sources** - Clickable reference links
- **Integration Status** - API health info

### 📝 **Markdown Export**
- Structured research reports
- Auto-generated filenames
- Custom path support
- Timestamp metadata

### 🔄 **GitHub Integration**
- Automatic commit to repositories
- Create or update files
- SHA-based versioning
- Non-blocking design (works without tokens)

### 🤝 **CodeRabbit Ready**
- PR review automation
- AI-powered feedback
- Consistency checking
- Future PR integration

### 🎨 **Modern Frontend**
- Clean React dashboard
- Real-time API calls
- Loading states
- Error handling
- Mobile responsive

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Client (React)                          │
│  • Search Input  • Loading Spinner  • Result Display        │
└─────────────────────────┬───────────────────────────────────┘
                          │
                    POST /research
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   FastAPI Backend                           │
│  • CORS  • Logging  • Error Handling  • Pydantic Models     │
└─────────────────────────┬───────────────────────────────────┘
                          │
              ┌───────────┴───────────┐
              ▼                       ▼
    ┌──────────────────┐    ┌──────────────────┐
    │  WebCrawler      │    │  POST            │
    │  (Apify Actor)   │    │  /github/report  │
    └────────┬─────────┘    └────────┬─────────┘
             │                       │
             ▼                       ▼
    ┌──────────────────┐    ┌──────────────────┐
    │  clean_text()    │    │  Markdown        │
    │  (Regex + Norm)  │    │  Generator       │
    └────────┬─────────┘    └────────┬─────────┘
             │                       │
             ▼                       ▼
    ┌──────────────────┐    ┌──────────────────┐
    │  Summarizer      │    │  GitHub API      │
    │  Groq/OpenAI/    │    │  (Create/Update) │
    │  Gemini          │    └────────┬─────────┘
    └────────┬─────────┘             │
             │                       ▼
             ▼              ┌──────────────────┐
    ┌──────────────────┐   │  CodeRabbit      │
    │  Result JSON     │   │  (PR Reviews)    │
    │  {raw, cleaned,  │   └──────────────────┘
    │   summary, srcs} │
    └────────┬─────────┘
             │
             ▼
    ┌──────────────────┐
    │  Frontend Cards  │
# AutoResearcher AI – Autonomous Internet Research Agent

**AI-powered web crawling + LLM summarization + GitHub automation.**

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18.2-61DAFB)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688)](https://fastapi.tiangolo.com/)

---

## 🎯 Problem Statement

People waste **hours** searching, reading, and summarizing information from the internet. Students, researchers, and developers constantly:
- Jump across multiple tabs and websites
- Manually gather sources and copy-paste content
- Clean and structure messy text
- Write summaries from scratch
- Lose track of sources and references

This process is **slow, repetitive, and prone to errors**. Naive LLM queries often hallucinate or miss critical sources, while manual research is exhausting and time-consuming.

## 💡 Solution

**AutoResearcher AI** automates the entire research workflow end-to-end:

✅ **Crawl** any website or topic using Apify's powerful web scraper  
✅ **Clean** and normalize extracted text automatically  
✅ **Summarize** content using multi-provider LLM (Groq/OpenAI/Gemini)  
✅ **Export** results into clean Markdown research reports  
✅ **Commit** reports directly to GitHub repositories (optional)  
✅ **Review** PRs automatically with CodeRabbit integration  

No more manual copy-pasting. No more lost sources. Just instant, comprehensive research reports.

---

## ✨ Key Features

### 🔍 **Universal Query Support**
- Research any **topic** or **URL**
- Automatic detection of input type
- DuckDuckGo search integration for topics

### 🕷️ **Advanced Web Scraping**
- **Hybrid Crawler** - DuckDuckGo Lite for fast, free results
- **Apify Ready** - Architecture designed for Apify Actor integration
- **Smart Extraction** - Removes ads, scripts, and clutter
- **Multi-Source** - Aggregates data from top 5 search results

### 🤖 **Multi-Provider AI**
- **Groq** (Default - Free tier)
- **OpenAI** (GPT-3.5/GPT-4)
- **Google Gemini** (Gemini Pro/Flash)
- Graceful fallbacks if no API keys

### 📊 **Comprehensive Output**
- **AI Summary** - Key insights highlighted
- **Cleaned Text** - Normalized content
- **Raw Data** - Original crawl results
- **Sources** - Clickable reference links
- **Integration Status** - API health info

### 📝 **Markdown Export**
- Structured research reports
- Auto-generated filenames
- Custom path support
- Timestamp metadata

### 🔄 **GitHub Integration**
- Automatic commit to repositories
- Create or update files
- SHA-based versioning
- Non-blocking design (works without tokens)

### 🤝 **CodeRabbit Ready**
- PR review automation
- AI-powered feedback
- Consistency checking
- Future PR integration

### 🎨 **Modern Frontend**
- Clean React dashboard
- Real-time API calls
- Loading states
- Error handling
- Mobile responsive

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Client (React)                          │
│  • Search Input  • Loading Spinner  • Result Display        │
└─────────────────────────┬───────────────────────────────────┘
                          │
                    POST /research
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   FastAPI Backend                           │
│  • CORS  • Logging  • Error Handling  • Pydantic Models     │
└─────────────────────────┬───────────────────────────────────┘
                          │
              ┌───────────┴───────────┐
              ▼                       ▼
    ┌──────────────────┐    ┌──────────────────┐
    │  WebCrawler      │    │  POST            │
    │  (Apify Actor)   │    │  /github/report  │
    └────────┬─────────┘    └────────┬─────────┘
             │                       │
             ▼                       ▼
    ┌──────────────────┐    ┌──────────────────┐
    │  clean_text()    │    │  Markdown        │
    │  (Regex + Norm)  │    │  Generator       │
    └────────┬─────────┘    └────────┬─────────┘
             │                       │
             ▼                       ▼
    ┌──────────────────┐    ┌──────────────────┐
    │  Summarizer      │    │  GitHub API      │
    │  Groq/OpenAI/    │    │  (Create/Update) │
    │  Gemini          │    └────────┬─────────┘
    └────────┬─────────┘             │
             │                       ▼
             ▼              ┌──────────────────┐
    ┌──────────────────┐   │  CodeRabbit      │
    │  Result JSON     │   │  (PR Reviews)    │
    │  {raw, cleaned,  │   └──────────────────┘
    │   summary, srcs} │
    └────────┬─────────┘
             │
             ▼
    ┌──────────────────┐
    │  Frontend Cards  │
    │  (5 Sections)    │
    └──────────────────┘
```

---

## 🛠️ Tech Stack

**Frontend:**
- React 18.2
- CSS3 (Vanilla + Custom)
- Fetch API

**Backend:**
- FastAPI (Python)
- Pydantic for validation
- Uvicorn ASGI server
- python-dotenv for config

**Crawling:**
- Apify Web Scraper actors
- Requests library for HTTP

**LLM Integration:**
- Groq (Default - Free)
- OpenAI API
- Google Gemini API

**Version Control:**
- GitHub REST API
- Base64 encoding
- Bearer token auth

**Automation:**
- CodeRabbit GitHub App
- Markdown report generation

**Deployment:**
- Render-ready
- Vultr-compatible
- Docker-ready (optional)

---

## 📦 Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env with your API keys
# (See Environment Variables section below)

# Run the server
python main.py
```

Backend runs on `http://localhost:8000`

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Frontend runs on `http://localhost:3000`

---

## 🔐 Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# Apify Configuration (Required for real crawling)
APIFY_API_TOKEN=your_apify_token_here

# LLM Configuration (Choose one provider)
LLM_PROVIDER=groq                    # Options: groq, openai, gemini
LLM_API_KEY=your_llm_api_key_here
MODEL_NAME=mixtral-8x7b-32768        # Groq default model

# GitHub Integration (Optional - for report export)
GITHUB_TOKEN=ghp_your_github_token
GITHUB_REPO=username/repository-name
GITHUB_DEFAULT_BRANCH=main

# CodeRabbit (Optional - for PR reviews)
CODERABBIT_ENABLED=false
CODERABBIT_API_KEY=
```

### Getting API Keys

| Service | Link | Free Tier |
|---------|------|-----------|
| **Apify** | [console.apify.com](https://console.apify.com/account/integrations) | ✅ 20 runs/month |
| **Groq** | [console.groq.com/keys](https://console.groq.com/keys) | ✅ Generous free tier |
| **OpenAI** | [platform.openai.com/api-keys](https://platform.openai.com/api-keys) | ⚠️ Paid |
| **Gemini** | [makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey) | ✅ Free tier available |
| **GitHub** | [github.com/settings/tokens](https://github.com/settings/tokens) | ✅ Free (needs 'repo' scope) |

---

## 🌐 API Endpoints

### `POST /research`
Run the research pipeline (crawl → clean → summarize).

**Request:**
```json
{
  "query": "artificial intelligence" 
}
```

**Response:**
```json
{
  "status": "ok",
  "raw": "Crawled text...",
  "cleaned": "Normalized text...",
  "summary": "AI-generated summary...",
  "sources": ["https://example.com"],
  "integration_status": {
    "apify_enabled": true,
    "llm_enabled": true,
    "llm_provider": "groq"
  }
}
```

### `POST /github/report`
Generate Markdown report and optionally commit to GitHub.

**Request:**
```json
{
  "query": "quantum computing",
  "file_path": "reports/quantum.md"  // optional
}
```

**Response:**
```json
{
  "status": "ok",
  "query": "quantum computing",
  "file_path": "reports/quantum_computing.md",
  "github": {
    "attempted": true,
    "success": true,
    "file_url": "https://github.com/user/repo/blob/main/reports/quantum_computing.md",
    "action": "created"
  },
  "coderabbit": {
    "enabled": false,
    "note": "Install CodeRabbit for PR reviews"
  },
  "preview": {
    "markdown": "# AutoResearcher AI Report\n\n..."
  }
}
```

### `GET /ping`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "message": "pong"
}
```

---

## 🎬 Demo Instructions

### Quick Start

1.  **Start Backend**
    ```bash
    cd backend
    python main.py
    ```

2.  **Start Frontend** (in new terminal)
    ```bash
    cd frontend
    npm start
    ```

3.  **Open Browser**
    - Navigate to `http://localhost:3000`

4.  **Run Research**
    - Enter a topic: `"machine learning"`
    - OR enter a URL: `"https://en.wikipedia.org/wiki/AI"`
    - Click "Run Research"

5.  **View Results**
    - 📝 **AI Summary** (highlighted card)
    - 🧹 **Cleaned Text**
    - 📄 **Raw Crawl Data**
    - 🔗 **Sources** (clickable links)
    - ⚙️ **Integration Status**

6.  **Export to GitHub** (Optional)
    - Use API: `POST /github/report`
    - Or integrate into frontend
    - Report auto-commits to your repo

7.  **CodeRabbit Reviews** (Optional)
    - Install CodeRabbit on your GitHub repo
    - Create PR modifying research report
    - Get automatic AI-powered review

---

## 📸 Screenshots

### Frontend Dashboard
![Research Dashboard](docs/screenshots/dashboard.png)
*Modern Glassmorphism interface with real-time agentic loading states*

### Research Results
![Result Display](docs/screenshots/results.png)
*Comprehensive research report with AI summary, sources, and raw data inspection*

### API Response
```json
{
  "status": "ok",
  "summary": "Artificial intelligence (AI) is intelligence demonstrated by machines...",
  "sources": ["https://en.wikipedia.org/wiki/Artificial_intelligence"]
}
```

---

## 🗺️ Roadmap

### Phase 1: Core Features ✅
- [x] Apify web crawling integration
- [x] Multi-provider LLM support
- [x] Text cleaning and normalization
- [x] React frontend dashboard
- [x] GitHub report export

### Phase 2: Enhanced Features 🚧
- [ ] **Multi-Crawl Comparison** - Compare research from multiple sources
- [ ] **PDF Export** - Download reports as formatted PDFs
- [ ] **JSON Export** - Machine-readable output format
- [ ] **Research History** - Save and browse past research
- [ ] **Dark Mode** - UI theme toggle

### Phase 3: Advanced AI 🔮
- [ ] **RAG-Powered Fact Verification** - Cross-check claims
- [ ] **Citation Generation** - Auto-format references
- [ ] **Multi-Language Support** - Translate summaries
- [ ] **Custom Prompts** - User-defined summary styles
- [ ] **Embeddings Search** - Semantic similarity

### Phase 4: Integrations 🔗
- [ ] **Browser Extension** - Research from any webpage
- [ ] **PR Creation** - Auto-create PRs instead of direct commits
- [ ] **Notion Integration** - Export to Notion databases
- [ ] **Slack Bot** - Query via Slack commands
- [ ] **Discord Bot** - Research in Discord servers

### Phase 5: Enterprise 🏢
- [ ] **Authentication** - User accounts and API keys
- [ ] **Rate Limiting** - Usage quotas
- [ ] **Analytics Dashboard** - Usage statistics
- [ ] **Team Workspaces** - Collaborative research
- [ ] **Webhook Support** - Real-time notifications

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

*   **Groq** for fast, free LLM inference
*   **DuckDuckGo** for privacy-focused search results
*   **GitHub** for excellent API and platform
*   **FastAPI** for the amazing web framework
*   **React** for the frontend library

## 📧 Contact

**Project Link:** [https://github.com/adithyakrish0/AutoResearcher-AI](https://github.com/adithyakrish0/AutoResearcher-AI)

**Built with ❤️ for HackThisFall 2025**

---

### 🌟 Star this repo if you find it useful!
