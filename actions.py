from chronyk import Chronyk
import json
import requests
from texts import *
from classes import *
from settings import ENTRYPOINT, FILE_TX, RECIPIENT, MEMO, LIMIT, CALORIES_AMOUNT, PATH_USERFILES, PATH_OTHERFILES
from random import randint
from daltonapi.api import Atom, Wax
from daltonapi.tools.atomic_errors import RequestFailedError

def is_not_able_to_move(name, user, collector_data, collector_inv, equipment):
    """Check if the collector is able to make a move.
    Receives
        name:   name of the Telegram user;
        d:      json data;
        c:      json data of particular collector.
    Returns
        String with the reason why collector can't move. Or None if he is able to move.
    """
    # Is overburdened
    if collector_inv > collector_data.max_inv:
        return f"@{name}, your Collector {collector_data.number} is currently overburdened.\n" \
               f"This means he has more inventory than what he can carry. His current maximum is 3 items. \n " \
               f"Use the command /drop <collector number> <item you want to drop>\n\n" \
               f"If your collector has a Teleportal 🔮 equipped, then you can use:\n" \
               f"/teleport <Collector Number> to withdraw and receive your rewards next Monday"
    # Has no actions left
    if collector_data.actions >= collector_data.actions_max:
        return f"Dear @{name}, your Collector {collector_data.number} is too tired to act again this week!\n" \
               f"Try again next week!!"
    # Has not enough energy
    if user.food_bank < 45 or user.food_bank < 50 and boots == "None":
        return f"Dear @{name}, your Collector {collector_data.number} " \
               f"don't have enough energy in the Food Bank to perform this task."

def check_boots(name, collector_data, equipment):
    # Has boots
    if equiment.boots == "Collector's Boots":
        print("Boots discount")
        return f"🥾=✅\n\n" \
               f"@{name}, your Collector {collector_data.number} has a slight discount by having boots 🥾\n" \
               f"Used less than 50 Calories (from Food Bank)."
    # Has no boots
    else:
        return f"🥾=❌\n\n" \
               f"@{name}, your Collector {collector_data.number} used 50 energy (from Food Bank) to perform this task."


# If enough Add count
def exploreC(user, message, name):
    number = 0
    if user.explore == 5:
        number = 1
    elif user.explore == 15:
        number = 2
    elif user.explore == 30:
        number = 3
    elif user.explore == 50:
        number = 4
    elif user.explore == 100:
        number = 5
    if number > 0:
        user.coins += number
        user.save()
        bot.send_message(
            message.chat.id,
            f"🥳🎉Congratz🎉🥳\n\n"
            f"@{name}! You explored your {user.explore}th time.\n"
            f"You earned {number}Coin/s 🪙! \nCoins : {user.coins}\n"
            f"Keep it up!",
        )

def drops(collector_data, user, message, name):
    if collector_data.location == "Plains":
        plainE(collector_data, user, message, name)
        save_to_userfile(data, name)
    elif collector_data.location == "Woodland":
        woodlandE(collector_data, user, message, name)
        save_to_userfile(data, name)
    elif collector_data.location == "Forest":
        forestE(collector_data, user, message, name)
        save_to_userfile(data, name)
    elif collector_data.location == "Rocky":
        rockyE(collector_data, user, message, name)
        save_to_userfile(data, name)
    elif collector_data.location == "Muddy":
        # no loot func
        d["inv"].append("Red Clay")
        bot.send_message(
            message.chat.id,
            f"🚶 EXPLORE 🚶\n\n@{name}, your Collector {d['number']} has found 1 Red Clay!",
        )
        save_to_userfile(data, name)
    elif collector_data.location == "Lake":
        # no loot func
        d["inv"].append("Water")
        bot.send_message(
            message.chat.id,
            "🚶 EXPLORE 🚶\n\n@"
            + name
            + ", your Collector "
            + str(d["number"])
            + " has found 1 Water!",
        )
        save_to_userfile(data, name)
    elif collector_data.location == "Beach":
        beachE(collector_data, user, message, name)
        save_to_userfile(data, name)
    else:
        print("shit")


        
# Clover checks
def cloverExplore(collector_data, user, message, name, equipment):
    if equipment.clover == "Lucky Clover":
        chance = randint(0, 5)
        if chance == 0:
            user.collected += 2
            user.save()
            # moraleUp(d, data, message, name)
            bot.send_message(
                message.chat.id,
                "Clover 🍀=✅\n\n🎲=✅\n@"
                + name
                + " Collector "
                + str(collector_data.number)
                + " got really Lucky with his Clover 🍀! Double Drop Incoming... \n 🍀!\n🎲=✅",
            )
            drops(collector_data, user, message, name)
        else:
            user.collected += 1
            user.save()
            bot.send_message(
                message.chat.id,
                "Clover 🍀=✅\n\n🎲=❌\n\n@"
                + name
                + " collector"
                + str(collector_data.number)
                + "  wasn't lucky with his clover 🍀 this time!\n",
            )
    else: collector_data.number
        bot.send_message(
            message.chat.id,
            "Clover 🍀=❌\n\n@"
            + name
            + " Collector "
            + str(collector_data.number)
            + " doesn't own a Clover 🍀.\n\n 🍀=❌",
        )
        user.collected += 1
        user.save()



        
