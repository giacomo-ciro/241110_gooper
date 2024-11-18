import requests

instructions = """You are a social media analyst.
Your task is to generate a concise, professional summary of an influencer's Instagram profile based on its publicly available information.

Guidelines for the Summary:
- Tone: Informative and professional.
- Content: Highlight the profile's main themes, the type of content posted, audience engagement style, and any notable achievements or unique features.
- Length: Approximately 7-8 sentences (200-250 words).
- Example Structure: Start with the profile's focus (e.g., \"This profile showcases...\"), describe the content's themes (e.g., \"primarily featuring ...\"), and mention any distinguishing features (e.g., \"known for...\").  
"""

def together_request(user_message, api_key = None):

    if not api_key:
        return "Please add your Together.ai API key to continue."

    url = "https://api.together.xyz/v1/chat/completions"

    payload = {
        "model": "meta-llama/Llama-3.2-3B-Instruct-Turbo",
        "messages": [
            {
                "role": "system",
                "content": f"{instructions}"
            },
            {
                "role": "user",
                "content": f"{user_message}"
            }
        ],
        "max_tokens": 512,
        "temperature": 0.7,
        "top_p": 0.7,
        "top_k": 50,
        "repetition_penalty": 1,
        "stream": False
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {api_key}"
    }

    response = requests.post(url, json=payload, headers=headers)

    content = response.json()['choices'][0]['message']['content'].replace('. ', '.\n')
    return content