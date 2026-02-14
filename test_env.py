"""Test environment variables"""

import os
import sys

print("=" * 80)
print("TEST: Environment Variables Check")
print("=" * 80)

print(f"\nPython: {sys.version}")
print(f"CWD: {os.getcwd()}")

print("\n" + "=" * 80)
print("ALL ENVIRONMENT VARIABLES:")
print("=" * 80)

for key in sorted(os.environ.keys()):
    value = os.environ[key]
    if any(x in key.upper() for x in ['KEY', 'SECRET', 'PASSWORD', 'TOKEN']):
        print(f"{key:30} = ***{value[-4:] if len(value) > 4 else '****'}")
    else:
        # Truncate long values
        if len(value) > 100:
            print(f"{key:30} = {value[:100]}...")
        else:
            print(f"{key:30} = {value}")

print("=" * 80)

# Check specific variables
print("\nSPECIFIC VARIABLES CHECK:")
print("=" * 80)

required_vars = [
    "ANTHROPIC_API_KEY",
    "DEFAULT_MODEL",
    "COMPANY_NAME",
    "CONTACT_PERSON",
    "EMAIL",
    "PHONE",
    "PORT",
]

for var in required_vars:
    value = os.environ.get(var)
    if value:
        if 'KEY' in var:
            print(f"✅ {var:20} = ***{value[-4:]}")
        else:
            print(f"✅ {var:20} = {value}")
    else:
        print(f"❌ {var:20} = NOT SET")

print("=" * 80)
print("Test complete. Starting server...")
print("=" * 80)
