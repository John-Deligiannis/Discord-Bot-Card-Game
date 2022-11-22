#-----------------------------------#
import discord
#-----------------------------------#
def normalCommands():
  embedVar = discord.Embed(title = "All Normal Commands", color = 0x00ff00)

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

  embedVar.add_field(
    name = ".gamble",
    value = "Literally what the command says, but be wary that the reward may be worse than the entry price! Or it could be x10 the worth :)",
    inline = False)
  embedVar.add_field(
    name = ".meme",
    value = "Get you a random awesome meme that'd actually make you laugh :D",
    inline = False)

  embedVar.add_field(
    name = ".connectDMOJAccount <DMOJ Account Username>",
    value = "Connects the bot to your DMOJ account so rewards can be processed for every CCC question you complete or semi-complete. Accounts must have solved at least 1 problem in order to be connected!",
    inline = False)
  embedVar.add_field(
    name = ".CCCProgressList",
    value = "Bot will send you a printed out your CCC progress list ranging from 2000 - 2021 based on your DMOJ account progress.",
    inline = False)
  embedVar.add_field(
    name = ".FetchCCCProgress",
    value = "Bot will update your CCC progress list by doing a comparison on the DMOJ website.",
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
    name = ".CCCProgressList <@user>",
    value = "Prints out the CCC progress list of the given user.",
    inline = False)
  embedVar.add_field(
    name = ".FetchCCCProgress <@user>",
    value = "Bot will update given user's CCC progress list.",
    inline = False)
  embedVar.add_field(
    name = ".GetDMOJAccount <@user>",
    value = "Bot will return back the given user's DMOJ account. If no user is given, the bot will return the caller's attached DMOJ account.",
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
    name = ".SCUServerThemeChange",
    value = "For the SCU's monthly server theme change. This command is only useable by ClasyClass.",
    inline = False)
  embedVar.add_field(
    name = ".votingEmotes <start> <end>",
    value = "Add number emotes to a message for annoucement voting purposes. Number emotes begin from <start> and discloses at <end>. Max range is from 1 - 10.",
    inline = False)
  embedVar.add_field(
    name = ".botTalk <channelID> \"<message>\"",
    value = "Impersonate the bot to talk in a specific channel. Ensure that the message is closed off with a set of single quotations ''.",
    inline = False)

  embedVar.add_field(
    name = ".disconnectDMOJAccount <@user>",
    value = "Disconnects the given user's DMOJ account from the bot.",
    inline = False)
  embedVar.add_field(
    name = ".resetDMOJProgress <@user>",
    value = "Resets the given user's DMOJ progress within the bot's database. Nothing will be affected on the DMOJ website.",
    inline = False)
  embedVar.add_field(
    name = ".resetUserStat <@user>",
    value = "Resets the given user's stats. User's CCC progress is not included. Use **.resetDMOJProgress** or **.disconnectDMOJAccount** to alter a user's DMOJ progress.",
    inline = False)

  return embedVar
#-----------------------------------#