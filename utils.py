from mangaIndex import bakaWebScrap as bak
import discord
import pydogapi
import anime_images_api

##############################
#Random api libaries and also util for the bot to list help commands
#############################



def list_genres():
    obj = bak.baka()
    tmp = ''
    for i in obj.all_genres:
        tmp += '`' + i + '`\n'
    emb = discord.Embed(title="List of all Manga genres", description=tmp)
    emb.set_thumbnail(url='https://2.bp.blogspot.com/-7qXydPpzXYE/V5_P-CpefUI/AAAAAAAADSU'
                          '/h9pzlyPlpR4CuaWmgYyVbEF8YPDEtW78wCLcB/s1600/manga-girl-gif.gif')
    return emb;


def list_search_options():
    emb = discord.Embed(title="Search options: ", description="Change how you search for a manga")
    emb.set_thumbnail(url='https://static1.cbrimages.com/wordpress/wp-content/uploads/2020/02/Featured-Image-Nichijou'
                          '-Magnifying-Glass-Cropped.jpg?q=50&fit=crop&w=960&h=500&dpr=1.5')
    emb.add_field(name='`!amount`', value="Prints # of manga results based on the number. `MAX 5`", inline=False)
    emb.add_field(name='`!searchby`', value='Changes how the search works.\nOptions: rating year title', inline=False)
    return emb

    # = ['title','year','rating']


def getUserPreference(user):
    try:
        file = open('storage/' + user + '.txt', 'r')
        line = file.readline()
        while line:
            user = line.split(" ")
            line = file.readline()


    except FileNotFoundError:
        file = open('include.txt', 'w')
        file.close()


def getDogPic():
    emb = discord.Embed()
    dog = pydogapi.DogAPI().random()['message']
    emb.set_image(url=dog)
    return emb


def getAnimePic():
    pic = anime_images_api.Anime_Images()
    anime = anime_images_api.Anime_Images()

    # anime.help()

    sfw = anime.get_sfw('pat')
    emb = discord.Embed()
    emb.set_image(url=sfw)
    return emb





def showPref(name, pref, profile_pic):
    strName = name + "'s manga preference"
    emb = discord.Embed(title=strName, description='Manga search profile')
    emb.set_thumbnail(url=profile_pic)
    tmp = pref['include']
    val = ''
    if len(tmp) == 0:
        val = "None"
    else:
        for i in tmp:
            val += i + '\n'

    emb.add_field(name='`Include`', value=val, inline=False)

    tmp = pref['exclude']
    val = ''
    if len(tmp) == 0:
        val = "None"
    else:
        for i in tmp:
            val += i + '\n'
    emb.add_field(name='`Exclude`', value=val, inline=False)

    pageAmount = "Search result amount: " + str(pref['options']['show_amount'])
    order_by = "Order by: " + pref['options']['order_by']
    emb.add_field(name='`Search Options`', value=pageAmount + '\n' + order_by)

    return emb;


def search_rand_manga(pref):
    tmp = bak.baka()
    tmp.reset_exclude_tag()
    tmp.reset_include_tag()
    tmp.setInclude_tags(pref['include'])
    tmp.setExclude_tags(pref['exclude'])
    show_amount = int(pref['options']['show_amount'])
    result = tmp.random_search_by_tag()


    emb_list = []
    for i in range(show_amount):
        if i < len(result):
            emb_list.append(mangaEmb(result[i]))
    return emb_list

def search_manga(pref, page_num):
    tmp = bak.baka()
    tmp.reset_exclude_tag()
    tmp.reset_include_tag()
    tmp.setInclude_tags(pref['include'])
    tmp.setExclude_tags(pref['exclude'])
    order_by = pref['options']['order_by']
    show_amount = int(pref['options']['show_amount'])
    tmp.setSearchInfo(page=page_num,perpage=5,orderby=order_by)
    result = tmp.search_by_tags(page=page_num)

    emb_list = []
    for i in range(show_amount):
        if i < len(result):
            emb_list.append(mangaEmb(result[i]))
    return emb_list

def mangaEmb(result):
    desc = result['desc'] + '\n' + result['score']
    emb = discord.Embed(title=result['title'], description=result['desc'])
    img = ''
    if result['img'] is None:
        img = 'https://cdn.discordapp.com/attachments/764231420440215632/866920140196937748/diepls.jpg'
    else:
        img = result['img']
    emb.set_image(url=img)
    emb.add_field(name="More details", value=result['web'], inline=False)
    return emb

def getPages(pref):
    tmp = bak.baka()
    tmp.setInclude_tags(pref['include'])
    tmp.setExclude_tags(pref['exclude'])
    order_by = pref['options']['order_by']
    tmp.setSearchInfo(perpage=5,orderby=order_by)
    return tmp.getPageNumber()


def newCommand():
    emb = discord.Embed(title='Bakaupdates Manga Generator', description="Everything you need to know about "
                                                                         "the how to start and manage the generator"
                                                                         "step by step")

    emb.set_thumbnail(url='https://www.pikpng.com/pngl/b/114-1145964_view-loli-thinking-1-anime-thinking-clipart.png')

    emb.add_field(name='`1. !create`', value="This will create a new profile for you to insert/remove preferences",
                  inline=False)
    emb.add_field(name='`2. !genres`', value="This will list all of the possible genres for you to include/exclude")
    emb.add_field(name='`3. !help`', value="Use `!help` to see one of the many `!include`, `!exclude` commands"
                                           "\n The [genre(s)] allow you to list the multiple genres with a space"
                                           "\n `GENRES WITH MULTIPLE WORDS MUST BE WRITTEN WITH _ BETWEEN EACH WORD`"
                                           "\n Ex. slice_of_life", inline=False)
    emb.add_field(name='`4. !save`', value="Use `!save` to save your preferences. This is so if the bot shuts down,"
                                           " it will retain your info upon next launch", inline=False)
    emb.add_field(name='`5. !options`', value="OPTIONAL. Search is set to 1 result and by rating by default")
    emb.add_field(name="`6. !amount and !orderby`", value="Change your search preferences if needed(Optional)."
                                                          "\n`WARNING`: These search results are not saved, so if "
                                                          "the bot turns off, you must set the commands again."
                                                          "\nUse `!pref` to see your current commands")
    emb.add_field(name='`7. !pages`',value='Only for !search [page#]. Tells you the amount of search results pages'
                                           ' based on your preferences')
    emb.add_field(name='`8. !randomSearch or !search [page#]`', value='Search for some manga!', inline=False)
    emb.add_field(name='`WARNINGS`', value='All manga is being webscrapped from bakaupdates. That means that `hentai`,'
                                           '`lolicon` and other interesting tags are included. You can choose to '
                                           'exclude them in your search by `!exclude [genre(s)]`', inline=False)

    return emb;
