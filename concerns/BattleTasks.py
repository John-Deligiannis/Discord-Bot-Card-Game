#-----------------------------------#
#Importations#
#-----------------------------------#
import uuid
import time
import math
import random
import sqlite3
import requests
import numpy as np

from io import BytesIO
from termcolor import colored
from concerns import SubTasks as ST
from concerns import DataLists as DL
from PIL import Image, ImageDraw, ImageFont
#-----------------------------------#
def GetCardData(cardStat):
  CardIndexNumber = cardStat[2]
  BaseStat = int(cardStat[3].split())
  HeldItem1 = int(cardStat[4])
  HeldItem2 = int(cardStat[5])
  return [CardIndexNumber, BaseStat, HeldItem1, HeldItem2]

def CreateCardCode(string_length = 6):
  connection = sqlite3.connect("Database.db")
  cursor = connection.cursor()

  while True:
    RandomCode = str(uuid.uuid4()) # Convert UUID format to a Python string.
    RandomCode = RandomCode.upper() # Make all characters uppercase.
    RandomCode = RandomCode.replace("-", "") # Remove the UUID '-'.

    cursor.execute(f"SELECT * FROM cards WHERE CardCode = '{RandomCode}';")
    cards = cursor.fetchall()
    
    if(len(cards) == 0):
      connection.close()
      return RandomCode[0:string_length] # Return the random string.
#-----------------------------------#
def GetEnemyRarity(userLevel):
  #Common% / Uncommon% / Rare% / Epic% / Legendary%
  raritySpawn = []
  
  if(0 <= userLevel <= 5):
    raritySpawn = [0.85, 0.13, 0.01, 0.01, 0.00]
  elif(6 <= userLevel <= 15):
    raritySpawn = [0.70, 0.20, 0.05, 0.04, 0.01]
  elif(16 <= userLevel <= 30):
    raritySpawn = [0.35, 0.40, 0.15, 0.08, 0.02]
  elif(31 <= userLevel <= 50):
    raritySpawn = [0.20, 0.25, 0.30, 0.15, 0.10]
  elif(51 <= userLevel <= 80):
    raritySpawn = [0.10, 0.15, 0.25, 0.30, 0.20]
  elif(81 <= userLevel <= 150):
    raritySpawn = [0.05, 0.08, 0.07, 0.30, 0.50]
  else: #lvl 150+
    raritySpawn = [0.01, 0.04, 0.05, 0.20, 0.70]

  rarity = np.random.choice(np.arange(0, 5), p = [raritySpawn[0], raritySpawn[1], raritySpawn[2], raritySpawn[3], raritySpawn[4]])
  return rarity

def GetEnemyLevel(userLevel):
  level = np.random.choice(np.arange(-5, 5))
  if(userLevel + level < 0):
    return 0
  return userLevel + level

def GetCardIndexNumber(rarity):
  CardsList = DL.GetCardsBaseStatList()
  startIndex = None
  endIndex = None
  for card in CardsList:
    if((card[2] == rarity) and (startIndex == None)):
      startIndex = card[0]
    elif((card[2] > rarity) and (startIndex != None)):
      endIndex = card[0]
      break  
  return np.random.choice(np.arange(startIndex, endIndex))


def RandomGenerateStatNumber(stat, CardLevel):
  c = np.random.choice(np.arange(-5,5))
  if(stat + c < 0):
    return 0 
  return stat + c + (CardLevel*5)
  
def GenerateCardStats(CardIndexNumber, CardLevel):
  CardsList = DL.GetCardsBaseStatList()
  #Base Stat (HP, Atk, Def, Magic, Magic Def, Speed)
  BaseStats = CardsList[CardIndexNumber][3]
  HP = RandomGenerateStatNumber(BaseStats[0], CardLevel)
  Atk = RandomGenerateStatNumber(BaseStats[1], CardLevel)
  Def = RandomGenerateStatNumber(BaseStats[2], CardLevel)
  Magic = RandomGenerateStatNumber(BaseStats[3], CardLevel)
  MagicDef = RandomGenerateStatNumber(BaseStats[4], CardLevel)
  Speed = RandomGenerateStatNumber(BaseStats[5], CardLevel)
  return [HP, Atk, Def, Magic, MagicDef, Speed]

def GenerateCard(level, rarity, CardIndexNumber, userLevel):
  if(level == None):
    level = GetEnemyLevel(userLevel)
  if(rarity == None):
    rarity = GetEnemyRarity(userLevel)
  if(CardIndexNumber == None):
    CardIndexNumber = GetCardIndexNumber(rarity)
  CardBaseStats = GenerateCardStats(CardIndexNumber, level)
  return [level, rarity, CardIndexNumber, CardBaseStats]
