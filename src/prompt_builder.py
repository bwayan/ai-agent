from typing import Optional
from .models import ConversationHistory


class PromptBuilder:
    """Builds prompts for AI interactions"""

    @staticmethod
    def create_brian_prompt(
            user_query: str,
            resume_content: str,
            personal_info: str,
            conversation_history: ConversationHistory,
            suggest_linkedin: bool = False
    ) -> str:
        """
        Create the prompt for OpenAI to act as Brian

        Args:
            user_query: User's question
            resume_content: Content from resume PDF
            personal_info: Personal information from text file
            conversation_history: Previous conversation exchanges
            suggest_linkedin: Whether to suggest LinkedIn connection

        Returns:
            Formatted prompt string
        """
        linkedin_instruction = ""
        if suggest_linkedin:
            linkedin_instruction = "\nIMPORTANT: At the end of your response, suggest connecting on LinkedIn for further discussion."

        return f"""
You are Brian VEAU, a Global CIO and Vice President of IT currently working at ShawKwei & Partners. You are responding to professional inquiries from recruiters and potential employers interested in CIO or CTO positions.

STRICT GUIDELINES:
- Only answer professional questions related to your career, experience, skills, and achievements
- Base ALL responses ONLY on the information provided in your resume and personal details
- Do NOT invent or extrapolate information not present in your documents
- If asked about something not in your resume, politely redirect to what IS in your resume
- Maintain a professional, confident, and engaging tone
- Keep responses concise but informative (max 3-4 paragraphs)
- Do NOT discuss personal topics unrelated to professional qualifications
- Focus on leadership achievements, technical expertise, and business impact{linkedin_instruction}

RESUME CONTENT:
{resume_content}

PERSONAL INFORMATION:
{personal_info}

CONVERSATION HISTORY:
{conversation_history.get_recent_history()}

USER QUERY: {user_query}

Respond as Brian VEAU would, focusing only on professional matters and information contained in the provided documents.
"""

    @staticmethod
    def create_quality_check_prompt(
            user_query: str,
            brian_response: str,
            resume_content: str,
            personal_info: str
    ) -> str:
        """
        Create prompt for Gemini quality control

        Args:
            user_query: Original user question
            brian_response: Brian's response to evaluate
            resume_content: Resume content for reference (truncated)
            personal_info: Personal information for reference

        Returns:
            Formatted quality check prompt
        """
        # Truncate resume content to avoid token limits
        truncated_resume = resume_content[:1500] + "..." if len(resume_content) > 1500 else resume_content

        return f"""
Evaluate this response from an AI agent acting as Brian VEAU (CIO/CTO professional) responding to a recruiter query.

EVALUATION CRITERIA:
1. Professional tone and appropriateness for recruiter audience
2. Relevance to the user's query
3. Based solely on resume/personal information provided (no invented facts)
4. Accuracy and consistency with source material
5. Appropriate length and engagement level
6. Maintains focus on professional qualifications only

USER QUERY: {user_query}

BRIAN'S RESPONSE: {brian_response}

RESUME REFERENCE MATERIAL:
{truncated_resume}

PERSONAL INFO REFERENCE:
{personal_info}

SPECIFIC ISSUES TO CHECK:
- Does the response invent any facts not in the source materials?
- Is the tone appropriate for a senior executive speaking to recruiters?
- Does it stay focused on professional topics only?
- Is the response length appropriate (not too brief, not too verbose)?
- Does it adequately address the user's specific question?

Provide evaluation in this exact JSON format (no additional text):
{{
    "is_professional": true/false,
    "is_relevant": true/false,
    "is_based_on_resume": true/false,
    "confidence_score": 0.0-1.0,
    "feedback": "specific feedback for improvement",
    "requires_revision": true/false
}}
"""

    @staticmethod
    def create_revision_prompt(
            original_prompt: str,
            initial_response: str,
            quality_feedback: str
    ) -> str:
        """
        Create prompt for response revision

        Args:
            original_prompt: The original Brian prompt
            initial_response: The initial response that needs revision
            quality_feedback: Feedback from quality assessment

        Returns:
            Revision prompt
        """
        return f"""
{original_prompt}

PREVIOUS RESPONSE: {initial_response}

QUALITY FEEDBACK: {quality_feedback}

Please provide an improved response addressing the feedback while maintaining your role as Brian VEAU. Focus on:
- Addressing the specific issues mentioned in the feedback
- Maintaining professional tone and accuracy
- Staying within the bounds of information provided in your resume and personal details
- Keeping the response appropriately concise and engaging
"""