# bot.py
import os
import json
import discord
from dotenv import load_dotenv
import re
import random
from mtsbotdata import aliases, suggestables, wikis
import timeout
import aiohttp

#constants
#any commands to the bot start with this character
prefix = "?"

uncolor = re.compile(r"^\[#[0-9A-Fa-f]{6}\](\S+?)$")
energy = re.compile(r"^(\[[RGBWE]])(.?)$")

#user IDs in this array will be ignored when making suggestions to modders
def banned_users():
    return []

def pin_links():
    return [
        "https://media.discordapp.net/attachments/398373038732738570/543527729077682187/sts-check-the-pins.gif",
        "https://media.discordapp.net/attachments/504438263012917254/542101742377107467/kumikopins.gif",
        "https://cdn.discordapp.com/attachments/504438263012917254/632966857292513320/fireworks.gif",
        "https://cdn.discordapp.com/attachments/504438263012917254/632966856596127745/ruiPins.gif",
    ]


def icon_dictionary():
    return {
        "[E]": "<:red_energy:382625376838615061>",
        "[R]": "<:red_energy:382625376838615061>",
        "[G]": "<:green_energy:646206147220471808>",
        "[B]": "<:blue_energy:668151236003889184>",
        "[W]": "<:purple_energy:620384758068674560>"
    }


def color_dictionary():
    return {
        "Red": "<:red_energy:382625376838615061>",
        "Green":  "<:green_energy:646206147220471808>",
        "Blue": "<:blue_energy:668151236003889184>",
        "Purple": "<:purple_energy:620384758068674560>",
        "Colorless": "<:colorless_energy:382625433016991745>"
    }
default_energy = color_dictionary().get("Red")


def meme_dictionary():
    return {
        "?notneh": not_neh,
        "?praise": praise,
        "big thanks papa kio!": big_thanks,
        "update body text": update_body_text
    }


def help_dictionary():
    return {
        "minimumcards": "When making a new character, upon generating card rewards, the game can crash if there are not enough cards in the pool.\nThe minimum requirements to not crash are:\n - 3 of each rarity to not crash on card rewards (4 if you have question card)\n - 3 of each type to not crash when using attack/skill/power potions\n - 2 attacks, 2 skills, and 1 power to not crash shops\n\n As a temporary solution, you can also give yourself prismatic shard. However, this will not prevent crashing in shops.",
        "contribute": "https://github.com/NellyDevo/mts-bot/blob/master/CONTRIBUTING.md",
        "list": "https://github.com/NellyDevo/mts-bot/tree/master/data",
        "basic": "https://github.com/Alchyr/BasicMod#basic-mod",
        "basicmod": "https://github.com/Alchyr/BasicMod#basic-mod",
        "xy": "http://xyproblem.info/",
        "debugger": "https://stackoverflow.com/questions/25385173/what-is-a-debugger-and-how-can-it-help-me-diagnose-problems",
        "optin": "https://github.com/NellyDevo/mts-bot/blob/master/README.md#opt-in-for-receiving-feedback",
        "console": "Enable it on the Main Menu by going to Mods>BaseMod>Config>Enable console.\nThen hit ` while in a run.",
        "124": "https://github.com/daviscook477/BaseMod/wiki/Custom-Relics#relicstrings",
        "126": "https://github.com/daviscook477/BaseMod/wiki/Custom-Relics#relicstrings",
        "relic:124": "https://github.com/daviscook477/BaseMod/wiki/Custom-Relics#relicstrings",
        "relic:126": "https://github.com/daviscook477/BaseMod/wiki/Custom-Relics#relicstrings",
        "cansuggest": "https://github.com/NellyDevo/mts-bot/blob/master/mtsbotdata.py#L32",
        "clipper": "https://github.com/JohnnyBazooka89/StSModdingToolCardImagesCreator",
        "cardartclipper": "https://github.com/JohnnyBazooka89/StSModdingToolCardImagesCreator",
        "artclipper": "https://github.com/JohnnyBazooka89/StSModdingToolCardImagesCreator"
    }


#let's try to keep these in order
def commands_dictionary():
    return {
        "info": info_command,
        "suggestion": dm_modder,
        "bug": dm_modder,
        "feedback": dm_modder,
        "wiki": wiki,
        "pins": pins,
        "pin": pins,
        "modder": get_mods_by_author,
        "mod": get_mod_info,
        "card": card,
        "find": find,
        "findcard": find,
        "relic": relic,
        "findrelic": findrelic,
        "keyword": keyword,
        "potion": potion
    }

