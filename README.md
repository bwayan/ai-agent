Project Structure
project/
├── src/
│   ├── __init__.py           # Package initializer
│   ├── config.py             # Configuration and environment variables
│   ├── models.py             # Pydantic models for data validation
│   ├── file_loader.py        # PDF and text file processing
│   ├── ai_clients.py         # OpenAI and Gemini API clients
│   ├── prompt_builder.py     # Prompt generation for AI models
│   └── ai_system.py          # Main system coordinator
├── main.py                   # Gradio application entry point
├── requirements.txt          # Python dependencies
├── app.yaml                  # Google App Engine configuration
├── deploy.sh                 # Deployment script
├── .env.template             # Environment variables template
├── .gitignore                # Git ignore rules
├── resume.pdf                # Your resume (add this file)
├── personal_info.txt         # Your personal info (add this file)
└── SETUP_INSTRUCTIONS.md     # This file
Prerequisites

Google Cloud Account with billing enabled
Google Cloud SDK installed
uv package manager
OpenAI API key
Google Gemini API key