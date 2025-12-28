import google.generativeai as genai
from groq import Groq 
import sys

#環境設置

#設定 API Key
api_key_user = input("Please enter your own Google Gemini API Key: ").strip()
genai.configure(api_key = api_key_user)
EMBEDDING_MODEL = "models/text-embedding-004"   #RAG model

#model types
MODEL_FAST = 'models/gemini-2.5-flash'
MODEL_SMART = 'models/gemini-2.5-flash'
MODEL_CREATIVE = 'models/gemini-2.5-flash'
MODEL_VISION = 'models/gemini-2.5-flash'

#安全設定
safety_settings = [
    { "category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    { "category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    { "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    { "category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]