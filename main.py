#-----------------------------------#F
#Importations#
#-----------------------------------#
"""- SM, Sonny Ma, 20998850
  - JD, John Deligiannis 21031687
  - BH, Brayden Herbert, 20999228, https://github.com/BraydenHerbert/NE-111
  - DS, Dhruv Shah, 21023078
  GitHub Link - https://github.com/RealClassyClass/Battle-Heroes-V2 
  """
import os
import re
import time
import string
import sqlite3
import requests
import numpy as np
import random
import asyncio

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
  """
  Documentation:

  Purpose - To allow us to print to the console extra info we need for testing and debugging
  """
  
  ST.PrintTextLine("cyan")
  print(colored(message, color))
  ST.PrintTextLine("cyan")


#-----------------------------------#
#Normal Commands#
#-----------------------------------#
"""
  Command: .viewStats
  Purpose - Allows database registered users to view their stats, which include Level, Coins, Exp, Messages Sent, and Rank (in terms of exp)
  - SM
"""
@client.command()
async def viewStats(ctx, user: discord.Member = None):
  if user == None:
    user = ctx.author
    
  #Connect to the database and read data
  connection = sqlite3.connect("Database.db")
  cursor = connection.cursor()
  cursor.execute(f"SELECT * FROM users WHERE UserID = {user.id};")
  US = cursor.fetchall()

  if(len(US) > 0):
    UserStats = US[0]
    print(UserStats)
    
    #Profile Picture (PFP)
    asset = user.display_avatar
    data = BytesIO(await asset.read())
    pfp = Image.open(data)
    pfp = pfp.resize((128, 128))

    #Stat Template
    UserStatsImage = Image.open("Images/UserStatTemplate.png")
    UserStatsImage.paste(pfp, (20, 10))

    #PFPCut
    PFPCut = Image.open("Images/PFPCut.png")
    UserStatsImage.paste(PFPCut, (20, 10), PFPCut)

    #User Name
    drawName = ImageDraw.Draw(UserStatsImage)
    customFont = ImageFont.truetype("Fonts/FiraSans.ttf", 35)
    drawName.text((165, 30), (f"{user.name}"), font=customFont)

    UsernameUnderline = Image.open("Images/UsernameUnderline.png")
    UsernameUnderline = UsernameUnderline.resize((350, 3))
    UserStatsImage.paste(UsernameUnderline, (165, 85), UsernameUnderline)

    #User Stats
    startX = 23
    endX = 603
    level = UserStats[2]
    EXPAtCurrentLevel = UserStats[1]
    EXPToReachNextLevel = (level + 1) * 1000

    #Get Ranking
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

    draw = ImageDraw.Draw(UserStatsImage)
    textFont1 = ImageFont.truetype("Fonts/FiraSans.ttf", 27)
    textFont2 = ImageFont.truetype("Fonts/FiraSans.ttf", 24)

    #Fill = (r, g, b, opacity)
    #Draw Stats
    draw.text((165, 97), (f"Level: "), font=textFont1, fill=(122, 192, 120, 1))
    draw.text((240, 100), (f"{level}"), font=textFont2)

    draw.text((285, 97), (f"EXP: "), font=textFont1, fill=(122, 192, 120, 1))
    draw.text((345, 100), (f"{ST.GetNumberAbbreviation(EXPAtCurrentLevel)} / {ST.GetNumberAbbreviation(EXPToReachNextLevel)}"), font=textFont2)

    draw.text((480, 97), (f"Rank: "), font=textFont1, fill=(122, 192, 120, 1))
    draw.text((555, 100), (f"{rank}"), font=textFont2)

    messagesSent = UserStats[4]
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

    #Draw Coin Count
    draw = ImageDraw.Draw(UserStatsImage)
    draw.ellipse((562, 9, 602, 49), fill=(10, 74, 8, 1))
    customFont = ImageFont.truetype("Fonts/Karla.ttf", 28)
    draw.text((612, 14), (f"{UserStats[3]}"),
              font=customFont,
              fill=(10, 74, 8, 1))  #shadow
    draw.text((610, 12), (f"{UserStats[3]}"),
              font=customFont,
              fill=(255, 255, 255, 1))  #font

    CoinCount = Image.open("Images/CoinDesign.png")
    CoinCount = CoinCount.resize((40, 40))
    UserStatsImage.paste(CoinCount, (560, 7), CoinCount)

    #Draw Percentage Bar
    percentage = abs(float(EXPAtCurrentLevel) / EXPToReachNextLevel)
    PBSizeX = abs(int(percentage * (endX - startX)))

    progressBar = Image.new('RGBA', (PBSizeX, 35), "#7ac078")
    Xoffset, Yoffset = progressBar.size
    UserStatsImage.paste(progressBar, (23, 150))

    PBEnding = Image.open("Images/ProgressBarEnding.png")
    UserStatsImage.paste(PBEnding, (23 + Xoffset, 150), PBEnding)

    #Send Out Image
    UserStatsImage.save("UserStats.png")
    await ctx.send(file=discord.File("UserStats.png"))  #sends image to discord
    os.remove("UserStats.png")

    ConsolePrint(f"Stat page was printed for {user}!", "green")

    connection.close() #closes connection to database


"""
  Command: .leaderboard
  Purpose - Displays Leaderboard of Top 10 highest EXP rank players in the database.
  - SM
"""
@client.command()
async def leaderboard(ctx):
  #Connect to the database and read data
  connection = sqlite3.connect("Database.db")
  cursor = connection.cursor()
  cursor.execute(f"SELECT * FROM users;")
  allUserStats = cursor.fetchall()

  #Create Ranking
  allUserStats.sort(key=lambda x: int(ST.FromLevelToEXP(x[1], x[2])), reverse=True) # Change 1 and 2 to change what leaderboard were doing

  #Get only the users from this server
  allUserStats = ST.GetUsersInTheServer(allUserStats, ctx.message.guild.members)

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

    #Draws Stat
    draw = ImageDraw.Draw(leaderboardImage)

    #Draws Name
    customFont = ImageFont.truetype("Fonts/Ubuntu.ttf", 31)
    draw.text((175, 113 + newY), (f"{user.name}"), font=customFont)

    #Draws Level
    customFont = ImageFont.truetype("Fonts/Ubuntu.ttf", 25)
    draw.text((545, 115 + newY), (f"Level:  {allUserStats[i][2]}"),
              font=customFont)

  leaderboardImage.save("Leaderboard.png")
  await ctx.send(file=discord.File("Leaderboard.png")) #Prints Leaderboard
  os.remove("Leaderboard.png")

  ConsolePrint(f"The leaderboard was printed!", "green")

  connection.close()


"""
  Command: .instructions
  Purpose - Prints a short instructions manual on how to play and on the basic commands to how to start playing the game.
  - DS, Dhruv Shah, 21023078
  """
@client.command()
async def instructions(ctx):
  embed = discord.Embed(title="**How to Play!**", description="Battle Heroes is a Discord Bot Game where you can Collect Heroes and Battle with them. Defeat enemies to capture them and earn coins. You can use whichever card you own to battle the enemy with the .selectHero command. Coins can be used to buy items from the shop with the .shop and .buy commands. Cards that you don't want (you might have a better copy of the card) can be burned with .burn command. Also Remember to use .daily to get more rewards!!")
  await ctx.send(embed=embed)


#-----------------------------------#
#Inventory Edits#
#-----------------------------------#
"""
  Command: .AddRandomizedCardToInventory
  Purpose - Random Card Generator with Random Stats
  - SM
  - BH
"""

def AddRandomizedCardToInventory(UserID, CardIndexNumber):
  #Connects to database and read data
  connection = sqlite3.connect("Database.db")
  cursor = connection.cursor()
  cursor.execute(f"SELECT * FROM cards WHERE CardOwnerUserID = {UserID};")
  userCards = cursor.fetchall()
  
  #Gets UserID of user to give card to
  cursor.execute(f"SELECT * FROM users WHERE UserID = {UserID};")
  UserStats = cursor.fetchall()[0]
  
  #Generates random card with random stats
  CardStats = BT.GenerateCard(None, None, CardIndexNumber, UserStats[2])
  CardLevel = CardStats[0]
  CardRarity = CardStats[1]
  CardIndexNumber = CardStats[2]
  CardBaseStats = CardStats[3]
  
  CBSString = "/".join(str(s) for s in CardBaseStats) #String of Card Base Stats
  CardCode = BT.CreateCardCode() #Unique Card Code Generator

  #Card Code / Card Owner UserID / Card Index Number / Card Level / Base Stat (HP, Atk, Def, Magic, Magic Def, Spd) / HeldItems
  cursor.execute(f"INSERT INTO cards VALUES('{CardCode}',{UserStats[0]},{CardIndexNumber}, {0},'{CBSString}','','')")
  #Gives User Card
  cursor.execute(f"SELECT * FROM cards WHERE CardOwnerUserID = {UserID};")
  userCards = cursor.fetchall()
  print(userCards)

  #Commit changes to the database
  connection.commit()
  #Close connection to the database
  connection.close()


