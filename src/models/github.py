from typing import List, Optional

from pydantic import BaseModel, Field


# Repository models:
class RepositorySummary(BaseModel):
    name: str = Field(..., json_schema_extra={"example": "awesome-project"})
    description: Optional[str] = Field(None, json_schema_extra={"example": "A really awesome project"})
    html_url: str = Field(..., json_schema_extra={"example": "https://github.com/username/awesome-project"})


class RepositoryDetail(BaseModel):
    name: str = Field(..., json_schema_extra={"example": "awesome-project"})
    description: Optional[str] = Field(None, json_schema_extra={"example": "A really awesome project"})
    html_url: str = Field(..., json_schema_extra={"example": "https://github.com/username/awesome-project"})
    stargazers_count: int = Field(..., json_schema_extra={"example": 42})
    forks_count: int = Field(..., json_schema_extra={"example": 13})


# User data response models:
class UserData(BaseModel):
    username: str = Field(..., json_schema_extra={"example": "github-user"})
    followers: int = Field(..., json_schema_extra={"example": 100})
    following: int = Field(..., json_schema_extra={"example": 50})
    repositories: List[RepositorySummary]


# Issue models:
class IssueCreate(BaseModel):
    title: str = Field(..., json_schema_extra={"example": "Bug in the login page"})
    body: str = Field(..., json_schema_extra={
        "example": "There's an issue with the login page where users cannot submit the form when using Firefox."})


class IssueResponse(BaseModel):
    issue_url: str = Field(..., json_schema_extra={"example": "https://github.com/username/awesome-project/issues/123"})


# Error response models:
class ErrorResponse(BaseModel):
    error: str = Field(..., json_schema_extra={"example": "Resource not found on GitHub"})
    code: int = Field(..., json_schema_extra={"example": 404})
