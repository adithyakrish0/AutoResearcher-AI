# AutoResearcher AI - Architecture

## Overview

This document outlines the architecture of AutoResearcher AI.

## System Components

### Frontend
- React-based user interface
- Component-based architecture
- State management (TBD)

### Backend
- FastAPI server
- RESTful API endpoints
- Modular structure with separate concerns:
  - Web crawling (Apify integration)
  - LLM processing (summarization)
  - Utility functions

### External Integrations
- Apify for web crawling
- LLM service for text summarization
- GitHub API for repository management
- CodeRabbit for PR reviews

## Data Flow

1. User submits research request via frontend
2. Backend receives request and initiates web crawling
3. Crawled data is processed and cleaned
4. LLM generates summary
5. Results are returned to frontend
6. Optional GitHub integration for storing results

## Technology Stack

**Frontend:**
- React
- React Router (TBD)

**Backend:**
- Python 3.x
- FastAPI
- Uvicorn
- Pydantic
- python-dotenv
- requests

**External Services:**
- Apify Web Scraper
- LLM Providers: Groq / OpenAI / Gemini
- GitHub API (TBD)
- CodeRabbit (TBD)

## Integration Architecture

### Apify Web Crawling Flow

```
User Query → WebCrawler.run_crawl()
    ↓
Check if URL or Topic
    ↓
Build Actor Payload
    ├─ URL: Direct crawl with startUrls
    └─ Topic: Google search + scrape
    ↓
POST /v2/acts/apify~web-scraper/runs
    ↓
Poll run status (max 60s)
    ↓
GET /v2/acts/.../runs/{id}/dataset/items
    ↓
Extract text + sources
    ↓
Return crawl results
```

**Configuration:**
- API Token loaded from `APIFY_API_TOKEN` env var
- Fallback to placeholder if no token
- Extracts `body` text and `url` from results

### LLM Provider Selection

The system supports multiple LLM providers with automatic selection based on `LLM_PROVIDER` env var:

**Provider Flow:**
```
Summarizer.summarize(text)
    ↓
Check LLM_PROVIDER config
    ├─ "groq" → summarize_with_groq()
    ├─ "openai" → summarize_with_openai()
    └─ "gemini" → summarize_with_gemini()
    ↓
Make API request
    ↓
Return summary or fallback
```

**Groq Provider** (Recommended - Free):
- Endpoint: `https://api.groq.com/openai/v1/chat/completions`
- Models: `mixtral-8x7b-32768`, `llama2-70b-4096`
- Free tier with generous limits

**OpenAI Provider**:
- Endpoint: `https://api.openai.com/v1/chat/completions`
- Models: `gpt-3.5-turbo`, `gpt-4`
- Paid API

**Gemini Provider**:
- Endpoint: `https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent`
- Models: `gemini-pro`, `gemini-1.5-flash`
- Free tier available

### Configuration Management

Environment variables loaded via `backend/config.py`:

```python
APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN", "")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
MODEL_NAME = os.getenv("MODEL_NAME", "mixtral-8x7b-32768")
```

**Fallback Strategy:**
- Missing Apify token → Placeholder crawl text
- Missing LLM key → Truncated text with error message
- API errors → Graceful degradation

## GitHub and CodeRabbit Integration Flow

AutoResearcher AI can export research reports as Markdown files and commit them to GitHub repositories for version control and collaboration.

### Report Generation Flow

```
POST /github/report
    ↓
Run Research Pipeline
    ├─ WebCrawler.run_crawl()
    ├─ clean_text()
    └─ Summarizer.summarize()
    ↓
generate_markdown_report()
    ├─ Format query, summary, cleaned text
    ├─ Truncate raw data (2000 chars)
    ├─ List sources
    └─ Add integration status
    ↓
create_or_update_file()
    ├─ Check GitHub configuration
    ├─ GET existing file SHA (if exists)
    ├─ Base64 encode content
    ├─ PUT to GitHub API
    └─Return success/failure status
    ↓
Return JSON Response
    ├─ github.success: true/false
    ├─ github.file_url: link to file
    ├─ coderabbit.enabled: status
    └─ preview.markdown: first 2000 chars
```

### GitHub API Integration

**Authentication:**
- Uses Personal Access Token (PAT)
- Required scope: `repo`
- Configured via `GITHUB_TOKEN` env var

**File Operations:**
- Creates new files if they don't exist
- Updates existing files (requires SHA)
- Uses GitHub Contents API
- Supports any branch (default: main)

**Repository Format:**
- `GITHUB_REPO` must be in `owner/repo` format
- Example: `johndoe/research-reports`

### CodeRabbit Integration

CodeRabbit is a GitHub App that provides AI-powered PR reviews.

**Setup Process:**
1. Install CodeRabbit GitHub App on your repository
2. Visit: https://coderabbit.ai
3. Grant permissions for PR access
4. Set `CODERABBIT_ENABLED=true` in `.env`

**Workflow:**
```
AutoResearcher generates report
    ↓
POST /github/report commits to main branch
    ↓
Developer creates PR to modify report
    ↓
CodeRabbit automatically triggered
    ↓
AI reviews changes in PR
    ↓
Provides feedback and suggestions
```

**Benefits:**
- Automated code review for research reports
- Consistency checking
- Formatting suggestions
- Context-aware feedback

**Non-Blocking Design:**
- GitHub integration is fully optional
- Endpoint works without tokens
- Returns Markdown preview regardless
- Graceful degradation if GitHub API fails
- CodeRabbit status informational only

**Manual Alternative:**
If GitHub integration is not configured, users can:
1. Call `/github/report` endpoint
2. Copy markdown from `preview.markdown` in response
3. Manually create file in their repository
4. Commit and push changes

## Future Enhancements

- Authentication and user management
- Database integration for storing research history
- Advanced LLM features
- Real-time updates via WebSockets
