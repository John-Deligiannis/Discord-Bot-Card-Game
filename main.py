#-----------------------------------#
#Importations#
#-----------------------------------#
import os
import re
import time
import random
import asyncio
import display
import sqlite3

from concerns import (SubTasks, DataLists)

from io import BytesIO
from termcolor import colored
from PIL import Image, ImageDraw, ImageFont

import discord
import discord.ext.commands
from discord.utils import get
#-----------------------------------#
#Set Up Bot#
#-----------------------------------#
intents = discord.Intents.all()
intents.presences = True
intents.members = True
client = discord.ext.commands.Bot(command_prefix='.',
                                  intents=intents,
                                  help_command=None)


#-----------------------------------#
#Global Variables#
#-----------------------------------#
def ConsolePrint(message, color):
  SubTasks.PrintTextLine("cyan")
  print(colored(message, color))
  SubTasks.PrintTextLine("cyan")


#-----------------------------------#
#Commands#
#-----------------------------------#
@client.command()
async def stat(ctx, user: discord.Member = None):
  if user == None:
    user = ctx.author

  connection = sqlite3.connect("Database.db")
  cursor = connection.cursor()
  cursor.execute(f"SELECT * FROM users WHERE UserID = {user.id};")
  userStat = cursor.fetchall()[0]
  print(userStat)

  if len(userStat) > 0:
    #PFP#
    asset = user.display_avatar
    data = BytesIO(await asset.read())
    pfp = Image.open(data)
    pfp = pfp.resize((128, 128))

    #Template#
    userStatImage = Image.open("Images/UserStatTemplate.png")
    userStatImage.paste(pfp, (20, 10))

    #PFPCut#
    PFPCut = Image.open("Images/PFPCut.png")
    userStatImage.paste(PFPCut, (20, 10), PFPCut)

    #User Name#
    drawName = ImageDraw.Draw(userStatImage)
    customFont = ImageFont.truetype("Fonts/FiraSans.ttf", 35)
    drawName.text((165, 30), (f"{user.name}"), font=customFont)

    UsernameUnderline = Image.open("Images/UsernameUnderline.png")
    UsernameUnderline = UsernameUnderline.resize((350, 3))
    userStatImage.paste(UsernameUnderline, (165, 85), UsernameUnderline)

    #User Stats#
    startX = 23
    endX = 603
    level = userStat[2]
    EXPAtCurrentLevel = userStat[1]
    EXPToReachNextLevel = (level + 1) * 1000

    #Get Ranking#
    cursor.execute(f"SELECT * FROM users;")
    allUserStats = cursor.fetchall()
    allUserStats.sort(key=lambda x: int(SubTasks.FromLevelToEXP(x[1], x[2])),
                      reverse=True)
    allUserStats = SubTasks.GetUsersInTheServer(allUserStats,
                                                ctx.message.guild.members)
    rank = 0
    for i in range(0, len(allUserStats)):
      if allUserStats[i][0] == user.id:
        rank = i + 1

    draw = ImageDraw.Draw(userStatImage)
    textFont1 = ImageFont.truetype("Fonts/FiraSans.ttf", 27)
    textFont2 = ImageFont.truetype("Fonts/FiraSans.ttf", 24)

    #Fill = (r, g, b, opacity)#
    #Draw Stats#
    draw.text((165, 97), (f"Level: "), font=textFont1, fill=(122, 192, 120, 1))
    draw.text((240, 100), (f"{level}"), font=textFont2)

    draw.text((285, 97), (f"EXP: "), font=textFont1, fill=(122, 192, 120, 1))
    draw.text((345, 100), (
      f"{SubTasks.GetNumberAbbreviation(EXPAtCurrentLevel)} / {SubTasks.GetNumberAbbreviation(EXPToReachNextLevel)}"
    ),
              font=textFont2)

    draw.text((480, 97), (f"Rank: "), font=textFont1, fill=(122, 192, 120, 1))
    draw.text((555, 100), (f"{rank}"), font=textFont2)

    messagesSent = userStat[4]
    customFont = ImageFont.truetype("Fonts/Karla.ttf", 22)
    draw.text((687, 152), ("Msg:"), font=customFont,
              fill=(10, 74, 8, 1))  #shadow
    draw.text((685, 150), ("Msg:"), font=customFont,
              fill=(180, 230, 255, 1))  #text

    draw.text((747, 152), (f"{SubTasks.GetNumberAbbreviation(messagesSent)}"),
              font=customFont,
              fill=(10, 74, 8, 1))  #shadow
    draw.text((745, 150), (f"{SubTasks.GetNumberAbbreviation(messagesSent)}"),
              font=customFont,
              fill=(255, 255, 255, 1))  #font

    #Draw Coin Count#
    draw = ImageDraw.Draw(userStatImage)
    draw.ellipse((562, 9, 602, 49), fill=(10, 74, 8, 1))
    customFont = ImageFont.truetype("Fonts/Karla.ttf", 28)
    draw.text((612, 14), (f"{userStat[3]}"),
              font=customFont,
              fill=(10, 74, 8, 1))  #shadow
    draw.text((610, 12), (f"{userStat[3]}"),
              font=customFont,
              fill=(255, 255, 255, 1))  #font

    CoinCount = Image.open("Images/CoinDesign.png")
    CoinCount = CoinCount.resize((40, 40))
    userStatImage.paste(CoinCount, (560, 7), CoinCount)

    #Draw Percentage Bar#
    percentage = abs(float(EXPAtCurrentLevel) / EXPToReachNextLevel)
    PBSizeX = abs(int(percentage * (endX - startX)))

    progressBar = Image.new('RGBA', (PBSizeX, 35), "#7ac078")
    Xoffset, Yoffset = progressBar.size
    userStatImage.paste(progressBar, (23, 150))

    PBEnding = Image.open("Images/ProgressBarEnding.png")
    userStatImage.paste(PBEnding, (23 + Xoffset, 150), PBEnding)

    #Send Out Image*
    userStatImage.save("UserStat.png")
    await ctx.send(file=discord.File("UserStat.png"))
    os.remove("UserStat.png")

    ConsolePrint(f"Stat page was printed for {user}!", "green")


