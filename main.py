# bot.py
import os
import json
import discord
from dotenv import load_dotenv
import os
import random

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

client = discord.Client()
prefix = '?'

class Mod_Data:
    def __init__(self, id):
        self.data = self.get_data(id)

    def get_data(self, id):
        data = []
        if os.path.exists(f'data/{id}.json'):
            with open(f'data/{id}.json') as json_file:
                data.append(json.load(json_file))
        else:
            for file in os.listdir('data/'):
                with open(f'data/{file}') as json_file:
                    data.append(json.load(json_file))
        return data 

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    print('Loaded mod data')

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
    if s == 'help':
        await help_command(message.channel)
    if s == 'praise' and message.author.id == 86261397213708288:
        await message.channel.send('i love reina <3')
    if s == 'contribute':
        await message.channel.send('https://github.com/velvet-halation/mts-bot#contributing')
    if os.path.exists(f'data/{s.split(" ")[1]}.json'):
        tokenized_message  = s.split(' ', 2)
    else:
        tokenized_message = s.split(' ', 1)
    await do_command(message.channel, tokenized_message)

async def do_command(channel, tokenized_message):
    commands = {
        'help': help_command,
        'card': card,
        'relic': relic,
        'keyword': keyword
    }
    callback = commands.get(tokenized_message[0])
    await callback(channel, tokenized_message)

@client.event
async def send_failure(channel, tokenized_message):
    await channel.send(f'Unable to find mod {tokenized_message[1]}')

@client.event
async def card(channel, tokenized_message):
    cards = Mod_Data(tokenized_message[1]).data
    if len(tokenized_message) == 3:
        if tokenized_message[2] == 'random':
            if 'mod' in cards[0]:
                await channel.send(card_format(random.choice(cards[0]['cards']), cards[0]['mod']['name']))
                return
            else:
                card = random.choice(cards[0]['cards'])
                await channel.send(card_format(card, card['mod']))
                return
    if len(tokenized_message) == 2:
        if tokenized_message[1] == 'random':
            mod_object = random.choice(cards)
            if len(mod_object['cards']) == 0:
                await card(channel, tokenized_message)
                return
            cards_object = random.choice(mod_object['cards'])
            if 'mod' in mod_object:
                await channel.send(card_format(cards_object, mod_object['mod']['name']))
                return
            else:
                await channel.send(card_format(cards_object, cards_object['mod']))
                return
    for x in range(len(cards)):
        for card in cards[x]['cards']:
            if len(tokenized_message) == 3:
                if tokenized_message[2] == card['name'].lower():
                    if 'mod' in cards[x]:
                        await channel.send(card_format(card, cards[x]['mod']['name']))
                        return
                    else:
                        await channel.send(card_format(card, card['mod']))
                        return
                else:
                    if tokenized_message[1] == card['name'].lower():
                        if 'mod' in cards[x]:
                            await channel.send(card_format(card, cards[x]['mod']['name']))
                            return
                        else:
                            await channel.send(card_format(card, card['mod']))
                            return
    if len(tokenized_message) == 3:
        await channel.send(f'No card named {tokenized_message[2]} found in {tokenized_message[1]}.')
    else:
        await channel.send(f'No card named {tokenized_message[1]} found.')

@client.event
async def relic(channel, tokenized_message):
    relics = Mod_Data(tokenized_message[1]).data
    if len(tokenized_message) == 3:
        if tokenized_message[2] == 'random':
            if 'mod' in relics[0]:
                await channel.send(relic_format(random.choice(relics[0]['relics']), relics[0]['mod']['name']))
                return
            else:
                relic = random.choice(relics[0]['relics'])
                await channel.send(relic_format(relic, relic['mod']))
                return
    if len(tokenized_message) == 2:
        if tokenized_message[1] == 'random':
            mod_object = random.choice(relics)
            if len(mod_object['relics']) == 0:
                await relic(channel, tokenized_message)
                return
            relics_object = random.choice(mod_object['relics'])
            if 'mod' in mod_object:
                await channel.send(relic_format(relics_object, mod_object['mod']['name']))
                return
            else:
                await channel.send(relic_format(relics_object, relics_object['mod']))
                return
    for x in range(len(relics)):
        for relic in relics[x]['relics']:
            if len(tokenized_message) == 3:
                if tokenized_message[2] == relic['name'].lower():
                    if 'mod' in relics[x]:
                        await channel.send(relic_format(relic, relics[x]['mod']['name']))
                        return
                    else:
                        await channel.send(relic_format(relic, relic['mod']))
                        return
                else:
                    if tokenized_message[1] == relic['name'].lower():
                        if 'mod' in relics[x]:
                            await channel.send(relic_format(relic, relics[x]['mod']['name']))
                            return
                        else:
                            await channel.send(relic_format(relic, relic['mod']))
                            return
    if len(tokenized_message) == 3:
        await channel.send(f'No relic named {tokenized_message[2]} found in {tokenized_message[1]}.')
    else:
        await channel.send(f'No relic named {tokenized_message[1]} found.')

@client.event
async def keyword(channel, tokenized_message):
    keywords = Mod_Data(tokenized_message[1]).data
    for x in range(len(keywords)):
        for keyword in keywords[x]['keywords']:
            keyword_name = ''
            split_keyword = keyword['name'].split(':')
            if len(split_keyword) == 2:
                keyword_name = split_keyword[1]
            else:
                keyword_name = split_keyword[0]
            if len(tokenized_message) == 3:
                if tokenized_message[2] == keyword_name.lower():
                    if len(split_keyword) == 2:
                        await channel.send(keyword_format_mod(keyword, keyword_name, split_keyword[0]))
                        return
                    else:
                        await channel.send(keyword_format(keyword, keyword_name))
                        return
            else:
                if tokenized_message[1] == keyword_name.lower():
                    if len(split_keyword) == 2:
                        await channel.send(keyword_format_mod(keyword, keyword_name, split_keyword[0]))
                        return
                    else:
                        await channel.send(keyword_format(keyword, keyword_name))
                        return

    if len(tokenized_message) == 3:
        await channel.send(f'No keyword named {tokenized_message[2]} found in {tokenized_message[1]}.')
    else:
        await channel.send(f'No keyword named {tokenized_message[1]} found.')

@client.event
async def help_command(channel):
    await channel.send(f'I can look up modded info with {prefix}card, {prefix}relic or {prefix}keyword!')

def card_format(card, id):
    return "**{0}**\n`{1}`  `{2}`  `{3}`  `{4}`  `{5}`\n{6}".format(card['name'], energy_string(card['cost']), card['type'], card['rarity'], card['color'], id, remove_keyword_prefixes(card['description']))

def relic_format(relic, id):
    if relic['pool'] == '':
        return "**{0}**\n`{1}`, `{2}`\n{3}\n*{4}*".format(relic['name'], relic['tier'], id, relic['description'], relic['flavorText'])

    return "**{0}**\n`{1}` `{2}` `{3}`\n{4}\n*{5}*".format(relic['name'], relic['tier'], relic['pool'], id, relic['description'], relic['flavorText'])

def keyword_format_mod(keyword, name, mod):
    return "**{0}**\n {1}".format(name.capitalize(), keyword['description'])

def keyword_format(keyword, name):
    return "**{0}**\n{1}".format(name.capitalize(), keyword['description'])

def energy_string(cost):
    if cost == 'X' or '0':
        return cost

    cost = int(cost)
    s = ''
    for i in range (0, cost):
        s += '[E] '
    return s

def remove_keyword_prefixes(description):
    description = description.replace('\n', '\n ')
    description = description.split(' ')
    final_description = ''
    for word in description:
        if word.startswith('!'):
            continue
        if is_keyword(word):
            if word.split(':', 1)[1][len(word.split(':', 1)[1]) - 1] == '.':
                final_description += word.split(':', 1)[1]
            else:
                final_description += word.split(':', 1)[1] + ' '
            continue
        final_description += word + ' '
    final_description = final_description.replace('\n ', '\n')
    return final_description

def is_keyword(word):
    return not word[0].isupper() and ':' in word

client.run(token)


