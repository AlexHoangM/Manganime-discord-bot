import sqlite3
from datetime import datetime
import logging


logger = logging.getLogger('__name__')

logger.setLevel(level=logging.INFO)

format = logging.Formatter('[%(asctime)s]-[%(levelname)s] - %(message)s')

filehandler = logging.FileHandler('sqlite.log')
filehandler.setFormatter(format)

logger.addHandler(filehandler)




#=============================================SELECT QUERIES==============================================




#Check if the guild is in guildinfo table
def select_guild(guildid) -> bool:
    try:
        connection = sqlite3.connect('botuser.db')
        cursor = connection.cursor()
        logger.info('Connected to sqlite')
        #print(str(datetime.now().strftime('%Y-%m-%d at %H:%M:%S')), 'Connected to sqlite')

        select_guild_query='''SELECT guildid FROM guildinfo WHERE guildid = ?'''
        cursor.execute(select_guild_query, (guildid,))
        record = cursor.fetchone()

        cursor.close()
        
    except sqlite3.Error as error:
        logger.error('Failed to get guildid', error)
        #print('Failed to get requested guildid', error)
    finally:
        if connection:
            connection.close()
            logger.info('Sqlite connection closed')
            #print(str(datetime.now().strftime('%Y-%m-%d at %H:%M:%S')), 'Sqlite connection closed')
    return record[0]


#Check if user is in mangauser table
def select_userguild(userid) -> bool:
    try:
        connection = sqlite3.connect('botuser.db')
        cursor = connection.cursor()
        logger.info('Connected to sqlite')
        #print(str(datetime.now().strftime('%Y-%m-%d at %H:%M:%S')), 'Connected to sqlite')

        select_user_query='''SELECT userid FROM mangauser WHERE userid = ?'''
        cursor.execute(select_user_query, (userid,))
        record = cursor.fetchone()

        cursor.close()
        
    except sqlite3.Error as error:
        logger.error('Failed to get requested userid', error)
        #print('Failed to get requested userid', error)
    finally:
        if connection:
            connection.close()
            logger.info('Sqlite connection closed')
            #print(str(datetime.now().strftime('%Y-%m-%d at %H:%M:%S')), 'Sqlite connection closed')
    return record[0]


#Get all userids from the title
def select_follow(title):
    userids = []
    try:
        connection = sqlite3.connect('botuser.db')
        cursor = connection.cursor()
        logger.info('Connected to sqlite')
        #print(str(datetime.now().strftime('%Y-%m-%d at %H:%M:%S')), 'Connected to sqlite')

        select_user_query='''SELECT userid 
                            FROM mangauser 
                            WHERE title = ?'''
        cursor.execute(select_user_query, (title,))
        record = cursor.fetchall()
        for row in record:
            userids.append(row[0])

        cursor.close()
        
    except sqlite3.Error as error:
        logger.error('Failed to get requested userid', error)
        #print('Failed to get requested userid', error)
    finally:
        if connection:
            connection.close()
            logger.info('Sqlite connection closed')
            #print(str(datetime.now().strftime('%Y-%m-%d at %H:%M:%S')), 'Sqlite connection closed')
    return userids


#Get title from specific userid
def select_specfollow(userid):
    titles = []
    try:
        connection = sqlite3.connect('botuser.db')
        cursor = connection.cursor()
        logger.info('Connected to sqlite')
        #print(str(datetime.now().strftime('%Y-%m-%d at %H:%M:%S')), 'Connected to sqlite')

        select_user_query='''SELECT title 
                            FROM mangauser 
                            WHERE userid = ?'''
        cursor.execute(select_user_query, (userid,))
        record = cursor.fetchall()
        for row in record:
            titles.append(row[0])

        cursor.close()
        
    except sqlite3.Error as error:
        logger.error('Failed to get requested users manga', error)
        #print('Failed to get requested users manga', error)
    finally:
        if connection:
            connection.close()
            logger.info('Sqlite connection closed')
            #print(str(datetime.now().strftime('%Y-%m-%d at %H:%M:%S')), 'Sqlite connection closed')
    return titles


