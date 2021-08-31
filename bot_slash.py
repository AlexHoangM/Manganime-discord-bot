import os
import discord
import asyncio
import threading
import time
import logging
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component
from discord_slash.model import ButtonStyle
from dotenv import load_dotenv
import db.dbsqlite as dbsqlite
import mdexapi
import rss.rssMangaUpdate as rssMangaUpdate
import rss.rssFanFox as rssFanFox
import rss.rssScanlatorsParser as rssScanlatorsParser




logger = logging.getLogger('__name__')

logger.setLevel(level=logging.INFO)

format = logging.Formatter('[%(asctime)s]-[%(levelname)s] - %(message)s')

filehandler = logging.FileHandler('bot.log')
filehandler.setFormatter(format)

logger.addHandler(filehandler)



load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.members = True
intents.reactions = True

bot = commands.Bot(command_prefix = '/', intents=intents)
slash = SlashCommand(bot, sync_commands=True)

def checkUpdate_rssMU():
    olddata_tuplelist = []
    rssMU_olddata = rssMangaUpdate.rssParser()
    for i in range(len(rssMU_olddata)):
        release = rssMU_olddata[i]
        olddata_tuplelist.append((release['Title'], release['Chapter'], release['Author'], release['Date']))
    dbsqlite.populate_mangaupdate_table(olddata_tuplelist)
    
    while True:
        newdata_tuplelist = []
        rssMU_newdata = rssMangaUpdate.rssParser()
        if rssMU_newdata != rssMU_olddata:
            new_releases = [manga for manga in rssMU_newdata if manga not in rssMU_olddata]
            logger.info('Checked RSS MangaUpdate')
            #print(str(datetime.now().strftime("%H:%M:%S")), 'Checked RSS MangaUpdate')
            
            for release in new_releases:
                newdata_tuplelist.append((release['Title'], release['Chapter'], release['Author'], release['Date']))
                releasedata = getdata(release['Title'])
                asyncio.run_coroutine_threadsafe(sendNotification(releasedata[0], release['Chapter'], release['Author'], releasedata[2], releasedata[3], releasedata[4]), bot.loop)
            dbsqlite.populate_mangaupdate_table(newdata_tuplelist)
        time.sleep(30)
        rssMU_olddata = rssMU_newdata
        
def checkUpdate_rssFF():
    olddata_tuplelist = []
    rssFF_olddata = rssFanFox.rssParser()
    for i in range(len(rssFF_olddata)):
        release = rssFF_olddata[i]
        olddata_tuplelist.append((release['Title'], release['Chapter'], release['Date'], release['Link'], release['Source']))        
    dbsqlite.populate_fanfox_table(olddata_tuplelist)

    while True:
        newdata_tuplelist = []
        rssFF_newdata = rssFanFox.rssParser()
        if rssFF_newdata != rssFF_olddata:
            new_releases = [manga for manga in rssFF_newdata if manga not in rssFF_olddata]
            logger.info('Checked RSS Fanfox')
            #print(str(datetime.now().strftime("%H:%M:%S")) + 'Checked RSS Fanfox')

            for j in range(len(new_releases)):
                release = new_releases[j]
                newdata_tuplelist.append((release['Title'], release['Chapter'], release['Date'], release['Link'], release['Source']))
            dbsqlite.populate_fanfox_table(newdata_tuplelist)  
        time.sleep(30)
        rssFF_olddata = rssFF_newdata

def checkUpdate_rssScanlators():
    olddata_tuplelist = []
    rssS_olddata = rssScanlatorsParser.rssParser()
    for i in range(len(rssS_olddata)):
        release = rssS_olddata[i]
        olddata_tuplelist.append((release['Title'], release['Chapter'], release['Author'], release['Date'], release['Link'], release['Source']))    
    dbsqlite.populate_scanlator_table(olddata_tuplelist)
    
    while True:
        newdata_tuplelist = []
        rssS_newdata = rssScanlatorsParser.rssParser()
        if rssS_newdata != rssS_olddata:
            new_releases = [manga for manga in rssS_newdata if manga not in rssS_olddata]
            logger.info('Checked RSS Scanlators')
            #print(str(datetime.now().strftime("%H:%M:%S")) + 'Checked RSS Scanlators')

            for j in range(len(new_releases)):
                release = new_releases[j]
                newdata_tuplelist.append((release['Title'], release['Chapter'], release['Author'], release['Date'], release['Link'], release['Source']))
            dbsqlite.populate_scanlator_table(newdata_tuplelist)
        time.sleep(30)
        rssS_olddata = rssS_newdata