def commands_info():
    return {
        "info": f"I can display modded info with {prefix}card, {prefix}relic or {prefix}keyword!\nYou can use {prefix}info [command], {prefix}list, {prefix}find or {prefix}contribute to get information!\nYou can use {prefix}bug, {prefix}feedback or {prefix}suggestion to send information to the developer of certain mods that have opted in.",
        "suggestion": f"The {prefix}suggestion command expects a mod id followed by whatever suggestion you might have. If the author has {prefix}optin, they will receive the suggestion.",
        "bug": f"The {prefix}bug command expects a mod id followed by whatever bug you might have found. If the author has {prefix}optin, they will receive the bug report.",
        "feedback": f"The {prefix}suggestion command expects a mod id followed by whatever suggestion you might have. If the author has {prefix}optin, they will receive the suggestion.",
        "wiki": f"""
The {prefix}wiki command will attempt to find a given wiki page from any github wikis in my database. If it matches a page found in my database, I will link it.

The command's anatomy looks as follows:
{prefix}wiki [optional: name of wiki] [name of page]

You can also retrieve the homepage of a wiki by just using {prefix}wiki [name of wiki]
""",
        "modder": f"The {prefix}modder command expects a name. If that name is in my database, I will list all mods by that author.",
        "mod": f"The {prefix}mod command expects a name. If that name is in my database, I will list information about that mod.",
        "card": f"""
The {prefix}card command will attempt to find a card matching the name sent to this command.

The command's anatomy looks as follows:
{prefix}card [optional: name of mod] [name of card]

If you are in the <#384046138610941953> channel, you can also run it with "random" in place of the card name to retrieve a random card.
""",
        "find": f"""
The {prefix}find command will attempt to find a card containing card text sent to this command.

The command's anatomy looks as follows:
{prefix}find [args] [text]

[args] can be any combination of the following arguments:
-n indicates I should search name rather than description
-c=[amount] specifies a card cost
-t=[type] to specify card type (attack, skill, etc)
-r=[rarity] to specify rarity (basic, common, etc)
""",
        "findcard": f"""
The {prefix}find command will attempt to find a card containing text sent to this command.

The command's anatomy looks as follows:
{prefix}find [args] [text]

[args] can be any combination of the following arguments:
-n indicates I should search name rather than description
-c=[amount] specifies a card cost
-t=[type] to specify card type (attack, skill, etc)
-r=[rarity] to specify rarity (basic, common, etc)
""",
        "relic": f"""
The {prefix}relic command will attempt to find a relic matching the name sent to this command.

The command's anatomy looks as follows:
{prefix}card [optional: name of mod] [name of relic]

If you are in the <#384046138610941953> channel, you can also run it with "random" in place of the relic name to retrieve a random relic.
""",
        "findrelic": f"""
The {prefix}findrelic command will attempt to find a relic containing text sent to this command.

The command's anatomy looks as follows:
{prefix}findrelic [args] [text]

[args] can be any combination of the following arguments:
-n indicates I should search name rather than description
-c=[color] to specify a color
-t=[tier] to specify tier (boss, common, etc)
""",
        "keyword": "The ?keyword command expects the name of a keyword. If it matches a keyword found in my database, I will list information about that keyword.",
        "potion": f"""
The {prefix}potion command will attempt to find a potion matching the name sent to this command.

The command's anatomy looks as follows:
{prefix}card [optional: name of mod] [name of potion]

If you are in the <#384046138610941953> channel, you can also run it with "random" in place of the card name to retrieve a random potion.
"""
    }

client = discord.Client()
session = aiohttp.ClientSession()
load_dotenv()
token = os.getenv("DISCORD_TOKEN")


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


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    lowercase = message.content.lower()
    if (isinstance(message.channel, discord.channel.DMChannel) and message.author.id == 138858311410909184):
        if (lowercase.startswith("?sentient ")):
            tokenized_message = tokenize_message(message.content)
            ind = 1
            found_channel = None
            default_channel = None
            for server in client.guilds:
                for channel in server.channels:
                    if channel.id == tokenized_message[ind]:
                        found_channel = channel
                    if channel.id == 398373038732738570:
                        default_channel = channel

            if found_channel is not None:
                ind = 2
            else:
                if default_channel is not None:
                    found_channel = default_channel
                else:
                    found_channel = message.channel
            if len(tokenized_message) < ind:
                return
            toSend = " ".join(tokenized_message[ind:])
            await found_channel.send(toSend)
    if is_modding_channel(message.channel):
        if (
            "🦊" in message.author.display_name
            and ("🦊" in lowercase or "fox" in lowercase)
            and message.author.id != 258676126090657793
        ):
            await message.add_reaction("🦊")
    memes = meme_dictionary()
    if lowercase in memes:
        callback = memes.get(lowercase)
        if callback is not None:
            reply = callback(message)
            if reply is not None:
                await message.channel.send(reply)
                return
    if is_command(message):
        print(message.content)
        message.content = del_char(message.content, len(prefix))
        await get_id(message)


