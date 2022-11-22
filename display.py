#-----------------------------------#
import discord
#-----------------------------------#
def normalCommands():
  embedVar = discord.Embed(title = "All Standard Commands", color = 0x00ff00)

  embedVar.add_field(
    name = ".stat <@user>",
    value = "Print out the stat of the user inputted. If no user is provided, your own stat will be shown.",
    inline = False)
  embedVar.add_field(
    name = ".leaderboard",
    value = "Print out the top 10 ranking list based on levels.",
    inline = False)
  embedVar.add_field(
    name = ".transactCoins <@recieverUserID> <coinAmount>",
    value = "Transact coin balance with another user. Please ensure that the coinAmount is > 0.",
    inline = False)

  return embedVar
#-----------------------------------#
def adminCommands():
  embedVar = discord.Embed(title = "All Admin Commands", color = 0x00ff00)

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
    name = ".PrintAllUsers",
    value = "Print all the users within the database.",
    inline = False)
  embedVar.add_field(
    name = ".RemoveUser <@user or userID>",
    value = "Delete a user from the database entirely. BE CAREFUL!",
    inline = False)

  embedVar.add_field(
    name = ".botTalk <channelID> \"<message>\"",
    value = "Impersonate the bot to talk in a specific channel. Ensure that the message is closed off with a set of single quotations ''.",
    inline = False)

  embedVar.add_field(
    name = ".resetUserStat <@user>",
    value = "Resets the given user's stats.",
    inline = False)

  return embedVar
#-----------------------------------#