#Select to view all manga
def select_viewall(userid):
    allmanga = []
    try:
        connection = sqlite3.connect('botuser.db')
        cursor = connection.cursor()
        logger.info('Connected to sqlite')
        #print(str(datetime.now().strftime('%Y-%m-%d at %H:%M:%S')), 'Connected to sqlite')

        select_user_query='''SELECT title 
                            FROM mangauser WHERE userid = ?'''
        cursor.execute(select_user_query, (userid, ))
        record = cursor.fetchall()
        for row in record:
            allmanga.append(row[0])

        cursor.close()
        
    except sqlite3.Error as error:
        logger.error('Failed to get requested users all manga', error)
        #print('Failed to get requested users manga', error)
    finally:
        if connection:
            connection.close()
            logger.info('Sqlite connection closed')
            #print(str(datetime.now().strftime('%Y-%m-%d at %H:%M:%S')), 'Sqlite connection closed')
    return allmanga


#Select alternative link of scanlator
def select_altlinkscan(title):
    try:
        connection = sqlite3.connect('botuser.db')
        cursor = connection.cursor()
        logger.info('Connected to sqlite')
        #print(str(datetime.now().strftime('%Y-%m-%d at %H:%M:%S')), 'Connected to sqlite')

        select_user_query='''SELECT link 
                            FROM scanlator 
                            WHERE title = ?'''
        cursor.execute(select_user_query, (title,))
        record = cursor.fetchone()

        cursor.close()
        
    except sqlite3.Error as error:
        logger.error('Failed to get requested link', error)
        #print('Failed to get requested userid', error)
    finally:
        if connection:
            connection.close()
            logger.info('Sqlite connection closed')
            #print(str(datetime.now().strftime('%Y-%m-%d at %H:%M:%S')), 'Sqlite connection closed')
    return record


#Select alternative link of fanfox
def select_altlinkfox(title):
    try:
        connection = sqlite3.connect('botuser.db')
        cursor = connection.cursor()
        logger.info('Connected to sqlite')
        #print(str(datetime.now().strftime('%Y-%m-%d at %H:%M:%S')), 'Connected to sqlite')

        select_user_query='''SELECT link 
                            FROM fanfox 
                            WHERE title = ?'''
        cursor.execute(select_user_query, (title,))
        record = cursor.fetchone()

        cursor.close()
        
    except sqlite3.Error as error:
        logger.error('Failed to get requested link', error)
        #print('Failed to get requested userid', error)
    finally:
        if connection:
            connection.close()
            logger.info('Sqlite connection closed')
            #print(str(datetime.now().strftime('%Y-%m-%d at %H:%M:%S')), 'Sqlite connection closed')
    return record




#=============================================POPULATE QUERIES==============================================




#INPUT MUST BE LIST OF TUPLE [(), (), (),...]
#Add new entries to guildinfo table
def populate_guild_table(recordlist):
    try:
        connection = sqlite3.connect('botuser.db')
        cursor = connection.cursor()

        #print(str(datetime.now().strftime('%Y-%m-%d at %H:%M:%S')), 'Connected to sqlite')

        populate_guild_query='''INSERT INTO guildinfo(guildname, guildid)
                                VALUES(?, ?);'''

        cursor.executemany(populate_guild_query, recordlist)
        connection.commit()
        logger.info('total', cursor.rowcount, 'added to guildinfo table')
        #print(str(datetime.now().strftime('%Y-%m-%d at %H:%M:%S')), 'total', cursor.rowcount, 'added to guildinfo table')
        connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        logger.error('Failed to add records to guildinfo table', error)
        #print('Failed to add records to guildinfo table', error)
    finally:
        if connection:
            connection.close()
            logger.info('Sqlite connection closed')
            #print('Sqlite connection closed')


