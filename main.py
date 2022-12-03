#-----------------------------------#
#Importations#
#-----------------------------------#
import os
import re
import time
import string
import sqlite3
import numpy as np

# Manually Force Replit to Check For Install#
"""os.system('pip install pymongo[srv]')
import subprocess
subprocess.call(['pip', 'install', 'pymongo[srv]'])"""

from concerns import SubTasks as ST
from concerns import DataLists as DL
from concerns import BattleTasks as BT
from concerns import TagDisplays as TD

from io import BytesIO
from termcolor import colored
from PIL import Image, ImageDraw, ImageFont

import discord
import discord.ext.commands
from discord.ui import Button, View
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
  ST.PrintTextLine("cyan")
  print(colored(message, color))
  ST.PrintTextLine("cyan")


#-----------------------------------#
#Commands#
#-----------------------------------#
@client.command()
async def viewStats(ctx, user: discord.Member = None):
  if user == None:
    user = ctx.author

  connection = sqlite3.connect("Database.db")  #table
  cursor = connection.cursor()  #goes to specific area in table
  cursor.execute(f"SELECT * FROM users WHERE UserID = {user.id};")  #get userid
  userStat = cursor.fetchall()[0]  #finds user
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
    allUserStats.sort(key=lambda x: int(ST.FromLevelToEXP(x[1], x[2])),
                      reverse=True)
    allUserStats = ST.GetUsersInTheServer(allUserStats,
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
      f"{ST.GetNumberAbbreviation(EXPAtCurrentLevel)} / {ST.GetNumberAbbreviation(EXPToReachNextLevel)}"
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

    draw.text((747, 152), (f"{ST.GetNumberAbbreviation(messagesSent)}"),
              font=customFont,
              fill=(10, 74, 8, 1))  #shadow
    draw.text((745, 150), (f"{ST.GetNumberAbbreviation(messagesSent)}"),
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
    await ctx.send(file=discord.File("UserStat.png"))  #sends image to discord
    os.remove("UserStat.png")

    ConsolePrint(f"Stat page was printed for {user}!", "green")


@client.command()
async def leaderboard(ctx):
  connection = sqlite3.connect("Database.db")
  cursor = connection.cursor()
  cursor.execute(f"SELECT * FROM users;")
  allUserStats = cursor.fetchall()

  #create ranking
  allUserStats.sort(
    key=lambda x: int(ST.FromLevelToEXP(x[1], x[2])),
    reverse=True)  # change 1 and 2 to change what leaderboard were doing

  #Get only the users from this server (since the SonnyBot is ran on multiple servers)
  allUserStats = ST.GetUsersInTheServer(allUserStats,
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
  cursor.execute(f"DELETE FROM cards WHERE UserID = {userID}")

  connection.commit()
  connection.close()


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
    newLevel, EXPAtCurrentLevel, n = ST.CalculateForLevel(
      EXPInput, userStat[1], userStat[2])

    if newLevel != userStat[2]:  #level up
      channel = client.get_channel(ST.GetBotChannelID(ctx.message.guild.name))

      if EXPInput > 0:
        levelUpCoinReward = ST.GetLevelUpCoinReward(userStat[2], newLevel)
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

    #commit and close database
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
  recieverUserID = re.split("<@!|>", recieverUserID)[1]
  print(recieverUserID)
  print(type(recieverUserID))
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
async def ResetUserStat(ctx, userID):
  userID = int(re.split("<@!|>", userID)[1])

  connection = sqlite3.connect("Database.db")
  cursor = connection.cursor()

  cursor.execute(
    f"UPDATE users SET EXPAtCurrentLevel = '{0}', Level = '{0}', Coins = '{0}', MessagesSent = '{0}' WHERE UserID = {userID};"
  )

  connection.commit()
  connection.close()

  await ctx.send(
    f"<@{userID}>'s stats has been reset! (Cards are not included)")
  ConsolePrint(f"<@{client.get_user(userID)}>'s stat has been reset!", "green")


@client.command()
@discord.ext.commands.has_permissions(administrator=True)
async def ResetUserCardInventory(ctx):
  UserID = ctx.author.id
  connection = sqlite3.connect("Database.db")
  cursor = connection.cursor()

  cursor.execute(f"DELETE * FROM cards WHERE CardOwnerUserID = {UserID};")

  connection.commit()
  connection.close()


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
"""@client.command()
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

"""


#-----------------------------------#
#Help Commands#
#-----------------------------------#
@client.command()
async def help(ctx):
  await ctx.send(embed=TD.normalCommands())


@client.command()
@discord.ext.commands.has_permissions(administrator=True)
async def adminhelp(ctx):
  await ctx.send(embed=TD.adminCommands())


@client.command()
async def heroList(ctx):
  await ctx.send(embed=TD.heroList())


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
    userStat = ST.SetDefaultData(user.id)
    channel = client.get_channel(ST.GetBotChannelID(message.guild.name))

    #vvvvvv problem with channel send
    await channel.send(f"{user.mention} has been added to the database!")
    ConsolePrint(f"{user.name} has been added to the database!", "green")

  cursor.execute(f"SELECT * FROM users WHERE UserID = {user.id};")
  userStat = cursor.fetchall()[0]
  EXPReward = ST.CalculateForChatEXP(len((message.content).split()))
  newLevel, EXPAtCurrentLevel, n = ST.CalculateForLevel(
    EXPReward, userStat[1], userStat[2])

  #Level Up#
  if userStat[2] != newLevel and newLevel > 0:
    levelUpCoinReward = ST.GetLevelUpCoinReward(userStat[2], newLevel)
    cursor.execute(
      f"UPDATE users SET Level = '{newLevel}', Coins = '{userStat[3] + levelUpCoinReward}' WHERE UserID = {user.id}"
    )

    channel = client.get_channel(ST.GetBotChannelID(message.guild.name))
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
  channel = client.get_channel(ST.GetBotChannelID(user.guild.name))
  await channel.send(f"<@{user.id}> has joined the server!")

  connection = sqlite3.connect("Database.db")
  cursor = connection.cursor()
  cursor.execute(f"SELECT * FROM users WHERE UserID = {user.id};")
  userStat = cursor.fetchall()

  if len(userStat) == 0:
    ST.SetDefaultData(user.id)
    await channel.send(f"<@{user}> has been added to the database!")
    ConsolePrint(f"{user.name} has been added to the database!", "green")


#-----------------------------------#
#Battle#
#-----------------------------------#
@client.command()
async def claim_starter_hero(ctx):
  user = ctx.author

  connection = sqlite3.connect("Database.db")  #table
  cursor = connection.cursor()  #goes to specific area in table
  cursor.execute(f"SELECT * FROM cards WHERE CardOwnerUserID = {user.id};")
  userCards = cursor.fetchall()

  cursor.execute(f"SELECT * FROM users WHERE UserID = {user.id};")
  userStats = cursor.fetchall()[0]

  H1 = Image.open("Images/Heroes/Kotaro.png")
  H2 = Image.open("Images/Heroes/Glaceor.png")
  H3 = Image.open("Images/Heroes/Captain Curtis.png")
  combinedImg = Image.fromarray(
    np.hstack((np.array(H1), np.array(H2), np.array(H3))))

  imagefinal = combinedImg.save("CardImage.png", "PNG")

  #ConsolePrint(f"Card Displayed for {user. id}!", "green")

  if len(userCards) == 0:
    button1 = Button(label="Kotaro")
    button2 = Button(label="Glaceor")
    button3 = Button(label="Captain Curtis")

    async def AddStarterCard(CardIndexNumber):
      level, rarity, CN, CardBaseStats = BT.GenerateCard(
        None, None, CardIndexNumber, userStats[2])
      CBSString = "/".join(str(s) for s in CardBaseStats)
      CardCode = BT.CreateCardCode()

      cursor.execute(
        f"INSERT INTO cards VALUES('{CardCode}',{userStats[0]},{CardIndexNumber},'{CBSString}','','')"
      )

      cursor.execute(f"SELECT * FROM cards WHERE CardOwnerUserID = {user.id};")
      userCards = cursor.fetchall()
      print(userCards)

      connection.commit()
      connection.close()

    async def button1_callback(interaction):
      if interaction.user == ctx.author:
        await interaction.response.edit_message(content="Kotaro was Selected",
                                                view=None)
        await AddStarterCard(1)

    async def button2_callback(interaction):
      if interaction.user == ctx.author:
        await interaction.response.edit_message(content="Glaceor was Selected",
                                                view=None)
        await AddStarterCard(2)

    async def button3_callback(interaction):
      if interaction.user == ctx.author:
        await interaction.response.edit_message(
          content="Captain Curtis was Selected", view=None)
        await AddStarterCard(4)

    button1.callback = button1_callback
    button2.callback = button2_callback
    button3.callback = button3_callback

    view = View()
    view.add_item(button1)
    view.add_item(button2)
    view.add_item(button3)

    await ctx.send(file=discord.File("CardImage.png"),
                   view=view)  #sends image to discord
    os.remove("CardImage.png")
    await ctx.send(
      f"Congragulations <@{user.id}>! You've recruited your first hero!")
    ConsolePrint(f"{user} recieved their first ever hero!", "green")

  else:
    await ctx.send(
      f"<@{user.id}>, you seem to already have a hero! Type .select_hero to select a hero or .battle to start a battle!"
    )
    ConsolePrint(
      f"{user} attempted to recieve a start hero when they already have a collection of heroes! REQUEST DENIED!",
      "red")


@client.command()
async def select_hero(ctx):
  #allows ctx.author to select a hero from (inventory) to then use in battle using cardID
  """
  user = ctx.author
  connection = sqlite3.connect("Database.db")  #table
  cursor = connection.cursor()  #goes to specific area in table
  cursor.execute(f"SELECT * FROM cards WHERE CardOwnerUserID = {user.id};")
  userCards = cursor.fetchall()  #finds user's cards

  cursor.execute(f"SELECT * FROM users WHERE UserID = {user.id};")
  userStats = cursor.fetchall()
  print(userCards)
  """
  pass


@client.command()
async def battle(ctx):
  user = ctx.author
  connection = sqlite3.connect("Database.db")  #table
  cursor = connection.cursor()  #goes to specific area in table
  cursor.execute(f"SELECT * FROM cards WHERE CardOwnerUserID = {user.id};")
  userCards = cursor.fetchall()  #finds user's cards

  cursor.execute(f"SELECT * FROM users WHERE UserID = {user.id};")
  userStats = cursor.fetchall()
  print(userCards)

  if len(userCards) == 0:
    await ctx.send(
      f"<@{user.id}>, you do not seem to have any heroes! Type .claim_starter_hero to claim your first hero!"
    )
  else:
    userLevel = userStats[2]
    CardStats = BT.GenerateCard(None, None, userLevel)
    print(CardStats)

    #generate wild card through connecting to card database
    #display an image of enemy and your hero side by side with it's hp, level and name
    #has 4 button options underneath to select your move
    #Enemy AI selects 1 of 4 preset moves by randint(1,4)
    #use calculation to subtract defence from attack and use that as damage, if damage is negative then set to 0
    #next image to display will have updated hp until a card has 0 or less hp
    #if you win then rewards will be given and a chance at getting a hero
    #if you lose nothing happens


@client.command()
async def HPBar(ctx):
  currentHP = 50
  maxHP = 100
  txt = Image.new("RGBA", (1000, 1000), (255, 255, 255, 0))
  draw = ImageDraw.Draw(txt)

  textFont1 = ImageFont.truetype("Fonts/FiraSans.ttf", 27)
  textFont2 = ImageFont.truetype("Fonts/FiraSans.ttf", 24)

  #Fill = (r, g, b, opacity)#
  #Draw Stats#
  draw.text((285, 97), (f"HP: "), font=textFont1, fill=(122, 192, 120, 1))
  draw.text((345, 100), (
    f"{ST.GetNumberAbbreviation(currentHP)} / {ST.GetNumberAbbreviation(maxHP)}"
  ),
            font=textFont2)

  #Draw Percentage Bar#
  startX = 23
  endX = 603
  percentage = abs(float(currentHP) / maxHP)
  PBSizeX = abs(int(percentage * (endX - startX)))

  progressBar = Image.new('RGBA', (PBSizeX, 35), "#7ac078")
  Xoffset, Yoffset = progressBar.size
  txt.paste(progressBar, (23, 150))

  PBEnding = Image.open("Images/ProgressBarEnding.png")
  txt.paste(PBEnding, (23 + Xoffset, 150), PBEnding)

  txt.save("HPBar.png")
  await ctx.send(file=discord.File("HPBar.png"))  #sends image to discord
  os.remove("HPBar.png")


"""@client.command()
async def viewHero(ctx, user: discord.Member = None):
  H1 = Image.open("Images/Heroes/Kotaro.png")
  H2 = Image.open("Images/Heroes/Glaceor.png")
  H3 = Image.open("Images/Heroes/Captain Curtis.png")
  combinedImg = Image.fromarray(
    np.hstack((np.array(H1), np.array(H2), np.array(H3)))
  )

  combinedImg.save("Images/TempImages/CardImage.png", "PNG")
  file = discord.File(
      f"Images/TempImages/CardImage.png",
      filename=f"CardImage.png")
  await ctx.send(file=file))  #sends image to discord
  os.remove("Images/TempImages/CardImage.png")

  #ConsolePrint(f"Card Displayed for {user. id}!", "green")"""


@client.command()
async def battleHero(ctx, user: discord.Member = None):
  Hero1 = Image.open("Images/Heroes/Kotoshi.png")
  VS = Image.open("Images/Heroes/VS.png")
  VSresize = VS.resize((720, 720))
  Hero2 = Image.open("Images/Heroes/Pyralis.png")

  newimage = Image.fromarray(
    np.hstack((np.array(Hero1), np.array(VSresize), np.array(Hero2))))

  newimage.save("CardImage.png", "PNG")
  await ctx.send(file=discord.File("CardImage.png"))  #sends image to discord
  os.remove("CardImage.png")


"""@client.command()
async def inspect(ctx, HeroName):
  try:
    shownHero = Image.open(f"Images/Heroes/{HeroName}.png")
    shownHero.save("CardImage.png","PNG")
    await ctx.send(file = discord.File("CardImage.png"))  #sends image to discord
    os.remove("CardImage.png")
  except:
    await ctx.send(f"{HeroName} is not the name of a Battle Hero! Use the command **.heroList** to see all Battle Heros names")"""


@client.command()
async def inspect(ctx, HeroName):
  HeroName = string.capwords(HeroName)
  CardsList = DL.GetCardsBaseStatList()
  Hero = None
  for h in CardsList:
    if (h[1] == HeroName):
      Hero = h
      break

  if (Hero != None):
    HeroCardIndexNumber = Hero[0]
    HeroRarity = Hero[2]
    HeroLore = Hero[4]

    FrameName = BT.GetFrameName(HeroRarity)
    Card = Image.new("RGBA", (876, 876), (255, 255, 255, 0))
    cI = Image.open(f"Images/Heroes/{HeroName}.png")
    fI = Image.open(f"Images/Frames/{FrameName}")
    cardImage = cI.resize((720, 720))
    frameImage = fI.resize((876, 876))
    frameImage.convert("RGBA")

    Card.paste(cardImage, (78, 98))
    Card.paste(frameImage, (0, 0), frameImage)
    Card.save(f"Images/TempImages/{HeroName}.png", "PNG")

    #Get Frame Rarity Color Set Numbers#
    R, G, B = BT.GetRarityColor(HeroRarity)

    file = discord.File(f"Images/TempImages/{HeroName}.png",
                        filename=f"{HeroName}.png")
    embed = discord.Embed(title=f"{HeroName}",
                          description=HeroLore,
                          color=discord.Color.from_rgb(R, G, B))
    embed.set_image(url=f"attachment://{HeroName}.png")

    #Send Embed File and Texts & Clean Up#
    await ctx.send(file=file, embed=embed)
    os.remove(f"Images/TempImages/{HeroName}.png")
    ConsolePrint(f"Hero info was printed!", "green")
  else:
    await ctx.send(
      f"{HeroName} is not a valid Battle Hero name! Use the command **.heroList** to see all the available Battle Heros!"
    )
    ConsolePrint(f"Hero info was NOT printed!", "red")


#-----------------------------------#
#-----------------------------------#
client.run(os.environ['BotToken'])
#-----------------------------------#
