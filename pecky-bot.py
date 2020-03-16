import requests
import discord
import json
import os
from colorama import init, Fore
init(autoreset=True)


botUrl = os.environ.get('botUrl')
token = os.environ.get('token')
apiKey = os.environ.get('apiKey')

authorTemp = 'x'

# Bot trigger when user DM or user mention @Pecky (on discord server)
def engageCondition(message):
  if (str(message.channel.type) == 'private'): # Trigger when user direct message bot
    return True
  # Trigger when user mention pecky (@pecky) on pc
  elif (message.content.startswith('<@!555643509311406101>')):
    return True 
  # Trigger when user mention pecky (@pecky) on mobile
  elif (message.content.startswith('<@555643509311406101>') or message.content.startswith('.Pecky')):
    return True
  else:
    return False # Trigger conditions false

client = discord.Client()
@client.event
async def on_ready():
    print(f"{Fore.RED}Pecky{Fore.RESET} is alive and breathing! 😺\n")
    await client.change_presence(activity=discord.Game(name="😺"))
    

@client.event
async def on_message(message):
    if message.author != client.user:
      # Respond only when user DM or user mention with @Pecky
      if (engageCondition(message)):
        try:
          # Replace @Pecky discord mention variable to Pecky
          message.content = message.content.replace('<@!555643509311406101>', 'Pecky')
          message.content = message.content.replace('<@555643509311406101>', 'Pecky')
          params = {
            "bid" : 10697,
            "key" : apiKey,
            "uid" : message.author,
            "msg" :  message.content
            }

          response = requests.get(botUrl, params=params)
          reply = json.loads(response.content.decode('utf-8'))['cnt']
          
          await message.channel.send(reply)

          # Conversation Log
          global authorTemp
          if (authorTemp != str(message.author)): # Print a newline if message user is different
            print('')
          authorTemp = str(message.author)

          print(f"{Fore.GREEN}{message.author.name}:{Fore.RESET}{message.content}\n{Fore.RED}Pecky:{Fore.RESET}{reply}")

        except Exception as err:
          print(f'Error Occured: {err}')
      
client.run(token)