#Add new entries to mangauser table
def populate_mangauser_table(recordlist):
    try:
        connection = sqlite3.connect('botuser.db')
        cursor = connection.cursor()
        logger.info('Connected to sqlite')
        #print(str(datetime.now().strftime('%Y-%m-%d at %H:%M:%S')), 'Connected to sqlite')

        populate_mangauser_query='''INSERT INTO mangauser(guildid, username, userid, title)
                                    VALUES(?, ?, ?, ?);'''

        cursor.executemany(populate_mangauser_query, recordlist)
        connection.commit()
        logger.info('total', cursor.rowcount, 'added to mangauser table')
        #print(str(datetime.now().strftime('%Y-%m-%d at %H:%M:%S')), 'total', cursor.rowcount, 'added to mangauser table')
        cursor.close()
    except sqlite3.Error as error:
        logger.error('Failed to add records to mangauser table', error)
        #print('Failed to add records to mangauser table', error)
    finally:
        if connection:
            connection.close()
            logger.info('Sqlite connection closed')
            #print('Sqlite connection closed')


#Add new entries to mangaupdate table
def populate_mangaupdate_table(recordlist):
    try:
        connection = sqlite3.connect('botuser.db')
        cursor = connection.cursor()
        logger.info('Connected to sqlite')
        #print(str(datetime.now().strftime('%Y-%m-%d at %H:%M:%S')), 'Connected to sqlite')

        populate_mangaupdate_query='''INSERT INTO mangauser(title, chapter, date, author, link)
                                    VALUES(?, ?, ?, ?, ?);'''

        cursor.executemany(populate_mangaupdate_query, recordlist)
        connection.commit()
        logger.info('total', cursor.rowcount, 'added to mangaupdate table')
        #print(str(datetime.now().strftime('%Y-%m-%d at %H:%M:%S')), 'total', cursor.rowcount, 'added to mangaupdate table')
        cursor.close()
    except sqlite3.Error as error:
        logger.error('Failed to add records to mangaupdate table', error)
        #print('Failed to add records to mangaupdate table', error)
    finally:
        if connection:
            connection.close()
            logger.info('Sqlite connection closed')
            #print('Sqlite connection closed')


#add new entries to scanlator table
def populate_scanlator_table(recordlist):
    try:
        connection = sqlite3.connect('botuser.db')
        cursor = connection.cursor()
        logger.info('Connected to sqlite')
        #print(str(datetime.now().strftime('%Y-%m-%d at %H:%M:%S')), 'Connected to sqlite')

        populate_scanlator_query='''INSERT INTO mangauser(title, chapter, date, author, link)
                                    VALUES(?, ?, ?, ?, ?);'''

        cursor.executemany(populate_scanlator_query, recordlist)
        connection.commit()
        logger.info('total', cursor.rowcount, 'added to scanlator table')
        #print(str(datetime.now().strftime('%Y-%m-%d at %H:%M:%S')), 'total', cursor.rowcount, 'added to scanlator table')
        cursor.close()
    except sqlite3.Error as error:
        logger.error('Failed to add records to scanlator table', error)
        #print('Failed to add records to scanlator table', error)
    finally:
        if connection:
            connection.close()
            logger.info('Sqlite connection closed')
            #print('Sqlite connection closed')


#Add new entries to fanfox table
def populate_fanfox_table(recordlist):
    try:
        connection = sqlite3.connect('botuser.db')
        cursor = connection.cursor()
        logger.info('Connected to sqlite')
        #print(str(datetime.now().strftime('%Y-%m-%d at %H:%M:%S')), 'Connected to sqlite')

        populate_fanfox_query='''INSERT INTO mangauser(title, chapter, date, author, link)
                                    VALUES(?, ?, ?, ?, ?);'''

        cursor.executemany(populate_fanfox_query, recordlist)
        connection.commit()
        logger.info('total', cursor.rowcount, 'added to fanfox table')
        #print(str(datetime.now().strftime('%Y-%m-%d at %H:%M:%S')), 'total', cursor.rowcount, 'added to fanfox table')
        cursor.close()
    except sqlite3.Error as error:
        logger.error('Failed to add records to fanfox table', error)
        #print('Failed to add records to fanfox table', error)
    finally:
        if connection:
            connection.close()
            logger.info('Sqlite connection closed')
            #print('Sqlite connection closed')




