from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Apify Configuration
APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN", "")

# LLM Configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")  # Options: groq, openai, gemini
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")

# GitHub Configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_REPO = os.getenv("GITHUB_REPO", "")  # format: "owner/repo"
GITHUB_DEFAULT_BRANCH = os.getenv("GITHUB_DEFAULT_BRANCH", "main")

# CodeRabbit Configuration
CODERABBIT_API_KEY = os.getenv("CODERABBIT_API_KEY", "")
CODERABBIT_ENABLED = bool(os.getenv("CODERABBIT_ENABLED", "").lower() in ["1", "true", "yes"])

# API Endpoints
APIFY_BASE_URL = "https://api.apify.com/v2"
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
OPENAI_BASE_URL = "https://api.openai.com/v1"
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
