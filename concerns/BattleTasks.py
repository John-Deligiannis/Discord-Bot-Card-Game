#-----------------------------------#
#Importations#
#-----------------------------------#
import uuid
import time
import random
import sqlite3
from termcolor import colored
import numpy as np

from concerns import DataLists as DL
#-----------------------------------#
def GetCardData(cardStat):
  CardIndexNumber = cardStat[2]
  BaseStat = int(cardStat[3].split())
  HeldItem1 = int(cardStat[4])
  HeldItem2 = int(cardStat[5])
  return [CardIndexNumber, BaseStat, HeldItem1, HeldItem2]

def CreateCardCode(string_length = 6):
    random = str(uuid.uuid4()) # Convert UUID format to a Python string.
    random = random.upper() # Make all characters uppercase.
    random = random.replace("-", "") # Remove the UUID '-'.
    return random[0:string_length] # Return the random string.
#-----------------------------------#
def GetEnemyRarity(userLevel):
  #Common% / Uncommon% / Rare% / Legendary%
  raritySpawn = []
  
  if(0 <= userLevel <= 5):
    raritySpawn = [0.95, 0.05, 0, 0]
  elif(6 <= userLevel <= 15):
    raritySpawn = [0.74, 0.20, 0.05, 0.01]
  elif(16 <= userLevel <= 30):
    raritySpawn = [0.50, 0.30, 0.15, 0.05]
  else:
    raritySpawn = [0.20, 0.35, 0.30, 0.15]

  rarity = np.random.choice(np.arange(0, 4), p = [raritySpawn[0], raritySpawn[1], raritySpawn[2], raritySpawn[3]])
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


def RandomGenerateStatNumber(stat):
  c = np.random.choice(np.arange(-5,5))
  if(stat + c < 0):
    return 0
  return stat + c
  
def GenerateCardStats(cardIndexNumber):
  CardsList = DL.GetCardsBaseStatList()
  #Base Stat (HP, Atk, Def, Magic, Magic Def, Speed)
  BaseStats = CardsList[cardIndexNumber][3]
  HP = RandomGenerateStatNumber(BaseStats[0])
  Atk = RandomGenerateStatNumber(BaseStats[1])
  Def = RandomGenerateStatNumber(BaseStats[2])
  Magic = RandomGenerateStatNumber(BaseStats[3])
  MagicDef = RandomGenerateStatNumber(BaseStats[4])
  Speed = RandomGenerateStatNumber(BaseStats[5])
  return [HP, Atk, Def, Magic, MagicDef, Speed]

def GenerateCard(level, rarity, cardIndexNumber, userLevel):
  if(level == None):
    level = GetEnemyLevel(userLevel)
  if(rarity == None):
    rarity = GetEnemyRarity(userLevel)
  if(cardIndexNumber == None):
    cardIndexNumber = GetCardIndexNumber(rarity)
  CardBaseStats = GenerateCardStats(cardIndexNumber)
  return level, rarity, cardIndexNumber, CardBaseStats
#-----------------------------------#
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
def damage(p1, p2, attackType):
  #p1 damaging p2
  #HP, Atk, Def, Magic, Magic Def, Spd
  attackType = "normal"
  p1 = [9, 7, 7, 2, 4, 3]
  p2 = [7, 6, 5, 4, 7, 8]
  if attackType == "normal":
    return(p2[2] - (((np.random.choice(np.arange(75,126))))*(p1[1]))*0.01).round(1)
  if attackType == "magic":
    return (p2[4] - ((((np.random.choice(np.arange(75,126))))*(p1[3]))*0.01).round(1))

def whoMovesFirst(p1, p2):
  p1 = [9, 3, 7, 2, 2, 3]
  p2 = [7, 2, 5, 4, 3, 3]
  if p1[-1] > p2[-1]:
    return "p1"
  elif p1[-1] == p2[-1]:
      if np.random.choice(np.arange(0, 2)) == 1:
        return "p1"
      else:
        return "p2"
  else:
      return "p2"

def hpLeft(playerHP, damage):
  hp = playerHP - damage
  if hp < 0:
    return 0
  else:
    return hp


