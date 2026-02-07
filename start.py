"""Start script for Railway deployment"""

import os
import uvicorn

if __name__ == "__main__":
    # Get port from environment variable (Railway provides PORT)
    port = int(os.environ.get("PORT", "8000"))
    host = os.environ.get("HOST", "0.0.0.0")

    # Debug: Check if GOOGLE_API_KEY is set
    api_key = os.environ.get("GOOGLE_API_KEY")
    if api_key:
        print(f"✅ GOOGLE_API_KEY is set (length: {len(api_key)})")
    else:
        print("❌ WARNING: GOOGLE_API_KEY is NOT set!")
        print("Available environment variables:")
        for key in sorted(os.environ.keys()):
            if 'API' in key or 'GOOGLE' in key or 'KEY' in key:
                print(f"  - {key}")

    print(f"Starting server on {host}:{port}")

    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        log_level="info"
    )
