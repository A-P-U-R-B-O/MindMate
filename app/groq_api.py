import os
from groq import Groq

# It's a best practice to get your API key from an environment variable
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

def get_gpt_oss_response(user_message):
    """
    Sends a user message to the GPT-OSS 120B model on Groq and returns the response.
    """
    # The system prompt that gives the chatbot its personality
    system_prompt = (
        "You are MindMate, a compassionate and supportive mental health chatbot. "
        "Your responses should be empathetic, non-judgmental, and encourage positive mental health practices. "
        "If the user is in crisis, provide appropriate resources and encourage them to seek professional help. "
        "If asked about your developer or creator, mention that you were developed by Tamzid Ahmed Apurbo."
    )

    try:
        # Make the API call
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            stream=False # We want the full response back at once for the Flask app
        )
        
        # Return the content of the first message in the completion
        return completion.choices[0].message.content.strip()

    except Exception as e:
        print(f"Error calling Groq API: {e}")
        return "Sorry, I'm unable to provide a response right now. Please try again later."
