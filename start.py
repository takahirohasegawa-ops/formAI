"""Start script for Railway deployment"""

import os
import uvicorn

if __name__ == "__main__":
    # Get port from environment variable (Railway provides PORT)
    port = int(os.environ.get("PORT", "8000"))
    host = os.environ.get("HOST", "0.0.0.0")

    print(f"Starting server on {host}:{port}")

    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        log_level="info"
    )
