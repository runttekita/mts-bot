# bot.py
import os
import json
import discord
from dotenv import load_dotenv
import re
import random
from mtsbotdata import aliases, suggestables
import timeout

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
pin_links = [
    "https://media.discordapp.net/attachments/398373038732738570/543527729077682187/sts-check-the-pins.gif",
    "https://media.discordapp.net/attachments/504438263012917254/542101742377107467/kumikopins.gif",
    "https://cdn.discordapp.com/attachments/504438263012917254/632966857292513320/fireworks.gif",
    "https://cdn.discordapp.com/attachments/504438263012917254/632966856596127745/ruiPins.gif",
]
broken_mod_situation = [
    "Thanks to the 2.0 update changing the game code, many mods that were compatible with 1.1 will probably have bugs or crash when used with 2.0, most mods should be fixed eventually (we hope).",
    "Modders are working in mod fixing for 2.0, plz be patient :)"
]

client = discord.Client()
prefix = "?"

banned_users = []

uncolor = re.compile(r"^\[#[0-9A-Fa-f]{6}\](\S+?)$")
energy = re.compile(r"^(\[[RGBWE]])(.?)$")

default_energy = "<:red_energy:382625376838615061>"

icon_dictionary = { 
    "[R]": "<:red_energy:382625376838615061>", 
    "[G]": "<:green_energy:646206147220471808>", 
    "[B]": "<:blue_energy:668151236003889184>", 
    "[W]": "<:purple_energy:620384758068674560>"
}

color_dictionary = {
    "Red": "<:red_energy:382625376838615061>", 
    "Green":  "<:green_energy:646206147220471808>", 
    "Blue": "<:blue_energy:668151236003889184>", 
    "Purple": "<:purple_energy:620384758068674560>",
    "Colorless": "<:colorless_energy:382625433016991745>"
}

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
    if s == "praise":
        if message.author.id == 132940023522656256:
            await message.channel.send("i love reina <3")
        if message.author.id == 86261397213708288:
            await message.channel.send("i love alchy <3")
        return
    if s == "notneh" and message.author.id == 125669982041276416:
        await message.channel.send("djbtkdkfndn")
        return
    if s == "contribute":
        await message.channel.send(
            "https://github.com/runttekita/mts-bot/blob/master/CONTRIBUTING.md"
        )
        return
    if s == "list":
        await message.channel.send(
            "https://github.com/runttekita/mts-bot/tree/master/data"
        )
        return
    if s == "default":
        await message.channel.send("https://github.com/Gremious/StS-DefaultModBase")
        return
    if s == "pins" or s == "pin":
        await message.channel.send(random.choice(pin_links))
        return
    if s == "brokenmod":
        await message.channel.send(random.choice(broken_mod_situation))
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
    if s == "cardmods":
        await message.channel.send(
            "https://github.com/daviscook477/BaseMod/wiki/CardModifiers"
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
    if s == "cansuggest":
        await message.channel.send(
            "https://github.com/velvet-halation/mts-bot/blob/master/mtsbotdata.py#L32"
        )
    if s == "pathwater":
        await message.channel.send(
            "https://cdn.discordapp.com/attachments/398373038732738570/633779880873689110/FB_IMG_1570999646277.png"
        )
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
        "find": find,
        "findcard": find,
        "findrelic": findrelic,
        "modder": get_mods_by_author,
        "mod": get_mod_info
    }
    callback = commands.get(tokenized_message[0])
    await callback(channel, tokenized_message)


@client.event
async def get_mod_info(channel, tokenized_message):
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
        await channel.send(f"**{tokenized_message[1]}** is not a mod! (Or the author has not uploaded the data to me)")
        return

    # Mod has a file but doesn't have mod info
    if "mod" not in mod[0]:
        # await channel.send(f"**{tokenized_message[1]}** does not have a correctly formatted data file. Complain to the mod author")
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
        await channel.send(f"**{tokenized_message[1]}** does not have a correctly formatted data file. Complain to the mod author")
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

    await channel.send(message)


@client.event
async def get_mods_by_author(channel, tokenized_message):
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
        await channel.send("**%s** does not have any mods" % tokenized_message[1])
    else:
        await channel.send("**%s**\n%s" % (author_name, "  ".join(mod_list)))


@client.event
async def find(channel, tokenized_message):
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
                
            regex = re.compile(data)
            
            failure = "No card "
            if cost is not None:
                failure += "with cost " + cost + " "
            if type is not None:
                failure += "of type " + type + " "
            if rarity is not None:
                failure += "of rarity " + rarity + " "
                
            if len(tokenized_message) == 3:
                failure += f"with {data} in the {search_field} found in {tokenized_message[1]}."
            else:
                failure += f"with {data} in the {search_field} found."
                
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
                await channel.send(message)
                return
            await channel.send(failure)
    except TimeoutError:
        await channel.send("Unable to find a match in time!")


@client.event
async def findrelic(channel, tokenized_message):
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
                
            regex = re.compile(data)
            
            failure = "No relic "
            if color is not None:
                failure += "of color " + color + " "
            if tier is not None:
                failure += "of tier " + tier + " "
                
            if len(tokenized_message) == 3:
                failure += f"with {data} in the {search_field} found in {tokenized_message[1]}."
            else:
                failure += f"with {data} in the {search_field} found."
                
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
                await channel.send(message)
                return
            await channel.send(failure)
    except TimeoutError:
        await channel.send("Unable to find a match in time!")
        

def makeCaps(string):
    split_word = string.split(" ")
    for word in split_word:
        word.capitalize()
        if split_word.index(word) != len(split_word) - 1:
            word += " "
    final_string = ""
    return final_string.join(split_word)


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
    first_match = {}
    other_results = {}
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
                if tokenized_message[1] == card["name"].lower():
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
        await channel.send(message)
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
    first_match = {}
    other_results = {}
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
            else:
                if tokenized_message[1] == relic["name"].lower():
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
        await channel.send(message)
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
        + f"You can use {prefix}help, {prefix}list, {prefix}find or {prefix}contribute to get information!"
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


client.run(token)