#-----------------------------------#
#-----------------------------------#
def GetCardRarity(CardIndexNumber):
  CardsList = DL.GetCardsBaseStatList()
  return CardsList[CardIndexNumber][2]

def GetRarityName(rarity):
  if(rarity == 0):
    return "Common"
  elif(rarity == 1):
    return "Uncommon"
  elif(rarity == 2):
    return "Rare"
  elif(rarity == 3):
    return "Epic"
  elif(rarity == 4):
    return "Legendary"
  else:
    return "Common"
    
def GetFrameName(rarity):
  return GetRarityName(rarity) + "Frame.png"

def GetRarityColor(rarity):
  if(rarity == 0):
    return 180, 180, 180
  elif(rarity == 1):
    return 90, 205, 40
  elif(rarity == 2):
    return 30, 90, 200
  elif(rarity == 3):
    return 150, 110, 245
  elif(rarity == 4):
    return 255, 210, 60
  else:
    return 180, 180, 180
#-----------------------------------#
def DrawCardFrame(HeroRarity):
  FrameName = GetFrameName(HeroRarity)
  Card = Image.new("RGBA", (876, 876), (255, 255, 255, 0))

  fI = Image.open(f"Images/Frames/{FrameName}")
  frameImage = fI.resize((876, 876))
  frameImage.convert("RGBA")

  return frameImage


def GetHPBarColor(HP):
  if HP > 0.75:
    return "#7ac078"
  elif 0.35 < HP < 0.75:
    return "#d9bd4c"
  elif HP > 0:
    return "#d62727"
  else:
    return "#23272a"
    

def DrawBattleScene(HeroCardStats, EnemyCardStats, HeroMaxHP, EnemyMaxHP):  
  HCLevel = HeroCardStats[0]
  HCRarity = HeroCardStats[1]
  HCCardIndexNumber = HeroCardStats[2]
  HCCurrentHP = HeroCardStats[3][0]
  ECLevel = EnemyCardStats[0]
  ECRarity = EnemyCardStats[1]
  ECCardIndexNumber = EnemyCardStats[2]
  ECCurrentHP = EnemyCardStats[3][0]

  CardsList = DL.GetCardsBaseStatList()

  #Get Card Images#
  HRequest = requests.get(CardsList[HCCardIndexNumber][5]) # user's hero
  HCF = DrawCardFrame(HCRarity)
  ECRequest = requests.get(CardsList[ECCardIndexNumber][5]) # AI enemy
  ECF = DrawCardFrame(ECRarity)
  
  H = Image.open(BytesIO(HRequest.content))
  CS = Image.open("Images/CrossedSwords.png")
  EC = Image.open(BytesIO(ECRequest.content))
  
  HeroCard = H.resize((720, 720))
  HeroCardFrame = HCF.resize((876, 876))
  CSR = CS.resize((360, 360))
  EnemyCard = EC.resize((720, 720))
  EnemyCardFrame = ECF.resize((876, 876))

  BattleScene = Image.new("RGBA", (2328, 1076), (255, 255, 255, 0))
  
  BattleScene.paste(HeroCard, (78, 298))
  BattleScene.paste(HeroCardFrame, (0, 200), HeroCardFrame)
  BattleScene.paste(CSR, (978, 458))
  BattleScene.paste(EnemyCard, (1518, 298))
  BattleScene.paste(EnemyCardFrame, (1440, 200), EnemyCardFrame)

  #Heath Bar Set Up#
  textFont1 = ImageFont.truetype("Fonts/Karla.ttf", 40)
  textFont2 = ImageFont.truetype("Fonts/FiraSans.ttf", 50)
  draw = ImageDraw.Draw(BattleScene)
  startX = 30
  endX = 700

  #Left Bar
  percentage = abs(float(HCCurrentHP) / HeroMaxHP)
  PBSizeX = abs(int(percentage * (endX - startX)))
  HPColor = GetHPBarColor(percentage)
  progressBarL = Image.new("RGBA", (PBSizeX, 80), HPColor)
  progressBarFrameL = Image.new("RGBA", (PBSizeX + 20, 100), "#23272a")
  BattleScene.paste(progressBarFrameL, (180, 70))
  BattleScene.paste(progressBarL, (190, 80))
  #Right Bar
  percentage = abs(float(ECCurrentHP) / EnemyMaxHP)
  PBSizeX = abs(int(percentage * (endX - startX)))
  HPColor = GetHPBarColor(percentage)
  progressBarL = Image.new("RGBA", (PBSizeX, 80), HPColor)
  progressBarFrameL = Image.new("RGBA", (PBSizeX + 20, 100), "#23272a")
  BattleScene.paste(progressBarFrameL, (1445, 70))
  BattleScene.paste(progressBarL, (1455, 80))

  #Left Circle
  draw.ellipse((10, 20, 200, 210), fill=(255, 255, 255)) #outer
  draw.ellipse((20, 30, 190, 200), fill=(35, 39, 42)) #inner
  #Right Circle
  draw.ellipse((2100, 20, 2300, 210), fill=(255, 255, 255)) #outer
  draw.ellipse((2110, 30, 2290, 200), fill=(35, 39, 42)) #inner

  #Hero Texts#
  draw.text((50, 92.5), (f"LVL {HCLevel}"), font=textFont1, fill=(255, 255, 255), stroke_width=2)
  draw.text((650, 15), (f"{ST.GetNumberAbbreviation(HCCurrentHP)} / {ST.GetNumberAbbreviation(HeroMaxHP)}"), font=textFont2, stroke_width=2)
  #Enemy Texts#
  draw.text((2150, 92.5), (f"LVL {ECLevel}"), font=textFont1, fill=(255, 255, 255), stroke_width=2)
  draw.text((1450, 15), (f"{ST.GetNumberAbbreviation(ECCurrentHP)} / {ST.GetNumberAbbreviation(EnemyMaxHP)}"), font=textFont2, stroke_width=2)

  BSR = BattleScene.resize((1600, 740))
  
  return BSR
