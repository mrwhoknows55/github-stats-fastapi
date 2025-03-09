import httpx
from typing import Dict, List, Any, Optional

from src.core import config


class GitHubClient:
    def __init__(self):
        self.base_url = config.GITHUB_API_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {config.GITHUB_TOKEN}",
            "Accept": "application/json"
        }

    async def _make_request(self, method: str, url: str, data: Optional[Dict] = None) -> Any:
        """Make a basic request to the GitHub API."""
        async with httpx.AsyncClient() as client:
            if method == "GET":
                response = await client.get(url, headers=self.headers)
            elif method == "POST":
                response = await client.post(url, headers=self.headers, json=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response.json()

    async def get_user_data(self) -> Dict:
        """Get user data."""
        return await self._make_request("GET", f"{self.base_url}/user")

    async def get_user_repos(self) -> List[Dict]:
        """Get list of repositories for the user."""
        return await self._make_request("GET", f"{self.base_url}/users/{config.GITHUB_USERNAME}/repos")

    async def get_repo_details(self, repo_name: str) -> Dict:
        """Get details about a specific repository."""
        return await self._make_request(
            "GET",
            f"{self.base_url}/repos/{config.GITHUB_USERNAME}/{repo_name}"
        )

    async def create_issue(self, repo_name: str, title: str, body: str) -> Dict:
        """Create a new issue in the specified repository."""
        data = {"title": title, "body": body}
        return await self._make_request(
            "POST",
            f"{self.base_url}/repos/{config.GITHUB_USERNAME}/{repo_name}/issues",
            data=data
        )