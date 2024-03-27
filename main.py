#!/usr/bin/python

import discord, random
from discord.ext import commands
from gemmyChat import *
from typing import Literal
####################
#     Bot Setup    #
####################

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot('.', intents=intents) #Basically discord.Client() with extra stuff.

####################
#      Events      #
####################

@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')
  await client.change_presence(activity=discord.Streaming(name="Introduction to LLMs", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"))
  await client.tree.sync()
  print('Status and slash commands are ready.')

@client.event
async def on_message(message):
  if (message.author == client.user) or (message.author.bot):
    return
    
  # print(f"Message from {message.author}: {message.content}")


  if message.channel.id in motivationEnabledChannels:
    emote = random.choice('😁,😌,🥲,💖,🥹,👍,😀,😃,😄,😆,🥰,😍,😙,😚,🫂,🤗,😇,😄'.split(','))
    await message.channel.send(f'สู้ๆ นะ! {emote}')

  elif message.channel.id in chatConfig:
    async with message.channel.typing():
      global chatRooms
      respondingMessage = None
      respondingContent = ""
      # await message.channel.send(await chatWithBard(message.channel.id, message.content, message.author.display_name))
      for response_chunk in chatWithBard(message.channel.id, message.content, message.author.display_name, streamingEnabled=chatConfig[message.channel.id]['streamingEnabled']):
        respondingContent += response_chunk
        if respondingMessage is None:
          respondingMessage = await message.channel.send(respondingContent)
        elif len(respondingContent) > 2000:
          respondingMessage = await message.channel.send(response_chunk)
          respondingContent = response_chunk
        else:
          await respondingMessage.edit(content=respondingContent)
  else:
    pass

####################
###SLASH COMMANDS###
####################

# https://dev.to/mannu/4slash-commands-in-discordpy-ofl
@client.tree.command(name="ping",description="Pong!")
async def enableChatbotCommand(interaction:discord.Interaction):
  await interaction.response.send_message(f"Pong! That was {round(client.latency * 1000)}ms!")

@client.tree.command(name="chat_toggle",description="Enable/Disable the chatbot in the current channel.")
async def enableChatbotCommand(interaction:discord.Interaction):
  global chatConfig

  chatbotCurrentlyEnabled = chatConfig.get(interaction.channel_id, DEFAULT_CHAT_CONFIG).get('chatEnabled')
  editChatConfig(interaction.channel_id, {'chatEnabled': not chatbotCurrentlyEnabled})
  await interaction.response.send_message(f"{'❌' if chatbotCurrentlyEnabled else '✅'} Chatbot successfully {'disabled' if chatbotCurrentlyEnabled else 'enabled'} in this channel.")
  

@client.tree.command(name="chat_reset",description="Resets the chat.")
async def resetChatCommand(interaction:discord.Interaction):
  global chatRooms
  if interaction.channel_id in chatRooms:
    newChat(interaction.channel_id)
    await interaction.response.send_message("✅ Chat reset.")
  else:
    await interaction.response.send_message("ℹ️ There seems to be nothing to reset here!")


@client.tree.command(name="chat_configure", description="Configure the chatbot in the current channel.")
async def resetChatCommand(interaction:discord.Interaction, options: Literal['chatEnabled', 'streamingEnabled'], value: bool):
  editChatConfig(interaction.channel_id, {options: value})
  await interaction.response.send_message(f"✅ Chatbot config {options} set to {value}.")


@client.tree.command(name="chat_viewconfig", description="View the chatbot configuration in the current channel.")
async def viewChatConfigCommand(interaction:discord.Interaction):
  global chatConfig
  currentConfig = chatConfig.get(interaction.channel_id, None)
  await interaction.response.send_message(f"Current Chatbot Configuration:\n```json\n{currentConfig}```")
####################
####### RUN ########
####################
  
client.run(os.environ['DISCORD_TOKEN'])

#modelName