"""
  Command: .AddEnemyCardToInventory
  Purpose - When defeating an AI enemy in .battle, you capture the enemy card, which means that the enemy card gets added to your card inventory.
  - SM
"""
def AddEnemyCardToInventory(UserID, CardStats):
  #Connects to database and read data
  connection = sqlite3.connect("Database.db") 
  cursor = connection.cursor() 
  
  #Unique Card Code Generator
  CardCode = BT.CreateCardCode() 
  
  #Generates random card with random stats
  CardLevel = CardStats[0]
  CardRarity = CardStats[1]
  CardIndexNumber = CardStats[2]
  CardBaseStats = CardStats[3]
  CardStats = BT.GenerateCard(CardLevel, CardRarity, CardIndexNumber, None)
  startingHP = CardStats[[3][0]]
  #String of Card Base Stats
  CBSString = "/".join(str(s) for s in CardBaseStats)

  #Card Code / Card Owner UserID / Card Index Number / Card Level / Base Stat (HP, Atk, Def, Magic, Magic Def, Spd) / HeldItems
  cursor.execute(f"INSERT INTO cards VALUES('{CardCode}',{UserID},{CardIndexNumber}, {0},'{CBSString}','','')")
  
  #Gives User Card
  cursor.execute(f"SELECT * FROM cards WHERE CardOwnerUserID = {UserID};")
  userCards = cursor.fetchall()
  print(userCards)

  #Commit changes to the database
  connection.commit()
  #Close connection to the database
  connection.close()
  

#-----------------------------------#
#Classes#
#-----------------------------------#
class claimStarterView(View):
  """
  Documentation:

  Purpose - Creates a object-orientated class for the view when claiming a starter card, used to implement buttons into code
  - Dhruv Shah, DS, 21023078
  """
  
  def __init__(self, ctx, button1, button2, button3):
    """
    Documentation:
  
    Purpose - Initializes Class 
    """
    
    super().__init__() #Allows the use of cycling through "Children" (Buttons in this case) to control them
    self.ctx = ctx
    self.user = ctx.author

  @discord.ui.button(label="Kotaro", style=discord.ButtonStyle.grey, disabled=False) #Creates Button
  async def button1_callback(self, interaction, button):
    """
    Documentation:
  
    Purpose - Allows button 1 interaction to be interpreted or referenced
    """
    
    #Checks if user is clicking the button not anyone else
    if interaction.user == self.user:
      button.style = discord.ButtonStyle.green #Updates button colour to green
      #Runs through all "Children" (Buttons) and disables them
      for child in self.children:
        child.disabled = True
      await interaction.response.edit_message(content="Kotaro was Selected!", view=self) #Prints that the hero was selected
      AddRandomizedCardToInventory(self.user.id, 1) #Gives the correct card with random stats
      await self.ctx.send(f"Congratulations, <@{self.user.id}>! You've recruited your first hero!")
      ConsolePrint(f"{self.user} received their first ever hero!", "green")
      
  @discord.ui.button(label="Glaceor", style=discord.ButtonStyle.grey, disabled=False) #Creates Button
  async def button2_callback(self, interaction, button):
    """
    Documentation:
  
    Purpose - Allows button 2 interaction to be interpreted or referenced
    """

    #Checks if user is clicking the button not anyone else
    if interaction.user == self.user:
      button.style = discord.ButtonStyle.green #Updates button colour to green
      #Runs through all "Children" (Buttons) and disables them
      for child in self.children:
        child.disabled = True
      await interaction.response.edit_message(content="Glaceor was Selected!", view=self) #Prints that the hero was selected
      AddRandomizedCardToInventory(self.user.id, 2) #Gives the correct card with random stats
      await self.ctx.send(f"Congratulations, <@{self.user.id}>! You've recruited your first hero!")
      ConsolePrint(f"{self.user} received their first ever hero!", "green")

  @discord.ui.button(label="Captain Curtis", style=discord.ButtonStyle.grey, disabled=False) #Creates Button
  async def button3_callback(self, interaction, button):
    """
    Documentation:
  
    Purpose - Allows button 3 interaction to be interpreted or referenced
    """

    #Checks if user is clicking the button not anyone else
    if interaction.user == self.user:
      button.style = discord.ButtonStyle.green #Updates button colour to green
      #Runs through all "Children" (Buttons) and disables them
      for child in self.children:
        child.disabled = True
      await interaction.response.edit_message(content="Captain Curtis was Selected!", view=self) #Prints that the hero was selected
      AddRandomizedCardToInventory(self.user.id, 4) #Gives the correct card with random stats
      await self.ctx.send(f"Congratulations, <@{self.user.id}>! You've recruited your first hero!")
      ConsolePrint(f"{self.user} received their first ever hero!", "green")


#-----------------------------------#
#Pre-Battle#
#-----------------------------------#
"""
  Command: .claimStarterHero
  Purpose - Allows User to claim their very first hero to battle with!
  - Dhruv Shah, DS, 21023078
"""
@client.command()
async def claimStarterHero(ctx):
  user = ctx.author
  
  #Connect to the database and read data
  connection = sqlite3.connect("Database.db")
  cursor = connection.cursor()
  cursor.execute(f"SELECT * FROM cards WHERE CardOwnerUserID = {user.id};")
  userCards = cursor.fetchall()
  cursor.execute(f"SELECT * FROM users WHERE UserID = {user.id};")
  UserStats = cursor.fetchall()[0]

  #Check if this is the first time that a player is claiming starter cards
  if(len(userCards) == 0):
    #Gets the 3 starter cards base stats
    CardsList = DL.GetCardsBaseStatList()
    H1R = requests.get(CardsList[1][5])
    H2R = requests.get(CardsList[2][5])
    H3R = requests.get(CardsList[4][5])
    
    #Opens up the 3 cards' image files and resize
    H1 = Image.open(BytesIO(H1R.content))
    H1R = H1.resize((720, 720))
    H2 = Image.open(BytesIO(H2R.content))
    H2R = H2.resize((720, 720))
    H3 = Image.open(BytesIO(H3R.content))
    H3R = H3.resize((720, 720))
    
    #Opens up common frame image (since all 3 starters are commons) and resizes to fit card size
    CommonFrame = Image.open(f"Images/Frames/CommonFrame.png")
    FrameImage = CommonFrame.resize((876, 876))
    FrameImage.convert("RGBA")
    
    #Create blank image template
    Card = Image.new("RGBA", (3028, 876), (255, 255, 255, 0)) 
    
    #Paste card and frame images onto the main template
    Card.paste(H1R, (78, 98))
    Card.paste(FrameImage, (0, 0), FrameImage)
    Card.paste(H2R, (998, 98))
    Card.paste(FrameImage, (898, 0), FrameImage)
    Card.paste(H3R, (1918, 98))
    Card.paste(FrameImage, (1818, 0), FrameImage)
    Card.save(f"Images/TempImages/CSH.png", "PNG") #save as temp image file
    
    #Insert Images and Text into an Embed
    file = discord.File(f"Images/TempImages/CSH.png", filename=f"CSH.png")
    embed = discord.Embed(
      title=f"Please Select A Hero!",
      color=0x109319)
    embed.set_image(url=f"attachment://CSH.png")
  
    #Create 3 Buttons
    button1 = Button(label="Kotaro", style=discord.ButtonStyle.grey, disabled=False, custom_id="K")
    button2 = Button(label="Glaceor", style=discord.ButtonStyle.grey, disabled=False, custom_id="G")
    button3 = Button(label="Captain Curtis", style=discord.ButtonStyle.grey, disabled=False, custom_id="CC")
    
    #Calls Class and creates the view for embed
    view = claimStarterView(ctx, button1, button2, button3)
    
    #Send Embed File, Buttons, and Texts
    await ctx.send(file=file, embed=embed, view=view)
    os.remove(f"Images/TempImages/CSH.png") #remove the temp image file
    ConsolePrint(f"Hero info was printed!", "green")
    
  else:
    #Prints if you already have at least 1 hero
    await ctx.send(f"<@{user.id}>, you seem to already have a hero! Type .select_hero to select a hero or .battle to start a battle!")
    ConsolePrint(f"{user} attempted to receive a starter hero when they already have a collection of heroes! REQUEST DENIED!", "red")

    connection.close() #Closes connection to database


