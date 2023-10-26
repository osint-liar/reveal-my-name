"""Site Schemas"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, model_validator, Field


class SiteOutputSchema(BaseModel):
    """For exporting to csv, json"""
    name: str
    category: str
    raw_response_data: Optional[str] = None
    http_status_code: int
    generated_uri: str
    username: str
    user_agent: str
    uri_pretty: Optional[str] = None
    error_hint: Optional[str] = None
    response_headers: Optional[str] = None


class SiteSchema(BaseModel):
    name: str
    e_code: int
    e_string: str
    m_string: str
    m_code: int
    known: List[str]
    category: str = Field(alias='cat')
    valid: bool
    post_body: Optional[str] = None
    uri_check: str
    request_method: str = None
    username: str = None
    generated_uri: str = None
    http_status_code: int = -1
    last_checked_on: Optional[datetime] = None
    comment: Optional[str] = None
    raw_response_data: Optional[str] = None
    cloudflare_enabled: bool = False
    user_agent: Optional[str] = None
    uri_pretty: Optional[str] = None
    error_hint: Optional[str] = None
    response_headers: Optional[str] = None
    invalid_chars: Optional[str] = None

    @model_validator(mode='after')
    def set_request_method(self) -> "SiteSchema":
        if self.post_body:
            self.request_method = 'POST'
        else:
            self.request_method = 'GET'
        return self


class SitesConfigurationSchema(BaseModel):
    license: List[str] = []
    authors: List[str] = []
    categories: List[str] = []
    sites: List[SiteSchema] = []
