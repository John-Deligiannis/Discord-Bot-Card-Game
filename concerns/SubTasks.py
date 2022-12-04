    #-----------------------------------#
            #Importations#
#-----------------------------------#
import time
import random
import sqlite3
from termcolor import colored
#-----------------------------------#
def PrintTextLine(color):
  print(colored("-" * 24, color))
#-----------------------------------#
def IsAdmin(userRoles):
  for role in userRoles:
    if(role.id == 864367392738246677):
      return True
  return False
#-----------------------------------#
def GetNumberAbbreviation(n):
  if n < 1000:
    return str(n)
  elif n >= 1000 and n < 1000000:
    return str(n//1000) + "K"
  elif n >= 1000000 and n < 1000000000:
    return str(n//1000000) + "M"
  elif n >= 1000000000 and n < 1000000000000:
    return str(n//1000000000) + "B"
  else:
    return str(n//1000000000000) + "T"
#-----------------------------------#
def GetLevelUpCoinReward(originalLevel, newLevel):
  if originalLevel != newLevel:
    collectiveCoins = 0
    for level in range(originalLevel, newLevel + 1):
      collectiveCoins += 5 + (level//15) 
    return collectiveCoins
  return 0
#-----------------------------------#
def CalculateForChatEXP(wordCount):
  return random.randint(round(wordCount/2), wordCount + round(wordCount/4))
#-----------------------------------#
#calculates for the new level count with a set exp increase. Existing level and EXP on the current plane of level are accounted for
def CalculateForLevel(EXPInput, EXPAtCurrentLevel, level):
  #Positive Value#
  if EXPInput > 0:
    if EXPInput + EXPAtCurrentLevel < (level + 1) * 1000: return level, EXPInput + EXPAtCurrentLevel, (level + 1) * 1000
    
    EXPInput += EXPAtCurrentLevel
    while EXPInput > 0:
      if EXPInput - ((level + 1) * 1000) < 0: break
      EXPInput -= (level + 1) * 1000
      level += 1

    return level, EXPInput, (level + 1) * 1000
  #Negative Value#
  elif EXPInput < 0: 
    if EXPAtCurrentLevel - abs(EXPInput) >= 0:
      return level, (EXPAtCurrentLevel - abs(EXPInput)), ((level + 1) * 1000)

    EXPInput += EXPAtCurrentLevel
    while EXPInput < 0 and level > 0:
      EXPInput += level * 1000
      level -= 1
  #Zero#
  else:
    return level, EXPAtCurrentLevel, (level + 1) * 1000

  if level < 0: level = 0
  if EXPInput < 0: EXPInput = 0
  return level, EXPInput, (level + 1) * 1000


#calculate from a given level to the corresponding EXP count
def FromLevelToEXP(EXPAtLevel, level):
  return EXPAtLevel + 1000 * sum(range(1, level + 1))
#-----------------------------------#
#-----------------------------------#
def CalculateForReward(PointsScored, TotalPoints, PreviousCompletionValue, TotalReward):
  #20:80 completion reward ratio
  firstFiftyPercent = 0.2
  secondFiftyPercent = 0.8

  #re-evaluate CV and PCV
  completionValue = PointsScored / TotalPoints
  PreviousCompletionValue = PreviousCompletionValue / 100
  
  if completionValue <= 0.5:
    return round(((completionValue - PreviousCompletionValue) / 0.5) * (firstFiftyPercent * TotalReward))
    
  else:
    PCV = 0
    if PreviousCompletionValue > 50:
      PCV = ((PreviousCompletionValue - 0.5) / 0.5) * (secondFiftyPercent * TotalReward)
    else:
      PCV = ((PreviousCompletionValue) / 0.5) * (firstFiftyPercent * TotalReward)
      
    CV = ((completionValue - 0.5) / 0.5) * (secondFiftyPercent * TotalReward) + (firstFiftyPercent * TotalReward)
    
    return round(CV - PCV)


def CalculateForCCCEXPReward(PointsScored, TotalPoints, PreviousCompletionValue):
  TotalEXPReward = ((TotalPoints - 2) * (1.1 ** (TotalPoints - 3))) * 1000 #exp reward formula
  return CalculateForReward(PointsScored, TotalPoints, PreviousCompletionValue, TotalEXPReward)


def CalculateForCCCCoinReward(PointsScored, TotalPoints, PreviousCompletionValue):
  TotalCoinReward = (TotalPoints ** 2) - (TotalPoints ** 1.85) + (13 ** (TotalPoints//10)) #coin reward formula
  return CalculateForReward(PointsScored, TotalPoints, PreviousCompletionValue, TotalCoinReward)
#-----------------------------------#
def SetDefaultData(UserID):
  connection = sqlite3.connect("Database.db")
  cursor = connection.cursor()
  
  cursor.execute(f"INSERT INTO users VALUES({UserID}, {0}, {0}, {0}, {0}, '', '');")
  
  #cardList = []
  cursor.execute(f"INSERT INTO cards VALUES({UserID});")

  cursor.execute(f"SELECT * FROM users WHERE UserID = {UserID};")
  userStat = cursor.fetchall()
  
  connection.commit()
  connection.close()

  return userStat
#-----------------------------------#
def GetBotChannelID(ServerName):
  if ServerName == "Test Server":
    return 869696625017229432
  elif ServerName == "Fallen Hope: Battle Heroes":
    return 1044473570425847878
  elif ServerName[:7] == "The SCU":
    return 833831903878053908
  return None
#-----------------------------------#
#Database contains data from every server, the following cuts out users of which are not associated with the server that the command is ran on#
def GetUsersInTheServer(allUserStats, guildMembers):
  indexToRemove = []
  for i in range (0, len(allUserStats)):
    UserIsInServer = False
    for member in guildMembers:
      if allUserStats[i][0] == member.id:
        UserIsInServer = True
        break
    if not UserIsInServer:
      indexToRemove.append(i)

  for i in range(len(indexToRemove) - 1, -1, -1):
    del allUserStats[indexToRemove[i]]
  
  return allUserStats
#-----------------------------------#
