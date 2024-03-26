import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai.types.generation_types import BlockedPromptException, StopCandidateException

load_dotenv()

# Refer to: https://ai.google.dev/api/python/google/generativeai/GenerationConfig
geminiConfig = genai.GenerationConfig(
  max_output_tokens=200, 
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

def newChat(channelId: int, preprompt=None):
  #if not preprompt:
    #preprompt = "Hi! You're currently in a discord channel among a group of friends. Try to be helpful, fun, and don't forget to keep your response concise easy to understand! By the way, the author of each message will be noted at the start of the prompt so you can know who is talking to you, although please do NOT prepend your name (or anything like Assistant: , etc.) Here we go!"
  global chatRooms
  chatRooms[channelId] = model.start_chat(history=[])
  #chatRooms[channelId].send_message(preprompt)


async def chatWithBard(channelId: int, message: str, username: str):
  global chatRooms

  if not chatRooms.get(channelId):
    newChat(channelId)

  try:
    response = chatRooms[channelId].send_message(f"{username}: {message}").text
  except ValueError:
    response = "\*No response...\*"
  except BlockedPromptException:
    response = "This prompt was blocked by Google's Security Settings ☝️. What were you doing???"
  except StopCandidateException as e:
    response = f"Cannot Generate Response.\n `{type(e).__name__}`: *{str(e)}*"
  except Exception as e:
    response = f"Unhandled Error.\n `{type(e).__name__}`: *{str(e)}*"
  return response[:2000]


def streamBardReponse(channelId: int, message: str, username: str):
  global chatRooms

  if not chatRooms.get(channelId):
    newChat(channelId)

  try:
    for response_chunk in chatRooms[channelId].send_message(f"{username}: {message}", stream=True):
      yield response_chunk.text
    
  except ValueError:
    return "\*No response...\*"
  except BlockedPromptException:
    return "This prompt was blocked by Google's Security Settings ☝️. What were you doing???"
  except StopCandidateException as e:
    return f"Cannot Generate Response.\n `{type(e).__name__}`: *{str(e)}*"
  except Exception as e:
    return f"Unhandled Error.\n `{type(e).__name__}`: *{str(e)}*"
  #return response[:2000]