# Boots Checks
def boots(collector_data, user, message, name, equipment):
    ## Boots Branch
    if equipment.boots == "Collector's Boots":
        user.food_bank -= 45
        user.save()
        print("- 45")
        cloverExplore(collector_data, user, message, name, equpment)
        drops(collector_data, user, message, name)

        ## No Boots Branch
    else:
        user.food_bank -= 50
        user.save()
        print("- 50")
        cloverExplore(collector_data, user, message, name, equipment)
        drops(collector_data, user, message, name)


        
def belt(collector_data, user, message, name, equipment):
    if collector_inv > collector_data.max_inv:
        bot.send_message(
            message.chat.id,
            f"""⚠️🚶‍♂️ EXPLORE 🚶‍♂️⚠️
            
@{name}, your Collector {d.number} is currently overburdened.
This means he has more inventory than what he can carry. His current maximum is 3 items.
Use the command /drop <collector number> <item you want to drop>

If your collector has a Teleportal 🔮 equipped, then you can use:
/teleport <Collector Number> to withdraw and receive your rewards next Monday"""
        )

    elif equipment.belt == "Belt of Fullness":
        chance = randint(0, 7)
        ## Free Move branch
        if chance == 7:
            user.belt_tick += 1
            user.save()
            # moraleUp(d, data, message, name)
            print("free move")
            bot.send_message(
                message.chat.id, f """🚶‍♂️ EXPLORE 🚶‍♂️
                
Belt=✅
🎲=✅

@"{name}, your Collector {collector_data.number} belt shined mysteriously and you performed this action without spending energy!✅""",
            )
            cloverExplore(collector_data, user, message, name, equipment)
            drops(collector_data, user, message, name)
            print(collector_data)
        else:
            print("no luck with belt")
            bot.send_message(
                message.chat.id, f"""🚶‍♂️ EXPLORE 🚶‍♂️
Belt=✅
🎲=❌
@{name}, your Collector {collector_data.number} belt hadn't shined this time!❌"""
            )
            boots(collector_data, user, message, name, equpment)
    else:
        bot.send_message(
            message.chat.id, f"""🚶‍♂️ EXPLORE 🚶‍♂️
Belt=❌

@{name}, your Collector {collector_data.number} has no belt!❌"""
        )
        boots(collector_data, user, message, name, collector_data, equpment)


def addDist(collector_data, user, message, name):
    d.distance += 1
    
    print("add dist")
    if d.distance > 4:
        d.distance = 4
        d.save()
    belt(collector_data, user, message, name, equipment)

# And Roll location after
def locatRoll(collector_data, user, message, name):
    chance = randint(0, 99)
    if chance <= 28:
        d.location = "Plains"
        d.save()
        bot.send_message(
            message.chat.id, f"@{name}, your Collector {d.number} arrived at {d.location}!")
        addDist(collector_data, user, message, name)
    elif 29 <= chance <= 49:
        d.location = "Woodland"
        d.save()
        bot.send_message(
            message.chat.id,
            f"@{name}, your Collector {d.number} arrived at {d.location}!")
        addDist(collector_data, user, message, name)
    elif 50 <= chance <= 68:
        d.location = "Rocky"
        d.save()
        bot.send_message(
            message.chat.id,
            f"@{name}, your Collector {d.number} arrived at {d.location}!")
        addDist(collector_data, user, message, name)
    elif 69 <= chance <= 85:
        d.location = "Forest"
        d.save()
        bot.send_message(
            message.chat.id,
            f"@{name}, your Collector {d.number} arrived at {d.location}!")
        addDist(collector_data, user, message, name)
    elif 86 <= chance <= 89:
        d.location = "Muddy"
        d.save()
        bot.send_message(
            message.chat.id,
            f"@{name}, your Collector {d.number} arrived at {d.location}!")
        addDist(collector_data, user, message, name)
    elif 90 <= chance <= 95:
        d.location = "Beach"
        d.save()
        bot.send_message(
            message.chat.id,
            f"@{name}, your Collector {d.number} arrived at {d.location}!")
        addDist(collector_data, user, message, name)
    elif chance >= 96:
        d.location = "Lake"
        d.save()
        bot.send_message(
            message.chat.id,
            f"@{name}, your Collector {d.number} arrived at {d.location}!")
        addDist(collector_data, user, message, name)
