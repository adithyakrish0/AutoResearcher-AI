from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
import logging

# Import our modules
from apify_agent.crawler import WebCrawler
from utils.cleaner import clean_text
from llm.summarizer import Summarizer
from config import APIFY_API_TOKEN, LLM_PROVIDER, LLM_API_KEY, GITHUB_TOKEN, GITHUB_REPO, GITHUB_DEFAULT_BRANCH, CODERABBIT_ENABLED

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AutoResearcher AI API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize pipeline components
crawler = WebCrawler()
summarizer = Summarizer()


# Request models
class ResearchRequest(BaseModel):
    query: str


# Response models
class SourceItem(BaseModel):
    url: str
    raw: str
    cleaned: str

class ResearchResponse(BaseModel):
    status: str
    summary: str
    merged_cleaned: str
    sources: List[str] = []
    integration_status: dict = {}


@app.get("/")
async def root():
    return {"message": "AutoResearcher AI API"}


@app.get("/ping")
async def health_check():
    return {"status": "healthy", "message": "pong"}


@app.post("/research")
async def research_topic(request: ResearchRequest):
    """
    Multi-source research pipeline:
    1. Search & Collect URLs (DuckDuckGo Lite)
    2. Crawl 5 sources (Requests + BS4)
    3. Clean & Merge texts
    4. Summarize unified text
    """
    query = request.query
    logger.info(f"Researching: {query}")
    
    try:
        # Step A: Search for URLs
        urls = crawler.search_top_urls(request.query)
        print(f"[MultiSource] Using URLs: {urls}")

        # Step B: Crawl each URL
        raw_pages = {}
        for u in urls:
            raw_text = crawler.crawl_url(u)
            raw_pages[u] = raw_text
            
        # Step C: Clean & Merge
        merged_cleaned = ""
        for src, raw in raw_pages.items():
            cleaned = clean_text(raw)
            merged_cleaned += f"\n\n--- SOURCE: {src} ---\n{cleaned}\n"
        
        # Step D: Summarize
        # We need to use the multi-source summarizer method if it exists, or just summarize
        # The prompt asked to use "summarize_multi_source" in Phase 16, but didn't explicitly mention it in this "DuckDuckGo Lite" update prompt.
        # However, since we are doing multi-source, we should probably use the multi-source summarizer if available.
        # Let's check if Summarizer has summarize_multi_source. It should from previous steps.
        # If not, we fall back to summarize.
        
        if hasattr(summarizer, 'summarize_multi_source'):
            summary = summarizer.summarize_multi_source(merged_cleaned)
        else:
            summary = summarizer.summarize(merged_cleaned)
        
        return {
            "status": "ok",
            "summary": summary,
            "merged_cleaned": merged_cleaned,
            "sources": list(raw_pages.keys()),
            "integration_status": {
                "apify_enabled": False,
                "llm_enabled": True,
                "llm_provider": LLM_PROVIDER
            }
        }

    except Exception as e:
        logger.error(f"Research pipeline failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Research pipeline failed: {str(e)}"
        )


# Request model for GitHub report
class GitHubReportRequest(BaseModel):
    query: str
    file_path: Optional[str] = None


# Helper function to slugify query for filename
def slugify(text: str) -> str:
    """Convert text to URL-safe slug"""
    import re
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '_', text)
    text = re.sub(r'^-+|-+$', '', text)
    return text[:50]  # Limit length


@app.post("/github/report")
async def github_report(request: GitHubReportRequest):
    """
    Generate research report and export to GitHub.
    """
    from github_integration.report_generator import generate_markdown_report
    from github_integration.github_client import create_or_update_file
    
    query = request.query
    
    # Determine file path
    if request.file_path:
        file_path = request.file_path
    else:
        # Generate filename from query
        slug = slugify(query)
        file_path = f"reports/{slug}.md"
    
    logger.info(f"GitHub report request for query: {query}")
    
    try:
        # Re-run pipeline logic for report
        urls = crawler.search_top_urls(query)
        raw_pages = {}
        for u in urls:
            raw_text = crawler.crawl_url(u)
            raw_pages[u] = raw_text
            
        merged_cleaned = ""
        cleaned_pages = {}
        for src, raw in raw_pages.items():
            cleaned = clean_text(raw)
            merged_cleaned += f"\n\n--- SOURCE: {src} ---\n{cleaned}\n"
            cleaned_pages[src] = cleaned
            
        if hasattr(summarizer, 'summarize_multi_source'):
            summary_text = summarizer.summarize_multi_source(merged_cleaned)
        else:
            summary_text = summarizer.summarize(merged_cleaned)
        
        # Build result dict for report generator
        # Adapting to match what report generator might expect
        sources_list = []
        for url, raw in raw_pages.items():
            sources_list.append({
                "url": url,
                "raw": raw[:500] + "...",
                "cleaned": cleaned_pages.get(url, "")[:500] + "..."
            })

        integration_status = {
            "apify_enabled": False,
            "llm_enabled": True,
            "llm_provider": LLM_PROVIDER
        }
        
        result_dict = {
            "status": "ok",
            "raw": str(raw_pages), 
            "cleaned": merged_cleaned,
            "summary": summary_text,
            "sources": sources_list,
            "integration_status": integration_status
        }
        
        # Step 2: Generate Markdown report
        logger.info("Generating Markdown report...")
        markdown_content = generate_markdown_report(query, result_dict)
        
        # Step 3: Attempt GitHub commit
        logger.info("Attempting GitHub commit...")
        github_result = create_or_update_file(
            path=file_path,
            content=markdown_content,
            commit_message=f"Add research report for: {query}",
            github_token=GITHUB_TOKEN,
            github_repo=GITHUB_REPO,
            branch=GITHUB_DEFAULT_BRANCH
        )
        
        # Build response
        response = {
            "status": "ok",
            "query": query,
            "file_path": file_path,
            "github": {
                "attempted": True,
                "success": github_result.get("success", False),
                "file_url": github_result.get("file_url"),
                "reason": github_result.get("reason") if not github_result.get("success") else None,
                "action": github_result.get("action")
            },
            "coderabbit": {
                "enabled": CODERABBIT_ENABLED,
                "note": "If CodeRabbit is installed on this repo, future pull requests that modify this report will be auto-reviewed."
            },
            "preview": {
                "markdown": markdown_content[:2000]
            }
        }
        
        return response
        
    except Exception as e:
        logger.error(f"GitHub report failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"GitHub report failed: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
