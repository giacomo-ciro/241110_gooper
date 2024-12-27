import re

from together import Together
from supabase import create_client

TOGETHER_API_KEY = "5a532872525382e32ebc396c6cc682d3b8d8d5ea428ef9468404286bb1417f2c"
SUPABSE_URL = "https://edcqmzluacqdqqmmklik.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVkY3Ftemx1YWNxZHFxbW1rbGlrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzQwMTM1MDgsImV4cCI6MjA0OTU4OTUwOH0.Po1jIO14A6mCuN1xo-K6ikpKR1XlGt4_ivoYVX2raSU"

class GooperModel:
    def __init__(self,
                 model_text = "meta-llama/Llama-3.2-3B-Instruct-Turbo",
                 model_embeddings = "BAAI/bge-base-en-v1.5"):
        
        self.version = "1.1.3"

        # Together
        self.together = Together(api_key = TOGETHER_API_KEY)
        self.model_text = model_text
        self.model_embeddings = model_embeddings

        # Supabase
        self.supabase = create_client(SUPABSE_URL, SUPABASE_KEY)

        return
    
    def discriminator_agent(self, 
                            userPrompt
                            ):
        """Discriminate whether a user's prompt is valid or not
        
        Args:
            userPrompt: str. The user prompt to provide to the model.
            
        Returns:
            int: 1 if the prompt is valid, 0 if not.
        """
        
        systemInstruction = open('./data/prompts/discriminator.txt', 'r').read()
            
        messages=[
            {
                "role": "system",
                "content": f"{systemInstruction}",
            },
            {
                "role": "user",
                "content": userPrompt,
            }]
            
        response = self.together.chat.completions.create(
            model=self.model_text,
            messages=messages,
            max_tokens=512,
            temperature=0.7,
            top_p = 0.7,
            top_k = 50,
            stream=False,
        )

        response = response.choices[0].message.content.replace('. ', '.\n')
        print('-----')
        print(response)
        response = response.split(':')[-1]
        response = re.sub(r'[^a-zA-Z]+', '', response)
        print(response)
        return 1 if response == "valid" else 0
        

    def retrieve(self,
                 query=None,
                 ):
        """Retrieve the most appropriate influencer's description from the influencer database using Together API to embed the query.

        Args:
            client: Together. The Together client.
            query: str. The query to embed and retrieve the most appropriate influencer's description.

        Returns:
            str: The retrieved text.
        """

        out = self.together.embeddings.create(
            input=query,
            model=self.model_embeddings,
        )

        query = out.data[0].embedding

        response = self.supabase.rpc("get_similar_items",{
            "query_embeddings": query,
            "result_limit": 1
        }).execute()
        
        return response.data[0]['description']
    
    def rag_agent(self,
                 userPrompt
                 ):
        """Answer a user's prompt using the Together API.

        Args:
            userPrompt: str. The user prompt to provide to the model.

        Returns:
            str: The generated text.
        """

        systemInstruction = open('./data/prompts/rag.txt', 'r').read().format(self.retrieve(userPrompt))
        userPrompt = "Explain why the provided influencer is a strong match for the following brand:\n\n" + userPrompt

            
        messages=[
            {
                "role": "system",
                "content": f"{systemInstruction}",
            },
            {
                "role": "user",
                "content": userPrompt,
            }]
            
        response = self.together.chat.completions.create(
            model=self.model_text,
            messages=messages,
            max_tokens=512,
            temperature=0.7,
            top_p = 0.7,
            top_k = 50,
            stream=False,
        )
        return response.choices[0].message.content.replace('. ', '.\n')
    
    def generate(self,
                 userPrompt
                 ):
        """Wrapper for the entire gooper pipeline.

        Args:
            userPrompt: str. The user prompt to provide to the model.

        Returns:
            str: The generated text.
        """
        
        if self.discriminator_agent(userPrompt):
            return self.rag_agent(userPrompt)
        else:
            return "I'm sorry, I am not able to provide a response to this prompt. Please, provide your brand's description and I will help you find the best influencer for your needs!"

    def get_influencer_count(self):
        return self.supabase.rpc('get_count').execute().data