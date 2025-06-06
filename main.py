import gradio as gr
import asyncio
from src.ai_system import AIAgentSystem

# Initialize the AI system
ai_system = AIAgentSystem()


async def chat_interface(message, history):
    """Gradio chat interface function"""
    if not message.strip():
        return "", history + [{"role": "assistant", "content": "Please enter a message."}]

    response, debug = await ai_system.process_query(message)

    # Update history with new message format
    new_history = history + [
        {"role": "user", "content": message},
        {"role": "assistant", "content": response}
    ]

    return "", new_history


# Create Gradio interface
with gr.Blocks(
        title="Brian VEAU - CIO/CTO Professional Assistant",
        theme=gr.themes.Soft(),
        css="""
    .gradio-container {
        max-width: 800px !important;
        margin: auto !important;
    }
    .chatbot {
        height: 600px !important;
    }
    """
) as demo:
    gr.Markdown("""
    # 🤖 Brian VEAU - Professional AI Assistant

    Hello! I'm an AI assistant representing **Brian VEAU**, Global CIO and Vice President of IT.

    I can answer questions about Brian's:
    - Professional experience and achievements
    - Technical skills and expertise  
    - Leadership background
    - Career progression
    - Availability for CIO/CTO positions

    *This assistant is designed for recruiters and hiring managers interested in senior IT leadership roles.*
    """)

    chatbot = gr.Chatbot(
        value=[],
        label="Chat with Brian's AI Assistant",
        height=600,
        show_label=True,
        container=True,
        type="messages"
    )

    msg = gr.Textbox(
        placeholder="Ask about Brian's experience, skills, or career objectives...",
        label="Your Message",
        lines=2,
        max_lines=5
    )

    clear = gr.Button("Clear Conversation")

    # Event handlers
    msg.submit(
        chat_interface,
        inputs=[msg, chatbot],
        outputs=[msg, chatbot]
    )

    clear.click(
        lambda: [],
        outputs=[chatbot]
    )

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=8080,
        share=False,
        debug=False
    )