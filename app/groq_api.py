import os
import requests

# Load your Groq API key from environment variable
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
LLAMA3_MODEL = "llama3-70b-8192"

# Optionally, you can define prompt templates for mental health context
MENTAL_HEALTH_PROMPT_TEMPLATE = (
    "You are MindMate, a compassionate and supportive mental health chatbot. "
    "Your responses should be empathetic, non-judgmental, and encourage positive mental health practices. "
    "If the user is in crisis, provide appropriate resources and encourage them to seek professional help. "
    "If asked about your developer or creator, mention that you were developed by Tamzid Ahmed Apurbo.\n\n"
    "User: {user_message}\n"
    "MindMate:"
)

def get_llama3_response(user_message):
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not set in environment variables.")
    if not user_message:
        return "I'm here to listen. Please share what you're feeling."

    prompt = MENTAL_HEALTH_PROMPT_TEMPLATE.format(user_message=user_message)
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": LLAMA3_MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are MindMate, a compassionate and supportive mental health chatbot. "
                    "Your responses should be empathetic, non-judgmental, and encourage positive mental health practices. "
                    "If the user is in crisis, provide appropriate resources and encourage them to seek professional help. "
                    "If asked about your developer or creator, mention that you were developed by Tamzid Ahmed Apurbo."
                )
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        "max_tokens": 1024,
        "temperature": 0.7
    }
    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=data)
        response.raise_for_status()
        resp_json = response.json()
        return resp_json["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return "Sorry, I'm having trouble connecting to my mental health support resources right now. Please try again later."

def get_llama3_response_context(user_message, history=None):
    """
    Sends user_message along with previous history to Groq's Llama-3 for context-aware response.
    history: list of dicts [{"role": "user", "content": "..."}, {"role": "bot", "content": "..."}]
    """
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not set in environment variables.")
    if not history:
        history = []
    messages = [{
        "role": "system",
        "content": (
            "You are MindMate, a compassionate and supportive mental health chatbot. "
            "Use the conversation history below to understand context and respond empathetically. "
            "Your responses should encourage positive mental health practices. "
            "If the user is in crisis, provide appropriate resources and encourage them to seek professional help. "
            "If asked about your developer or creator, mention that you were developed by Tamzid Ahmed Apurbo."
        )
    }]
    # Add history
    for turn in history:
        role = "user" if turn["role"] == "user" else "assistant"
        messages.append({"role": role, "content": turn["content"]})
    messages.append({"role": "user", "content": user_message})

    data = {
        "model": LLAMA3_MODEL,
        "messages": messages,
        "max_tokens": 1024,
        "temperature": 0.7
    }
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=data)
        response.raise_for_status()
        resp_json = response.json()
        return resp_json["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return "Sorry, I'm unable to provide a response right now. Please try again later."
