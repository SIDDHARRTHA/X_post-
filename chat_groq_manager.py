import os
import time
import requests
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

class ChatGroqManager:
    def __init__(self, model_name):
        self.model_name = model_name
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY not found. Please check your .env file.")

    def create_llm(self, temperature=0.4):
        return ChatGroq(
            temperature=temperature,
            groq_api_key=self.groq_api_key,
            model_name=self.model_name
        )

    def make_request(self, endpoint, data):
        headers = {
            'Authorization': f'Bearer {self.groq_api_key}'
        }
        
        while True:
            response = requests.post(endpoint, headers=headers, json=data)
            if response.status_code == 429:
                retry_after = int(response.headers.get('retry-after', 1))
                print(f"Rate limit reached. Retrying after {retry_after} seconds.")
                time.sleep(retry_after)
            elif response.status_code == 200:
                return response.json()
            else:
                response.raise_for_status()
