import discord
import menu
import utils
import userCollection

client = discord.Client()
user_list = userCollection.user_collection()
user_list.getAllUsersFile()
user_list.getUserFile()


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='!help'))
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower() == '!help':
        await message.channel.send(embed=menu.menuOp().showMangaIntro(pic=str(client.user.avatar_url)))
        await message.channel.send(embed=menu.menuOp().showMangaUtil())
        await message.channel.send(embed=menu.menuOp().showPicUtil())

    elif message.content.lower() == '!genres':
        await message.channel.send(embed=utils.list_genres())
    elif message.content.lower().startswith('!options'):
        await message.channel.send(embed=utils.list_search_options())

    elif message.content.lower().startswith('!include'):
        tmp = str(message.content).split(" ")[1:]
        res = user_list.insertPrefInclude(name=str(message.author), pref=tmp)
        if res is None:
            await message.channel.send("Command Failed. Please do !create first to create a profile")
        elif len(res) != 0:

            await message.channel.send("Failed to add: " + " ".join(res) + ". Use !genres to make sure you spelled it "
                                                                           "correctly")
        else:
            await message.channel.send("Added Genres to your preference")

    elif message.content.lower().startswith('!exclude'):
        tmp = str(message.content).split(" ")[1:]
        res = user_list.insertPrefExclude(name=str(message.author), pref=tmp)
        if res is None:
            await message.channel.send("Command Failed. Please do !create first to create a profile")
        elif len(res) != 0:
            await message.channel.send("Failed to add: " + " ".join(res) + ". Use !genres to make sure you spelled it "
                                                                           "correctly")
        else:
            await message.channel.send("Added Genres to your preference")

    elif message.content.lower().startswith('!rmInclude'):
        tmp = str(message.content).split(" ")[1:]
        res = user_list.removePrefInclude(name=str(message.author), pref=tmp)
        if res is None:
            await message.channel.send("Command Failed. Please do !create first to create a profile")
        elif len(res) != 0:
            await message.channel.send(
                "Failed to remove: " + " ".join(res) + ". Use !genres to make sure you spelled it "
                                                       "correctly")
        else:
            await message.channel.send("Removed Genres from your preference")

    elif message.content.lower().startswith('!rmExclude'):
        tmp = str(message.content).split(" ")[1:]
        res = user_list.removePrefExclude(name=str(message.author), pref=tmp)
        if res is None:
            await message.channel.send("Command Failed. Please do !create first to create a profile")
        elif len(res) != 0:
            await message.channel.send("Failed to remove: " + " ".join(res),
                                       ". Use !genres to make sure you spelled it "
                                       "correctly")
        else:
            await message.channel.send("Removed Genres from your preference")

    elif message.content.lower() == '!reset':
        user_list.resetAll(name=str(message.author))
        await message.channel.send("Removed all preferences")

    elif message.content.lower() == '!resetInclude':
        user_list.resetInclude(name=str(message.author))
        await message.channel.send("Removed all Include preferences")

    elif message.content.lower() == '!resetExclude':
        user_list.resetExclude(name=str(message.author))
        await message.channel.send("Removed all Exclude preferences")

    elif message.content.lower().startswith('!pref'):
        contents = user_list.getPref(name=str(message.author))
        res = utils.showPref(name=str(message.author), pref=contents, profile_pic=str(message.author.avatar_url))
        await message.channel.send(embed=res)

    elif message.content.lower().startswith('!new'):
        await message.channel.send(embed=utils.newCommand())

    elif message.content.lower().startswith('!amount'):
        msg = str(message.content).split(" ")
        if int(msg[1]) < 0 or int(msg[1]) > 5:
            await message.channel.send("Invalid number. You can only set from 1 - 5")
        else:
            user_list.set_show_amount(name=str(message.author), val=int(msg[1]))
            await message.channel.send("Amount set")

    elif message.content.lower().startswith('!orderby'):
        msg = str(message.content).split(" ")
        print(msg[1])
        tmp = user_list.set_order_by(name=str(message.author), op=str(msg[1]))

        if tmp is None:
            await message.channel.send("Invalid orderby tag. Do `!options` to see what tags there are")
        else:
            await message.channel.send("Orderby tag set")


    elif message.content.lower().startswith('!create'):
        user_list.createProfile(name=str(message.author))
        await message.channel.send("Profile created! You can now include/exclude genres from !genres\n"
                                   "Now you can use the !include [genre(s)] or !exclude [genre(s)] command.\n"
                                   "Do !help for more info")

    elif message.content.lower().startswith('!save'):
        user_list.writeAllUsersFile()
        user_list.writeUserFile()
        await message.channel.send("Preferences Saved")

    elif message.content.lower().startswith('!randomsearch'):

        pref = user_list.getPref(str(message.author))
        if pref is None:
            await message.channel.send("No profile detected. Use !create to make one")
            return

        res = utils.search_rand_manga(pref=pref)
        print(res)
        for emb in res:
            await message.channel.send(embed=emb)

    elif message.content.lower().startswith('!search'):
        pref = user_list.getPref(str(message.author))
        if pref is None:
            await message.channel.send("No profile detected. Use !create to make one")
            return

        tmp = str(message.content).split(" ")
        if len(tmp) == 1:
            await message.channel.send("Please specify a page number. Use !pages to see the range of pages you can "
                                       "choose from")
            return

        res = utils.search_manga(pref=pref, page_num=int(tmp[1]))
        for emb in res:
            await message.channel.send(embed=emb)

    elif message.content.lower().startswith('!pages'):
        pref = user_list.getPref(str(message.author))

        if pref is None:
            await message.channel.send("No profile detected. Use !create to make one")
            return

        result = utils.getPages(pref=pref)
        await message.channel.send("There are `" + str(result) + "` pages in your search list")

    elif message.content.lower().startswith('!dog'):
        await message.channel.send(embed=utils.getDogPic())

    elif message.content.lower().startswith('!pat'):
        await message.channel.send(embed=utils.getAnimePic())


    print(message.author)
    print(message.content)


client.run('Token here')
