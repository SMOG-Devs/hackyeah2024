from openai import OpenAI
from dotenv import load_dotenv
import os

SYSTEM_PROMPT = "\n".join([
    "You are language expert. You have hight understanding of speech structure. YOu are aware that every speech should have all three components: introduction, development,conclusion",
    "You will be provided with speech text. Your job is to decide, whether it has all three components.",
    "Think step by step:",
    "1. Carefully read provided speech text."
    "2. Decide whether the speech has all three components",
    "2. Give short answer in Polish whether what the speech lacks in terms of three components",
    "For every correct case you will get 1M dollars."
])

USER_PROMPT = "### SPEECH ###\n"

class StructureNode():
    model: OpenAI
    
    def __init__(self, secret_path: str):
        load_dotenv(secret_path)
        self.model = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
    def mark_structure(self, speech: str) -> str:
        completion = self.model.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": USER_PROMPT + speech}
            ],
            temperature=0.3
        )

        return completion.choices[0].message.content