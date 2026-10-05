"""
llm/model.py — LLM Configuration and Initialization

This file will configure and expose the language model (LLM) used
by the application for all AI-powered analysis tasks.

Responsibilities:
    - Load API keys and model settings from environment variables.
    - Initialize and configure the chosen LLM (model not yet selected).
    - Expose the configured LLM instance for use by workflow nodes.

Do not choose, initialize, or configure a model here yet —
it will be set up manually.
"""
from langchain_groq import ChatGroq

model= ChatGroq(
    model= "openai/gpt-oss-120b",
    temperature=0.9
)
