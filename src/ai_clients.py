import openai
import google.generativeai as genai
import json
import logging
from typing import Optional
from .config import Config
from .models import ResponseQuality

logger = logging.getLogger(__name__)


class OpenAIClient:
    """Handles OpenAI API interactions"""

    def __init__(self):
        self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)

    async def get_response(self, prompt: str) -> str:
        """
        Get response from OpenAI API

        Args:
            prompt: The prompt to send to OpenAI

        Returns:
            Generated response text
        """
        try:
            response = self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=Config.MAX_TOKENS,
                temperature=Config.TEMPERATURE
            )

            content = response.choices[0].message.content
            if not content:
                raise ValueError("Empty response from OpenAI")

            return content

        except openai.RateLimitError as e:
            error_msg = "OpenAI rate limit exceeded. Please try again later."
            logger.error(f"OpenAI rate limit: {str(e)}")
            return f"Error: {error_msg}"

        except openai.AuthenticationError as e:
            error_msg = "OpenAI authentication failed. Please check API key."
            logger.error(f"OpenAI auth error: {str(e)}")
            return f"Error: {error_msg}"

        except Exception as e:
            error_msg = f"Error getting OpenAI response: {str(e)}"
            logger.error(error_msg)
            return f"Error: {error_msg}"


class GeminiClient:
    """Handles Google Gemini API interactions"""

    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)

    async def get_quality_assessment(self, prompt: str) -> ResponseQuality:
        """
        Get quality assessment from Gemini API

        Args:
            prompt: The prompt for quality assessment

        Returns:
            ResponseQuality object with assessment results
        """
        try:
            response = self.model.generate_content(prompt)

            if not response.text:
                raise ValueError("Empty response from Gemini")

            # Parse JSON response
            json_str = response.text.strip()

            # Clean up potential markdown formatting
            if json_str.startswith("```json"):
                json_str = json_str[7:-3]
            elif json_str.startswith("```"):
                json_str = json_str[3:-3]

            # Parse and validate with Pydantic
            quality_data = json.loads(json_str)
            return ResponseQuality(**quality_data)

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Gemini JSON response: {str(e)}")
            return self._default_quality_assessment(f"JSON parsing failed: {str(e)}")

        except Exception as e:
            logger.error(f"Error getting Gemini quality assessment: {str(e)}")
            return self._default_quality_assessment(f"Gemini API error: {str(e)}")

    def _default_quality_assessment(self, error_msg: str) -> ResponseQuality:
        """
        Return default quality assessment when API fails

        Args:
            error_msg: Error message to include in feedback

        Returns:
            Default ResponseQuality object
        """
        return ResponseQuality(
            is_professional=True,
            is_relevant=True,
            is_based_on_resume=True,
            confidence_score=0.8,
            feedback=f"Quality check failed: {error_msg}",
            requires_revision=False
        )