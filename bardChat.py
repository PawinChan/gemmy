import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai.types.generation_types import BlockedPromptException

load_dotenv()

# Refer to: https://ai.google.dev/api/python/google/generativeai/GenerationConfig
geminiConfig = genai.GenerationConfig(
  max_output_tokens=1600, 
  temperature=None, 
  top_p=None, 
  top_k=None
  )

genai.configure(api_key=os.environ["GEMINI_API_KEY"]) # Obtain token from: https://aistudio.google.com/app/apikey

# Guide: https://ai.google.dev/tutorials/python_quickstart
model = genai.GenerativeModel('gemini-pro')
def printAvailableModels():
  print("Available Models: ")
  for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
      print(m.name)
  print('--------------------------------------\n\n')


#TODO: https://ai.google.dev/docs/safety_setting_gemini
"""
Available Models: 
models/gemini-1.0-pro
models/gemini-1.0-pro-001
models/gemini-1.0-pro-latest
models/gemini-1.0-pro-vision-latest
models/gemini-pro
models/gemini-pro-vision
--------------------------------------
"""

chatRooms = {}

def newChat(channelId: int):
  global chatRooms
  chatRooms[channelId] = model.start_chat(history=[])


def chatWithBard(channelId: int, message: str):
  global chatRooms

  if not chatRooms.get(channelId):
    newChat(channelId)

  try:
    response = chatRooms[channelId].send_message(message).text
  except ValueError:
    response = "\*No response...\*"
  except BlockedPromptException:
    response = "This prompt was blocked by Google's Security Settings ☝️. What were you doing???"
  return response