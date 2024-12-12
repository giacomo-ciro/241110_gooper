from together import Together
import numpy as np
from supabase import create_client

# TOGETHER_API_KEY = "5a532872525382e32ebc396c6cc682d3b8d8d5ea428ef9468404286bb1417f2c"
# client = Together(api_key = TOGETHER_API_KEY)

url = "https://edcqmzluacqdqqmmklik.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVkY3Ftemx1YWNxZHFxbW1rbGlrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzQwMTM1MDgsImV4cCI6MjA0OTU4OTUwOH0.Po1jIO14A6mCuN1xo-K6ikpKR1XlGt4_ivoYVX2raSU"
supabase = create_client(url, key)


def retrieve(client,
             query,
             ):
    """Retrieve the most appropriate influencer's description from the influencer database using Together API to embed the query.

    Args:
        client: Together. The Together client.
        query: str. The query to embed and retrieve the most appropriate influencer's description.

    Returns:
        str: The retrieved text.
    """

    model = "BAAI/bge-base-en-v1.5"

    out = client.embeddings.create(
        input=query,
        model=model,
    )

    query = out.data[0].embedding

    response = supabase.rpc("get_similar_items",{
        "query_embedding": query,
        "result_limit": 1
    }).execute()
    
    return response.data[0]['description']

def generate(client,
             TASK_TYPE=None,        
             userPrompt=None,
             imageUrl=None
             ):
    """Generate text using the Together API.

    Args:
        TASK_TYPE: str. The type of task to generate text for. Options are "summarize_post", "summarize_influencer", "summarize_brand", "rag".
        userPrompt: str. The user prompt to provide to the model.
        imageUrl: str. The URL of the image to be described (required for "summarize_post" task).

    Returns:
        str: The generated text.
    """

    if TASK_TYPE is None:
        raise ValueError("TASK_TYPE cannot be None.")
    
    if TASK_TYPE == "summarize_post":
        
        model = "meta-llama/Llama-Vision-Free"
        systemInstruction = open('./data/prompts/describe_image.txt', 'r').read()
        userPrompt = "Summarize the content of this instagram post"
        
        messages=[
            {
                "role": "system",
                "content": f"{systemInstruction}",
            },
            {
                "role": "user",
                "content": [{"type": "text", "text": userPrompt}, {"type": "image_url", "image_url": {"url": imageUrl}}],
            }]

    else:
        
        model = "meta-llama/Llama-3.2-3B-Instruct-Turbo"

        if TASK_TYPE == "summarize_influencer":
            systemInstruction = open('./data/prompts/summarize_influencer.txt', 'r').read()
            userPrompt = "Summarize the content of this influencer's profile:\n\n" + userPrompt
        
        elif TASK_TYPE == "summarize_brand":
            systemInstruction = open('./data/prompts/summarize_brand.txt', 'r').read()
            userPrompt = "Summarize the content of this brand's profile:\n\n" + userPrompt
        
        elif TASK_TYPE == "rag":
            systemInstruction = open('./data/prompts/rag.txt', 'r').read().format(retrieve(client, userPrompt))
            userPrompt = "Explain why the provided influencer is a strong match for the following brand:\n\n" + userPrompt
        
        else:
            raise ValueError(f"Invalid TASK_TYPE: {TASK_TYPE}.")
        
        messages=[
            {
                "role": "system",
                "content": f"{systemInstruction}",
            },
            {
                "role": "user",
                "content": userPrompt,
            }]
        
    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=512,
        temperature=0.7,
        top_p = 0.7,
        top_k = 50,
        stream=False,
    )
    return stream.choices[0].message.content.replace('. ', '.\n')

def get_influencer_count():
    return supabase.rpc('get_count').execute().data
