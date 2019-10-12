# bot.py
import os
import json
import discord
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

client = discord.Client()
cirno_data = None
prefix = '!'

class Mod_Data:
    def __init__(self, id):
        self.data = self.get_data(id)

    def get_data(self, id):
        if os.path.exists(f'data/{id}.json'):
            with open(f'data/{id}.json') as json_file:
                return json.load(json_file)
        else:
            data = dict()
            for file in os.listdir('data/'):
                with open(f'data/{file}') as json_file:
                    data.update(json.load(json_file))
            print(data)
            return data

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
    if os.path.exists(f'data/{s.split(" ")[1]}.json'):
        tokenized_message  = s.split(' ', 2)
    else:
        tokenized_message = s.split(' ', 1)
    await do_command(message.channel, tokenized_message)

async def do_command(channel, tokenized_message):
    commands = {
        'card': card,
        'relic': relic
    }
    callback = commands.get(tokenized_message[0])
    await callback(channel, tokenized_message)

@client.event
async def send_failure(channel, tokenized_message):
    await channel.send(f'Unable to find mod {tokenized_message[1]}')

@client.event
async def card(channel, tokenized_message):
    cards = Mod_Data(tokenized_message[1]).data['cards']
    for card in cards:
        if len(tokenized_message) == 3:
            if tokenized_message[2] == card['name'].lower():
                await channel.send(card_format(card))
                return
        else:
            if tokenized_message[1] == card['name'].lower():
                await channel.send(card_format(card))
                return
    if len(tokenized_message) == 3:
        await channel.send(f'No card named {tokenized_message[2]} found in {tokenized_message[1]}.')
    else:
        await channel.send(f'No card named {tokenized_message[1]} found.')

@client.event
async def relic(channel, tokenized_message):
    relics = Mod_Data(tokenized_message[1]).data['relics']
    for relic in relics:
        if len(tokenized_message) == 3:
            if tokenized_message[2] == relic['name'].lower():
                await channel.send(relic_format(relic))
                return
        else:
            if tokenized_message[1] == relic['name'].lower():
                await channel.send(relic_format(relic))
                return
    if len(tokenized_message) == 3:
        await channel.send(f'No relic named {tokenized_message[2]} found in {tokenized_message[1]}.')
    else:
        await channel.send(f'No relic named {tokenized_message[1]} found.')

def card_format(card):
    return "**{0}**\n{1}  `{2}`  `{3}`  `{4}`  `{5}`\n{6}".format(card['name'], energy_string(card['cost']), card['type'], card['rarity'], card['mod'], card['color'], card['description'])

def relic_format(relic):
    print(relic)
    return "**{0}**\n`{1}`  `{2}`  `{3}`\n{4}\n*{5}*".format(relic['name'], relic['tier'], relic['pool'], relic['mod'], relic['description'], relic['flavorText'])

def energy_string(cost):
    if cost == 'X':
        return cost
    cost = int(cost)
    s = ''
    for i in range (0, cost):
        s += '[E] '
    return s
client.run(token)