def getdata(manganame):
    datalist = []
    data = mdexapi.titleResult(manganame)
    #Check if this is the right manga
    if data != None:
        cleanTitle = mdexapi.mangaTitle(data)
        cleanDescription = mdexapi.mangaDescription(data)
        cleanURL = mdexapi.mangaLink(data)
        cleanID = mdexapi.mangaID(data)
        cleanimgID = mdexapi.coverID(mdexapi.coverResult(cleanID))
        cleanList = mdexapi.mangaList(data)

        datalist.extend([cleanTitle, cleanDescription, cleanURL, cleanID, cleanimgID, cleanList])
        return datalist
    else:
        datalist = None
        return datalist

async def sendNotification(title: str, chapter: int, author: str, url: str, id: int, imgid: int):
    if title != None:
        altlink1 = dbsqlite.select_altlinkscan(title)
        altlink2 = dbsqlite.select_altlinkfox(title)
        logger.info('Sending notification...')
        #print(str(datetime.now().strftime("%H:%M:%S")), 'Sending notification...')
        alluserids = dbsqlite.select_follow(title)
        for userid in alluserids:
            userstitle = dbsqlite.select_specfollow(userid)
            for reqtitle in userstitle:
                if reqtitle == title:
                    embednoti = discord.Embed(title = f'**{title}**', url = url, description = 'A new Chapter is out!')
                    embednoti.add_field(name = 'Chapter:', value = chapter, inline = True)                
                    embednoti.add_field(name = 'Scanlator:', value = author, inline = True)
                    embednoti.add_field(name = 'Alternate Link:', value = altlink1)
                    embednoti.add_field(name = 'Alternate Link:', value = altlink2)                
                    embednoti.set_image(url = f'https://uploads.mangadex.org/covers/{id}/{imgid}')
                    await bot.send_message(userid, embed=embednoti)
                    logger.info('Notification sent')
                    #print(str(datetime.now().strftime("%H:%M:%S")), 'Notification sent')
                    break


@bot.event
async def on_ready():
    logger.info('Bot is online')
    #print(str(datetime.now().strftime('%Y-%m-%d at %H:%M:%S')) + 'Bot is online')

@bot.event
async def on_guild_join(guild):
    if dbsqlite.select_guild(int(guild.id)):
        response = f'{guild} is already in database.'    
    else:
        try:
            recordlist = []
            recordlist.append((str(guild), int(guild.id)))
            dbsqlite.populate_guild_table(recordlist)
            response = f'{guild} is added to database.'
        except:
            response = f'{guild} is NOT added to database.'
    logger.info(f'{str(guild)} - {int(guild.id)}', response)
    #print(str(datetime.now().strftime('%Y-%m-%d at %H:%M:%S')), f'{str(guild)} - {int(guild.id)}', response)

@bot.event
async def on_guild_remove(guild):
    if dbsqlite.select_guild(int(guild.id)):
        try:
            dbsqlite.delete_guild(int(guild.id))
            response = f'{guild} is removed from database.'
        except:
            response = f'{guild} is NOT removed from database.'
    else:
        response = f'{guild} is NOT in databse.'
    logger.info(response)
    #print(str(datetime.now().strftime('%Y-%m-%d at %H:%M:%S')), response)


@slash.slash(name = 'ping', description = 'Ping bot\'s latency', guild_ids = [741769720830885970])
async def ping(ctx:SlashContext):
    await ctx.send(f'pong! {round(bot.latency * 1000)}ms ', delete_after=5)


