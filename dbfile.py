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
connection.execute('''CREATE TABLE users(
  UserID              INT      PRIMARY KEY    NOT NULL,
  EXPAtCurrentLevel   INT      NOT NULL,
  Level               INT      NOT NULL,
  Coins               INT      NOT NULL,
  MessagesSent        INT      NOT NULL,
  EXPBooster          TEXT     NOT NULL,
  CoinBooster         TEXT     NOT NULL);''')

connection.execute('''CREATE TABLE cards_inventory(
  UserID          INT      PRIMARY KEY    NOT NULL);''')

connection.commit()
connection.close()

SubTasks.PrintTextLine("cyan")
print(colored("Databases have been successfully created and saved!","green"))
SubTasks.PrintTextLine("cyan")
#-----------------------------------#