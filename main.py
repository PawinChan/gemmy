#!/usr/bin/python

import discord, random
from discord.ext import commands
from bardChat import *

DEBUGMODEENABLED = True
def printd(*args):
  if DEBUGMODEENABLED:
    print(*args)

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot('.', intents=intents) #Basically discord.Client() with extra features.

@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')
  await client.change_presence(activity=discord.Streaming(name="Introduction to LLMs", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"))
  await client.tree.sync()
  print('Status and slash commands are ready.')

@client.event
async def on_message(message):
  if message.author == client.user:
    return
    
  # print(f"Message from {message.author}: {message.content}")

  async with message.channel.typing():
    if message.channel.id in [968384363538550808, 1221714436973269052]:
      emote = random.choice('😁,😌,🥲,💖,🥹,👍,😀,😃,😄,😆,🥰,😍,😙,😚,🫂,🤗,😇,😄'.split(','))
      await message.channel.send(f'สู้ๆ นะ! {emote}')
    elif message.channel.id in [1222075484863467531]:
      await message.channel.send(chatWithBard(message.channel.id, message.content))
    else:
      pass


@client.tree.command(name="reset_chat",description="Resets the chat.")
async def slash_command(interaction:discord.Interaction):
  global chatRooms
  if interaction.channel_id in chatRooms:
    newChat(interaction.channel_id)
    await interaction.response.send_message("Chat reset.")
  else:
    await interaction.response.send_message("Gemini is not enabled in this channel.")

client.run(os.environ['DISCORD_TOKEN'])

