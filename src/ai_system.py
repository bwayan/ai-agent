import logging
from typing import Tuple
from .config import Config
from .models import ConversationHistory, ProcessingResult
from .file_loader import FileLoader
from .ai_clients import OpenAIClient, GeminiClient
from .prompt_builder import PromptBuilder

logger = logging.getLogger(__name__)


class AIAgentSystem:
    """Main AI agent system coordinating all components"""

    def __init__(self):
        # Validate configuration
        Config.validate_config()

        # Initialize AI clients
        self.openai_client = OpenAIClient()
        self.gemini_client = GeminiClient()

        # Load content
        self.resume_content = FileLoader.load_pdf_content(Config.PDF_PATH)
        self.personal_info = FileLoader.load_txt_content(Config.TXT_PATH)

        # Validate loaded content
        if not FileLoader.validate_content(self.resume_content, self.personal_info):
            raise ValueError("Invalid content loaded from files")

        # Initialize conversation tracking
        self.conversation_history = ConversationHistory()

        logger.info("AI Agent System initialized successfully")

    def _should_suggest_linkedin(self) -> bool:
        """Determine if LinkedIn should be suggested based on interaction count"""
        return self.conversation_history.interaction_count >= Config.LINKEDIN_THRESHOLD

    def _add_linkedin_suggestion(self, response: str) -> str:
        """Add LinkedIn connection suggestion to response"""
        linkedin_msg = ("\n\nI'd be happy to connect with you on LinkedIn for further "
                        "discussion about potential opportunities: "
                        "https://www.linkedin.com/in/brian-veau")
        return response + linkedin_msg

    async def process_query(self, user_query: str) -> Tuple[str, str]:
        """
        Main processing function for user queries

        Args:
            user_query: User's question or message

        Returns:
            Tuple of (final_response, debug_info)
        """
        try:
            # Check if LinkedIn should be suggested
            suggest_linkedin = self._should_suggest_linkedin()

            # Create Brian's prompt
            brian_prompt = PromptBuilder.create_brian_prompt(
                user_query=user_query,
                resume_content=self.resume_content,
                personal_info=self.personal_info,
                conversation_history=self.conversation_history,
                suggest_linkedin=suggest_linkedin
            )

            # Get initial response from OpenAI
            initial_response = await self.openai_client.get_response(brian_prompt)

            # Handle API errors
            if initial_response.startswith("Error:"):
                self.conversation_history.add_exchange(user_query, initial_response)
                return initial_response, "OpenAI API Error"

            # Quality check with Gemini
            quality_prompt = PromptBuilder.create_quality_check_prompt(
                user_query=user_query,
                brian_response=initial_response,
                resume_content=self.resume_content,
                personal_info=self.personal_info
            )

            quality_assessment = await self.gemini_client.get_quality_assessment(quality_prompt)

            final_response = initial_response
            revision_info = ""

            # If revision needed, get improved response
            if quality_assessment.requires_revision:
                revision_prompt = PromptBuilder.create_revision_prompt(
                    original_prompt=brian_prompt,
                    initial_response=initial_response,
                    quality_feedback=quality_assessment.feedback
                )

                revised_response = await self.openai_client.get_response(revision_prompt)

                # Use revised response if it's valid
                if not revised_response.startswith("Error:"):
                    final_response = revised_response
                    revision_info = f"(Revised: {quality_assessment.feedback})"

            # Add LinkedIn suggestion if appropriate and not already included
            linkedin_suggested = False
            if suggest_linkedin and "linkedin.com/in/brian-veau" not in final_response.lower():
                final_response = self._add_linkedin_suggestion(final_response)
                linkedin_suggested = True

            # Update conversation history
            self.conversation_history.add_exchange(user_query, final_response)

            # Prepare debug information
            debug_info = self._create_debug_info(
                quality_assessment=quality_assessment,
                revision_info=revision_info,
                linkedin_suggested=linkedin_suggested
            )

            logger.info(f"Query processed successfully. Quality score: {quality_assessment.confidence_score}")

            return final_response, debug_info

        except Exception as e:
            error_msg = f"I apologize, but I'm experiencing technical difficulties. Please try again."
            logger.error(f"Error processing query: {str(e)}")

            # Still update conversation history for context
            self.conversation_history.add_exchange(user_query, error_msg)

            return error_msg, f"System Error: {str(e)}"

    def _create_debug_info(self, quality_assessment, revision_info: str, linkedin_suggested: bool) -> str:
        """Create debug information string"""
        return f"""
Quality Score: {quality_assessment.confidence_score:.2f}
Professional: {quality_assessment.is_professional}
Relevant: {quality_assessment.is_relevant}
Based on Resume: {quality_assessment.is_based_on_resume}
{revision_info}
Interaction Count: {self.conversation_history.interaction_count}
LinkedIn Suggested: {linkedin_suggested}
"""

    def reset_conversation(self):
        """Reset conversation history"""
        self.conversation_history.clear()
        logger.info("Conversation history reset")

    def get_conversation_stats(self) -> dict:
        """Get conversation statistics"""
        return {
            "total_interactions": self.conversation_history.interaction_count,
            "exchanges": len(self.conversation_history.exchanges),
            "linkedin_threshold": Config.LINKEDIN_THRESHOLD
        }