"""
  Command: .selectHero
  Purpose - Allows User to select 1 of their heroes they own to set on deck and use in future battles, also used to switch which hero is on deck if user has multiple heroes.
  - Dhruv Shah, DS, 21023078
"""
@client.command()
async def selectHero(ctx, cardCode):
  user = ctx.author
  
  #Connect to the database and read data
  connection = sqlite3.connect("Database.db")
  cursor = connection.cursor()
  cursor.execute(f"SELECT * FROM cards WHERE CardCode = '{cardCode}';")
  UC = cursor.fetchall()[0]

  #Check to make sure the player's card inventory has at least one card
  if(len(UC) > 0):
    userCards = UC[0]
    cursor.execute(f"UPDATE users SET SelectedCardCode = '{cardCode}' WHERE UserID = {user.id}")
    
    #Commit changes to the database
    connection.commit()
    
    #Prints that hero has been selected
    await ctx.send(f"<@{user.id}>, {cardCode} has been selected as the new hero on deck!")
    ConsolePrint(f"{client.get_user(user.id)} selected {cardCode} as their new hero!", "green")
  else:
    #Prints that you don't own a hero yet
    await ctx.send(f"<@{user.id}>, you do not seem to own this card!")
    ConsolePrint(f"{client.get_user(user.id)} tried selecting a hero that they don't own!", "red")

  #Close connection to the database
  connection.close()

  
#-----------------------------------#
#Battle#
#-----------------------------------#
"""
  Command: .battle
  Purpose - Allows players to play the main game of the bot. The player's selected hero will battle a randomly generated enemy AI card with random stats. If the player wins, they capture the enemy and receive coins and exp, but if they lose there're' no consequences except moral humiliation >:).
  - SM
"""
@client.command()
async def battle(ctx):
  user = ctx.author
    
  #Connects to database and read info
  connection = sqlite3.connect("Database.db")
  cursor = connection.cursor()
  cursor.execute(f"SELECT * FROM users WHERE UserID = {user.id};")
  UserStats = cursor.fetchall()[0]
  SelectedHeroCardCode = UserStats[5]
  
  #Checks if user has a hero selected on deck
  if SelectedHeroCardCode == "":
    #Prints that user doesn't have hero on deck
    await ctx.send(f"<@{user.id}>, you do not seem to have any selected heroes! Type .claimStarterHero to claim your first hero or .selectHero <herocode> (herocode can be found by using the command .viewCardInventory) if you already have one!")
    
  else:
    #Gets card code of selected hero on deck
    userLevel = UserStats[2]
    cursor.execute(f"SELECT * FROM cards WHERE CardCode = '{SelectedHeroCardCode}';")
    HCDBSavedStat = cursor.fetchall()[0]
    HBS = HCDBSavedStat[4].split("/") #[HP, Atk, Def, Magic, Magic Def, Speed]
    HBSM = list(map(int, HBS))

    CardsList = DL.GetCardsBaseStatList()
    HeroCardRarity = CardsList[HCDBSavedStat[2]][2]
    
    #Get Hero Stats
    #level, rarity, CardIndexNumber, CardBaseStats
    HeroCardStats = [HCDBSavedStat[3], HeroCardRarity, HCDBSavedStat[2], HBSM]
    HeroLevel = HeroCardStats[0]
    HeroBaseStats = HeroCardStats[3] #[HP, Atk, Def, Magic, Magic Def, Speed]
    HeroMaxHP = HeroBaseStats[0] #[HP, Atk, Def, Magic, Magic Def, Speed]

    #Get Enemy Stats
    EnemyCardStats = BT.GenerateCard(None, None, None, userLevel) #Generates random enemy
    EnemyLevel = EnemyCardStats[0]
    EnemyBaseStats = EnemyCardStats[3]
    EnemyMaxHP = EnemyBaseStats[0]
    EnemyCardIndex = EnemyCardStats[2]
    
    #Setup
    CardsList = DL.GetCardsBaseStatList()
    #Controls
    button1 = Button(label = "💥 Physical Attack", custom_id = "button1", style = discord.ButtonStyle.red)
    button2 = Button(label = "🔮 Magic Attack", custom_id = "button2", style = discord.ButtonStyle.primary)
    button3 = Button(label = "🚪 Forfeit", custom_id = "button3", style = discord.ButtonStyle.grey)
    
    #The screen
    view = View(timeout=60) #If buttons aren't pressed in 60 secs then timeout occurs
    
    #Adds buttons to view
    view.add_item(button1)
    view.add_item(button2)
    view.add_item(button3)

    winStatus = 2 #In game
    while(True):
      #Send out generating text
      msg = await ctx.send(f"Generating embed for <@{user.id}>...")
      
      #Draw battle scene embed
      BattleScene = BT.DrawBattleScene(HeroCardStats, EnemyCardStats, HeroMaxHP, EnemyMaxHP)
      BattleScene.save("Images/TempImages/BattleScene.png", "PNG")
      file = discord.File("Images/TempImages/BattleScene.png", filename="BattleScene.png")
      embed = discord.Embed(
        title="**BATTLE**",
        description=f"{ctx.author.mention} is battling an enemy!", 
        color=discord.Color.from_rgb(122, 192, 120))
      embed.set_image(url="attachment://BattleScene.png")

      #Delete the generating text
      await msg.delete()
      
      #Send view to discord 
      msg2 = await ctx.send(file=file, embed=embed, view=view)
      os.remove(f"Images/TempImages/BattleScene.png")

      #Game has ended
      if(winStatus == 1) or (winStatus == 0):
        for button in view.children: #disable all buttons
          button.disabled = True
        await msg2.edit(embed=embed, view=view)
        break
        
      #Wait for button press with 60 secs timeout
      try:
        interactionEvent = await client.wait_for('interaction', timeout = 60, check=lambda interaction: interaction.data["component_type"] == 2 and "custom_id" in interaction.data.keys())

      except asyncio.TimeoutError: #player took too long to respond, so automatic forfeit
        for button in view.children: #disable all buttons
          button.disabled = True
        await msg2.edit(embed=embed, view=view)
        winStatus = -2
        break #break the while loop

      else:
        #Get Attack Damages
        HeroAttackType = ""
        if(interactionEvent.data["custom_id"] == "button1"):
          HeroAttackType = "physical"
        elif(interactionEvent.data["custom_id"] == "button2"):
          HeroAttackType = "magic"
        else: #Player Pressed Forfeit Button
          winStatus = -1
          break
  
        #Enemy's choice of physical or magic attack
        EnemyAttackType = "physical"
        if(np.random.choice(np.arange(0,2)) == 1):
          EnemyAttackType = "magic"
  
        #Get Damage
        HeroDamage = round(BT.GetDamage(HeroBaseStats, EnemyBaseStats, HeroAttackType), 2)
        EnemyDamage = round(BT.GetDamage(EnemyBaseStats, HeroBaseStats, EnemyAttackType), 2)
        #Prints speed stats of hero and enemy and who goes first to console
        print(f"Hero Speed: {HeroBaseStats[5]}")
        print(f"Enemy Speed: {EnemyBaseStats[5]}")
        print(f"Move First: {BT.WhoMovesFirst(HeroBaseStats[5], EnemyBaseStats[5])}")
        #Decides who goes first (based on speed)
        if(BT.WhoMovesFirst(HeroBaseStats[5], EnemyBaseStats[5]) == "p1"): #Hero goes first
          EnemyHP = round(BT.HPLeft(EnemyBaseStats[0], HeroDamage), 2)
          EnemyBaseStats[0] = EnemyHP
          await ctx.send(f"<@{user.id}>'s hero went first! <@{user.id}>'s hero dealt **{HeroDamage}** {HeroAttackType} damage to the opponent!")
          if(EnemyHP <= 0): #When enemy HP drops to or below 0
            EnemyHP = 0
            winStatus = 1
            #EnemyHP = 0
            
          HeroHP = round(BT.HPLeft(HeroBaseStats[0], EnemyDamage), 2)
          HeroBaseStats[0] = HeroHP        
          await ctx.send(f"<@{user.id}>'s hero recieved **{EnemyDamage}** {EnemyAttackType} damage from the opponent!")
          if((HeroHP <= 0)and(winStatus == 2)): #When hero HP <= 0
            HeroHP = 0
            winStatus = 0
            
        else: #Enemy goes first
          HeroHP = round(BT.HPLeft(HeroBaseStats[0], HeroDamage), 2)
          HeroBaseStats[0] = HeroHP
          await ctx.send(f"The opponent went first! <@{user.id}>'s hero recieved **{EnemyDamage}** {EnemyAttackType} damage from the opponent!")
          if(HeroHP <= 0): #When hero HP drops to or below 0
            HeroHP = 0
            winStatus = 0
            
          EnemyHP = round(BT.HPLeft(EnemyBaseStats[0], EnemyDamage), 2)
          EnemyBaseStats[0] = EnemyHP
          await ctx.send(f"<@{user.id}>'s hero dealt **{HeroDamage}** {HeroAttackType} damage to the opponent!")
          if((EnemyHP <= 0)and(winStatus == 2)): #When enemy HP <= 0
            EnemyHP = 0
            winStatus = 1

        
    #While loop ended
    for item in view.children:
      item.disabled = True
    
    #Output results
    if (winStatus == 1): #If user wins
      #Captures enemy
      EnemyCardStats[3][0] = EnemyMaxHP #reset hero HP
      AddEnemyCardToInventory(user.id, EnemyCardStats)
      print("hi", EnemyCardStats)
      ConsolePrint(f"{client.get_user(user.id)} won!", "green")
      await ctx.send(f"<@{user.id}> has captured the enemy!")
      
      #Give coin and exp rewards
      CoinReward = BT.BattleCoinReward(EnemyCardStats)
      EXPReward = BT.BattleEXPReward(EnemyCardStats)
      cursor.execute(f"UPDATE users SET Coins = '{UserStats[3] + CoinReward}' WHERE UserID = {user.id}")
      cursor.execute(f"UPDATE users SET EXPAtCurrentLevel = '{UserStats[1] + EXPReward}' WHERE UserID = {user.id}")
      
      newLevel, EXPAtCurrentLevel, n = ST.CalculateForLevel(EXPReward, UserStats[1], UserStats[2])

      if newLevel != UserStats[2]:  #level up
        channel = client.get_channel(ST.GetBotChannelID(ctx.message.guild.name))
        #Get coins for leveling up
        if EXPReward > 0:
          levelUpCoinReward = ST.GetLevelUpCoinReward(UserStats[2], newLevel)
          cursor.execute(f"UPDATE users SET Level = '{newLevel}', Coins = '{UserStats[3] + levelUpCoinReward}' WHERE UserID = {user.id}") #Sets new level and coins
          #Prints EXP, level and coin info
          await channel.send(f"<@{userID}> obtained {EXPReward} EXP points and has leveled up to level {newLevel}! In correspondence, <@{user.id}> has been rewarded {levelUpCoinReward} coins!")
        else:
          #If -'ve EXP was given then level goes down
          cursor.execute(f"UPDATE users SET Level = '{newLevel}' WHERE UserID = {userID}") #Sets downgraded level
          #Prints EXP loss and downgraded level
          await channel.send(f"<@{user.id}> lost {EXPReward} EXP points and has been downgraded to level {newLevel}!")

          
      #Commit changes to the database
      connection.commit()
      
      await ctx.send(f"<@{user.id}> earned {EXPReward} EXP points and {CoinReward} coins!")
      ConsolePrint(f"{client.get_user(user.id)} earned {EXPReward} EXP points and {CoinReward} coins!", "green")
      
    elif(winStatus == 0): #If user loses
      await ctx.send(f"<@{user.id}> lost!")
      ConsolePrint(f"{client.get_user(user.id)} lost!", "red")
      
    elif(winStatus == -2):
      await ctx.send(f"<@{user.id}> took too long to respond, so automatic forfeit!")
      ConsolePrint(f"{client.get_user(user.id)} lost!", "red")
      
    else: #If winStatus = -1, user manually forfeited
      await ctx.send(f"<@{user.id}> forfeited!")
      ConsolePrint(f"{client.get_user(user.id)} forfeited!", "yellow")

    #Close connection to the database
    connection.close()


