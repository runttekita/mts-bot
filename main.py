# bot.py
import os
import json
import discord
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

client = discord.Client()
cirnoData = None

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    print('Loading mod data')
    loadData(cirnoData, 'cirno')

def loadData(dataField, modId):
    with open(f'data/{modId}/items.json') as json_file:
        dataField = json.load(json_file)
    print('Loaded modId!')

client.run(token)
