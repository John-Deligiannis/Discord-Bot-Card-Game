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
connection.execute('''DROP TABLE cards''')
#connection.execute('''ALTER TABLE users RENAME COLUMN SelectedCard TO SelectedCardCode;''')

"""connection.execute('''CREATE TABLE IF NOT EXISTS users(
  UserID              INT      PRIMARY KEY    NOT NULL,
  EXPAtCurrentLevel   INT      NOT NULL,
  Level               INT      NOT NULL,
  Coins               INT      NOT NULL,
  MessagesSent        INT      NOT NULL,
  SelectedCardCode    TEXT     NOT NULL,
  Equipments          TEXT     NOT NULL);''')"""

#Card Code / Card Owner UserID / Card Index Number / Card Level / Base Stat (HP, Atk, Def, Magic, Magic Def, Spd) / HeldItems
connection.execute('''CREATE TABLE IF NOT EXISTS cards(
  CardCode          TEXT     PRIMARY KEY    NOT NULL,
  CardOwnerUserID   INT      NOT NULL,
  CardIndexNumber   INT      NOT NULL,
  CardLevel         INT      NOT NULL,
  BaseStat          TEXT     NOT NULL,
  HeldItem1         TEXT     NOT NULL,
  HeldItem2         TEXT     NOT NULL);''')

connection.commit()
connection.close()

SubTasks.PrintTextLine("cyan")
print(colored("Databases have been successfully created and saved!","green"))
SubTasks.PrintTextLine("cyan")
#-----------------------------------#
