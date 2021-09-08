import sqlite3
from datetime import datetime
import logging


logger = logging.getLogger('__name__')

try:
    connection = sqlite3.connect('botuser.db')
    cursor = connection.cursor()

    sqlite_guild_table='''CREATE TABLE guildinfo(
        guildname TEXT NOT NULL,
        guildid INTEGER
    );'''


    sqlite_mangauser_table='''CREATE TABLE mangauser(
        guildid INTEGER,
        username TEXT NOT NULL,
        userid INTEGER,
        title TEXT NOT NULL
    );'''


    sqlite_mangaupdate_table='''CREATE TABLE mangaupdate(
        title TEXT NOT NULL,
        chapter TEXT NOT NULL,
        author TEXT NOT NULL,
        date DATE
    );'''

    sqlite_scanlator_table='''CREATE TABLE scanlator(
        title TEXT NOT NULL,
        chapter TEXT NOT NULL,
        author TEXT NOT NULL,
        date DATE,
        link TEXT NOT NULL
    );'''

    sqlite_fanfox_table='''CREATE TABLE fanfox(
        title TEXT NOT NULL,
        chapter TEXT NOT NULL,
        author TEXT NOT NULL,
        date DATE,
        link TEXT NOT NULL
    );'''

    cursor.execute(sqlite_guild_table)
    cursor.execute(sqlite_mangauser_table)
    cursor.execute(sqlite_mangaupdate_table)
    cursor.execute(sqlite_scanlator_table)
    cursor.execute(sqlite_fanfox_table)

    connection.commit()
    logger.info('Tables created')

    cursor.close()

except sqlite3.Error as error:
    logger.error(f'Error while executing {error}')
finally:
    if connection:
        connection.close()
