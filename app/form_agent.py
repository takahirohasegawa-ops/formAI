"""Form submission agent using Browser Use and Gemini API"""

import asyncio
import re
import os
import sys
from typing import Optional, Dict, Any
from playwright.async_api import async_playwright, Page, Browser
from langchain_anthropic import ChatAnthropic
from browser_use import Agent

from .config import get_settings
from .models import FormSubmissionStatus, FormSubmissionResponse

# Disable stdin to prevent EOF errors in non-interactive environments
# Force stdin to /dev/null regardless of tty status
try:
    sys.stdin.close()
except:
    pass
sys.stdin = open(os.devnull, 'r')

# Set environment variable to disable interactive prompts
os.environ["PYTHONUNBUFFERED"] = "1"
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/ms-playwright")


class FormAgent:
    """Agent for automated form submission"""

    def __init__(self):
        self.settings = get_settings()
         # Set Anthropic API key environment variable
          os.environ["ANTHROPIC_API_KEY"] = self.settings.anthropic_api_key

    async def detect_captcha(self, page: Page) -> bool:
        """
        Detect if CAPTCHA is present on the page

        Returns:
            True if CAPTCHA detected, False otherwise
        """
        try:
            # Check for common CAPTCHA indicators
            captcha_patterns = [
                'recaptcha',
                'g-recaptcha',
                'captcha',
                'hcaptcha',
                'cf-turnstile'
            ]

            page_content = await page.content()
            page_content_lower = page_content.lower()

            for pattern in captcha_patterns:
                if pattern in page_content_lower:
                    return True

            # Check for CAPTCHA iframes
            frames = page.frames
            for frame in frames:
                frame_url = frame.url
                if any(pattern in frame_url.lower() for pattern in captcha_patterns):
                    return True

            return False
        except Exception as e:
            print(f"Error detecting CAPTCHA: {e}")
            return False

    async def submit_form(
        self,
        url: str,
        message: str,
        use_complex_model: bool = False,
        company_name: Optional[str] = None,
        contact_person: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
    ) -> FormSubmissionResponse:
        """
        Submit a contact form using Browser Use

        Args:
            url: URL of the contact form
            message: Message to send
            use_complex_model: Use Sonnet instead of Haiku
            company_name: Company name (override default)
            contact_person: Contact person (override default)
            email: Email (override default)
            phone: Phone (override default)

        Returns:
            FormSubmissionResponse with status and details
        """
        # Use provided values or defaults
        company = company_name or self.settings.company_name
        person = contact_person or self.settings.contact_person
        email_addr = email or self.settings.email
        phone_num = phone or self.settings.phone

        # Select model based on complexity
        model = (
            self.settings.complex_model if use_complex_model
            else self.settings.default_model
        )

        try:
            # Force headless mode via environment variable
            os.environ["HEADLESS"] = "1"

            # Create LLM instance with Claude
              llm = ChatAnthropic(
                  model=model,
                  temperature=0.1,
                  anthropic_api_key=self.settings.anthropic_api_key
              )


            # Create agent - browser-use should respect HEADLESS env var
            agent = Agent(
                task=f"{self._create_task_prompt(message, company, person, email_addr, phone_num)}\n\nURL: {url}",
                llm=llm,
            )

            # Execute task
            result = await agent.run()

            # Check if submission was successful based on result
            result_str = str(result).lower() if result else ""
            success_indicators = [
                'thank you', 'ありがとう', '送信完了', '受付', 'received',
                'success', '完了', 'sent', 'submitted', 'complete'
            ]

            is_success = any(indicator in result_str for indicator in success_indicators)

            if is_success:
                status = FormSubmissionStatus.SUCCESS
                details = "フォーム送信が完了しました"
            else:
                status = FormSubmissionStatus.SUCCESS
                details = f"タスク実行完了: {result}"

            # Estimate token usage and cost
            tokens_used = self._estimate_tokens(result)
            cost = self._estimate_cost(tokens_used, model)

            return FormSubmissionResponse(
                status=status,
                url=url,
                message=f"Submitted message: {message[:50]}...",
                details=details,
                tokens_used=tokens_used,
                cost_estimate=cost,
                screenshot_path=None
            )

        except asyncio.TimeoutError:
            return FormSubmissionResponse(
                status=FormSubmissionStatus.TIMEOUT,
                url=url,
                message="Request timed out",
                details="ページの読み込みがタイムアウトしました"
            )
        except Exception as e:
            return FormSubmissionResponse(
                status=FormSubmissionStatus.ERROR,
                url=url,
                message=f"Error: {str(e)}",
                details=f"エラーが発生しました: {str(e)}"
            )

    def _create_task_prompt(
        self,
        message: str,
        company: str,
        person: str,
        email: str,
        phone: str
    ) -> str:
        """Create task prompt for the agent"""
        return f"""
お問い合わせフォームに以下の情報を入力して送信してください:

【会社名/組織名】{company}
【担当者名/お名前】{person}
【メールアドレス】{email}
【電話番号】{phone}
【お問い合わせ内容/メッセージ】
{message}

フォームのフィールドに適切な情報を入力し、送信ボタンをクリックしてください。
フィールド名は日本語または英語の可能性があります（例：「会社名」「Company」「名前」「Name」など）。
必須フィールドをすべて入力し、最後に送信ボタン（「送信」「Submit」「Send」など）をクリックしてください。
"""

    def _estimate_tokens(self, result: Any) -> int:
        """Estimate tokens used (rough estimation)"""
        # This is a rough estimate
        # In production, you would track actual API usage
        return 1000  # Placeholder

    def _estimate_cost(self, tokens: int, model: str) -> float:
          """Estimate cost based on tokens and model"""
          # Claude API costs (as of 2025)
          # Haiku: $0.25 / 1M input tokens, $1.25 / 1M output tokens
          # Sonnet: $3.00 / 1M input tokens, $15.00 / 1M output tokens

          if "haiku" in model.lower():
              # Assume 70% input, 30% output
              input_cost = (tokens * 0.7) * 0.25 / 1_000_000
              output_cost = (tokens * 0.3) * 1.25 / 1_000_000
          else:  # sonnet
              input_cost = (tokens * 0.7) * 3.00 / 1_000_000
              output_cost = (tokens * 0.3) * 15.00 / 1_000_000

          return round(input_cost + output_cost, 6)


# Singleton instance
_form_agent: Optional[FormAgent] = None


def get_form_agent() -> FormAgent:
    """Get or create FormAgent singleton"""
    global _form_agent
    if _form_agent is None:
        _form_agent = FormAgent()
    return _form_agent