#-----------------------------------#
#Main Commands#
#-----------------------------------#
  """
    Command: .inspect
    Purpose - Allows user to individually inspect a hero (contains same info as .heroList but less messy)
    - JD
    - BH
  """
@client.command()
async def inspect(ctx, *args):
  #Searching for hero
  HeroName = " ".join(str(x) for x in args)
  HeroName = string.capwords(HeroName)
  CardsList = DL.GetCardsBaseStatList()
  Hero = None
  for h in CardsList:
    if (h[1] == HeroName):
      Hero = h
      break
  #if hero exists, then get all their info
  if (Hero != None):
    HeroCardIndexNumber = Hero[0] #Index Number
    HeroRarity = Hero[2] #Rarity
    HeroLore = Hero[4] #Lore
    HeroImageURL = Hero[5] #Image
    R, G, B = BT.GetRarityColor(HeroRarity) #Get frame rarity color
    #Get frame
    FrameName = BT.GetFrameName(HeroRarity)
    #Get Card
    Card = Image.new("RGBA", (876, 876), (255, 255, 255, 0))
    response = requests.get(HeroImageURL) #Image
    #Opens frame and image
    cI = Image.open(BytesIO(response.content))
    fI = Image.open(f"Images/Frames/{FrameName}")
    #Resizes
    cardImage = cI.resize((720, 720)) 
    frameImage = fI.resize((876, 876))
    frameImage.convert("RGBA")
    #Puts card and frame together
    Card.paste(cardImage, (78, 98))
    Card.paste(frameImage, (0, 0), frameImage)
    CN = f"{HeroName}.png".replace(" ","")
    Card.save(f"Images/TempImages/{CN}", "PNG") #Saves combined image
    #Creates embed with all info
    file = discord.File(f"Images/TempImages/{CN}", filename=f"{CN}")
    embed = discord.Embed(title=f"{HeroName}",
                          description=HeroLore,
                          color=discord.Color.from_rgb(R,G,B))
    embed.set_image(url=f"attachment://{CN}")
    
    #Send embed file and texts & clean up
    await ctx.send(file=file, embed=embed)
    os.remove(f"Images/TempImages/{CN}")
    ConsolePrint(f"Hero info was printed!", "green")
  else:
    #Prints if user doesn't input valid hero name
    await ctx.send(f"{HeroName} is not a valid Battle Hero name! Use the command **.heroList** to see all the available Battle Heros!")
    ConsolePrint(f"Hero info was NOT printed!", "red")


"""
  Command: .shop
  Purpose - UI that allows you to see what items are on sale and for what price
  -BH
"""
#Brayden Herbert
@client.command()
async def shop(ctx):
  #Embed
  embed=discord.Embed(title="Browse Item Shop", description="Spend your gold on valubles to power up your Battle Heros!", color=0x109319)
  #Shop Image
  embed.set_thumbnail(url="https://i.imgur.com/xS1olI5.png")
  #Items
  embed.add_field(name="|Common| ⚔️ Chipped Blade", value="🪙 250 | Slightly Increase Attack | ***.buy CB***", inline=False)
  embed.add_field(name="|Rare| ⚡ Boots of Lightning", value="🪙 750 | Increases Speed | ***.buy BL***", inline=False)
  embed.add_field(name="|Legendary| ✨ Cloak of Cosmos", value="🪙 1500 | Greatly Increases Defense | ***.buy CC***", inline=False)
  #Sends to discord
  await ctx.send(embed=embed)


