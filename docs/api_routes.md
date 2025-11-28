# AutoResearcher AI - API Routes

## Base URL
`http://localhost:8000`

## Endpoints

### Health Check

#### GET `/ping`
Check if the API server is running.

**Response:**
```json
{
  "status": "healthy",
  "message": "pong"
}
```

### Root

#### GET `/`
Get API information.

**Response:**
```json
{
  "message": "AutoResearcher AI API"
}
```

---

## Research Pipeline

### POST `/research`
Execute the complete research pipeline: crawl → clean → summarize.

**Pipeline Flow:**
1. **Crawl** - WebCrawler fetches content from URL or searches for topic
2. **Clean** - Text normalization and cleaning
3. **Summarize** - LLM-based summarization

**Request Body:**
```json
{
  "query": "https://example.com OR research topic"
}
```

**Response (200 OK):**
```json
{
  "status": "ok",
  "raw": "Extracted text from crawl...",
  "cleaned": "Cleaned and normalized text...",
  "summary": "AI-generated summary...",
  "sources": ["https://example.com"],
  "integration_status": {
    "apify_enabled": true,
    "llm_enabled": true,
    "llm_provider": "groq"
  }
}
```

**Error Response (500):**
```json
{
  "detail": "Research pipeline failed: error message"
}
```

**Example Usage:**

```bash
curl -X POST http://localhost:8000/research \
  -H "Content-Type: application/json" \
  -d '{"query": "artificial intelligence"}'
```

### Integration Details

#### Apify Crawling
- **With API Key**: Uses Apify Web Scraper actor for real crawling
- **URL Mode**: Crawls specified URL with depth 1, max 5 pages
- **Topic Mode**: Searches Google and extracts results
- **Fallback**: Returns placeholder text if no API key

#### LLM Summarization
Supports three providers selected via `LLM_PROVIDER` environment variable:

**Groq** (Default - Free):
- Models: `mixtral-8x7b-32768`, `llama2-70b-4096`, `gemma-7b-it`
- Endpoint: `https://api.groq.com/openai/v1/chat/completions`

**OpenAI**:
- Models: `gpt-3.5-turbo`, `gpt-4`
- Endpoint: `https://api.openai.com/v1/chat/completions`

**Gemini**:
- Models: `gemini-pro`, `gemini-1.5-flash`
- Endpoint: `https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent`

#### Environment Configuration

Create a `.env` file in the `backend/` directory:

```env
# Required for web crawling
APIFY_API_TOKEN=your_apify_token

# LLM Provider (groq, openai, or gemini)
LLM_PROVIDER=groq
LLM_API_KEY=your_llm_api_key
MODEL_NAME=mixtral-8x7b-32768
```

**Getting API Keys:**
- **Apify**: https://console.apify.com/account/integrations
- **Groq**: https://console.groq.com/keys (Free tier available)
- **OpenAI**: https://platform.openai.com/api-keys
- **Gemini**: https://makersuite.google.com/app/apikey

**Fallback Behavior:**
- If no Apify key: Returns placeholder crawl text
- If no LLM key: Returns truncated raw text with error message
- Both integrations work independently

**Implementation Notes:**
- Uses `requests` library only (no SDK dependencies)
- Apify actor runs poll for completion (max 60 seconds)
- LLM input limited to 4000 characters
- Error handling with graceful fallbacks

---

## GitHub Integration

### POST `/github/report`
Generate research report as Markdown and optionally export to GitHub repository.

**Purpose:**
- Runs complete research pipeline
- Generates structured Markdown report
- Commits report to GitHub (if configured)
- Returns CodeRabbit integration status

**Request Body:**
```json
{
  "query": "research topic or URL",
  "file_path": "reports/custom_name.md"  // optional
}
```