async def get_id(message):
    lowercase = message.content.lower()
    
    help = help_dictionary()
    if lowercase in help:
        reply = help.get(lowercase)
        await send_with_ping(reply, message)

    tokenized_message = []
    if len(lowercase.split(" ")) == 1:
        tokenized_message = [lowercase]
    else:
        tokenized_message = tokenize_message(lowercase)
    await do_command(message.channel, tokenized_message, message)


async def do_command(channel, tokenized_message, discord_message):
    commands = commands_dictionary()
    if tokenized_message[0] != "pins" and tokenized_message[0] != "pin" and len(tokenized_message) == 1:
        if tokenized_message[0] in commands:
            tokenized_message = ["info", tokenized_message[0]]
        else:
            return
    if tokenized_message[0] in commands:
        callback = commands.get(tokenized_message[0])
        if callback is not None:
            await callback(channel, tokenized_message, discord_message)


#commands go here (let's try to keep them in order)
@client.event
async def info_command(channel, tokenized_message, discord_message):
    query = ""
    replies = commands_info()
    if len(tokenized_message) != 1 and tokenized_message[1] in replies:
        query = tokenized_message[1]
    else:
        query = "info"
    reply = replies.get(query)
    await send_with_ping(reply, discord_message)


@client.event
async def dm_modder(channel, tokenized_message, discord_message):
    if discord_message.author.id in banned_users():
        return
    if len(tokenized_message) == 2:
        await send_with_ping("No mod ID or feedback supplied!", discord_message)
        return
    for id in suggestables:
        mods = suggestables.get(id)
        if tokenized_message[1] in mods:
            modder = await client.fetch_user(id)
            await modder.send(
                tokenized_message[0].capitalize()
                + " from " + discord_message.author.name + " for "
                + tokenized_message[1].capitalize()
                + "\n"
                + tokenized_message[2]
            )
            await send_with_ping(f"Feedback sent to developer of {tokenized_message[1]}!", discord_message)
            return
    await send_with_ping(
        f"{tokenized_message[1].capitalize()} does not currently accept feedback.",
        discord_message
    )


@client.event
async def wiki(channel, tokenized_message, discord_message):
    tokenized_message = discord_message.content.split(" ")
    wiki_site = None
    if tokenized_message[1] in wikis:
        wiki_site = wikis.get(tokenized_message[1])
    index = 1
    if wiki_site is not None:
        if len(tokenized_message) == 2:
            await send_with_ping(wiki_site, discord_message)
            return
        index = 2
    page = "-".join(tokenized_message[index:])
    if wiki_site is not None:
        wiki_page = wiki_site + page
        if await page_exists(wiki_page):
            await send_with_ping(wiki_page, discord_message)
            return
    else:
        for site in wikis.values():
            wiki_page = site + page
            if await page_exists(wiki_page):
                await send_with_ping(wiki_page, discord_message)
                return
    await discord_message.add_reaction("📑")
    await discord_message.add_reaction("❌")


@client.event
async def pins(channel, tokenized_message, discord_message):
    await send_with_ping(random.choice(pin_links()), discord_message)


@client.event
async def get_mods_by_author(channel, tokenized_message, discord_message):
    mod_list = []
    author_name = "reina" if tokenized_message[1] == "reina" else None
    for mod in Mod_Data("").data:
        if (
            "mod" in mod
            and "authors" in mod["mod"]
            and tokenized_message[1]
            in [author.lower() for author in mod["mod"]["authors"]]
        ):
            mod_list.append("`%s`" % mod["mod"]["name"])
            if author_name is None:
                author_name = mod["mod"]["authors"][
                    [author.lower() for author in mod["mod"]["authors"]].index(
                        tokenized_message[1]
                    )
                ]  # Ugly way to get the correct caps for a name since tokenized_message is always lowercase
    if len(mod_list) == 0:
        await send_with_ping("**%s** does not have any mods" % tokenized_message[1], discord_message)
    else:
        await send_with_ping("**%s**\n%s" % (author_name, "  ".join(mod_list)), discord_message)