"""
  Command: .buy
  Purpose - Allows players to buy items from the shop, given that the player has enough coins for the purchase.
  - BH
"""
@client.command()
async def buy(ctx, purchase):
  user = ctx.author
  
  item = purchase.upper() #Always captilizes item code that the user typed in so both upper- and lower-case works
  
  #Connect to database and read data
  connection = sqlite3.connect("Database.db")
  cursor = connection.cursor()
  cursor.execute(f"SELECT * FROM users WHERE UserID = {user.id};")
  UserStats = cursor.fetchall()[0]

  if (item =="CB"): #Name of item
    if UserStats[3] >= 250: #User coins
      UserCoins = UserStats[3]
      BonusCoins = -250 #Cost of coins
      
      cursor.execute(f"UPDATE users SET Coins = '{UserCoins + BonusCoins}' WHERE UserID = {user.id}") #Subtracting coins
      
      #Commit changes to the database
      connection.commit()

      embed=discord.Embed(title="**HeroBot Shop**", description=f"@{user} purchased Chipped Blade for 250 coins!", color=0xB6B6B6) #Embed text & image
      embed.set_thumbnail(url="https://i.imgur.com/jpdO9o4.png") #Embed image
      await ctx.send(embed=embed)
      ConsolePrint(f"{client.get_user(user.id)} purchased Chipped Blade for 250 coins!", "yellow") #Prints purchase
    else:
      #prints if user doesn't have enough coins
      await ctx.send(f"@{user}, you do not have enough coin to purchase that item!")
      ConsolePrint(f"{client.get_user(user.id)} is trying to buy an expensive weapon, but he BROKE!", "red")

  elif (item =="BL"): #Name of item
    if UserStats[3] >= 750: #User coins
      UserCoins = UserStats[3]
      BonusCoins = -750 #Cost of coins
      
      cursor.execute(f"UPDATE users SET Coins = '{UserCoins + BonusCoins}' WHERE UserID = {user.id}") #Subtracting coins

      #Commit changes to the database
      connection.commit()

      #Creates embed
      embed=discord.Embed(title="**HeroBot Shop**", description=f"{user} purchased Boots of Lightning for 750 coins!", color=0x4682B4) #Embed text & image
      embed.set_thumbnail(url="https://i.imgur.com/3ErqGf4.png") #Embed image
      await ctx.send(embed=embed)
      ConsolePrint(f"{client.get_user(user.id)} purchased Boots of Lightning for 750 coins!", "yellow") #Prints purchase
    else:
      #prints if user doesn't have enough coins
      await ctx.send(f"@{user}, you do not have enough coin to purchase that item!")
      ConsolePrint(f"{client.get_user(user.id)} is trying to buy an expensive weapon, but he BROKE!", "red")

  elif (item =="CC"): #Name of item
    if UserStats[3] >= 1500: #User coins
      UserCoins = UserStats[3]
      BonusCoins = -1500 #Cost of coins
      
      cursor.execute(f"UPDATE users SET Coins = '{UserCoins + BonusCoins}' WHERE UserID = {user.id}") #Subtracting coins

      #Commit changes to the database
      connection.commit()

      #Creates embed
      embed=discord.Embed(title="**HeroBot Shop**", description=f"{user} purchased Cloak of Cosmos for 1500 coins!", color=0xFFD700) #Embed text & image
      embed.set_thumbnail(url="https://i.imgur.com/HRZP9xt.png") #Embed image
      await ctx.send(embed=embed)
      ConsolePrint(f"{client.get_user(user.id)} purchased Cloak of Cosmos for 1500 coins!", "yellow") #Prints purchase
    else:
      #prints if user doesn't have enough coins
      await ctx.send(f"@{user}, you do not have enough coin to purchase that item!")
      ConsolePrint(f"{client.get_user(user.id)} is trying to buy an expensive weapon, but he BROKE!", "red")
      
  else:
    #Prints if user doesn't type correct item code
    await ctx.send(f"@{user}, that is not an item!")

  #Close connection to the database
  connection.close()


"""
  Command: .burn
  Purpose - Allows players to burn any unwanted hero cards they obtain from battle for coins and exp.
  - SM
"""
@client.command()
async def burn(ctx, cardID):
  user = ctx.author
  
  #Connects to database and read data
  connection = sqlite3.connect("Database.db")
  cursor = connection.cursor()
  cursor.execute(f"SELECT * FROM cards WHERE CardCode = '{cardID}';")
  UserCards = cursor.fetchall()
  cursor.execute(f"SELECT * FROM users WHERE UserID = {user.id};")
  UserStats = cursor.fetchall()[0]
  #Creates buttons 
  button1 = Button(label = "❌", custom_id = "button1", style = discord.ButtonStyle.grey)
  button2 = Button(label = "✅", custom_id = "button2", style = discord.ButtonStyle.grey)
  #60 secs timeout
  view = View(timeout=60)
  view.add_item(button1)
  view.add_item(button2)
  #Checks if user has cards to burn
  if(len(UserCards) > 0):
    CardStats = UserCards[0]
    CardCode = CardStats[0]
    CardOwner = CardStats[1]
    UserCoins = UserStats[3]
    #Rewards for burning
    if(CardOwner == user.id):
      cursor.execute(f"DELETE FROM cards WHERE CardCode = '{cardID}'")
      CoinReward = BT.GetBurntCardReward(CardStats)
      cursor.execute(f"UPDATE users SET Coins = '{UserCoins + CoinReward}' WHERE UserID = {user.id}")
      #Confirm burn
      await ctx.send("Do you want to burn this card?", view=view)
      interactionEvent = await client.wait_for('interaction', timeout = 60, check=lambda interaction: interaction.data["component_type"] == 2 and "custom_id" in interaction.data.keys())
      
      if(interactionEvent.data["custom_id"] == "button2"): #Prints successful burn
        await ctx.send(f"<@{user.id}>, `{CardCode}` has been burnt! You recieved {CoinReward} coins as compensation!")
        ConsolePrint(f"{client.get_user(user.id)} successfully burnt {CardCode} coins and recieved {CoinReward} coins as compensation!", "green")
      elif(interactionEvent.data["custom_id"] == "button1"): #Prints cancellation of burn
        await ctx.send(f"<@{user.id}> cancelled the card burn!")
        ConsolePrint(f"{client.get_user(user.id)} cancelled the card burn!", "yellow")
    else:
      #Prints if incorrect card code is typed
      await ctx.send(f"<@{user.id}>, you can't burn a card you don't own!")
      ConsolePrint(f"{client.get_user(user.id)} tried burning {CardCode}, a card they don't own!", "red")

  #Commit changes to the database
  connection.commit()
  #Close connection to the database
  connection.close()
  

"""
  Command: .upgrade
  Purpose - Allows players to upgrade their cards to the next level.
  - SM
"""
@client.command()
async def upgrade(ctx, cardID):
  user = ctx.author

  #Connects to database and read data
  connection = sqlite3.connect("Database.db")
  cursor = connection.cursor()
  cursor.execute(f"SELECT * FROM cards WHERE CardCode = '{cardID}';")
  UC1 = cursor.fetchall()
  cursor.execute(f"SELECT * FROM users WHERE UserID = {user.id};")
  UserStats = cursor.fetchall()[0]
  
  if(len(UC1) > 0):
    Card = UC1[0]
    CardCode = Card[0]
    CardOwnerUserID = Card[1]

    if(CardOwnerUserID == user.id): #Checks user 
      CardIndexNumber = Card[2]
      CardLevel = Card[3]
      CardBaseStats = Card[4]
      #Gets rarity and upgrade cost
      CardRarity = BT.GetCardRarity(CardIndexNumber)
      UpgradeCost = BT.GetUpgradeCost(CardLevel, CardRarity)
      
      UserCoins = UserStats[3] #Finds user's coin value
      
      if(UserCoins >= UpgradeCost): #Checks if user has enough coins
        #Updates coin value and card level
        cursor.execute(f"UPDATE users SET Coins = {UserCoins - UpgradeCost} WHERE UserID = {user.id}")
        cursor.execute(f"UPDATE cards SET CardLevel = {CardLevel + 1} WHERE CardCode = '{CardCode}'")
        #Updates card's stats according to new level
        CBSString = CardBaseStats.split("/")
        NewCBSString = ""
        for s in CBSString:
          NewCBSString += str(int(s) + 5) + "/"
        #Prints new stats
        print(f"Card Stats: {NewCBSString[0:-1]}")
        cursor.execute(f"UPDATE cards SET BaseStat = '{NewCBSString[0:-1]}' WHERE CardCode = '{CardCode}'") #Set new stats as base
        
        #Commit changes to the database
        connection.commit()
        #Prints upgrade 
        await ctx.send(f"<@{user.id}>, `{CardCode}` has been upgraded from {CardLevel} to {CardLevel + 1}!")
        ConsolePrint(f"{client.get_user(user.id)} has upgraded `{CardCode}` from {CardLevel} to {CardLevel + 1}!", "green")
        
      else:
        #Prints if user doesn't have enough coins
        await ctx.send(f"<@{user.id}>, you do not have enough coins to upgrade!")
        ConsolePrint(f"{client.get_user(user.id)} doesn't have enough coins to upgrade `{CardCode}`!", "red")
        
    else:
      #Prints if user doesn't have the card
      await ctx.send(f"<@{user.id}>, you can't upgrade a card you don't own!")
      ConsolePrint(f"{client.get_user(user.id)} tried upgrading a card they don't own!", "red")
      
  else:
    #Prints if card code doesn't exist
    await ctx.send(f"<@{user.id}>, {CardCode} is not a valid card code!")
    ConsolePrint(f"{client.get_user(user.id)} tried calling for an invalid card code!", "red")

  #Close connection to the database
  connection.close()


