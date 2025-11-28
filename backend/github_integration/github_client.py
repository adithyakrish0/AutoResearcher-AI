"""
GitHub API Client for AutoResearcher AI
Handles file creation and updates in GitHub repositories.
"""

import base64
import requests
import logging
from typing import Optional

# Configure logging
logger = logging.getLogger(__name__)


def create_or_update_file(
    path: str,
    content: str,
    commit_message: str,
    github_token: str = "",
    github_repo: str = "",
    branch: str = "main"
) -> dict:
    """
    Creates or updates a file in the configured GitHub repository.
    
    Args:
        path (str): File path in the repository (e.g., "reports/research.md")
        content (str): File content as string
        commit_message (str): Commit message
        github_token (str): GitHub personal access token
        github_repo (str): Repository in format "owner/repo"
        branch (str): Target branch (default: "main")
        
    Returns:
        dict: Result with success status, file URL, and details
    """
    # Check if GitHub integration is configured
    if not github_token or not github_repo:
        return {
            "success": False,
            "reason": "GitHub integration not configured - missing GITHUB_TOKEN or GITHUB_REPO",
            "status_code": None,
            "file_url": None
        }
    
    try:
        # Parse owner and repo
        if "/" not in github_repo:
            return {
                "success": False,
                "reason": "Invalid GITHUB_REPO format, expected 'owner/repo'",
                "status_code": None,
                "file_url": None
            }
        
        owner, repo = github_repo.split("/", 1)
        
        # GitHub API base URL
        base_url = "https://api.github.com"
        contents_url = f"{base_url}/repos/{owner}/{repo}/contents/{path}"
        
        # Headers
        headers = {
            "Authorization": f"Bearer {github_token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        
        # Step 1: Check if file already exists (to get SHA)
        existing_sha = None
        try:
            get_response = requests.get(
                contents_url,
                headers=headers,
                params={"ref": branch}
            )
            if get_response.status_code == 200:
                existing_data = get_response.json()
                existing_sha = existing_data.get("sha")
                logger.info(f"File exists, will update. SHA: {existing_sha}")
        except Exception as e:
            logger.info(f"File does not exist yet, will create new. Error: {str(e)}")
        
        # Step 2: Encode content to base64
        content_bytes = content.encode("utf-8")
        content_base64 = base64.b64encode(content_bytes).decode("utf-8")
        
        # Step 3: Build request body
        body = {
            "message": commit_message,
            "content": content_base64,
            "branch": branch
        }
        
        # Include SHA if file exists (for update)
        if existing_sha:
            body["sha"] = existing_sha
        
        # Step 4: Create or update file
        put_response = requests.put(
            contents_url,
            headers=headers,
            json=body
        )
        
        # Parse response
        if put_response.status_code in [200, 201]:
            response_data = put_response.json()
            file_url = response_data.get("content", {}).get("html_url")
            
            logger.info(f"Successfully {'updated' if existing_sha else 'created'} file: {file_url}")
            
            return {
                "success": True,
                "status_code": put_response.status_code,
                "file_url": file_url,
                "response": response_data,
                "action": "updated" if existing_sha else "created"
            }
        else:
            logger.error(f"GitHub API error: {put_response.status_code} - {put_response.text}")
            return {
                "success": False,
                "reason": f"GitHub API error: {put_response.status_code}",
                "status_code": put_response.status_code,
                "file_url": None,
                "error_details": put_response.text
            }
            
    except Exception as e:
        logger.error(f"GitHub integration error: {str(e)}")
        return {
            "success": False,
            "reason": f"Exception: {str(e)}",
            "status_code": None,
            "file_url": None
        }
