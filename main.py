# bot.py
import os
import json
import discord
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

client = discord.Client()
cirno_data = None
prefix = '!'

class Mod_Data:
    def __init__(self, id):
        self.data = self.get_data(id)

    def get_data(self, id):
        with open(f'data/{id}/items.json') as json_file:
            return json.load(json_file)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    print('Loading mod data')

def is_command(message):
    return message.content.startswith(prefix)

def del_char(string, index):
    return string[1:]

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if is_command(message):
        print(message.content)
        message.content = del_char(message.content, len(prefix))
        await get_id(message)
        
async def get_id(message):
    s = message.content.lower()
    tokenized_message  = s.split(' ', 2)
    await do_command(message.channel, tokenized_message)
    
async def do_command(channel, tokenized_message):
    commands = {
        'card': card
    }
    callback = commands.get(tokenized_message[0])
    await callback(channel, tokenized_message)

@client.event
async def card(channel, tokenized_message):
    cards = Mod_Data(tokenized_message[1]).data['cards']
    for card in cards:
        if tokenized_message[2] == card['name'].lower():
            await channel.send(card_format(card))
            return
    await channel.send(f'No card named {tokenized_message[2]} found in {tokenized_message[1]}')

def card_format(card):
    return "**{0}**\n{1} `{2}` `{3}` `{4}` `{5}`\n{6}".format(card['name'], energy_string(card['cost']), card['type'], card['rarity'], card['mod'], card['color'], card['description'])

def energy_string(cost):
    cost = int(cost)
    s = ''
    for i in range (0, cost):
        s += '[E] '
    return s
client.run(token)