@client.command()
async def leaderboard(ctx):
  connection = sqlite3.connect("Database.db")
  cursor = connection.cursor()
  cursor.execute(f"SELECT * FROM users;")
  allUserStats = cursor.fetchall()

  #create ranking
  allUserStats.sort(key=lambda x: int(SubTasks.FromLevelToEXP(x[1], x[2])),
                    reverse=True)

  #Get only the users from this server (since the SonnyBot is ran on multiple servers)
  allUserStats = SubTasks.GetUsersInTheServer(allUserStats,
                                              ctx.message.guild.members)

  #Get the leaderboard template board
  leaderboardImage = Image.open("Images/LeaderboardTemplate.png")
  PFPCut = Image.open("Images/PFPCut.png")
  PFPCut = PFPCut.resize((66, 66))

  #Print out the top 10 users in terms of levels
  for i in range(0, len(allUserStats)):
    if i > 9:
      break
    newY = (75 * i)

    user = await client.fetch_user(allUserStats[i][0])
    asset = user.display_avatar
    data = BytesIO(await asset.read())
    pfp = Image.open(data)
    pfp = pfp.resize((66, 66))
    leaderboardImage.paste(pfp, (5, 99 + newY))
    leaderboardImage.paste(PFPCut, (5, 99 + newY), PFPCut)

    #Stat#
    draw = ImageDraw.Draw(leaderboardImage)

    #Name
    customFont = ImageFont.truetype("Fonts/Ubuntu.ttf", 31)
    draw.text((175, 113 + newY), (f"{user.name}"), font=customFont)

    #Level
    customFont = ImageFont.truetype("Fonts/Ubuntu.ttf", 25)
    draw.text((565, 115 + newY), (f"Level:  {allUserStats[i][2]}"),
              font=customFont)

  leaderboardImage.save("Leaderboard.png")
  await ctx.send(file=discord.File("Leaderboard.png"))
  os.remove("Leaderboard.png")

  ConsolePrint(f"The leaderboard was printed!", "green")


@client.command()
@discord.ext.commands.has_permissions(administrator=True)
async def PrintAllUsers(ctx):
  connection = sqlite3.connect("Database.db")
  cursor = connection.cursor()
  cursor.execute(f"SELECT * FROM users;")
  allUserStats = cursor.fetchall()
  allUserStats.sort(key=lambda x: int(x[1]), reverse=True)

  ConsolePrint(f"Starting to print...", "yellow")

  for userStat in allUserStats:
    print(f"{client.get_user(userStat[0])} --> {userStat}")

  await ctx.send(
    f"<@{ctx.message.author.id}>, the list has been printed in the console log!"
  )
  ConsolePrint(f"All users' stats have been printed!", "green")