@client.event
async def get_mod_info(channel, tokenized_message, discord_message):
    """
    Get the info for a mod for the `?mod` command

    Example: ?mod challengethespire
    Input:  ["mod", "challengethespire"]
    Output: **Challenge The Spire**
            Author:	alexdriedger
            Boss Rush, Elite Rush, & Sneaky Strike!! Challenge The Spire adds a variety of challenge modes to Slay The Spire.

    :param channel: Channel to send message to
    :param tokenized_message: List of Strings with length == 2. The first string should be "mod" and the second string
                                should be the file name (without the .json) of the mod to get information about
    :return: None
    """
    mod = Mod_Data(tokenized_message[1]).data

    # If a mod name is supplied that a file doesn't exist for, `Mod_Data` will load all mod data
    if len(mod) != 1:
        await send_with_ping(f"**{tokenized_message[1]}** is not a mod! (Or the author has not uploaded the data to me)", discord_message)
        return

    # Mod has a file but doesn't have mod info
    if "mod" not in mod[0]:
        # await send_with_ping(f"**{tokenized_message[1]}** does not have a correctly formatted data file. Complain to the mod author", discord_message)
        print(f"**{tokenized_message[1]}** does not have a correctly formatted data file. Complain to the mod author")
        return

    mod_data = mod[0]["mod"]

    # Check if the file is incorrectly formatted
    if (
        mod_data["name"] is None
        or mod_data["authors"] is None
        or len(mod_data["authors"]) == 0
        or mod_data["description"] is None
    ):
        await send_with_ping(f"**{tokenized_message[1]}** does not have a correctly formatted data file. Complain to the mod author", discord_message)
        return

    # Formatted message should resemble
    # My Awesome Mod
    # Author: Casey Yano
    # This mod makes the spire more awesome by updating body text

    message = f"""**{mod_data["name"]}**\n"""

    message += "Authors:\t" if len(mod_data["authors"]) > 1 else "Author:\t"
    for author in mod_data["authors"]:
        message += author
        message += ", "
    message = message[: -2]  # Remove last comma and space
    message += "\n"

    message += mod_data["description"]

    await send_with_ping(message, discord_message)


@client.event
async def card(channel, tokenized_message, discord_message):
    cards = Mod_Data(tokenized_message[1]).data
    random.shuffle(cards)
    first_match = {}
    other_results = {}
    if len(tokenized_message) == 3:
        if tokenized_message[2] == "random" and channel.id == 384046138610941953:
            if "mod" in cards[0]:
                await send_with_ping(
                    card_format(
                        random.choice(cards[0]["cards"]), cards[0]["mod"]["name"]
                    ),
                    discord_message
                )
                return
            else:
                card_object = random.choice(cards[0]["cards"])
                await send_with_ping(card_format(card_object, card_object["mod"]), discord_message)
                return
    if len(tokenized_message) == 2:
        if tokenized_message[1] == "random" and channel.id == 384046138610941953:
            mod_object = random.choice(cards)
            if len(mod_object["cards"]) == 0:
                await card(channel, tokenized_message, discord_message)
                return
            cards_object = random.choice(mod_object["cards"])
            if "mod" in mod_object:
                await send_with_ping(card_format(cards_object, mod_object["mod"]["name"]), discord_message)
                return
            else:
                await send_with_ping(card_format(cards_object, cards_object["mod"]), discord_message)
                return
    for x in range(len(cards)):
        for card_object in cards[x]["cards"]:
            if len(tokenized_message) == 3:
                if tokenized_message[2] == card_object["name"].lower():
                    if "mod" in cards[x]:
                        if not first_match:
                            first_match.update({cards[x]["mod"]["name"]: card_object})
                        else:
                            if len(other_results) < 3:
                                other_results.update(
                                    {cards[x]["mod"]["name"]: card_object["name"]}
                                )
                    else:
                        if not first_match:
                            first_match.update({card_object["mod"]: card_object})
                        else:
                            if len(other_results) < 3:
                                other_results.update({card_object["mod"]: card_object["name"]})
            else:
                if tokenized_message[1] == card_object["name"].lower():
                    if "mod" in cards[x]:
                        if not first_match:
                            first_match.update({cards[x]["mod"]["name"]: card_object})
                        else:
                            if len(other_results) < 3:
                                other_results.update(
                                    {cards[x]["mod"]["name"]: card_object["name"]}
                                )
                    else:
                        if not first_match:
                            first_match.update({card_object["mod"]: card_object})
                        else:
                            if len(other_results) < 3:
                                other_results.update({card_object["mod"]: card_object["name"]})
    message = ""
    if first_match:
        for key in first_match:
            message += card_format(first_match.get(key), key) + "\n"
        if len(other_results) > 3:
            other_results = other_results[:2]
        if other_results:
            message += "Other matches include:\n"
            for match in other_results:
                name = other_results.get(match)
                message += f"`{makeCaps(name)} from {makeCaps(match)}`  "
        await send_with_ping(message, discord_message)
        return

    await discord_message.add_reaction("🃏")
    await discord_message.add_reaction("❌")
    #if len(tokenized_message) == 3:
    #    await send_with_ping(
    #        f"No card named {tokenized_message[2]} found in {tokenized_message[1]}.",
    #        discord_message
    #    )
    #else:
    #    await send_with_ping(f"No card named {tokenized_message[1]} found.", discord_message)


