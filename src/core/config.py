import os
from dotenv import load_dotenv

load_dotenv()

# GitHub Configuration
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_USERNAME = os.getenv('GITHUB_USERNAME')
GITHUB_API_BASE_URL = os.getenv('GITHUB_API_BASE_URL', 'https://api.github.com')

# CORS Configuration
CORS_WHITELIST = os.getenv('CORS_WHITELIST', '').split(',') 