@client.command()
@discord.ext.commands.has_permissions(administrator=True)
async def RemoveUser(ctx, userID):
  userID = int(re.split("<@!|>", userID)[1])

  connection = sqlite3.connect("Database.db")
  cursor = connection.cursor()
  cursor.execute(f"DELETE FROM users WHERE UserID = {userID}")

  connection = sqlite3.connect("Database.db")
  cursor = connection.cursor()
  cursor.execute(f"DELETE FROM cards_inventory WHERE UserID = {userID}")


#-----------------------------------#
#-----------------------------------#
@client.command()
@discord.ext.commands.has_permissions(administrator=True)
async def changeEXP(ctx, userID, EXPInput):
  userID = ctx.author.id  #int(re.split("<@!|>", userID)[1])
  EXPInput = round(int(EXPInput))

  connection = sqlite3.connect("Database.db")
  cursor = connection.cursor()
  cursor.execute(f"SELECT * FROM users WHERE UserID = '{userID}'")
  userStat = cursor.fetchall()
  print(f"Before: {userStat}")  #print before values

  #the [0] isn't place at the fetchall to prevent a index out of bounds error that occurs when cursor returns None
  if len(userStat[0]) > 0:
    userStat = userStat[0]
    newLevel, EXPAtCurrentLevel, n = SubTasks.CalculateForLevel(
      EXPInput, userStat[1], userStat[2])

    if newLevel != userStat[2]:  #level up
      channel = client.get_channel(
        SubTasks.GetBotChannelID(ctx.message.guild.name))

      if EXPInput > 0:
        levelUpCoinReward = SubTasks.GetLevelUpCoinReward(
          userStat[2], newLevel)
        cursor.execute(
          f"UPDATE users SET Level = '{newLevel}', Coins = '{userStat[3] + levelUpCoinReward}' WHERE UserID = {userID}"
        )

        await channel.send(
          f"<@{userID}> obtained {EXPInput} EXP points and has leveled up to level {newLevel}! In correspondence, <@{userID}> has been rewarded {levelUpCoinReward} coins!"
        )
      else:
        cursor.execute(
          f"UPDATE users SET Level = '{newLevel}' WHERE UserID = {userID}")

        await channel.send(
          f"<@{userID}> lost {EXPInput} EXP points and has been downgraded to level {newLevel}!"
        )

    #update data on the database
    cursor.execute(
      f"UPDATE users SET EXPAtCurrentLevel = '{EXPAtCurrentLevel}' WHERE UserID = {userID}"
    )

    #print after values
    cursor.execute(f"SELECT * FROM users WHERE UserID = {userID}")
    userStat = cursor.fetchall()[0]
    print(f"After: {userStat}")

    #commit and close databse
    connection.commit()
    connection.close()

    #delete original user command, and print command success
    await ctx.message.delete()
    await ctx.send(f"<@{userID}>'s EXP points has been updated by {EXPInput}!")
    ConsolePrint(
      f"<@{client.get_user(userID)}>'s EXP points has been updated by {EXPInput}!",
      "green")

  else:
    await ctx.send(f"<@{userID}> is not in the database!")
    ConsolePrint(f"{client.get_user(userID)} is not in the database!", "red")


@client.command()
@discord.ext.commands.has_permissions(administrator=True)
async def changeCoins(ctx, userID, amount):
  userID = ctx.author.id  #int(re.split("<@!|>", userID)[1])

  connection = sqlite3.connect("Database.db")
  cursor = connection.cursor()
  cursor.execute(f"SELECT * FROM users WHERE UserID = {userID};")
  userStat = cursor.fetchall()[0]
  print(f"Before: {userStat}")  #print before values

  if len(userStat) > 0:
    newCoinCount = userStat[3] + int(amount)
    if newCoinCount < 0:
      newCoinCount = 0

    cursor.execute(
      f"UPDATE users SET Coins = '{newCoinCount}' WHERE UserID = {userID}")

    cursor.execute(f"SELECT * FROM users WHERE UserID = {userID};")
    userStat = cursor.fetchall()[0]
    print(f"After: {userStat}")

    connection.commit()
    connection.close()

    #delete original user command, and print command success
    await ctx.message.delete()
    await ctx.send(
      f"<@{userID}>'s coin count has been updated by {amount} coin(s)!")
    ConsolePrint(
      f"<@{client.get_user(userID)}>'s coin count has been updated!", "green")

  else:
    await ctx.send(f"<@{userID}> is not in the database!")
    ConsolePrint(f"{client.get_user(userID)} is not in the database!", "red")