@client.event
async def find(channel, tokenized_message, discord_message):
    """
    find a card
    -n causes to search name rather than description
    -c=amount specifies a card cost
    -t=attack/skill/power to specify card type
    -r= to specify rarity
    """
    try:
        with timeout.timeout(1):
            cards = Mod_Data(tokenized_message[1]).data
            random.shuffle(cards)
            first_match = {}
            other_results = {}

            search_field = "description"
            cost = None
            type = None
            rarity = None

            if len(tokenized_message) == 3:
                tokens = tokenized_message[2].split()
            else:
                tokens = tokenized_message[1].split()

            data = ""

            for item in tokens:
                if data == "": # Once any value is found, the rest should be input regex
                    if item == "-n" and search_field != "name":
                        search_field = "name"
                        continue
                    if cost is None and item.startswith("-c=") and len(item) > 3:
                        cost = item[3:]
                        continue
                    if type is None and item.startswith("-t=") and len(item) > 3:
                        type = item[3:]
                        continue
                    if rarity is None and item.startswith("-r=") and len(item) > 3:
                        rarity = item[3:]
                        continue

                data += item + " "

            data = data[:-1]

            if data == "":
                data = "^[\s\S]*$"

            regex = None
            try:
                regex = re.compile(data)
            except re.error:
                data = re.escape(data)
                regex = re.compile(data)

            #failure = "No card "
            #if cost is not None:
            #    failure += "with cost " + cost + " "
            #if type is not None:
            #    failure += "of type " + type + " "
            #if rarity is not None:
            #    failure += "of rarity " + rarity + " "
            #
            #if len(tokenized_message) == 3:
            #    failure += f"with {data} in the {search_field} found in {tokenized_message[1]}."
            #else:
            #    failure += f"with {data} in the {search_field} found."

            for x in range(len(cards)):
                for card in cards[x]["cards"]:
                    if cost is not None and card["cost"].lower() != cost:
                        continue
                    if type is not None and card["type"].lower() != type:
                        continue
                    if rarity is not None and card["rarity"].lower() != rarity:
                        continue

                    if len(tokenized_message) == 3:
                        if regex.search(card[search_field].lower()):
                            if "mod" in cards[x]:
                                if not first_match:
                                    first_match.update({cards[x]["mod"]["name"]: card})
                                else:
                                    if len(other_results) < 3:
                                        other_results.update(
                                            {cards[x]["mod"]["name"]: card["name"]}
                                        )
                            else:
                                if not first_match:
                                    first_match.update({card["mod"]: card})
                                else:
                                    if len(other_results) < 3:
                                        other_results.update({card["mod"]: card["name"]})
                    else:
                        if regex.search(card[search_field].lower()):
                            if "mod" in cards[x]:
                                if not first_match:
                                    first_match.update({cards[x]["mod"]["name"]: card})
                                else:
                                    if len(other_results) < 3:
                                        other_results.update(
                                            {cards[x]["mod"]["name"]: card["name"]}
                                        )
                            else:
                                if not first_match:
                                    first_match.update({card["mod"]: card})
                                else:
                                    if len(other_results) < 3:
                                        other_results.update({card["mod"]: card["name"]})
            message = ""
            if first_match:
                for key in first_match:
                    message += card_format(first_match.get(key), key) + "\n"
                if len(other_results) > 3:
                    other_results = other_results[:2]
                if other_results:
                    message += "Other matches include:\n"
                    for match in other_results:
                        name = other_results.get(match)
                        message += f"`{makeCaps(name)} from {makeCaps(match)}`  "
                await send_with_ping(message, discord_message)
                return
            await discord_message.add_reaction("🃏")
            await discord_message.add_reaction("❌")
            #await send_with_ping(failure, discord_message)
    except TimeoutError:
        await discord_message.add_reaction("⏰")
        await discord_message.add_reaction("❌")
        #await send_with_ping("Unable to find a match in time!", discord_message)


