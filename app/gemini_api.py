import google.generativeai as genai
import os

# Load your Gemini API key from environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API client
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    raise ValueError("GEMINI_API_KEY not set in environment variables.")

# Optionally, you can define prompt templates for mental health context
MENTAL_HEALTH_PROMPT_TEMPLATE = (
    "You are a compassionate and supportive mental health chatbot. "
    "Your responses should be empathetic, non-judgmental, and encourage positive mental health practices. "
    "If the user is in crisis, provide appropriate resources and encourage them to seek professional help.\n\n"
    "User: {user_message}\n"
    "Chatbot:"
)

# Main function to get response from Gemini API
def get_gemini_response(user_message):
    if not user_message:
        return "I'm here to listen. Please share what you're feeling."

    prompt = MENTAL_HEALTH_PROMPT_TEMPLATE.format(user_message=user_message)
    try:
        # Using Gemini's text generation endpoint (modify as needed for your Gemini version)
        response = genai.generate_content(prompt)
        # If the response is an object, extract the text
        if isinstance(response, dict) and "text" in response:
            return response["text"]
        elif hasattr(response, "text"):
            return response.text
        else:
            return str(response)
    except Exception as e:
        # Log error as needed
        return "Sorry, I'm having trouble connecting to my mental health support resources right now. Please try again later."

# Optionally, you can add more advanced functions for contextual or multi-turn conversations
def get_gemini_response_context(user_message, history=None):
    """
    Sends user_message along with previous history to Gemini for context-aware response.
    history: list of dicts [{"role": "user", "content": "..."}, {"role": "bot", "content": "..."}]
    """
    if not history:
        history = []
    # Build a conversation prompt
    conversation = ""
    for turn in history:
        if turn["role"] == "user":
            conversation += f"User: {turn['content']}\n"
        else:
            conversation += f"Chatbot: {turn['content']}\n"
    conversation += f"User: {user_message}\nChatbot:"
    prompt = (
        "You are a compassionate mental health chatbot. Use the conversation history below to understand context and respond empathetically.\n\n"
        f"{conversation}"
    )
    try:
        response = genai.generate_content(prompt)
        if isinstance(response, dict) and "text" in response:
            return response["text"]
        elif hasattr(response, "text"):
            return response.text
        else:
            return str(response)
    except Exception as e:
        return "Sorry, I'm unable to provide a response right now. Please try again later."
