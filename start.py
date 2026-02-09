"""Start script for Railway deployment"""

import os
import sys
import builtins
import uvicorn

# Monkey-patch input() to prevent EOF errors in non-interactive environments
def _dummy_input(prompt=""):
    """Dummy input function that returns empty string instead of reading stdin"""
    print(f"[WARNING] input() called with prompt: {prompt}")
    return ""

builtins.input = _dummy_input

# Disable stdin immediately to prevent EOF errors
try:
    sys.stdin.close()
except:
    pass
sys.stdin = open(os.devnull, 'r')

# Set environment variables to disable interactive prompts
os.environ["PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD"] = "0"
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/ms-playwright")

# Force headless mode for browser-use
os.environ["HEADLESS"] = "true"
os.environ["BROWSER_HEADLESS"] = "true"

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
