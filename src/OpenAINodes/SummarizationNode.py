from openai import OpenAI
from dotenv import load_dotenv
import os

SYSTEM_PROMPT = "\n".join([
    "Your job is to prepare summarization of speech provided below containing all important informations.",
    "Think step by step:",
    "1. Carefully read the text.",
    "2. Filter which informations is crucial.",
    "3. Write all crucial information in form of bullet points.",
    "Write summarization in Polish"
])

USER_PROMPT = "### SPEECH ###\n"

class SummarizationNode():
    model: OpenAI
    
    def __init__(self, secret_path: str):
        load_dotenv(secret_path)
        self.model = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
    def summarize(self, speech: str) -> str:
        completion = self.model.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": USER_PROMPT + speech}
            ],
            temperature=0.1
        )

        return completion.choices[0].message.content