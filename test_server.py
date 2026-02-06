"""
Simplified test server without browser-use
Python 3.9+ compatible
"""

from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI(
    title="Form AI - Test Server",
    description="Simplified test server (browser-use disabled)",
    version="0.1.0-test"
)


class FormSubmissionRequest(BaseModel):
    url: HttpUrl
    message: str
    use_complex_model: bool = False


@app.get("/")
async def root():
    return {
        "service": "Form AI - Test Server",
        "version": "0.1.0-test",
        "status": "running",
        "note": "Browser automation disabled - API test only",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/api/submit")
async def submit_form(request: FormSubmissionRequest):
    """Test endpoint - returns mock response"""
    return {
        "status": "success",
        "url": str(request.url),
        "message": f"Test mode: Would submit to {request.url}",
        "details": "これはテストモードです。実際の送信にはPython 3.11+が必要です。",
        "tokens_used": 0,
        "cost_estimate": 0.0,
        "note": "Python 3.11+ required for actual form submission"
    }


@app.get("/api/config")
async def get_config():
    return {
        "default_model": "gemini-1.5-flash",
        "complex_model": "gemini-1.5-pro",
        "company_name": "RECHANCE株式会社",
        "contact_person": "桑原麻由",
        "email": "info@rechance.jp",
        "phone": "090-1234-7891",
        "mode": "test"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