"""
  Command: .transactCoins
  Purpose - Allows a user to perform a transaction of coins to another user in the database.
  - SM
"""
@client.command()
async def transactCoins(ctx, receiverUserID, coinAmount):
  #Sender and receiver ID's with transaction amount
  senderUserID = ctx.message.author.id
  receiverUserID = int(receiverUserID[2:-1]) #Substring for the userID from standard discord tag format <@userID>
  
  print(receiverUserID)
  print(type(receiverUserID))
  coinAmount = abs(int(coinAmount))

  #Coin amount must be greater than 0
  if coinAmount > 0:
    connection = sqlite3.connect("Database.db")
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM users WHERE UserID = {senderUserID};")
    senderUserStats = cursor.fetchall()[0]

    #Checks if sender has enough coins to send
    if senderUserStats[3] - coinAmount >= 0:
      #Updates sender's and receiver's total coins
      cursor.execute(f"UPDATE users SET Coins = '{senderUserStats[3] - coinAmount}' WHERE UserID = {senderUserStats[0]}")
      cursor.execute(f"SELECT * FROM users WHERE UserID = {receiverUserID};")
      receiverUserStats = cursor.fetchall()[0]
      cursor.execute(f"UPDATE users SET Coins = '{receiverUserStats[3] + coinAmount}' WHERE UserID = {receiverUserStats[0]}")

      #Commit changes to the database
      connection.commit()

      #Prints that transaction was successful
      await ctx.send(f"The transaction is a success! <@{senderUserID}> sent {coinAmount} coin(s) to <@{receiverUserID}>!")
      ConsolePrint(f"The transaction is a success! <@{client.get_user(senderUserID)}> sent {coinAmount} coin(s) to <@{client.get_user(receiverUserID)}>!", "green")
      
    else:
      #Prints if sender doesn't have enough coins
      await ctx.send(f"<@{senderUserID}>, you don't have enough coins for the transaction!")
      
  else:
    #Prints if transaction amount is under 0 coins
    await ctx.send(f"<@{senderUserID}>, a transaction must be greater than 0 for it to occur!")

  #Close connection to the database
  connection.close()

  
"""
  Command: .daily
  Purpose - Allows user to gain Daily Login Rewards
  Issues - The daily part doesn't work as our bot isn't running 24/7 so the daily counter isn't possible unless we run the bot from a paid 24/7 hosting server. This feature can be spammed once the bot logs in.
  - BH
"""   

@client.command()
async def daily(ctx):
  user = ctx.author
  
  #Connect to database and read data
  connection = sqlite3.connect("Database.db")
  cursor = connection.cursor()
  cursor.execute(f"SELECT * FROM users WHERE UserID = {user.id};")
  US = cursor.fetchall()
  
  #Checks if user is in the database
  if(len(US) > 0):
    UserStats = US[0]
    UserCoins = UserStats[3]
    BonusCoins = np.random.choice(np.arange(10,60)) #Bonus coins reward
    
    #Adds randomized coin value to existing value
    cursor.execute(f"UPDATE users SET Coins = '{UserCoins + BonusCoins}' WHERE UserID = {user.id}")

    #Commit changes to the database
    connection.commit()
    
    #Creates embed 
    embed=discord.Embed(title=f"@{user} claimed {BonusCoins} :coin: as their daily login rewards!", color=0x109319)
    await ctx.send(embed=embed)
    ConsolePrint(f"{client.get_user(user.id)} claimed {BonusCoins} coins as their daily login rewards!", "yellow") #Prints daily login rewards
  else:
    #Prints if user tries to claim reward more than once a day (If bot was connected 24/7)
    await ctx.send(f"@{user.id}, you have already claimed your daily bonus!")
    ConsolePrint(f"{client.get_user(user.id)} is trying to claim their daily bonus when they've already claimed it today!", "red")

  #Close connection to the database
  connection.close()


"""
  Command: .viewCardInventory
  Purpose - Allows the user to view their collected cards that are saved in their inventory
  Documentation:
    - Connects to the user's saved data in the sqlite3 database
    - Reads all of the user's hero cards
    - Displays the user's cards in an array of 10 cards per page
    - Clicking the left and right arrows will allow user to navigate through the pages
    - SM
  """
@client.command()
async def viewCardInventory(ctx):
  user = ctx.author
  "JD and SM"
  #Connect to database and read data
  connection = sqlite3.connect("Database.db")
  cursor = connection.cursor()
  cursor.execute(f"SELECT * FROM cards WHERE CardOwnerUserID = {user.id};")
  UserCardsDB = cursor.fetchall() #finds user's cards
  
  CardsList = DL.GetCardsBaseStatList()
  UserCardsInventory = []
  InventoryPageNumber = 0 #Sets default inventory page number
  NumberOfCards = 0 #Sets default number of cards owned

  #Check if the user has at least one card in their inventory
  if len(UserCardsDB) > 0:
    L1 = []
    for i in range(len(UserCardsDB)):
      card = UserCardsDB[i]
      L1.append(card) #Adds all cards user owns
      NumberOfCards += 1

      #For every 10th input or last card in the series, append row into a page
      if((((i + 1) % 10 == 0) and (i > 0)) or (i == len(UserCardsDB ) - 1)):
        UserCardsInventory.append(L1)
        L1 = []

    #Creates embed
    embedVar = discord.Embed(
      title=f"**Card Inventory**".format(user.mention),
      description=f"Cards carried by <@{user.id}>",
      color=discord.Color.from_rgb(255, 164, 101))
    
    #Keep looping tell timeout of buttons run out
    while True:
      #Extract individual card info on the current page into the embed
      InventoryPage = UserCardsInventory[InventoryPageNumber]
      embedString = "**\n" #Create string to hold card infos for each page
      
      print(InventoryPageNumber)
      for i in range(len(InventoryPage)):
        #Card info
        card = InventoryPage[i]
        cardCode = card[0]
        cardIndex = card[2]
        cardLevel = card[3]
        BC = CardsList[cardIndex]
        cardName = BC[1]
        cardRarity = BT.GetRarityName(BC[2])
        #Card stats
        cardStats = card[4].split("/")
        HP = cardStats[0]
        Atk = cardStats[1]
        Def = cardStats[2]
        Mag = cardStats[3]
        MagDef = cardStats[4]
        Speed = cardStats[5]
        
        #Add to embed string
        embedString += f"`🏷️{cardCode}` · `{cardName}` · 🔹{cardRarity} · `Lvl {cardLevel}` · {HP} ❤️ · {Atk} 🗡️ · {Def} 🛡️ · {Mag} 🔮 · {MagDef} 🔰 · {Speed} 👟\n"   
        #Add bottom of page footer for the inventory page
        if(i == len(InventoryPage) - 1):
          x = InventoryPageNumber*10 + 1
          y = (x + 9) if (NumberOfCards - InventoryPageNumber*10 > 10) else NumberOfCards
          z = "s" if (NumberOfCards > 1) else ""
          embedString += f"**\nDisplaying cards {x}-{y} of {NumberOfCards} card{z}."

          
      #Add all 10 cards' info into embed
      embedVar.add_field(
        name = f"---Code---|---Name---|--Rarity--|-Level-|-HP-|-Atk-|-Def-|-Mag-|-MD-|-Spd",
        value = f"{embedString}",
        inline = False)

      #Check which button to disable based on page number of the inventory
      DisableBackwardButton = False
      DisableForwardButton = False
      if(InventoryPageNumber == 0):
        DisableBackwardButton = True
      if(InventoryPageNumber == len(UserCardsInventory) - 1):
        DisableForwardButton = True
        
      #Buttons for page movement
      button1 = Button(label = "⏪", custom_id = "button1", style = discord.ButtonStyle.grey, disabled=DisableBackwardButton)
      button2 = Button(label = "◀", custom_id = "button2", style = discord.ButtonStyle.grey, disabled=DisableBackwardButton)
      button3 = Button(label = "▶", custom_id = "button3", style = discord.ButtonStyle.grey, disabled=DisableForwardButton)
      button4 = Button(label = "⏩", custom_id = "button4", style = discord.ButtonStyle.grey, disabled=DisableForwardButton)
      
      #View for embed with 60 secs timeout
      view = View()
      
      #Adds buttons to view
      view.add_item(button1)
      view.add_item(button2)
      view.add_item(button3)
      view.add_item(button4)

      #Sends embed to discord
      msg = await ctx.send(embed=embedVar, view=view)
      
      #Wait for button press with 60 secs timeout
      try: #To handle time out error
        interactionEvent = await client.wait_for(
          'interaction',
          timeout = 60,
          check=lambda interaction: interaction.data["component_type"] == 2 and "custom_id" in interaction.data.keys())
        print("BP3")
              
      except asyncio.TimeoutError: #When timeout occurs
        print("BP4")
        for button in view.children: #Disable all buttons
          button.disabled = True
        await msg.edit(embed=embedVar, view=view)
        break #Break the while loop 

      else:
        #Check if user flips through pages
        if(interactionEvent.data["custom_id"] == "button1"):
          InventoryPageNumber = 0
        elif(interactionEvent.data["custom_id"] == "button2"):
          InventoryPageNumber -= 1
        elif(interactionEvent.data["custom_id"] == "button3"):
          InventoryPageNumber += 1
        elif(interactionEvent.data["custom_id"] == "button4"):
          InventoryPageNumber = len(UserCardsInventory) - 1
          
  else:
    #Prints if you have no cards
    await ctx.send(f"<@{user.id}>, you don't have any cards in your inventory!")

    connection.close() #Closes connection to database

    
