#!/usr/bin/python

import discord, random
from discord.ext import commands
from gemmyChat import *
from jsonOperations import *

####################
#     Bot Setup    #
####################

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot('.', intents=intents) #Basically discord.Client() with extra stuff.

motivationEnabledChannels = readJson('data/motivationEnabledChannels.json', [968384363538550808, 1221714436973269052])
geminiEnabledChannels = readJson('data/geminiEnabledChannels.json', [1222075484863467531])

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
  elif message.channel.id in geminiEnabledChannels:
    async with message.channel.typing():
      respondingMessage = None
      respondingContent = ""
      # await message.channel.send(await chatWithBard(message.channel.id, message.content, message.author.display_name))
      for response_chunk in streamBardReponse(message.channel.id, message.content, message.author.display_name):
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

@client.tree.command(name="chat_enable",description="Enable Chatbot within the channel.")
async def enableChatbotCommand(interaction:discord.Interaction):
  global geminiEnabledChannels
  if interaction.channel_id not in geminiEnabledChannels:
    geminiEnabledChannels.append(interaction.channel_id)
    writeJson('data/geminiEnabledChannels.json', geminiEnabledChannels)
    newChat(interaction.channel_id)
    await interaction.response.send_message("✅ Chatbot successfully enabled in this channel.")
  else:
    await interaction.response.send_message("ℹ️ Chabot is already enabled in this channel.")


@client.tree.command(name="chat_disable",description="Disables the chatbot in the channel.")
async def disableChatbotCommand(interaction:discord.Interaction):
  global geminiEnabledChannels
  if interaction.channel_id in geminiEnabledChannels:
    geminiEnabledChannels.remove(interaction.channel_id)
    writeJson('data/geminiEnabledChannels.json', geminiEnabledChannels)
    await interaction.response.send_message("✅ Chatbot successfully disabled in this channel.")
  else:
    await interaction.response.send_message("ℹ️ Chatbot is not enabled in this channel.")


@client.tree.command(name="chat_reset",description="Resets the chat.")
async def resetChatCommand(interaction:discord.Interaction):
  global chatRooms
  if interaction.channel_id in chatRooms:
    newChat(interaction.channel_id)
    await interaction.response.send_message("✅ Chat reset.")
  else:
    await interaction.response.send_message("ℹ️ There seems to be nothing to reset here!")

####################
####### RUN ########
####################
client.run(os.environ['DISCORD_TOKEN'])

