from pydantic import BaseModel, Field
from typing import List, Optional, Tuple


class ResponseQuality(BaseModel):
    """Pydantic model for validating response quality from Gemini"""
    is_professional: bool = Field(description="Whether the response is professional")
    is_relevant: bool = Field(description="Whether the response is relevant to the query")
    is_based_on_resume: bool = Field(description="Whether the response is based on resume data")
    confidence_score: float = Field(description="Confidence score 0-1", ge=0.0, le=1.0)
    feedback: str = Field(description="Feedback for improvement")
    requires_revision: bool = Field(description="Whether response needs revision")


class ConversationHistory(BaseModel):
    """Model for storing conversation history"""
    exchanges: List[Tuple[str, str]] = Field(default_factory=list,
                                             description="List of (user_message, assistant_response) tuples")
    interaction_count: int = Field(default=0, description="Total number of interactions")

    def add_exchange(self, user_message: str, assistant_response: str):
        """Add a new exchange to the history"""
        self.exchanges.append((user_message, assistant_response))
        self.interaction_count += 1

    def get_recent_history(self, limit: int = 5) -> str:
        """Get formatted recent conversation history"""
        if not self.exchanges:
            return "No previous conversation."

        history = ""
        recent_exchanges = self.exchanges[-limit:]

        for i, (user_msg, assistant_msg) in enumerate(recent_exchanges, 1):
            history += f"Exchange {i}:\nUser: {user_msg}\nBrian: {assistant_msg}\n\n"

        return history

    def clear(self):
        """Clear conversation history"""
        self.exchanges.clear()
        self.interaction_count = 0


class ProcessingResult(BaseModel):
    """Model for processing results"""
    final_response: str = Field(description="Final response to user")
    debug_info: str = Field(description="Debug information")
    quality_score: float = Field(description="Quality assessment score")
    was_revised: bool = Field(description="Whether response was revised")
    linkedin_suggested: bool = Field(description="Whether LinkedIn was suggested")