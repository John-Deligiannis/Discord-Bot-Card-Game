#-----------------------------------#
            #Importations#
#-----------------------------------#
import sqlite3
#-----------------------------------#
            #Functions#
#-----------------------------------#
def extract_user_id(user_id_string):
  return int(user_id_string[3:-1])


def connect_to_db():
  connection = sqlite3.connect("Database.db")
  cursor = connection.cursor()
  return connection, cursor


def read_db(cursor, dbName, columnName, newValue):
  cursor.execute(f"SELECT * FROM {dbName} WHERE {columnName} = {newValue}")
  return cursor.fetchall()


def update_db(cursor, dbName, columnName, newValue, verifyColumnName, verifyValue):
  cursor.execute(f"UPDATE {dbName} SET {columnName} = '{newValue}' WHERE {verifyColumnName} = {verifyValue}")
#-----------------------------------#
