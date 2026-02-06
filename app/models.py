"""Data models"""

from pydantic import BaseModel, HttpUrl, Field
from typing import Optional
from enum import Enum


class FormSubmissionStatus(str, Enum):
    """Status of form submission"""
    SUCCESS = "success"
    FAILED = "failed"
    CAPTCHA_DETECTED = "captcha_detected"
    TIMEOUT = "timeout"
    ERROR = "error"


class FormSubmissionRequest(BaseModel):
    """Request model for form submission"""
    url: HttpUrl = Field(..., description="URL of the contact form")
    message: str = Field(..., description="Message to send", min_length=1)
    use_complex_model: bool = Field(
        default=False,
        description="Use Sonnet for complex forms (default: Haiku)"
    )
    company_name: Optional[str] = Field(None, description="Override company name")
    contact_person: Optional[str] = Field(None, description="Override contact person")
    email: Optional[str] = Field(None, description="Override email")
    phone: Optional[str] = Field(None, description="Override phone")


class FormSubmissionResponse(BaseModel):
    """Response model for form submission"""
    status: FormSubmissionStatus
    url: str
    message: str
    details: Optional[str] = None
    tokens_used: Optional[int] = None
    cost_estimate: Optional[float] = None
    screenshot_path: Optional[str] = None