@slash.slash(name='follow', description='Find and follow a manga', guild_ids = [741769720830885970])
async def find(ctx:SlashContext, title:str):

    listdata = getdata(title)
    if listdata != None:

        buttonYN = [create_button(style=ButtonStyle.green, label="Yes", custom_id='yes'), create_button(style=ButtonStyle.red, label="No", custom_id='no')]
        action_row = create_actionrow(*buttonYN)
            
        embed0 = discord.Embed(title = listdata[0], url = listdata[2], description = listdata[1])    
        embed0.add_field(name='Do you want to follow this manga ?', value='*Please react to the choices.*', inline=False)
        embed0.add_field(name='If this is _not_ the manga you are looking for', value='*Please provide with sufficient name length*', inline=False)
        embed0.set_thumbnail(url = f'https://uploads.mangadex.org/covers/{listdata[3]}/{listdata[4]}')

        embed0_edit = discord.Embed(title = listdata[0], url = listdata[2], description = listdata[1])
        embed0_edit.set_thumbnail(url = f'https://uploads.mangadex.org/covers/{listdata[3]}/{listdata[4]}')

        #Send embed and add button to message    
        confirm0mess = await ctx.send(embed = embed0, components=[action_row])

        #Add button to bot's message
        def check_buttonYN(res):
            return ctx.message.id == res.origin_message_id and ctx.channel == res.channel   
        try:
            res = await wait_for_component(bot, components=action_row , check=check_buttonYN, timeout=15)
            answer = res.component['label']
        except asyncio.TimeoutError:
            await ctx.send("**Timeout**, please try again", delete_after=3)
            await confirm0mess.edit(embed = embed0_edit, components=[])
        else:
            #If follow manga
            if answer == 'Yes':
                await confirm0mess.edit(embed = embed0_edit, components=[])
                
                #Add the message's author to the database
                if dbsqlite.select_userguild(str(ctx.message.author.id)) == ctx.message.author.id:
                    response0 = ''
                else:
                    try:
                        recordlist = []
                        recordlist.append((int(ctx.guild.id), str(ctx.message.author), int(ctx.message.author.id), listdata[0]))
                        dbsqlite.populate_mangauser_table(recordlist)
                        logger.info(f'{ctx.message.author} - {ctx.message.author.id} is added to database.')
                        #print(f'{ctx.message.author} - {ctx.message.author.id} is added to database.')
                        response0 = f'{ctx.message.author} - {ctx.message.author.id} is now be able to follow manga.'
                    except:
                        response0 = f'{ctx.message.author} - {ctx.message.author.id} is still not be able to follow manga.'

                #Follow the requested manga
                userstitle = dbsqlite.select_specfollow(ctx.message.author.id)
                for reqtitle in userstitle:
                    if reqtitle == listdata[0]:
                        response1 = f'{listdata[0]} is already being followed'
                    else:
                        try:
                            dbsqlite.populate_mangauser_table(str(ctx.message.guild), int(ctx.guild.id), str(ctx.message.author), listdata[0])
                            response1 = f'{ctx.message.author} is **following** {listdata[0]}'
                        except:
                            response1 = f'{listdata[0]} **could not** be followed'

                await ctx.send(response0 + '\n' + response1)
                logger.info(response0) 
                logger.info(response1)
                #print(str(datetime.now().strftime('%Y-%m-%d at %H:%M:%S'), response0, response1))
                
            #If no: return the link to the manga                
            elif answer == 'No':
                await confirm0mess.edit(embed = embed0_edit, components=[])       
    #If not found
    else:
        await ctx.send(f'{input} is **NOT found**! Please try again', delete_after=5)


@slash.slash(name='find', description='Find a manga', guild_ids = [741769720830885970])
async def find(ctx:SlashContext, title:str):

    listdata = getdata(title)
    if listdata != None:

        buttonYN = [create_button(style=ButtonStyle.green, label="Yes", custom_id='yes'), create_button(style=ButtonStyle.red, label="No", custom_id='no')]
        action_row = create_actionrow(*buttonYN)
            
        altlist = listdata[5]
        altlistmess = [f'-   {altlist[i]}' for i in range(len(altlist))]
        altmess = '\n'.join(message for message in altlistmess)

        embed0 = discord.Embed(title = listdata[0], url = listdata[2], description = listdata[1])    
        embed0.add_field(name='Is this the manga you are looking for ?', value='*Please react to the choices.*', inline=True)
        embed0.set_thumbnail(url = f'https://uploads.mangadex.org/covers/{listdata[3]}/{listdata[4]}')

        embed0_edit = discord.Embed(title = listdata[0], url = listdata[2], description = listdata[1])    
        embed0_edit.set_thumbnail(url = f'https://uploads.mangadex.org/covers/{listdata[3]}/{listdata[4]}')

        #Send embed and add button to message    
        confirm0mess = await ctx.send(embed = embed0, components=[action_row])

        #Add button to bot's message
        def check_buttonYN(res):
            return ctx.message.id == res.origin_message_id and ctx.channel == res.channel   
        try:
            res = await wait_for_component(bot, components=action_row , check=check_buttonYN, timeout=15)
            answer = res.component['label']
        except asyncio.TimeoutError:
            await ctx.send("**Timeout**, please try again", delete_after=3)
            await confirm0mess.edit(embed = embed0_edit, components=[])
        else:
            #If right manga
            if answer == 'Yes':
                await confirm0mess.edit(embed = embed0_edit, components=[])
            elif answer == 'No':
                await confirm0mess.edit(embed = embed0_edit, components=[])
                await ctx.send(f'>>> **Alternate possible mangas:** \n\n {altmess} \n\n *Please find other title in the list and search again*', delete_after=10)


