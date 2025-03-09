from typing import Dict, List, Any, Optional

import httpx
from fastapi import HTTPException

from src.core import config


class GitHubClient:
    def __init__(self):
        self.base_url = config.GITHUB_API_BASE_URL
        self.user_name = config.GITHUB_USERNAME
        self.headers = {
            "Authorization": f"Bearer {config.GITHUB_TOKEN}",
            "Accept": "application/json"
        }

    async def _make_request(self, method: str, url: str, data: Optional[Dict] = None) -> Any:
        """Make a basic request to the GitHub API."""
        async with httpx.AsyncClient() as client:
            try:
                if method == "GET":
                    response = await client.get(url, headers=self.headers)
                elif method == "POST":
                    response = await client.post(url, headers=self.headers, json=data)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")

                if response.status_code == 403 and "X-RateLimit-Remaining" in response.headers:
                    if int(response.headers["X-RateLimit-Remaining"]) == 0:
                        reset_time = response.headers.get("X-RateLimit-Reset", "unknown")
                        raise HTTPException(
                            status_code=429,
                            detail=f"GitHub API rate limit exceeded. Resets at {reset_time}"
                        )

                response.raise_for_status()
                return response.json()

            except httpx.HTTPStatusError as e:
                status_code = e.response.status_code
                if status_code == 404:
                    raise HTTPException(status_code=404, detail="Resource not found on GitHub")
                elif status_code == 401:
                    raise HTTPException(status_code=401, detail="Authentication error with GitHub API")
                elif status_code == 403 and "X-RateLimit-Remaining" not in e.response.headers:
                    raise HTTPException(status_code=403, detail="Forbidden: Access denied to GitHub resource")
                else:
                    raise HTTPException(
                        status_code=status_code,
                        detail=f"GitHub API error: {e.response.text}"
                    )
            except httpx.RequestError as e:
                raise HTTPException(status_code=503, detail=f"Error connecting to GitHub API: {str(e)}")

    async def get_user_data(self) -> Dict:
        """Get user data."""
        return await self._make_request("GET", f"{self.base_url}/user")

    async def get_user_repos(self) -> List[Dict]:
        """Get list of repositories for the user."""
        return await self._make_request("GET", f"{self.base_url}/users/{self.user_name}/repos")

    async def get_repo_details(self, repo_name: str) -> Dict:
        """Get details about a specific repository."""
        return await self._make_request(
            "GET",
            f"{self.base_url}/repos/{self.user_name}/{repo_name}"
        )

    async def create_issue(self, repo_name: str, title: str, body: str) -> Dict:
        """Create a new issue in the specified repository."""
        data = {"title": title, "body": body}
        return await self._make_request(
            "POST",
            f"{self.base_url}/repos/{self.user_name}/{repo_name}/issues",
            data=data
        )
