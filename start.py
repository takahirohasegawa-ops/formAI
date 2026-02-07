"""Start script for Railway deployment"""

import os
import sys
import uvicorn

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Starting Form AI Server")
    print("=" * 60)

    # Debug: Print Python version and path
    print(f"\n🐍 Python Version: {sys.version}")
    print(f"📁 Working Directory: {os.getcwd()}")
    print(f"📁 Python Path: {sys.executable}")

    # Get port from environment variable (Railway provides PORT)
    port = int(os.environ.get("PORT", "8000"))
    host = os.environ.get("HOST", "0.0.0.0")

    # Debug: Dump ALL environment variables
    print("\n🔍 ALL Environment Variables:")
    print("-" * 60)
    for key, value in sorted(os.environ.items()):
        # Mask sensitive values
        if any(keyword in key.upper() for keyword in ['KEY', 'SECRET', 'PASSWORD', 'TOKEN']):
            print(f"  {key} = ***{value[-4:] if len(value) > 4 else '****'}")
        else:
            print(f"  {key} = {value}")
    print("-" * 60)

    # Debug: Check ALL environment variables
    print("\n📋 Environment Variables Check:")
    print("-" * 60)

    required_vars = [
        "GOOGLE_API_KEY",
        "DEFAULT_MODEL",
        "COMPANY_NAME",
        "CONTACT_PERSON",
        "EMAIL",
        "PHONE"
    ]

    all_set = True
    for var in required_vars:
        value = os.environ.get(var)
        if value:
            # Hide sensitive data
            if "KEY" in var or "API" in var:
                print(f"✅ {var}: ***{value[-4:]} (length: {len(value)})")
            else:
                print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: NOT SET")
            all_set = False

    print("-" * 60)
    print(f"\n🌐 Server Configuration:")
    print(f"   Host: {host}")
    print(f"   Port: {port}")
    print("=" * 60)

    if not all_set:
        print("\n⚠️  WARNING: Some required environment variables are missing!")
        print("The application may not work correctly.\n")

    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        log_level="info"
    )
