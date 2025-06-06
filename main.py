import gradio as gr
import asyncio
from src.ai_system import AIAgentSystem

# Initialize the AI system
ai_system = AIAgentSystem()


async def chat_function(message, history):
    """Chat function for gr.ChatInterface"""
    if not message.strip():
        return "Please enter a message."

    response, debug = await ai_system.process_query(message)
    return response


# Create ChatInterface
demo = gr.ChatInterface(
    fn=chat_function,
    type="messages",
    title="🤖 Brian VEAU - Professional AI Assistant",
    description="""
Hello! I'm an AI assistant representing **Brian VEAU**, Global CIO and Vice President of IT.

I can answer questions about Brian's:
- Professional experience and achievements
- Technical skills and expertise  
- Leadership background
- Career progression
- Availability for CIO/CTO positions

*This assistant is designed for recruiters and hiring managers interested in senior IT leadership roles.*
    """,
    theme=gr.themes.Soft(),
    css="""
    .gradio-container {
        max-width: 800px !important;
        margin: auto !important;
    }
    """,
    chatbot=gr.Chatbot(height=400, type="messages"),
    textbox=gr.Textbox(
        placeholder="Ask about Brian's experience, skills, or career objectives...",
        container=False,
        scale=7
    ),
    submit_btn="Send",
    clear_btn="🗑️ Clear"
)

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=8080,
        share=False,
        debug=False
    )