@client.command()
@discord.ext.commands.has_permissions(administrator=True)
async def changeMessageSent(ctx, userID, amount):
  userID = ctx.author.id  #int(re.split("<@!|>", userID)[1])
  amount = int(amount)

  connection = sqlite3.connect("Database.db")
  cursor = connection.cursor()
  cursor.execute(f"SELECT * FROM users WHERE UserID = {userID};")
  userStat = cursor.fetchall()
  print(f"Before: {userStat}")  #print before values

  if len(userStat) > 0:
    userStat = userStat[0]
    #make sure msgAmount doesn't become a (-) value
    newMsgAmount = 0 if userStat[4] + amount < 0 else userStat[4] + amount

    cursor.execute(
      f"UPDATE users SET MessagesSent = '{newMsgAmount}' WHERE UserID = {userID}"
    )

    cursor.execute(f"SELECT * FROM users WHERE UserID = {userID};")
    userStat = cursor.fetchall()[0]
    print(f"After: {userStat}")

    connection.commit()
    connection.close()

    #delete original user command, and print command success
    await ctx.message.delete()
    await ctx.send(
      f"<@{userID}>'s message count has been updated by {amount} message(s)!")
    ConsolePrint(
      f"<@{client.get_user(userID)}>'s message count has been updated by {amount} message(s)!",
      "green")

  else:
    await ctx.send(f"<@{userID}> is not in the database!")
    ConsolePrint(f"{client.get_user(userID)} is not in the database!", "red")


@client.command()
async def transactCoins(ctx, recieverUserID, coinAmount):
  senderUserID = ctx.message.author.id
  recieverUserID = int(re.split("<@!|>", recieverUserID)[1])
  coinAmount = abs(int(coinAmount))

  if coinAmount > 0:
    connection = sqlite3.connect("Database.db")
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM users WHERE UserID = {senderUserID};")
    senderUserStat = cursor.fetchall()[0]

    if senderUserStat[3] - coinAmount >= 0:
      cursor.execute(
        f"UPDATE users SET Coins = '{senderUserStat[3] - coinAmount}' WHERE UserID = {senderUserStat[0]}"
      )

      cursor.execute(f"SELECT * FROM users WHERE UserID = {recieverUserID};")
      recieverUserStat = cursor.fetchall()[0]

      cursor.execute(
        f"UPDATE users SET Coins = '{recieverUserStat[3] + coinAmount}' WHERE UserID = {recieverUserStat[0]}"
      )

      connection.commit()

      await ctx.send(
        f"The transaction is a success! <@{senderUserID}> sent {coinAmount} coin(s) to <@{recieverUserID}>!"
      )
      ConsolePrint(
        f"The transaction is a success! <@{client.get_user(senderUserID)}> sent {coinAmount} coin(s) to <@{client.get_user(recieverUserID)}>!",
        "green")
    else:
      await ctx.send(
        f"<@{senderUserID}>, you don't have enough coins for the transaction!")
  else:
    await ctx.send(
      f"<@{senderUserID}>, a transaction must be greater than 0 for it to occur!"
    )

  connection.close()


@client.command()
@discord.ext.commands.has_permissions(administrator=True)
async def resetUserStat(ctx, userID):
  userID = int(re.split("<@!|>", userID)[1])

  connection = sqlite3.connect("Database.db")
  cursor = connection.cursor()

  cursor.execute(
    f"UPDATE users SET EXPAtCurrentLevel = '{0}', Level = '{0}', Coins = '{0}', MessagesSent = '{0}' WHERE UserID = {userID};"
  )

  connection.commit()
  connection.close()

  await ctx.send(
    f"<@{userID}>'s stats has been reset! (CCC progress are not included)")
  ConsolePrint(f"<@{client.get_user(userID)}>'s stat has been reset!", "green")


#-----------------------------------#
#-----------------------------------#


@client.command()
@discord.ext.commands.has_permissions(administrator=True)
async def botTalk(ctx, *args):
  print(args)
  channelID = args[0]
  message = args[1]

  channel = client.get_channel(int(channelID))
  await channel.send(message)
  await ctx.send(f"<@{ctx.message.author.id}>, the message has been sent!")


#-----------------------------------#
#Miscellaneous#
#-----------------------------------#
@client.command()
@discord.ext.commands.has_permissions(administrator=True)
async def mute(ctx, user: discord.Member):
  muteRole = get(ctx.message.guild.roles, name='Muted')
  await user.edit(roles=[muteRole])  #replaces all roles with 'Muted'
  await ctx.send(f"<@{user.id}> has been muted!")


