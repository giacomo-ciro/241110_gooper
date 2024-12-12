from together import Together
import numpy as np
from supabase import create_client

# TOGETHER_API_KEY = "5a532872525382e32ebc396c6cc682d3b8d8d5ea428ef9468404286bb1417f2c"
# client = Together(api_key = TOGETHER_API_KEY)

url = "https://edcqmzluacqdqqmmklik.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVkY3Ftemx1YWNxZHFxbW1rbGlrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzQwMTM1MDgsImV4cCI6MjA0OTU4OTUwOH0.Po1jIO14A6mCuN1xo-K6ikpKR1XlGt4_ivoYVX2raSU"
supabase = create_client(url, key)

def cosine_similarity(vectors,
                      target_vector
                      ):
    """
    Compute the cosine similarity between a set of vectors and a target vector.

    Parameters:
        vectors (array-like): A 2D array where each row is a vector.
        target_vector (array-like): A 1D array representing the target vector.

    Returns:
        np.ndarray: A 1D array containing cosine similarities for each vector in the set.
    """
    if not isinstance(vectors, np.ndarray):
        vectors = np.array(vectors)
    if not isinstance(target_vector, np.ndarray):
        target_vector = np.array(target_vector)
    
    dot_products = np.dot(vectors, target_vector)

    vector_norms = np.linalg.norm(vectors, axis=1)
    target_norm = np.linalg.norm(target_vector)
    
    if target_norm == 0:
        return np.zeros_like(dot_products)
    
    return dot_products / (vector_norms * target_norm)

def retrieve(client,
             query,
             vdb = None,
             descriptions = None,
             ):
    """Retrieve the most appropriate influencer's description from the influencer database using Together API to embed the query.

    Args:
        query: str. The input query.
        vdb: np.ndarray. A set of vectors representing influencer descriptions.
        descriptions: list. A list of corresponding descriptions.

    Returns:
        str: The retrieved text.
    """
    
    # if vdb is None:
    #     vdb = np.load('./data/embeddings.npy')
        
    # if descriptions is None:
    #     descriptions = open('./data/descriptions.txt', 'r').read().replace("\"","").splitlines()

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