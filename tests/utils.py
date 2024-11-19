import requests
import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np
import together
from together import Together

TOGETHER_API_KEY = "5a532872525382e32ebc396c6cc682d3b8d8d5ea428ef9468404286bb1417f2c"

summarize_influencer = """You are a social media analyst.
Your task is to generate a concise, professional summary of an influencer's Instagram profile based on its publicly available information.

Guidelines for the Summary:
- Tone: Informative and professional.
- Content: Highlight the profile's main themes, the type of content posted, audience engagement style, and any notable achievements or unique features.
- Length: Approximately 7-8 sentences (200-250 words).
- Example Structure: Start with the profile's focus (e.g., \"This profile showcases...\"), describe the content's themes (e.g., \"primarily featuring ...\"), and mention any distinguishing features (e.g., \"known for...\").  
"""

summarize_brand = """You are a marketing strategist.
Your task is to generate a concise, professional summary of a brand’s Instagram profile based on its publicly available information.  

Guidelines for the Summary:  
- Tone: Informative and professional.  
- Content: Highlight the brand's industry, key themes of its Instagram presence, type of content (e.g., promotional campaigns, product highlights, user-generated content), target audience, and any unique selling points or achievements.  
- Length: Approximately 7-8 sentences (200-250 words).  
- Example Structure: Start with the brand's core identity (e.g., "This profile represents ..."), mention its Instagram strategy (e.g., "focusing on ..."), and include any notable features (e.g., "renowned for ...").  
"""

retrieve_top_k_influencers = """You are an advanced AI specializing in influencer marketing.
Your task is to analyze the provided influencer description and generate a compelling response explaining why the influencer is a strong match for the given brand.
Be specific in your reasoning, citing traits such as audience demographics, content style, engagement metrics, or past collaborations that align with the company’s objectives.

Influencer Descriptions:  
{influencer_description_1}

Output:  
   - Reason for Match: [Explain why Influencer A aligns with the campaign goals.]  
   - Supporting Details: [Include specific information from the description.]
"""

def cosine_similarity(vectors, target_vector):
    """
    Compute the cosine similarity between a set of vectors and a target vector.

    Parameters:
        vectors (array-like): A 2D array where each row is a vector.
        target_vector (array-like): A 1D array representing the target vector.

    Returns:
        np.ndarray: A 1D array containing cosine similarities for each vector in the set.
    """
    # Convert to numpy arrays if not already
    vectors = np.array(vectors)
    target_vector = np.array(target_vector)
    
    # Compute dot products between each vector and the target vector
    dot_products = np.dot(vectors, target_vector)
    
    # Compute norms of the vectors
    vector_norms = np.linalg.norm(vectors, axis=1)
    target_norm = np.linalg.norm(target_vector)
    
    # Avoid division by zero
    if target_norm == 0:
        return np.zeros_like(dot_products)
    
    # Compute cosine similarities
    return dot_products / (vector_norms * target_norm)

def retrieve_top_k_influencers_request(brand_description, k = 1):

    vdb = np.load('./embeddings.npy')
    description = pd.read_csv('./description.csv')

    brand_embeddings = generate_embeddings([brand_description], "BAAI/bge-base-en-v1.5")[0]

    description['similarity'] = cosine_similarity(vdb, brand_embeddings)
    
    return description.sort_values(by='similarity', ascending=False)['description'].iloc[:k].to_list()


def together_request(user_message, api_key = None, request_type = 'default', influencer_description_1 = None):

    if request_type == 'default':
        instructions = ''
    elif request_type == 'summarize_influencer':
        instructions = summarize_influencer
    elif request_type == 'summarize_brand':
        instructions = summarize_brand
    elif request_type == 'retrieve_top_k_influencers':
        if not influencer_description_1:
            return "influencer_description_1 required when request_type == 'retrieve_top_k_influencers'."
        instructions = retrieve_top_k_influencers.format(influencer_description_1=influencer_description_1)
    else:
        return "Invalid request type. Please choose from 'default', 'summarize_influencer', 'summarize_brand', or 'retrieve_top_k_influencers'."

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

def generate_embeddings(input_texts: list,
                        model_api_string: str
                        ) -> list:
    """Generate embeddings from Together python library.

    Args:
        input_texts: a list of string input texts.
        model_api_string: str. An API string for a specific embedding model of your choice.

    Returns:
        embeddings_list: a list of embeddings. Each element corresponds to the each input text.
    """
    together_client = together.Together(api_key = TOGETHER_API_KEY)
    outputs = together_client.embeddings.create(
        input=input_texts,
        model=model_api_string,
    )
    return np.array([x.embedding for x in outputs.data])