@client.command()
@discord.ext.commands.has_permissions(administrator=True)
async def unmute(ctx, user: discord.Member):
  mutedRole = discord.utils.find(lambda r: r.name == 'Muted',
                                 ctx.message.guild.roles)
  if mutedRole in user.roles:
    gamerRole = get(ctx.message.guild.roles, name='Gamer')
    await user.edit(roles=[gamerRole])  #replaces all roles with 'Gamer'
    await ctx.send(
      f"<@{user.id}> has been unmuted! Default role of **Gamer** was given, but all roles from prior to muting requires manual replacement, , <@{ctx.message.author.id}>."
    )
  else:
    await ctx.send(
      f"<@{user.id}> is not muted at the moment. Type **.muteList <@user>** for all the user that are currently muted, , <@{ctx.message.author.id}>."
    )


@client.command()
@discord.ext.commands.has_permissions(administrator=True)
async def muteList(ctx):
  role = discord.utils.find(lambda r: r.name == 'Muted',
                            ctx.message.guild.roles)
  empty = True
  tempString = ""

  for member in ctx.message.guild.members:
    if role in member.roles:
      tempString += f"<@{member.id}>, "
      empty = False

  if empty:
    await ctx.send(
      f"<@{ctx.message.author.id}>, there are no one muted at the moment!")
  else:
    tempString = tempString[:-2]
    if tempString.count(",") > 0:
      lastIndex = tempString.rfind(", ")
      tempString = f"{tempString[:lastIndex]} and {tempString[lastIndex + 2:]}"
    await ctx.send(
      f"{tempString} are currently muted, <@{ctx.message.author.id}>.")


#-----------------------------------#
#-----------------------------------#
@client.command()
async def help(ctx):
  await ctx.send(embed=display.normalCommands())


@client.command()
@discord.ext.commands.has_permissions(administrator=True)
async def adminhelp(ctx):
  await ctx.send(embed=display.adminCommands())


#-----------------------------------#
#Events#
#-----------------------------------#
@client.event
async def on_ready():
  ConsolePrint(f"{client.user} have logged in!", "yellow")


@client.event
async def on_message(message):
  if message.author == client.user:  #prevent bot's own messages
    return
  user = message.author

  connection = sqlite3.connect("Database.db")
  cursor = connection.cursor()
  cursor.execute(f"SELECT * FROM users WHERE UserID = {user.id};")
  userStat = cursor.fetchall()

  #Create Default Data#
  if len(userStat) == 0:
    userStat = SubTasks.SetDefaultData(user.id)
    channel = client.get_channel(SubTasks.GetBotChannelID(message.guild.name))

    #vvvvvv problem with channel send
    await channel.send(f"{user.mention} has been added to the database!")
    ConsolePrint(f"{user.name} has been added to the database!", "green")

  cursor.execute(f"SELECT * FROM users WHERE UserID = {user.id};")
  userStat = cursor.fetchall()[0]
  EXPReward = SubTasks.CalculateForChatEXP(len((message.content).split()))
  newLevel, EXPAtCurrentLevel, n = SubTasks.CalculateForLevel(
    EXPReward, userStat[1], userStat[2])

  #Level Up#
  if userStat[2] != newLevel and newLevel > 0:
    levelUpCoinReward = SubTasks.GetLevelUpCoinReward(userStat[2], newLevel)
    cursor.execute(
      f"UPDATE users SET Level = '{newLevel}', Coins = '{userStat[3] + levelUpCoinReward}' WHERE UserID = {user.id}"
    )

    channel = client.get_channel(SubTasks.GetBotChannelID(message.guild.name))
    await channel.send(
      f"<@{message.author.id}> has leveled up to level {newLevel}! {levelUpCoinReward} coins were awarded!"
    )

  cursor.execute(
    f"UPDATE users SET EXPAtCurrentLevel = '{EXPAtCurrentLevel}', MessagesSent = '{userStat[4] + 1}' WHERE UserID = {user.id}"
  )
  connection.commit()
  connection.close()

  await client.process_commands(message)


@client.event
async def on_member_join(user):
  channel = client.get_channel(SubTasks.GetBotChannelID(user.guild.name))
  await channel.send(f"<@{user.id}> has joined the server!")

  connection = sqlite3.connect("Database.db")
  cursor = connection.cursor()
  cursor.execute(f"SELECT * FROM users WHERE UserID = {user.id};")
  userStat = cursor.fetchall()

  if len(userStat) == 0:
    SubTasks.SetDefaultData(user.id)
    await channel.send(f"<@{user}> has been added to the database!")
    ConsolePrint(f"{user.name} has been added to the database!", "green")


#-----------------------------------#
#-----------------------------------#
client.run(os.environ['BotToken'])
#-----------------------------------#
