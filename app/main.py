"""FastAPI application for form submission service"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from .models import FormSubmissionRequest, FormSubmissionResponse
from .form_agent import get_form_agent
from .config import get_settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Form AI - Automated Form Submission API",
    description="Automated contact form submission using Browser Use and Claude API",
    version="0.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

settings = get_settings()


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Form AI",
        "version": "0.1.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/api/submit", response_model=FormSubmissionResponse)
async def submit_form(request: FormSubmissionRequest):
    """
    Submit a contact form

    Args:
        request: FormSubmissionRequest with URL, message, and optional overrides

    Returns:
        FormSubmissionResponse with submission status and details
    """
    try:
        logger.info(f"Submitting form to: {request.url}")

        agent = get_form_agent()

        # Submit form
        result = await agent.submit_form(
            url=str(request.url),
            message=request.message,
            use_complex_model=request.use_complex_model,
            company_name=request.company_name,
            contact_person=request.contact_person,
            email=request.email,
            phone=request.phone,
        )

        logger.info(f"Form submission result: {result.status}")

        return result

    except Exception as e:
        logger.error(f"Error submitting form: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/batch-submit")
async def batch_submit(requests: list[FormSubmissionRequest]):
    """
    Submit multiple forms in batch

    Args:
        requests: List of FormSubmissionRequest objects

    Returns:
        List of FormSubmissionResponse objects
    """
    try:
        logger.info(f"Batch submitting {len(requests)} forms")

        agent = get_form_agent()
        results = []

        for req in requests:
            result = await agent.submit_form(
                url=str(req.url),
                message=req.message,
                use_complex_model=req.use_complex_model,
                company_name=req.company_name,
                contact_person=req.contact_person,
                email=req.email,
                phone=req.phone,
            )
            results.append(result)

        logger.info(f"Batch submission completed: {len(results)} results")

        return results

    except Exception as e:
        logger.error(f"Error in batch submission: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/config")
async def get_config():
    """
    Get current configuration (without sensitive data)

    Returns:
        Configuration details
    """
    return {
        "default_model": settings.default_model,
        "complex_model": settings.complex_model,
        "company_name": settings.company_name,
        "contact_person": settings.contact_person,
        "email": settings.email,
        "phone": settings.phone,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )
