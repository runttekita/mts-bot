# bot.py
import os
import json
import discord
from dotenv import load_dotenv
import re
import random
from mtsbotdata import aliases, suggestables

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
pin_links = [
    "https://media.discordapp.net/attachments/398373038732738570/543527729077682187/sts-check-the-pins.gif",
    "https://media.discordapp.net/attachments/504438263012917254/542101742377107467/kumikopins.gif",
    "https://cdn.discordapp.com/attachments/504438263012917254/632966857292513320/fireworks.gif",
    "https://cdn.discordapp.com/attachments/504438263012917254/632966856596127745/ruiPins.gif",
]

client = discord.Client()
prefix = "?"

banned_users = []

uncolor = re.compile(r"^\[#[0-9A-Fa-f]{6}\](\S+?)$")


class Mod_Data:
    def __init__(self, id):
        self.data = self.get_data(id)

    def get_data(self, id):
        data = []
        if os.path.exists(f"data/{id}.json"):
            with open(f"data/{id}.json") as json_file:
                data.append(json.load(json_file))
        else:
            for file in os.listdir("data/"):
                with open(f"data/{file}") as json_file:
                    data.append(json.load(json_file))
        return data


@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")
    print("Loaded mod data")


def is_command(message):
    return message.content.startswith(prefix)


def del_char(string, index):
    return string[1:]


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if (
        message.content.lower() == "update body text"
        and message.author.id == 114667440507453441
    ):
        await message.channel.send("UPDATE BODY TEXT")
        return
    if (
        message.content.lower() == "big thanks papa kio!"
        and message.author.id == 95258954090676224
    ):
        await message.channel.send("Big thanks papa Kio!")
        return
    if is_command(message):
        print(message.content)
        message.content = del_char(message.content, len(prefix))
        await get_id(message)


async def get_id(message):
    s = message.content.lower()
    if s == "help":
        await help_command(message.channel)
        return
    if s == "praise" and (
        message.author.id == 86261397213708288
        or message.author.id == 132940023522656256
    ):
        await message.channel.send("i love alchy <3")
        return
    if s == "contribute":
        await message.channel.send(
            "https://github.com/velvet-halation/mts-bot#contributing"
        )
        return
    if s == "list":
        await message.channel.send(
            "https://github.com/velvet-halation/mts-bot/tree/master/data"
        )
        return
    if s == "default":
        await message.channel.send("https://github.com/Gremious/StS-DefaultModBase")
        return
    if s == "pins" or s == "pin":
        await message.channel.send(random.choice(pin_links))
        return
    if s == "xy":
        await message.channel.send("http://xyproblem.info/")
        return
    if s == "debugger":
        await message.channel.send(
            "https://stackoverflow.com/questions/25385173/what-is-a-debugger-and-how-can-it-help-me-diagnose-problems"
        )
        return
    if s == "spirepatch":
        await message.channel.send(
            "https://github.com/kiooeht/ModTheSpire/wiki/SpirePatch"
        )
        return
    if s == "optin":
        await message.channel.send(
            "https://github.com/velvet-halation/mts-bot/blob/master/README.md#opt-in-for-receiving-feedback"
        )
        return
    if s == "console":
        await message.channel.send(
            "Enable it on the Main Menu by going to Mods>BaseMod>Config>Enable console.\n"
            + "Then hit ` while in a run."
        )
        return
    if s == "relic:124":
        await message.channel.send(
            "https://github.com/daviscook477/BaseMod/wiki/Custom-Relics#relicstrings"
        )
        return
    if len(s.split(" ")) == 1:
        return

    tokenized_message = tokenize_message(s)
    if (
        message.author.id in banned_users
        and tokenized_message[1] == "bug"
        or tokenized_message[1] == "feedback"
        or tokenized_message[1] == "suggestion"
    ):
        return
    await do_command(message.channel, tokenized_message)


def tokenize_message(message):
    if len(message.split(" ")) >= 3:
        for mod in aliases:
            names = aliases.get(mod)
            if message.split(" ")[1] in names:
                tokenized_message = message.split(" ", 2)
                del tokenized_message[1]
                tokenized_message.insert(1, mod)
                print(tokenized_message)
                return tokenized_message
    if os.path.exists(f'data/{message.split(" ")[1]}.json'):
        return message.split(" ", 2)
    else:
        return message.split(" ", 1)


def check_for_aliases(self, id):
    print(id)
    for mod in aliases:
        mod_aliases = aliases.get(mod)
        if id in mod_aliases:
            return mod


async def do_command(channel, tokenized_message):
    commands = {
        "help": help_command,
        "card": card,
        "relic": relic,
        "keyword": keyword,
        "suggestion": dm_modder,
        "bug": dm_modder,
        "feedback": dm_modder,
    }
    callback = commands.get(tokenized_message[0])
    await callback(channel, tokenized_message)


@client.event
async def dm_modder(channel, tokenized_message):
    if len(tokenized_message) == 2:
        await channel.send("No mod ID or feedback supplied!")
        return
    for id in suggestables:
        mods = suggestables.get(id)
        if tokenized_message[1] in mods:
            modder = await client.fetch_user(id)
            await modder.send(
                tokenized_message[0].capitalize()
                + " for "
                + tokenized_message[1].capitalize()
                + "\n"
                + tokenized_message[2]
            )
            await channel.send(f"Feedback sent to developer of {tokenized_message[1]}!")
            return
    await channel.send(
        f"{tokenized_message[1].capitalize()} does not currently accept feedback."
    )


@client.event
async def card(channel, tokenized_message):
    cards = Mod_Data(tokenized_message[1]).data
    random.shuffle(cards)
    if len(tokenized_message) == 3:
        if tokenized_message[2] == "random" and (
            channel.id == 384046138610941953 or channel.id == 632350690479570950
        ):
            if "mod" in cards[0]:
                await channel.send(
                    card_format(
                        random.choice(cards[0]["cards"]), cards[0]["mod"]["name"]
                    )
                )
                return
            else:
                card = random.choice(cards[0]["cards"])
                await channel.send(card_format(card, card["mod"]))
                return
    if len(tokenized_message) == 2:
        if tokenized_message[1] == "random" and (
            channel.id == 384046138610941953 or channel.id == 632350690479570950
        ):
            mod_object = random.choice(cards)
            if len(mod_object["cards"]) == 0:
                await card(channel, tokenized_message)
                return
            cards_object = random.choice(mod_object["cards"])
            if "mod" in mod_object:
                await channel.send(card_format(cards_object, mod_object["mod"]["name"]))
                return
            else:
                await channel.send(card_format(cards_object, cards_object["mod"]))
                return
    for x in range(len(cards)):
        for card in cards[x]["cards"]:
            if len(tokenized_message) == 3:
                if tokenized_message[2] == card["name"].lower():
                    if "mod" in cards[x]:
                        await channel.send(card_format(card, cards[x]["mod"]["name"]))
                        return
                    else:
                        await channel.send(card_format(card, card["mod"]))
                        return
            else:
                if tokenized_message[1] == card["name"].lower():
                    if "mod" in cards[x]:
                        await channel.send(card_format(card, cards[x]["mod"]["name"]))
                        return
                    else:
                        await channel.send(card_format(card, card["mod"]))
                        return
    if len(tokenized_message) == 3:
        await channel.send(
            f"No card named {tokenized_message[2]} found in {tokenized_message[1]}."
        )
    else:
        await channel.send(f"No card named {tokenized_message[1]} found.")


@client.event
async def relic(channel, tokenized_message):
    relics = Mod_Data(tokenized_message[1]).data
    random.shuffle(relics)
    if "star compass" in tokenized_message:
        await channel.send("Oops, I dropped it. Oh well.")
        return
    if len(tokenized_message) == 3:
        if tokenized_message[2] == "random" and (
            channel.id == 384046138610941953 or channel.id == 632350690479570950
        ):
            if "mod" in relics[0]:
                await channel.send(
                    relic_format(
                        random.choice(relics[0]["relics"]), relics[0]["mod"]["name"]
                    )
                )
                return
            else:
                relic = random.choice(relics[0]["relics"])
                await channel.send(relic_format(relic, relic["mod"]))
                return
    if len(tokenized_message) == 2:
        if tokenized_message[1] == "random" and (
            channel.id == 384046138610941953 or channel.id == 632350690479570950
        ):
            mod_object = random.choice(relics)
            if len(mod_object["relics"]) == 0:
                await relic(channel, tokenized_message)
                return
            relics_object = random.choice(mod_object["relics"])
            if "mod" in mod_object:
                await channel.send(
                    relic_format(relics_object, mod_object["mod"]["name"])
                )
                return
            else:
                await channel.send(relic_format(relics_object, relics_object["mod"]))
                return
    for x in range(len(relics)):
        for relic in relics[x]["relics"]:
            if len(tokenized_message) == 3:
                if tokenized_message[2] == relic["name"].lower():
                    if "mod" in relics[x]:
                        await channel.send(
                            relic_format(relic, relics[x]["mod"]["name"])
                        )
                        return
                    else:
                        await channel.send(relic_format(relic, relic["mod"]))
                        return
            else:
                if tokenized_message[1] == relic["name"].lower():
                    if "mod" in relics[x]:
                        await channel.send(
                            relic_format(relic, relics[x]["mod"]["name"])
                        )
                        return
                    else:
                        await channel.send(relic_format(relic, relic["mod"]))
                        return
    if len(tokenized_message) == 3:
        await channel.send(
            f"No relic named {tokenized_message[2]} found in {tokenized_message[1]}."
        )
    else:
        await channel.send(f"No relic named {tokenized_message[1]} found.")


@client.event
async def keyword(channel, tokenized_message):
    keywords = Mod_Data(tokenized_message[1]).data
    for x in range(len(keywords)):
        for keyword in keywords[x]["keywords"]:
            keyword_name = ""
            split_keyword = keyword["name"].split(":")
            if len(split_keyword) == 2:
                keyword_name = split_keyword[1]
            else:
                keyword_name = split_keyword[0]
            if len(tokenized_message) == 3:
                if tokenized_message[2] == keyword_name.lower():
                    if len(split_keyword) == 2:
                        await channel.send(
                            keyword_format_mod(keyword, keyword_name, split_keyword[0])
                        )
                        return
                    else:
                        await channel.send(keyword_format(keyword, keyword_name))
                        return
            else:
                if tokenized_message[1] == keyword_name.lower():
                    if len(split_keyword) == 2:
                        await channel.send(
                            keyword_format_mod(keyword, keyword_name, split_keyword[0])
                        )
                        return
                    else:
                        await channel.send(keyword_format(keyword, keyword_name))
                        return

    if len(tokenized_message) == 3:
        await channel.send(
            f"No keyword named {tokenized_message[2]} found in {tokenized_message[1]}."
        )
    else:
        await channel.send(f"No keyword named {tokenized_message[1]} found.")


@client.event
async def help_command(channel):
    await channel.send(
        f"I can display modded info with {prefix}card, {prefix}relic or {prefix}keyword!"
        + "\n"
        + f"You can use {prefix}help, {prefix}list or {prefix}contribute to get information!"
        + "\n"
        + f"You can use {prefix}bug, {prefix}feedback or {prefix}suggestion to send information to the developer of certain mods that have opted in."
    )


def card_format(card, id):
    if card["cost"] == "":
        return "**{0}**\n`{1}`  `{2}`  `{3}`  `{4}`\n{5}".format(
            card["name"],
            card["type"],
            card["rarity"],
            card["color"],
            id,
            remove_keyword_prefixes(card["description"]),
        )
    return "**{0}**\n`{1}`  `{2}`  `{3}`  `{4}`  `{5}`\n{6}".format(
        card["name"],
        energy_string(card["cost"]),
        card["type"],
        card["rarity"],
        card["color"],
        id,
        remove_keyword_prefixes(card["description"]),
    )


def relic_format(relic, id):
    if relic["pool"] == "":
        return "**{0}**\n`{1}`  `{2}`\n{3}\n*{4}*".format(
            relic["name"], relic["tier"], id, relic["description"], relic["flavorText"]
        )

    return "**{0}**\n`{1}`  `{2}`  `{3}`\n{4}\n*{5}*".format(
        relic["name"],
        relic["tier"],
        relic["pool"],
        id,
        relic["description"],
        relic["flavorText"],
    )


def keyword_format_mod(keyword, name, mod):
    return "**{0}**\n {1}".format(name.capitalize(), keyword["description"])


def keyword_format(keyword, name):
    return "**{0}**\n{1}".format(name.capitalize(), keyword["description"])


def energy_string(cost):
    if cost == "X" or "0":
        return cost

    cost = int(cost)
    s = ""
    for i in range(0, cost):
        s += "[E] "
    return s


def remove_keyword_prefixes(description):
    description = description.replace("\n", "\n ")
    description = description.split(" ")
    final_description = ""
    for word in description:
        res = uncolor.match(word)
        if res:
            final_description += res.group(1).replace("[]", "", 1) + " "
            continue
        if word.startswith("!"):
            if word.find("!", 1) > 0:
                final_description += "#"
                if word.find("!", 1) + 1 < len(word):
                    final_description += word[word.index("!", 1) + 1 :]
                final_description += " "
                continue
        if is_keyword(word):
            if word.split(":", 1)[1][len(word.split(":", 1)[1]) - 1] == ".":
                final_description += word.split(":", 1)[1]
            else:
                final_description += word.split(":", 1)[1] + " "
            continue
        final_description += word + " "
    final_description = final_description.replace("\n ", "\n")
    return final_description


def is_keyword(word):
    return (
        len(word) > 0
        and not word[0].isupper()
        and ":" in word
        and word.find(":") < len(word) - 1
        and word[word.find(":") + 1] != "\n"
    )


client.run(token)
