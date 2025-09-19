import os
from groq import Groq

# Ensure your GROQ_API_KEY is set as an environment variable
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

# User's message to the chatbot
user_message = "I've been feeling really down lately, and it's hard to find motivation."

# API call to Groq
completion = client.chat.completions.create(
    # Specify the GPT-OSS 120B model
    model="openai/gpt-oss-120b",
    messages=[
        # 1. System Prompt: This is the core of the chatbot's identity.
        {
            "role": "system",
            "content": (
                "You are MindMate, a compassionate and supportive mental health chatbot. "
                "Your responses should be empathetic, non-judgmental, and encourage positive mental health practices. "
                "If the user is in crisis, provide appropriate resources and encourage them to seek professional help. "
                "If asked about your developer or creator, mention that you were developed by Tamzid Ahmed Apurbo."
            )
        },
        # 2. User Message: The input from the person seeking support.
        {
            "role": "user",
            "content": user_message
        }
    ],
    # Configuration for the model's response
    temperature=0.7,
    max_tokens=1024,
    top_p=1,
    stream=True
)

# Stream the chatbot's response to the console
print("MindMate:")
for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")
print() # Adds a newline at the end