#-----------------------------------#
#Admin Commands#
#-----------------------------------#
"""
  Command: .changeEXP
  Purpose - Allows an admin to change exp of a given user.
  - SM
"""
@client.command()
@discord.ext.commands.has_permissions(administrator=True) #Only admins can use
async def changeEXP(ctx, userID, EXPInput):  
  userID = int(userID[2:-1]) #Substring for the userID from standard discord tag format <@userID>
  
  EXPInput = round(int(EXPInput)) #Ensures EXP is a whole number
  
  #Connect to database and read data
  connection = sqlite3.connect("Database.db")
  cursor = connection.cursor()
  cursor.execute(f"SELECT * FROM users WHERE UserID = '{userID}'")
  US = cursor.fetchall()
  print(f"Before: {US}")  #Print before EXP values

  #The [0] isn't place at the fetchall to prevent a index out of bounds error that occurs when cursor returns None
  if(len(US) > 0):
    UserStats = US[0]
    #Calculate what level user goes to
    newLevel, EXPAtCurrentLevel, n = ST.CalculateForLevel(
      EXPInput, UserStats[1], UserStats[2])

    if newLevel != UserStats[2]:  #level up
      channel = client.get_channel(ST.GetBotChannelID(ctx.message.guild.name))
      #Get coins for leveling up
      if EXPInput > 0:
        levelUpCoinReward = ST.GetLevelUpCoinReward(UserStats[2], newLevel)
        cursor.execute(f"UPDATE users SET Level = '{newLevel}', Coins = '{UserStats[3] + levelUpCoinReward}' WHERE UserID = {userID}") #Sets new level and coins
        #Prints EXP, level and coin info
        await channel.send(f"<@{userID}> obtained {EXPInput} EXP points and has leveled up to level {newLevel}! In correspondence, <@{userID}> has been rewarded {levelUpCoinReward} coins!")
      else:
        #If -'ve EXP was given then level goes down
        cursor.execute(f"UPDATE users SET Level = '{newLevel}' WHERE UserID = {userID}") #Sets downgraded level
        #Prints EXP loss and downgraded level
        await channel.send(f"<@{userID}> lost {EXPInput} EXP points and has been downgraded to level {newLevel}!")

    #Update data in the database
    cursor.execute(f"UPDATE users SET EXPAtCurrentLevel = '{EXPAtCurrentLevel}' WHERE UserID = {userID}")

    #Print after values
    cursor.execute(f"SELECT * FROM users WHERE UserID = {userID}")
    UserStats = cursor.fetchall()[0]
    print(f"After: {UserStats}")

    #Commit changes to the database
    connection.commit()

    #Delete original user command, and print command success
    await ctx.message.delete()
    await ctx.send(f"<@{userID}>'s EXP points has been updated by {EXPInput}!")
    ConsolePrint(f"<@{client.get_user(userID)}>'s EXP points has been updated by {EXPInput}!", "green")

  else:
    #Prints that user isn't in the database
    await ctx.send(f"<@{userID}> is not in the database!")
    ConsolePrint(f"{client.get_user(userID)} is not in the database!", "red")

  #Close connection to the database
  connection.close()


"""
  Commands: .changeCoins
  Purpose - Allows an admin to change coins of a given user.
  - SM
"""
@client.command()
@discord.ext.commands.has_permissions(administrator=True) #Only admins can use
async def changeCoins(ctx, userID, amount):
  userID = int(userID[2:-1]) #substring for the userID from standard discord tag format <@userID>
  
  #Connect to the database and read data
  connection = sqlite3.connect("Database.db")
  cursor = connection.cursor()
  cursor.execute(f"SELECT * FROM users WHERE UserID = {userID};")
  US = cursor.fetchall()
  print(f"Before: {US}")
  
  #Makes sure user is in the database
  if(len(US) > 0):
    UserStats = US[0]
    newCoinCount = UserStats[3] + int(amount) #Calculate new coin value
    if newCoinCount < 0: #Make -'ve values 0
      newCoinCount = 0
    #Updates coin amount
    cursor.execute(f"UPDATE users SET Coins = '{newCoinCount}' WHERE UserID = {userID}")

    cursor.execute(f"SELECT * FROM users WHERE UserID = {userID};")
    UserStats = cursor.fetchall()[0]
    print(f"After: {UserStats}")

    #Commit changes to the database
    connection.commit()

    #Delete original user command, and print command success.
    await ctx.message.delete()
    await ctx.send(
      f"<@{userID}>'s coin count has been updated by {amount} coin(s)!")
    ConsolePrint(
      f"<@{client.get_user(userID)}>'s coin count has been updated!", "green")

  else:
    #Prints that user isn't in the database
    await ctx.send(f"<@{userID}> is not in the database!")
    ConsolePrint(f"{client.get_user(userID)} is not in the database!", "red")

  connection.close() #Closes connection to database


"""
  Commands: .changeMessageSent
  Purpose - Allows an admin to change the number of messages a user sent.
  - SM
"""
@client.command()
@discord.ext.commands.has_permissions(administrator=True) #Only admins can use
async def changeMessageSent(ctx, userID, amount):
  userID = int(userID[2:-1]) #Substring for the userID from standard discord tag format <@userID>
  amount = int(amount)
  
  #Connects to database and read data
  connection = sqlite3.connect("Database.db")
  cursor = connection.cursor()
  cursor.execute(f"SELECT * FROM users WHERE UserID = {userID};")
  US = cursor.fetchall()
  print(f"Before: {US}")  #print before values

  if len(US) > 0:
    UserStats = US[0]
    
    #Make sure msgAmount doesn't become a -'ve
    newMsgAmount = 0 if UserStats[4] + amount < 0 else UserStats[4] + amount

    cursor.execute(f"UPDATE users SET MessagesSent = '{newMsgAmount}' WHERE UserID = {userID}")

    cursor.execute(f"SELECT * FROM users WHERE UserID = {userID};")
    UserStats = cursor.fetchall()[0]
    print(f"After: {UserStats}")

    #Commit changes to the database
    connection.commit()

    #Delete original user command, and print command success
    await ctx.message.delete()
    await ctx.send(
      f"<@{userID}>'s message count has been updated by {amount} message(s)!")
    ConsolePrint(
      f"<@{client.get_user(userID)}>'s message count has been updated by {amount} message(s)!",
      "green")

  else:
    #Prints that user isn't in database
    await ctx.send(f"<@{userID}> is not in the database!")
    ConsolePrint(f"{client.get_user(userID)} is not in the database!", "red")

  #Close the database connection
  connection.close()


"""
  Commands: .AddCard
  Purpose - Allows an admin add a customized hero card to a given user's card inventory.
  - SM
"""
@client.command()
@discord.ext.commands.has_permissions(administrator=True) #Only admins can use
async def AddCard(ctx, CardIndexNumber, CardLevel, CBSString):
  user = ctx.author
  
  #Connect to the database and read data
  connection = sqlite3.connect("Database.db")
  cursor = connection.cursor()

  CardCode = BT.CreateCardCode()

  #Card Code / Card Owner UserID / Card Index Number / Card Level / Base Stat (HP/Atk/Def/Magic/Magic Def/Spd) / HeldItems
  cursor.execute(f"INSERT INTO cards VALUES('{CardCode}',{user.id},{int(CardIndexNumber)}, {int(CardLevel)},'{CBSString}','','')")

  #Commit changes to the database
  connection.commit()
  #Close connection to the database
  connection.close()