#-----------------------------------#
#Battle Functions#
#-----------------------------------#
def GetDamage(H1BaseStats, H2BaseStats, attackType):
  #p1 damaging p2
  #HP, Atk, Def, Magic, Magic Def, Spd
  if attackType == "physical":
    dmgResult = (((((np.random.choice(np.arange(85,116))))*(H1BaseStats[1]))*0.01).round(1)) - H2BaseStats[2]
    print(dmgResult)
    if dmgResult < 0:
      return 0
    else:
      return dmgResult
    return #roll +/- 25% on the attack damage
  elif attackType == "magic":
    dmgResult = (((((np.random.choice(np.arange(85,116))))*(H1BaseStats[3]))*0.01).round(1)) - H2BaseStats[4]
    print(dmgResult)
    if dmgResult < 0:
      return 0
    else:
      return dmgResult

    
def WhoMovesFirst(p1Speed, p2Speed):
  if p1Speed > p2Speed:
    return "p1"
  elif p1Speed == p2Speed:
    if np.random.choice(np.arange(0, 2)) == 1:
      return "p1"
    else:
      return "p2"
  return "p2"

def HPLeft(HP, damage):
  if (HP - damage) <= 0:
    return 0
  else:
    return HP - damage
#-----------------------------------#
def BattleEXPReward(CardStats):
  CardLevel = CardStats[0]
  CardRarity = CardStats[1]
  EXPReward = 0

  #Card Rarity Reward#
  EXPReward = (100*(CardRarity**2) + CardRarity + 10)
  #Card Level Reward#
  EXPReward += (CardLevel**(1*(CardRarity/5) + 2.0))
  
  return math.ceil(EXPReward)

  
def BattleCoinReward(CardStats):
  CardLevel = CardStats[0]
  CardRarity = CardStats[1]
  CoinReward = 0

  #Card Rarity Reward#
  CoinReward = (50*(CardRarity**2) + CardRarity + 10)/2
  #Card Level Reward#
  CoinReward += (CardLevel**(1*(CardRarity/5) + 1.25))/2
  
  return math.ceil(CoinReward)


def GetBurntCardReward(CardStats):
  print(CardStats)
  CardLevel = CardStats[3]
  CardIndexNumber = CardStats[2]
  CardRarity = GetCardRarity(CardIndexNumber)
  CoinReward = 0

  #Card Rarity Reward#
  CoinReward = 50*(CardRarity**2) + CardRarity + 10
  #Card Level Reward#
  CoinReward += CardLevel**(1*(CardRarity/5) + 1.25)
  
  return CoinReward


def GetUpgradeCost(CardLevel, CardRarity):
  UpgradeCost = CardLevel*20
  UpgradeCost += 10*(CardRarity**2) + CardRarity + 10
  return UpgradeCost
#-----------------------------------#