@client.event
async def relic(channel, tokenized_message, discord_message):
    relics = Mod_Data(tokenized_message[1]).data
    random.shuffle(relics)
    first_match = {}
    other_results = {}
    if "star compass" in tokenized_message:
        await send_with_ping("Oops, I dropped it. Oh well.", discord_message)
        return
    if len(tokenized_message) == 3:
        if tokenized_message[2] == "random" and channel.id == 384046138610941953:
            if "mod" in relics[0]:
                await send_with_ping(
                    relic_format(
                        random.choice(relics[0]["relics"]), relics[0]["mod"]["name"]
                    ),
                    discord_message
                )
                return
            else:
                relic_object = random.choice(relics[0]["relics"])
                await send_with_ping(relic_format(relic_object, relic_object["mod"]), discord_message)
                return
    if len(tokenized_message) == 2:
        if tokenized_message[1] == "random" and channel.id == 384046138610941953:
            mod_object = random.choice(relics)
            if len(mod_object["relics"]) == 0:
                await relic(channel, tokenized_message, discord_message)
                return
            relics_object = random.choice(mod_object["relics"])
            if "mod" in mod_object:
                await send_with_ping(
                    relic_format(relics_object, mod_object["mod"]["name"]),
                    discord_message
                )
                return
            else:
                await send_with_ping(relic_format(relics_object, relics_object["mod"]), discord_message)
                return
    for x in range(len(relics)):
        for relic_object in relics[x]["relics"]:
            if len(tokenized_message) == 3:
                if tokenized_message[2] == relic_object["name"].lower():
                    if "mod" in relics[x]:
                        if not first_match:
                            first_match.update({relics[x]["mod"]["name"]: relic_object})
                        else:
                            if len(other_results) < 3:
                                other_results.update(
                                    {relics[x]["mod"]["name"]: relic_object["name"]}
                                )
                    else:
                        if not first_match:
                            first_match.update({relic_object["mod"]: relic_object})
                        else:
                            if len(other_results) < 3:
                                other_results.update({relic_object["mod"]: relic_object["name"]})
            else:
                if tokenized_message[1] == relic_object["name"].lower():
                    if "mod" in relics[x]:
                        if not first_match:
                            first_match.update({relics[x]["mod"]["name"]: relic_object})
                        else:
                            if len(other_results) < 3:
                                other_results.update(
                                    {relics[x]["mod"]["name"]: relic_object["name"]}
                                )
                    else:
                        if not first_match:
                            first_match.update({relic_object["mod"]: relic_object})
                        else:
                            if len(other_results) < 3:
                                other_results.update({relic_object["mod"]: relic_object["name"]})
    message = ""
    if first_match:
        for key in first_match:
            message += relic_format(first_match.get(key), key) + "\n"
        if len(other_results) > 3:
            other_results = other_results[:2]
        if other_results:
            message += "Other matches include:\n"
            for match in other_results:
                name = other_results.get(match)
                message += f"`{makeCaps(name)} from {makeCaps(match)}`  "
        await send_with_ping(message, discord_message)
        return

    await discord_message.add_reaction("<:derpRock:509737899504304135>")
    await discord_message.add_reaction("❌")
    #if len(tokenized_message) == 3:
    #    await send_with_ping(
    #        f"No relic named {tokenized_message[2]} found in {tokenized_message[1]}.",
    #        discord_message
    #    )
    #else:
    #    await send_with_ping(f"No relic named {tokenized_message[1]} found.", discord_message)


@client.event
async def findrelic(channel, tokenized_message, discord_message):
    """
    find a relic
    -n causes to search name rather than description
    -c= to specify a color
    -t= to specify tier
    """
    try:
        with timeout.timeout(1):
            relics = Mod_Data(tokenized_message[1]).data
            random.shuffle(relics)
            first_match = {}
            other_results = {}

            search_field = "description"
            tier = None
            color = None

            if len(tokenized_message) == 3:
                tokens = tokenized_message[2].split()
            else:
                tokens = tokenized_message[1].split()

            data = ""

            for item in tokens:
                if data == "": # Once any value is found, the rest should be input regex
                    if item == "-n" and search_field != "name":
                        search_field = "name"
                        continue
                    if color is None and item.startswith("-c=") and len(item) > 3:
                        color = item[3:]
                        continue
                    if tier is None and item.startswith("-t=") and len(item) > 3:
                        tier = item[3:]
                        continue

                data += item + " "

            data = data[:-1]

            if data == "":
                data = "^[\s\S]*$"

            regex = None
            try:
                regex = re.compile(data)
            except re.error:
                data = re.escape(data)
                regex = re.compile(data)

            #failure = "No relic "
            #if color is not None:
            #    failure += "of color " + color + " "
            #if tier is not None:
            #    failure += "of tier " + tier + " "
            #
            #if len(tokenized_message) == 3:
            #    failure += f"with {data} in the {search_field} found in {tokenized_message[1]}."
            #else:
            #    failure += f"with {data} in the {search_field} found."

            for x in range(len(relics)):
                for relic in relics[x]["relics"]:
                    if tier is not None and relic["tier"].lower() != tier:
                        continue
                    if color is not None and relic["pool"].lower() != color:
                        continue

                    if regex.search(relic[search_field].lower()):
                        if "mod" in relics[x]:
                            if not first_match:
                                first_match.update({relics[x]["mod"]["name"]: relic})
                            else:
                                if len(other_results) < 3:
                                    other_results.update(
                                        {relics[x]["mod"]["name"]: relic["name"]}
                                    )
                        else:
                            if not first_match:
                                first_match.update({relic["mod"]: relic})
                            else:
                                if len(other_results) < 3:
                                    other_results.update({relic["mod"]: relic["name"]})

            message = ""
            if first_match:
                for key in first_match:
                    message += relic_format(first_match.get(key), key) + "\n"
                if len(other_results) > 3:
                    other_results = other_results[:2]
                if other_results:
                    message += "Other matches include:\n"
                    for match in other_results:
                        name = other_results.get(match)
                        message += f"`{makeCaps(name)} from {makeCaps(match)}`  "
                await send_with_ping(message, discord_message)
                return

            await discord_message.add_reaction("<:derpRock:509737899504304135>")
            await discord_message.add_reaction("❌")
            #await send_with_ping(failure, discord_message)
    except TimeoutError:
        await discord_message.add_reaction("⏰")
        await discord_message.add_reaction("❌")
        #await send_with_ping("Unable to find a match in time!", discord_message)


