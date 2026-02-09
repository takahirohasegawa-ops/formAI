"""Patch browser-use to force headless mode"""

import os
import sys

def patch_browser_use():
    """Patch browser-use library to force headless browser"""
    try:
        # Find browser-use installation
        import browser_use
        browser_use_path = os.path.dirname(browser_use.__file__)

        # Patch browser.py
        browser_py = os.path.join(browser_use_path, 'browser', 'browser.py')

        if os.path.exists(browser_py):
            with open(browser_py, 'r') as f:
                content = f.read()

            # Check if already patched
            if 'PATCHED_FOR_HEADLESS' not in content:
                # Find launch call and add headless=True
                original = 'await self.playwright.chromium.launch('
                if original in content:
                    # Add marker and force headless
                    patched = f'# PATCHED_FOR_HEADLESS\n        await self.playwright.chromium.launch(headless=True, '
                    content = content.replace(original, patched)

                    with open(browser_py, 'w') as f:
                        f.write(content)

                    print(f"✅ Patched {browser_py} to force headless mode")
                    return True
                else:
                    print(f"⚠️  Could not find launch call in {browser_py}")
            else:
                print(f"✅ {browser_py} already patched")
                return True
        else:
            print(f"❌ {browser_py} not found")

    except Exception as e:
        print(f"❌ Error patching browser-use: {e}")
        import traceback
        traceback.print_exc()

    return False

if __name__ == "__main__":
    patch_browser_use()