@slash.slash(name = 'link', description='Get link of a manga\'s chapter', guild_ids = [741769720830885970])
async def chapter_link(ctx:SlashContext, title:str, chapter:str):

    listdata = getdata(title)
    if listdata != None:

        cleanChapter = chapter.strip()
        chapterLink = mdexapi.chapterLink(listdata[3], cleanChapter)

        if chapterLink is not None:
            embed = discord.Embed(title = f'{listdata[0]} - Chapter {cleanChapter} -  English', url = chapterLink, description = listdata[1])
            embed.set_thumbnail(url = f'https://uploads.mangadex.org/covers/{listdata[3]}/{listdata[4]}')
            await ctx.send(embed = embed)
        else:
            await ctx.send('Chapter **not found**', delete_after=5)
    else:
        await ctx.send('Manga **not found**', delete_after=5)


@slash.slash(name = 'unflmanga', description='Unfollow a manga from your list', guild_ids = [741769720830885970])
async def unfollow_single(ctx:SlashContext, title:str):

    listdata = getdata(title)
    cleanTitle = listdata[0]
    if cleanTitle != None:
        if dbsqlite.select_userguild(str(ctx.message.author)) == ctx.message.author:
            try:
                dbsqlite.delete_user_unfollow(cleanTitle)
                response = f'{cleanTitle} is no longer being followed!'
            except:
                response = f'Failed. {cleanTitle} could NOT be unfollowed!'
        else:
            response = f'{cleanTitle} is not being followed!'
    else:
        response = f'{cleanTitle} is NOT found!'
    await ctx.send(response, delete_after=5)
    logger.info(response)
    #print(str(datetime.now().strftime('%Y-%m-%d at %H:%M:%S')), response)


@slash.slash(name = 'unflallmanga', description='Unfollow all mangas from your list', guild_ids = [741769720830885970])
async def unfollow_all(ctx:SlashContext):
    try:
        dbsqlite.delete_user(int(ctx.message.author.id))
        response = f'{ctx.message.author} is NOT following any manga!'
    except:
        response = f'Failed. {ctx.message.author} is still following some mangas.'
    await ctx.send(response, delete_after=5)
    logger.info(response)
    #print(str(datetime.now().strftime('%Y-%m-%d at %H:%M:%S')), response)


@bot.command(name = 'mymangalist', description='View your entire manga list', guild_ids = [741769720830885970])
async def view_all(ctx):
    outmessage = ''
    try:
        mlist = dbsqlite.select_viewall(int(ctx.message.author.id))
        if len(mlist) == 0:
            response = f'{ctx.message.author} is NOT following any manga!'
            await ctx.send(response)
        else:
            for m in mlist:
                outmessage += ' - ' + m + '\n'
            embed = discord.Embed(title = f'{ctx.message.author}\'s manga', description = outmessage)
            embed.set_thumbnail(url = ctx.message.author.avatar.url)
            await ctx.send(embed = embed)
    except:
        response = f'Failed. Data of {ctx.message.author} could NOT be retrieved.'
        await ctx.send(response, delete_after=5)
    logger.info(response)

checkUpdate1 = threading.Thread(target=checkUpdate_rssMU)
checkUpdate2 = threading.Thread(target=checkUpdate_rssFF)
checkUpdate3 = threading.Thread(target=checkUpdate_rssScanlators)

checkUpdate1.start()
checkUpdate2.start()
checkUpdate3.start()

bot.run(TOKEN)