@client.event
async def keyword(channel, tokenized_message, discord_message):
    keywords = Mod_Data(tokenized_message[1]).data
    for x in range(len(keywords)):
        if "keywords" in keywords[x]:
            for keyword in keywords[x]["keywords"]:
                keyword_name = ""
                if "name" in keyword:
                    split_keyword = keyword["name"].split(":")
                    if len(split_keyword) == 2:
                        keyword_name = split_keyword[1]
                    else:
                        keyword_name = keyword["name"]
                    if len(tokenized_message) == 3:
                        if tokenized_message[2] == keyword_name.lower():
                            if len(split_keyword) == 2:
                                mod_name = split_keyword[0]
                                if "mod" in keywords[x]:
                                    if "name" in keywords[x]["mod"]:
                                        mod_name = keywords[x]["mod"]["name"]
                                
                                await send_with_ping(
                                    keyword_format_mod(keyword, keyword_name, mod_name), discord_message
                                )
                                return
                            else:
                                await send_with_ping(keyword_format(keyword, keyword_name), discord_message)
                                return
                    else:
                        if tokenized_message[1] == keyword_name.lower():
                            if "mod" in keywords[x]:
                                if "name" in keywords[x]["mod"]:
                                    await send_with_ping(
                                        keyword_format_mod(keyword, keyword_name, keywords[x]["mod"]["name"]), discord_message
                                    )
                                    return
                            if len(split_keyword) == 2:
                                await send_with_ping(
                                    keyword_format_mod(keyword, keyword_name, split_keyword[0]), discord_message
                                )
                                return
                            else:
                                await send_with_ping(keyword_format(keyword, keyword_name), discord_message)
                                return

    await discord_message.add_reaction("🔑")
    await discord_message.add_reaction("❌")
    #if len(tokenized_message) == 3:
    #    await send_with_ping(
    #        f"No keyword named {tokenized_message[2]} found in {tokenized_message[1]}.",
    #        discord_message
    #    )
    #else:
    #    await send_with_ping(f"No keyword named {tokenized_message[1]} found.", discord_message)


@client.event
async def potion(channel, tokenized_message, discord_message):
    potions = Mod_Data(tokenized_message[1]).data
    random.shuffle(potions)
    first_match = {}
    other_results = {}
    if len(tokenized_message) == 3:
        if tokenized_message[2] == "random" and (
            channel.id == 384046138610941953 or channel.id == 632350690479570950
        ):
            message = ""
            if "mod" in potions[0]:
                message = potion_format(random.choice(potions[0]["potions"]), potions[0]["mod"]["name"])
            else:
                potion_object = random.choice(potions[0]["potions"])
                message = potion_format(potion_object, potion_object["mod"])
            await send_with_ping(message, discord_message)
            return
    if len(tokenized_message) == 2:
        if tokenized_message[1] == "random" and (
            channel.id == 384046138610941953 or channel.id == 632350690479570950
        ):
            mod_object = random.choice(potions)
            if len(mod_object["potions"]) == 0:
                await potion(channel, tokenized_message, discord_message)
                return
            message = ""
            potions_object = random.choice(mod_object["potions"])
            if "mod" in mod_object:
                message = potion_format(potions_object, mod_object["mod"]["name"])
            else:
                message = potion_format(potions_object, potions_object["mod"])
            await send_with_ping(message, discord_message)
    for x in range(len(potions)):
        for potion_object in potions[x]["potions"]:
            if len(tokenized_message) == 3:
                if tokenized_message[2] == potion_object["name"].lower():
                    if "mod" in potions[x]:
                        if not first_match:
                            first_match.update({potions[x]["mod"]["name"]: potion_object})
                        else:
                            if len(other_results) < 3:
                                other_results.update(
                                    {potions[x]["mod"]["name"]: potion_object["name"]}
                                )
                    else:
                        if not first_match:
                            first_match.update({potion_object["mod"]: potion_object})
                        else:
                            if len(other_results) < 3:
                                other_results.update({potion_object["mod"]: potion_object["name"]})
            else:
                if tokenized_message[1] == potion_object["name"].lower():
                    if "mod" in potions[x]:
                        if not first_match:
                            first_match.update({potions[x]["mod"]["name"]: potion_object})
                        else:
                            if len(other_results) < 3:
                                other_results.update(
                                    {potions[x]["mod"]["name"]: potion_object["name"]}
                                )
                    else:
                        if not first_match:
                            first_match.update({potion_object["mod"]: potion_object})
                        else:
                            if len(other_results) < 3:
                                other_results.update({potion_object["mod"]: potion_object["name"]})
    message = ""
    if first_match:
        for key in first_match:
            message += potion_format(first_match.get(key), key) + "\n"
        if len(other_results) > 3:
            other_results = other_results[:2]
        if other_results:
            message += "Other matches include:\n"
            for match in other_results:
                name = other_results.get(match)
                message += f"`{makeCaps(name)} from {makeCaps(match)}`  "
        await send_with_ping(message, discord_message)
        return

    await discord_message.add_reaction("🥤")
    await discord_message.add_reaction("❌")
    #if len(tokenized_message) == 3:
    #    await send_with_ping(
    #        f"No potion named {tokenized_message[2]} found in {tokenized_message[1]}.",
    #        discord_message
    #    )
    #else:
    #    await send_with_ping(f"No potion named {tokenized_message[1]} found.", discord_message)


