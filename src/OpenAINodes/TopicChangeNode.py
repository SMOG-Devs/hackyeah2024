from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from traceback import print_exc

SYSTEM_PROMPT = "\n".join([
    "You are linguistic export. You are able to understand topic and sense unnatural shift in topic.",
    "You will be provided speech fragment. ",
    "Your task is to detect whether the provided speech contains sudden switch in topic or not.",
    "Follow this step by step:",
    "1. Read the speech carefully.",
    "2. Decide whether in the speech sudden switch in topic occured.",
    '3. Return json in format {"Change Detected": boolean}, indicating whether shift occured'
])

USER_PROMPT = "### SPEECH ###\n"

class TopicChangeNode():
    model: OpenAI
    
    def __init__(self, secret_path: str):
        load_dotenv(secret_path)
        self.model = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
    def detect_change(self, speech: str) -> bool:
        completion = self.model.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": USER_PROMPT + speech}
            ],
            response_format={"type": "json_object"},
            temperature=0.1
        )
        
        response = completion.choices[0].message.content

        try:
            dict_ = json.loads(response)
        except Exception: 
            print_exc()
            return False
        return dict_["Change Detected"]