"""
  Commands: .printAllUsers
  Purpose - Allows an admin to print all existing users in the database for logging and debugging purposes.
  - SM
"""
@client.command()
@discord.ext.commands.has_permissions(administrator=True) #Only admins can use
async def printAllUsers(ctx):
  #Connects to database and read data
  connection = sqlite3.connect("Database.db")
  cursor = connection.cursor()
  cursor.execute(f"SELECT * FROM users;")
  allUserStats = cursor.fetchall()
  allUserStats.sort(key=lambda x: int(x[1]), reverse=True)
  #Starts print
  ConsolePrint(f"Starting to print...", "yellow")
  
  for UserStats in allUserStats: #Gets users stats
    print(f"{client.get_user(UserStats[0])} --> {UserStats}")
  #Finished printing
  await ctx.send(f"<@{ctx.message.author.id}>, the list has been printed in the console log!")
  ConsolePrint(f"All users' stats have been printed!", "green")

  #Close connection to the database
  connection.close()

  
#-----------------------------------#
#Reset and Remove Commands
#-----------------------------------#
"""
  Command: .removeUser
  Purpose: If userID exists in the database, removes the specified user with  from the database
  - SM
"""
@client.command()
@discord.ext.commands.has_permissions(administrator=True) #Only admins can use
async def removeUser(ctx, userID):
  userID = int(userID[2:-1]) #Substring for the userID from standard discord tag format <@userID>
  
  #Connects to the database and gets rid of all the user's defined stats
  connection = sqlite3.connect("Database.db")
  cursor = connection.cursor()
  cursor.execute(f"DELETE FROM users WHERE UserID = {userID}")
  cursor.execute(f"DELETE FROM cards WHERE UserID = {userID}")

  #Commit changes to the database
  connection.commit()
  #Close connection to the database
  connection.close()


"""
  Command: .resetUserStats
  Purpose: If userID exists in the database, reset all stat of the user to default
  - SM
"""
@client.command()
@discord.ext.commands.has_permissions(administrator=True) #Only admins can use
async def resetUserStats(ctx, userID):
  userID = int(userID[2:-1]) #Substring for the userID from standard discord tag format <@userID>
  
  #Connects to the database and set default 0 values
  connection = sqlite3.connect("Database.db")
  cursor = connection.cursor()
  
  cursor.execute(f"UPDATE users SET EXPAtCurrentLevel = '{0}', Level = '{0}', Coins = '{0}', MessagesSent = '{0}' WHERE UserID = {userID};")

  #Commit changes to the database
  connection.commit()
  #Close connection to the database
  connection.close()
  #Prints reset
  await ctx.send(f"<@{userID}>'s stats has been reset! (Cards are not included)")
  ConsolePrint(f"<@{client.get_user(userID)}>'s stat has been reset!", "green")


"""
  Command: .resetUserCardInventory
  Purpose: If userID exists in the database, clear their entire card inventory by deleting all the cards from the 'cards' sqlite3 table that is owned by the user.
  - SM
"""
@client.command()
@discord.ext.commands.has_permissions(administrator=True) #Only admins can use
async def resetUserCardInventory(ctx, userID):
  UserID = int(userID[2:-1]) #Substring for the userID from standard discord tag format <@userID>
  
  #Connects to the database and delete all user owned cards
  connection = sqlite3.connect("Database.db")
  cursor = connection.cursor()
  #Resets database of specific user's cards
  n = ""
  cursor.execute(f"DELETE FROM cards WHERE CardOwnerUserID = {UserID};")
  cursor.execute(f"UPDATE users SET SelectedCardCode = '{n}' WHERE UserID = {UserID}")
  
  #Commit changes to the database
  connection.commit()
  #Close connection to the database
  connection.close()

  #Prints that reset has occured
  await ctx.send(f"<@{UserID}>'s card inventory has been reset! (User stats not included!)")
  ConsolePrint(f"<@{client.get_user(UserID)}>'s cards inventory has been reset!", "green")

  
#-----------------------------------#
#Fun
#-----------------------------------#
"""
  Command: .botTalk
  Purpose: Emitate the bot to say any string text by giving the channelID and the string to be sent as the command perimeter.
  - SM
"""
@client.command()
@discord.ext.commands.has_permissions(administrator=True) #Only admins can use
async def botTalk(ctx, *args):
  user = ctx.author
  channelID = args[0] #Records channel
  message = args[1] #Records message
  #Requests message to be sent on bots behalf
  ConsolePrint(f"<@{client.get_user(user.id)}> has requested for the bot to send this following message to channel {channelID}: {message}", "yellow")
  #Sends message out
  channel = client.get_channel(int(channelID))
  await channel.send(message)
  await ctx.send(f"<@{user.id}>, the message has been sent!")

  
#-----------------------------------#
#Help Commands#
#-----------------------------------#
"""
  Command: .help
  Purpose: Sends out a printed list of the specifications of basic user commands.
  - SM
  - BH
"""
@client.command()
async def help(ctx):
  await ctx.send(embed=TD.normalCommands())


"""
  Command: .adminHelp
  Purpose: Sends out a printed list of the specifications of admin commands.
  - SM
"""
@client.command()
@discord.ext.commands.has_permissions(administrator=True)
async def adminHelp(ctx):
  await ctx.send(embed=TD.adminCommands())


"""
  Command: .heroList
  Purpose - Prints list of all heroes with their names, rarities and backstories
  - BH
"""
@client.command()
async def heroList(ctx):
  await ctx.send(embed=TD.heroList())

  
#-----------------------------------#
#Events#
#-----------------------------------#
"""
  Event: on_ready
  Purpose: Sends out a console alert that the bot is now online.
  - SM
"""
@client.event
async def on_ready():
  ConsolePrint(f"{client.user} has logged in!", "yellow")


"""
  Event: on_message
  Purpose: On player message, add EXP.
  - SM
"""
@client.event
async def on_message(message):
  if message.author == client.user:  #Prevent bot's own messages
    return
  user = message.author
  
  #Connects to the database and read data
  connection = sqlite3.connect("Database.db")
  cursor = connection.cursor()
  cursor.execute(f"SELECT * FROM users WHERE UserID = {user.id};")
  UserStats = cursor.fetchall()

  #Create default data
  if len(UserStats) == 0:
    UserStats = ST.SetDefaultData(user.id)
    channel = client.get_channel(ST.GetBotChannelID(message.guild.name))

    #Prints addition of user's message to database
    await channel.send(f"{user.mention} has been added to the database!")
    ConsolePrint(f"{user.name} has been added to the database!", "green")
  #Rewards user for messaging with EXP
  cursor.execute(f"SELECT * FROM users WHERE UserID = {user.id};")
  UserStats = cursor.fetchall()[0]
  EXPReward = ST.CalculateForChatEXP(len((message.content).split()))
  newLevel, EXPAtCurrentLevel, n = ST.CalculateForLevel(
    EXPReward, UserStats[1], UserStats[2])

  #Level up if enough EXP gathered
  if UserStats[2] != newLevel and newLevel > 0:
    levelUpCoinReward = ST.GetLevelUpCoinReward(UserStats[2], newLevel) #Gains coins for level up
    cursor.execute(f"UPDATE users SET Level = '{newLevel}', Coins = '{UserStats[3] + levelUpCoinReward}' WHERE UserID = {user.id}")
    #Prints level up and coins to channel specified
    channel = client.get_channel(ST.GetBotChannelID(message.guild.name))
    await channel.send(f"<@{message.author.id}> has leveled up to level {newLevel}! {levelUpCoinReward} coins were awarded!")

  cursor.execute(f"UPDATE users SET EXPAtCurrentLevel = '{EXPAtCurrentLevel}', MessagesSent = '{UserStats[4] + 1}' WHERE UserID = {user.id}")

  #Commit changes to the database
  connection.commit()
  #Close connection to the database
  connection.close()

  await client.process_commands(message)


"""
  Event: on_member_join
  Purpose: On member join, if they aren't in the database, they will be added with default stats.
  - SM
"""
@client.event
async def on_member_join(user):
  channel = client.get_channel(ST.GetBotChannelID(user.guild.name)) #Gets channel info
  await channel.send(f"<@{user.id}> has joined the server!") #Announces server entry
  
  #Connect to the database and read data
  connection = sqlite3.connect("Database.db")
  cursor = connection.cursor()
  cursor.execute(f"SELECT * FROM users WHERE UserID = {user.id};")
  UserStats = cursor.fetchall()
  #Only adds user to database if they first join and aren't already in it
  if len(UserStats) == 0:
    ST.SetDefaultData(user.id)
    await channel.send(f"<@{user}> has been added to the database!")
    ConsolePrint(f"{user.name} has been added to the database!", "green")

    connection.close() #Closes connection to database


#-----------------------------------#
"""
  Purpose: Signal for the bot to run.
  - SM
"""
#-----------------------------------#
client.run(os.environ['BotToken'])
#-----------------------------------#
