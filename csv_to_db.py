import csv
import sqlite3
from sqlite3 import Error
import pandas as pd


def createSqliteConnection(database):

    conn = None
    try:
        print("----------Attempting to connect to database using Sqlite3 version {version} ...".format(version = sqlite3.version))
        conn = sqlite3.connect(database)
        print("----------Successfully to connected to {database}".format(database = database))

    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def pandasToDatabase(csvDocument, database, tableName):
    conn = sqlite3.connect(database)
    df = pd.read_csv(csvDocument)
    df.to_sql(tableName, conn, if_exists = "append", index = False)

def viewDatabaseTable(database, tblName):
    conn = sqlite3.connect(database)
    curs = conn.cursor()
    query = "SELECT * FROM {0}".format(tblName)
    curs.execute(query)
    rows = curs.fetchall()
    for row in rows:
        print(row)

def getDatabaseTable(database, tblName):
    conn = sqlite3.connect(database)
    curs = conn.cursor()
    query = "SELECT * FROM {0}".format(tblName)
    curs.execute(query)
    rows = curs.fetchall()
    return rows

if __name__ == '__main__':
    createSqliteConnection(r"data/youtube_data.db")
    pandasToDatabase("data/youtubeData.csv", "data/youtube_data.db", "youtube_data", )
    viewDatabaseTable("data/youtube_data.db", "youtube_data")