#=============================================DELETE QUERIES==============================================




#In case the guild remove the bot -> delete guild and all user and user's related info from db
def delete_guild(guildidlist):
    try:
        connection = sqlite3.connect('botuser.db')
        cursor = connection.cursor()
        logger.info('Connected to sqlite')
        #print(str(datetime.now().strftime('%Y-%m-%d at %H:%M:%S')), 'Connected to sqlite')

        delete_guild_query='''DELETE FROM guildinfo WHERE guildid = ?'''
        cursor.execute(delete_guild_query, (guildidlist, ))
        connection.commit()
        logger.info('total', cursor.rowcount, 'deleted from guildinfo table')
        #print(str(datetime.now().strftime('%Y-%m-%d at %H:%M:%S')), 'total', cursor.rowcount, 'deleted from guildinfo table')

        delete_user_query ='''DELETE FROM mangauser WHERE guildid = ?'''
        cursor.executemany(delete_user_query, guildidlist)     
        connection.commit()
        logger.info('total', cursor.rowcount, 'deleted from mangauser table')
        #print(str(datetime.now().strftime('%Y-%m-%d at %H:%M:%S')), 'total', cursor.rowcount, 'deleted from mangauser table')
        
        cursor.close()
    except sqlite3.Error as error:
        logger.error('Failed to delete requested guildid from guildinfo table', error)
        #print('Failed to delete requested guildid from guildinfo table', error)
    finally:
        if connection:
            connection.close()
            logger.info('Sqlite connection closed')
            #print(str(datetime.now().strftime('%Y-%m-%d at %H:%M:%S')), 'Sqlite connection closed')


#In case user left the guild / unfollow all -> remove all user's related info
def delete_user(useridlist):
    try:
        connection = sqlite3.connect('botuser.db')
        cursor = connection.cursor()
        logger.info('Connected to sqlite')
        #print(str(datetime.now().strftime('%Y-%m-%d at %H:%M:%S')), 'Connected to sqlite')

        delete_user_query='''DELETE FROM mangauser WHERE userid = ?'''
        cursor.executemany(delete_user_query, (useridlist,))
        connection.commit()
        logger.info('total', cursor.rowcount, 'deleted from mangauser table')
        #print(str(datetime.now().strftime('%Y-%m-%d at %H:%M:%S')), 'total', cursor.rowcount, 'deleted from mangauser table')

        cursor.close()
    except sqlite3.Error as error:
        logger.error('Failed to delete requested userid from mangauser table', error)
        #print('Failed to delete requested userid from mangauser table', error)
    finally:
        if connection:
            connection.close()
            logger.info('Sqlite connection closed')
            #print(str(datetime.now().strftime('%Y-%m-%d at %H:%M:%S')), 'Sqlite connection closed')


#In case user unfollow -> remove
def delete_user_unfollow(manganame):
    try:
        connection = sqlite3.connect('botuser.db')
        cursor = connection.cursor()
        logger.info('Connected to sqlite')
        #print(str(datetime.now().strftime('%Y-%m-%d at %H:%M:%S')), 'Connected to sqlite')

        delete_userunfollow_query='''DELETE FROM mangauser WHERE title = ?'''
        cursor.execute(delete_userunfollow_query, (manganame,))
        connection.commit()
        logger.info('total', cursor.rowcount, 'unfollowed from mangauser table')
        #print(str(datetime.now().strftime('%Y-%m-%d at %H:%M:%S')), 'total', cursor.rowcount, 'unfollowed from mangauser table')
    except sqlite3.Error as error:
        logger.error('Failed to unfollow requested title from mangauser table', error)
        #print('Failed to unfollow requested title from mangauser table', error)
    finally:
        if connection:
            connection.close()
            logger.info('Sqlite connection closed')
            #print(str(datetime.now().strftime('%Y-%m-%d at %H:%M:%S')), 'Sqlite connection closed')