"""Patch browser-use to force headless mode"""

import os
import sys

def patch_browser_use():
    """Patch browser-use library to force headless browser"""
    try:
        # Find browser-use installation
        import browser_use
        browser_use_path = os.path.dirname(browser_use.__file__)

        # Patch service.py (the actual file that launches the browser)
        service_py = os.path.join(browser_use_path, 'browser', 'service.py')

        if os.path.exists(service_py):
            with open(service_py, 'r') as f:
                content = f.read()

            # Check if already patched
            if 'headless=True,' in content or 'headless = True' in content:
                print(f"✅ {service_py} already patched (headless=True found)")
                return True

            # Replace headless parameter value
            if 'headless=self.headless' in content:
                # Replace headless=self.headless with headless=True
                content = content.replace('headless=self.headless', 'headless=True')

                with open(service_py, 'w') as f:
                    f.write(content)

                print(f"✅ Patched {service_py} to force headless mode (replaced headless parameter)")
                return True
            elif 'headless=' in content:
                print(f"⚠️  Found 'headless=' but not 'headless=self.headless'")
                print(f"Content preview: {content[:500]}")
            else:
                print(f"⚠️  Could not find headless parameter in {service_py}")
                print(f"Content preview: {content[:500]}")
            else:
                print(f"✅ {service_py} already patched (headless=True found)")
                return True
        else:
            print(f"❌ {service_py} not found")

    except Exception as e:
        print(f"❌ Error patching browser-use: {e}")
        import traceback
        traceback.print_exc()

    return False

if __name__ == "__main__":
    patch_browser_use()
