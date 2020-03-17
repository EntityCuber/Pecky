import requests
import discord
import wikipedia
import json
import os
from colorama import init, Fore
init(autoreset=True)

testing = 0
hidden = 0

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

# set params
def setParams(message):
  params = {
          "bid" : 10697,
          "key" : apiKey,
          "uid" : message.author,
          "msg" :  message.content
          }
  return(params) 


client = discord.Client()

@client.event
async def on_ready():
  if (not testing):
    print(f"{Fore.RED}Pecky{Fore.RESET} is alive and breathing! 😺\n")
    await client.change_presence(activity=discord.Game(name="😺"))
  else:
    print(f"{Fore.RED}Pecky{Fore.RESET} is alive and breathing! 😺  Testing Mode\n")
    await client.change_presence(activity=discord.Game(name="😺  Testing Mode"))
    
    

@client.event
async def on_message(message):
  # variable
  reply = ''
  # Trigger only when user message
  if message.author != client.user:
    # Respond only when user DM or user mention with @Pecky
    if (engageCondition(message)):
      try:
        # Replace @Pecky discord mention variable to Pecky
        message.content = message.content.replace('<@!555643509311406101>', 'Pecky')
        message.content = message.content.replace('<@555643509311406101>', 'Pecky')


        # reply for help
        if (message.content.replace(' ','')=='Peckyhelp' or message.content == 'help'):
          reply = 'Commands: ?w <question> - wikipedia result'
          replyBot = 'Helper'
          

        # if ? is content start it uses wikipedia instead of bot api for reply
        elif (message.content.replace(' ','').startswith('Pecky?w') or message.content.startswith('?')):
          message.content = message.content.replace('?w','',1) # removes '?w'
          message.content = message.content.replace('Pecky','',1) # removes '?w'
          message.content = message.content.strip()
          try:
            reply = wikipedia.summary(message.content,2)
            reply = f'wikipedia: {reply}'
          except Exception as err:
            print(f'Error occured(wiki): {err}')

          if (not reply):
              reply = "wikipedia: sorry cant find results or there is an error"

          replyBot = 'Wiki'

        else:
          # chat bot api setup
          params = setParams(message)
          response = requests.get(botUrl, params=params)
          reply = json.loads(response.content.decode('utf-8'))['cnt']
          replyBot = 'Pecky'
        
        # check Stop sending reply to discord
        if (not hidden):
          await message.channel.send(reply)

        # Conversation Log
        global authorTemp
        if (authorTemp != str(message.author)): # Print a newline if message user is different
          print('')
        authorTemp = str(message.author)

        print(f"{Fore.GREEN}{message.author.name}: {Fore.RESET}{message.content}\n{Fore.RED}{replyBot}: {Fore.RESET}{reply}")

      except Exception as err:
        print(f'Error Occured: {err}')
      
client.run(token)