import json
import os
from random import randint
import telebot

from actions import is_not_able_to_move, check_boots, save_to_market, save_to_userfile, load_from_userfile, \
    count_calories, stashResources, cResources, load_from_market
from classes import *
from settings import RECIPIENT, MEMO

# Read API key
API_KEY = os.environ["API_KEY"]
# Create bot object
bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=["explore", "e"])
def bot_explore(message):
    name = message.from_user.username
    print(f"{name} {message.text}")
    if len(message.text.split()) == 1:
        bot.send_message(
            message.chat.id,
            f"🚶‍♂️ EXPLORE 🚶‍♂️\n\n"
            f"Explore is the command that allows you to send your Collectors into exploration "
            f"in order to find a random terrain type, with rewards that vary depending on its type.\n\n"
            f"Each exploration will place your collector farther from home up to a maximum "
            f"of 4 Units of Distance.\n\nThis command costs 50 energy, yet this cost can be reduced by or "
            f"offset depending on the equipment held by the collector.\n\n To start exploring with "
            f"a Collector use the command:\n/explore <Collector nr>\nReplace <Collector nr> with the number "
            f"of the collector you want to perform the action with.\n\n Once your collector successfuly "
            f"explores, a new NFT will be added to his inventory.\n\nIn case of doubt use /inv or "
            f"/inv <Collector nr> To find more info.\n\nRemember that in order to redeem the items you "
            f"earned you need to take your collector /home or /teleport 🔮 his items. Alternatively there "
            f"are many ways to use your earnings 'in game', to earn even more. /list will show you all the "
            f"possibilities you have at hand!\n\n"
            f"End of report 🧐",
        )
    elif len(message.text.split()) == 2:
        user = User.get_or_none(User.name==name)
        collector_number = int(message.text.split()[1]) - 1
        collector_data = Collector.get_or_none(Collector.owner==User, Collector.number==collector_number)
        collector_inv = len(Inventory.get_or_none(Inventory.owner==User, Inventory.holder==collector_number))
        equipment = Equipment.get_or_none(Equipment.owner==User, Equipment.holder==collector_number)
        reason_found = is_not_able_to_move(name, user, collector_data, collector_inv, equipment)
        if reason_found:
            bot.send_message(
                message.chat.id,
                reason_found
            )
            return
        bot.send_message(
            message.chat.id,
            check_boots(name, collector_data, boots)
        )
        user.explore += 1
        user.save()
        collector_data.actions += 1
        collector_data.save()
        exploreC(user, message, name)
        locatRoll(collector_data, user, message, name)
    else:
        bot.send_message(
            message.chat.id,
            f"@{name} you are doing something wrong. Try /explore <collector number> \n "
            f"replace <collector number> with a number.",
        )