**Response (200 OK):**
```json
{
  "status": "ok",
  "query": "artificial intelligence",
  "file_path": "reports/artificial_intelligence.md",
  "github": {
    "attempted": true,
    "success": true,
    "file_url": "https://github.com/owner/repo/blob/main/reports/artificial_intelligence.md",
    "action": "created",  // or "updated"
    "reason": null
  },
  "coderabbit": {
    "enabled": false,
    "note": "If CodeRabbit is installed on this repo, future pull requests that modify this report will be auto-reviewed."
  },
  "preview": {
    "markdown": "# AutoResearcher AI Report\n\n## Query\n..."
  }
}
```

**Without GitHub Configuration:**
```json
{
  "status": "ok",
  "query": "machine learning",
  "file_path": "reports/machine_learning.md",
  "github": {
    "attempted": true,
    "success": false,
    "file_url": null,
    "action": null,
    "reason": "GitHub integration not configured - missing GITHUB_TOKEN or GITHUB_REPO"
  },
  "coderabbit": {
    "enabled": false,
    "note": "If CodeRabbit is installed on this repo, future pull requests that modify this report will be auto-reviewed."
  },
  "preview": {
    "markdown": "# AutoResearcher AI Report\n\n..."
  }
}
```

**Example Usage:**

```bash
# With auto-generated filename
curl -X POST http://localhost:8000/github/report \
  -H "Content-Type: application/json" \
  -d '{"query": "quantum computing"}'

# With custom file path
curl -X POST http://localhost:8000/github/report \
  -H "Content-Type: application/json" \
  -d '{"query": "neural networks", "file_path": "research/2024/neural_nets.md"}'
```

**Markdown Report Structure:**
```markdown
# AutoResearcher AI Report

## Query
<user query>

## Summary
<AI-generated summary>

## Cleaned Text
<normalized crawled text>

## Raw Crawl Data (truncated)
<first 2000 characters>

## Sources
- <source URLs>

## Integration Status
- Apify enabled: true/false
- LLM enabled: true/false
- LLM provider: groq/openai/gemini
```

**GitHub Configuration:**

Required environment variables:
```env
GITHUB_TOKEN=ghp_your_personal_access_token
GITHUB_REPO=username/repository-name
GITHUB_DEFAULT_BRANCH=main
```

**Getting GitHub Token:**
1. Go to https://github.com/settings/tokens
2. Generate new token (classic)
3. Select scope: `repo` (Full control of private repositories)
4. Copy token to `.env` file

**CodeRabbit Integration:**

CodeRabbit is a GitHub App that automatically reviews pull requests.

**Setup:**
1. Install CodeRabbit on your repository: https://coderabbit.ai
2. Set `CODERABBIT_ENABLED=true` in `.env`
3. When PRs modify report files, CodeRabbit will auto-review

**Flow:**
1. Run `/github/report` → commits report to main branch
2. Create PR with changes to report
3. CodeRabbit automatically reviews the PR
4. Get AI-powered code review feedback

**Non-Blocking Behavior:**
- Endpoint works without GitHub configuration
- Returns Markdown preview even if GitHub commit fails
- Safe to use without tokens (useful for testing)

---

## Planned Endpoints

### Research

#### POST `/api/research`
Submit a new research request.

**Request Body:**
```json
{
  "query": "string",
  "depth": "shallow | deep",
  "sources": ["url1", "url2"]
}
```

**Response:**
```json
{
  "research_id": "uuid",
  "status": "processing"
}
```

#### GET `/api/research/{research_id}`
Get research results.

**Response:**
```json
{
  "research_id": "uuid",
  "status": "completed | processing | failed",
  "summary": "string",
  "sources": [],
  "created_at": "timestamp"
}
```

### Crawling

#### POST `/api/crawl`
Initiate web crawling for a URL.

**Request Body:**
```json
{
  "url": "string",
  "max_depth": 1
}
```

### Summarization

#### POST `/api/summarize`
Summarize provided text.

**Request Body:**
```json
{
  "text": "string",
  "max_length": 500
}
```

---

*Note: Planned endpoints are not yet implemented.*
