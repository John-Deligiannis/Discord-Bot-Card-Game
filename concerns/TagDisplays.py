#-----------------------------------#
import discord
from concerns import DataLists as DL
from concerns import BattleTasks as BT
#-----------------------------------#
def normalCommands():
  embedVar = discord.Embed(title = "All Standard Commands", color = 0x00ff00)
  embedVar.add_field(
    name = ".viewStats <@user>",
    value = "Print out the stat of the user inputted. If no user is provided, your own stat will be shown.",
    inline = False)
  embedVar.add_field(
    name = ".leaderboard",
    value = "Print out the top 10 ranking list based on levels.",
    inline = False)
  embedVar.add_field(
    name = ".instructions",
    value = "How to Play page pops up",
    inline = False)
  embedVar.add_field(
    name = ".transactCoins <@receiverUserID> <amount of coins>",
    value = "Transact coin balance with another user. Please ensure that the coinAmount is > 0.",
    inline = False)
  embedVar.add_field(
    name = ".claimStarterHero",
    value = "Choose from 3 Battle Heros and start your journey to be the strongest!",
    inline = False)
  embedVar.add_field(
    name = ".selectHero <card code>",
    value = "Select 1 of your Heros to participate in battle",
    inline = False)
  embedVar.add_field(
    name = ".battle",
    value = "Starts a battle with a randomly generated AI Enemy",
    inline = False)
  embedVar.add_field(
    name = ".heroList",
    value = "Print a list of all Battle Heros, with their rarity and backstories!",
    inline = False)
  embedVar.add_field(
    name = ".inspect <hero name>",
    value = "Display an image of selected the named Battle Heros.",
    inline = False)
  embedVar.add_field(
    name = ".shop",
    value = "Spend your coins on valubles to power up your Battle Heros.",
    inline = False)
  embedVar.add_field(
    name = ".buy <item>",
    value = "Purchase an item with coins to power up you Battle Heros.",
    inline = False)
  embedVar.add_field(
    name = ".daily",
    value = "Redeem a random amount of free coins every 24 hours.",
    inline = False)
  embedVar.add_field(
    name = ".viewCardInventory",
    value = "View the cards currently in your inventory.",
    inline = False)
  embedVar.add_field(
    name = ".upgrade <card code>",
    value = "Upgrade the specified card with coins.",
    inline = False)
  return embedVar
#-----------------------------------#
def adminCommands():
  embedVar = discord.Embed(title = "All Admin Commands", color = 0x00ff00)
  """
  embedVar.add_field(
    name = ".mute <@user>",
    value = "Mute the given user.",
    inline = False)
  embedVar.add_field(
    name = ".unmute <@user>",
    value = "Unmute the given user if they are currently muted.",
    inline = False)
  embedVar.add_field(
    name = ".muteList",
    value = "Print out all the muted users at the moment.",
    inline = False)
  """
  embedVar.add_field(
    name = ".changeEXP <@user> <integer amount>",
    value = "Add/Subtract EXP points for the given user; in accordance to the given integer amount.",
    inline = False)
  embedVar.add_field(
    name = ".changeCoins <@user> <integer amount>",
    value = "Add/Subtract coins for the given user; in accordance to the given integer amount.",
    inline = False)
  embedVar.add_field(
    name = ".changeMessagesSent <@user> <integer amount>",
    value = "Add/Subtract the number of messages sent from the given user; in accordance to the given integer amount.",
    inline = False)
  embedVar.add_field(
    name = ".printAllUsers",
    value = "Print all the users within the database.",
    inline = False)
  embedVar.add_field(
    name = ".removeUser <@user or userID>",
    value = "Delete a user from the database entirely. BE CAREFUL!",
    inline = False)

  embedVar.add_field(
    name = ".botTalk <channelID> \"<message>\"",
    value = "Impersonate the bot to talk in a specific channel. Ensure that the message is closed off with a set of single quotations ''.",
    inline = False)

  embedVar.add_field(
    name = ".resetUserStats <@user>",
    value = "Resets the given user's stats.",
    inline = False)
  embedVar.add_field(
    name = ".resetUserCardInventory <@user>",
    value = "Resets the given user's entire card inventory.",
    inline = False)
  
  return embedVar
#-----------------------------------#
def heroList():
  CardsList = DL.GetCardsBaseStatList()
  embedVar = discord.Embed(title = "Battle Heros", color = 0x00ff00)

  for card in CardsList:
    CardName = card[1]
    CardRarityName = BT.GetRarityName(card[2])
    CardLore = card[4]

    embedVar.add_field(
      name = f"{CardName}",
      value = f"""|*{CardRarityName}*|\n{CardLore}.""",
      inline = False)
  
  return embedVar
#-----------------------------------#
#-----------------------------------#
