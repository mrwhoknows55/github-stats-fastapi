from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Depends

from src.services.github_client import GitHubClient

from src.core.config import CORS_WHITELIST
from src.models.github import UserData, RepositoryDetail, IssueCreate, IssueResponse

app = FastAPI(
    title="GitHub Stats API Service",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_WHITELIST,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Health"], summary="Health check endpoint")
async def health_check():
    return {"status": "ok"}



TAGS = ["Github"]
async def get_github_client():
    return GitHubClient()

@app.get("/v1/github", response_model=UserData, tags=TAGS, summary="Get summary data for the user")
async def get_github_user_summary(github_client: GitHubClient = Depends(get_github_client)):
    """Get summary data for the GitHub user."""
    user_data = await github_client.get_user_data()
    repos_data = await github_client.get_user_repos()
    repositories = [
        {
            "name": repo["name"],
            "description": repo.get("description"),
            "html_url": repo["html_url"]
        }
        for repo in repos_data
    ]

    return {
        "username": user_data["login"],
        "followers": user_data["followers"],
        "following": user_data["following"],
        "repositories": repositories
    }


@app.get("/v1/github/{repo_name}", response_model=RepositoryDetail, tags=TAGS, summary="Get detailed repo data")
async def get_github_repo_details(
        repo_name: str,
        github_client: GitHubClient = Depends(get_github_client)
):
    """Get detailed information about a specific repository."""
    repo_data = await github_client.get_repo_details(repo_name)

    return {
        "name": repo_data["name"],
        "description": repo_data.get("description"),
        "html_url": repo_data["html_url"],
        "stargazers_count": repo_data["stargazers_count"],
        "forks_count": repo_data["forks_count"]
    }


@app.post("/v1/github/{repo_name}/issues", response_model=IssueResponse, tags=TAGS,
          summary="Create a new issue for given a repo")
async def create_github_issue(
        repo_name: str,
        issue: IssueCreate,
        github_client: GitHubClient = Depends(get_github_client)
):
    """Create a new issue in the given repository."""
    response = await github_client.create_issue(repo_name, issue.title, issue.body)

    return {
        "issue_url": response["html_url"]
    }
