#-----------------------------------#
            #Importations#
#-----------------------------------#
import sqlite3
from concerns import SubTasks
from termcolor import colored
connection = sqlite3.connect('Database.db')
#-----------------------------------#
        #Create & Save Table#
#-----------------------------------#
#connection.execute('''DROP TABLE cards_inventory''')
connection.execute('''CREATE TABLE IF NOT EXISTS users(
  UserID              INT      PRIMARY KEY    NOT NULL,
  EXPAtCurrentLevel   INT      NOT NULL,
  Level               INT      NOT NULL,
  Coins               INT      NOT NULL,
  MessagesSent        INT      NOT NULL,
  EXPBooster          TEXT     NOT NULL,
  CoinBooster         TEXT     NOT NULL);''')

#Card Code / Card Owner UserID / Card Index Number / Rarity (0, 1, 2, 3, 4, 5) / Base Stat (HP, Atk, Def, Magic, Magic Def, Spd) / HeldItems
connection.execute('''CREATE TABLE IF NOT EXISTS cards_inventory(
  CardCode          INT      PRIMARY KEY    NOT NULL,
  CardOwnerUserID   INT      NOT NULL,
  CardIndexNumber   INT      NOT NULL,
  BaseStat          TEXT     NOT NULL,
  HeldItem1         TEXT     NOT NULL,
  HeldItem2         TEXT     NOT NULL);''')

connection.commit()
connection.close()

SubTasks.PrintTextLine("cyan")
print(colored("Databases have been successfully created and saved!","green"))
SubTasks.PrintTextLine("cyan")
#-----------------------------------#
