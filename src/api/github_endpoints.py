from fastapi import APIRouter, Depends, status, Path, Body

from src.models.github import UserData, RepositoryDetail, IssueCreate, IssueResponse
from src.services.github_client import GitHubClient

router = APIRouter(prefix="/v1/github", tags=["GitHub"])

async def get_github_client():
    return GitHubClient()


@router.get(
    "",
    response_model=UserData,
    summary="Get GitHub user summary",
    description="Returns summary data for the authenticated GitHub user including number of followers, number of following, and a list of personal repositories.",
    responses={
        200: {
            "description": "Successful response with user data",
            "model": UserData
        },
        401: {
            "description": "Authentication error with GitHub API"
        },
        403: {
            "description": "Forbidden: Access denied to GitHub resource"
        },
        429: {
            "description": "GitHub API rate limit exceeded"
        },
        503: {
            "description": "Error connecting to GitHub API"
        }
    }
)
async def get_github_user_summary(github_client: GitHubClient = Depends(get_github_client)):
    """
    Get summary data for the given GitHub user.
    This endpoint retrieves information from GitHub API and returns:
    - Username
    - Number of followers
    - Number of following users
    - List of personal repositories with name, description, and URL
    """
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


@router.get(
    "/{repo_name}",
    response_model=RepositoryDetail,
    summary="Get repository details",
    description="Returns detailed data about the specified repository.",
    responses={
        200: {
            "description": "Successful response with repository details",
            "model": RepositoryDetail
        },
        404: {
            "description": "Repository not found on GitHub"
        },
        401: {
            "description": "Authentication error with GitHub API"
        },
        403: {
            "description": "Forbidden: Access denied to GitHub resource"
        },
        429: {
            "description": "GitHub API rate limit exceeded"
        },
        503: {
            "description": "Error connecting to GitHub API"
        }
    }
)
async def get_github_repo_details(
        repo_name: str = Path(..., description="Name of the repository to fetch details for"),
        github_client: GitHubClient = Depends(get_github_client)
):
    """
    Get detailed information about a specific repository.
    - Repository name
    - Description (if available)
    - HTML URL (link to the repository on GitHub)
    - Star count (number of users who starred the repository)
    - Fork count (number of repository forks)
    """
    repo_data = await github_client.get_repo_details(repo_name)
    return {
        "name": repo_data["name"],
        "description": repo_data.get("description"),
        "html_url": repo_data["html_url"],
        "stargazers_count": repo_data["stargazers_count"],
        "forks_count": repo_data["forks_count"]
    }


@router.post(
    "/{repo_name}/issues",
    response_model=IssueResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create an issue",
    description="Creates an issue in the specified repository.",
    responses={
        201: {
            "description": "Issue created successfully, returns URL of the created issue",
            "model": IssueResponse
        },
        400: {
            "description": "Invalid request body"
        },
        404: {
            "description": "Repository not found on GitHub"
        },
        401: {
            "description": "Authentication error with GitHub API"
        },
        403: {
            "description": "Forbidden: Access denied to GitHub resource"
        },
        429: {
            "description": "GitHub API rate limit exceeded"
        },
        503: {
            "description": "Error connecting to GitHub API"
        }
    }
)
async def create_github_issue(
        repo_name: str = Path(..., description="Name of the repository to create the issue in"),
        issue: IssueCreate = Body(
            ...,
            description="Issue details including title and body"
        ),
        github_client: GitHubClient = Depends(get_github_client)
):
    """
    Create a new issue in the specified repository.
    This endpoint creates a new issue in the specified repository using:
    - A title for the issue (required)
    - A body/description for the issue (required)
    """
    response = await github_client.create_issue(repo_name, issue.title, issue.body)

    return {
        "issue_url": response["html_url"]
    }