#utility methods go here
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


def makeCaps(string):
    split_word = string.split(" ")
    for word in split_word:
        word.capitalize()
        if split_word.index(word) != len(split_word) - 1:
            word += " "
    final_string = ""
    return final_string.join(split_word)


def energy_replace(strIn):
    retVal = strIn
    for key, value in icon_dictionary().items():
        retVal = retVal.replace(key, value)
    return retVal


def card_format(card, id):
    if card["cost"] == "":
        return energy_replace("**{0}**\n`{1}`  `{2}`  `{3}`  `{4}`\n{5}".format(
            card["name"],
            card["type"],
            card["rarity"],
            card["color"],
            id,
            remove_keyword_prefixes(card["description"]),
        ))
    return energy_replace("**{0}**\n`{1}`  `{2}`  `{3}`  `{4}`  `{5}`\n{6}".format(
        card["name"],
        energy_string(card["cost"]),
        card["type"],
        card["rarity"],
        card["color"],
        id,
        remove_keyword_prefixes(card["description"]),
    ))


def relic_format(relic, id):
    if relic["pool"] == "":
        return energy_replace("**{0}**\n`{1}`  `{2}`\n{3}\n*{4}*".format(
            relic["name"], relic["tier"], id, relic["description"], relic["flavorText"]
        ))

    return energy_replace("**{0}**\n`{1}`  `{2}`  `{3}`\n{4}\n*{5}*".format(
        relic["name"],
        relic["tier"],
        relic["pool"],
        id,
        relic["description"],
        relic["flavorText"],
    ))


def potion_format(potion, id):
    return "**{0}**\n`{1}`  `{2}`\n{3}".format(
        potion["name"], potion["rarity"], id, potion["description"]
    )


def keyword_format_mod(keyword, name, mod):
    return "**{0}** ({1})\n{2}".format(name.capitalize(), mod, keyword["description"])


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
                final_description += word.split(":", 1)[1].replace("_", " ")
            else:
                final_description += word.split(":", 1)[1].replace("_", " ") + " "
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


def check_for_aliases(self, id):
    print(id)
    for mod in aliases:
        mod_aliases = aliases.get(mod)
        if id in mod_aliases:
            return mod


def is_command(message):
    return message.content.startswith(prefix)


def del_char(string, index):
    return string[1:]


def is_modding_channel(channel):
    return channel.id == 398373038732738570 or channel.id == 724725673578463232


async def page_exists(wiki_page):
    response = await session.get(wiki_page)
    if (response.status >= 300):
        return False
    text = await response.text()
    return "<title>Home" not in text


async def send_with_ping(message, discord_message):
    if not is_modding_channel(discord_message.channel):
        message += "\n<@" + str(discord_message.author.id) + ">"
    sent = await discord_message.channel.send(message)
    if discord_message.author.id == 115569858724233216 and random.randrange(0, 10) == 0:
        await sent.add_reaction("👀")
        await sent.add_reaction("😤")
        await sent.add_reaction("👍")
        await sent.add_reaction("👆")


#meme methods go below this point
def not_neh(discord_message):
    if discord_message.author.id == 125669982041276416:
        return "djbtkdkfndn"
    return None


def praise(discord_message):
    if discord_message.author.id == 132940023522656256:
        return "i love reina <3"
    if discord_message.author.id == 86261397213708288:
        return "i love alchy <3"
    if discord_message.author.id == 138858311410909184:
        return "i love reina AND alchy <3"
    return None


def big_thanks(discord_message):
    if discord_message.author.id == 95258954090676224:
        return "Big thanks papa Kio!"
    return None


def update_body_text(discord_message):
    if discord_message.author.id == 114667440507453441:
        return "UPDATE BODY TEXT"
    return None


#start the bot
client.run(token)
