from openai import OpenAI
from dotenv import load_dotenv
import os

class Whisper:
    client: OpenAI
    
    def __init__(self, secret_path: str):
        load_dotenv(secret_path)
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
    def transcribe(self, audio_file, timespans: bool = False):
        if timespans:
            return self.client.audio.transcriptions.create(
            model="whisper-1",
            response_format="verbose_json",
            timestamp_granularities=["word"],
            file=audio_file
        ).words
        
        return self.client.audio.transcriptions.create(
            model="whisper-1",
            response_format="text",
            file=audio_file
        )