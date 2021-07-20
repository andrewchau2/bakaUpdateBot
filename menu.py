import discord



#Shows the list of commands that the discord bot can do. Returns as an emb

class menuOp(object):

    def mangaValueMsgIntro(self):
        new_command = '`!new`' + ': Brief manga util introduction for first time users\n\n';
        genres_command = '`!genres`' + ': Lists all genre options to choose from\n\n'
        options_command = '`!options`: Displays all the search options for the manga util\n\n'
        preference_command = '`!pref`' + ': Shows your include and exclude preference\n\n'
        pages_command = '`!pages`: Shows the amount of pages available based on your pref\n\n '

        return new_command + genres_command + options_command + preference_command + pages_command

    def mangaValueMsg(self):
        setIncludegenres_command = '`!include [genre(s)]`' + ': Adds one or more genres to your ' \
                                                             'include ' \
                                                             'preference\n\n'

        setExcludegenres_command = '`!exclude [genre(s)]`' + ': Adds one or more genres to your ' \
                                                             'exclude ' \
                                                             'preference\n\n'

        removeInclude_command = '`!rmInclude [genre(s)]`' + ':Removes one or more genres from your ' \
                                                            'include preference\n\n '

        removeExeclude_command = '`!rmExclude [genre(s)]`' + ': Removes one or more genres from ' \
                                                             'your exclude preference\n\n '

        page_amount_command = '`!amount [1-5]`: Changes the amount of manga results the Fila bot prints\n\n'

        order_by_command = '`!orderby [tag]`: Changes the search preference. Use !options to see all search tags\n\n'

        resetInclude_command = '`!resetInclude`' + ': Resets everything in your include preference\n\n'

        resetExeclude_command = '`!resetExeclude`' + ': Resets everything in your exclude ' \
                                                     'preference\n\n '

        create_command = '`!create`: Creates a new preference\n\n'

        reset_command = '`!reset`' + ': Resets everything in your include and exclude preference\n\n'

        random_search_command = '`!randomsearch`: Does a random search based on include and excldue pref. Ignores' \
                                ' Search option preferences\n\n'

        search_command = '`!search [page#]`: Given a page number, it searches based on your preferences. If invalid ' \
                         'page number, the maximum possible page# will be displayed\n\n'

        tmp = create_command + setIncludegenres_command + setExcludegenres_command + \
              removeInclude_command + removeExeclude_command + page_amount_command + order_by_command + \
              random_search_command + search_command + resetInclude_command + resetExeclude_command + reset_command

        return tmp

    def pictureValueMsg(self):
        dog_command = '`!dog`: Shows a dog image\n\n'
        pat_command = '`!pat`: Shows a anime pat gif\n\n'

        return dog_command + pat_command

    def showMangaIntro(self,pic):
        emb = discord.Embed(title="\U0001F490 \U00002728 Fila's Commands \U00002728 \U0001F490",
                            description="Fila's handy toolkit")
        emb.set_thumbnail(url=pic)
        emb.add_field(name='\U000027A1 Manga Helper Commands',
                      value=self.mangaValueMsgIntro(),
                      inline=False)
        return emb

    def showMangaUtil(self):
        emb = discord.Embed(title="\U000027A1 Manga Util Commands",
                            description=self.mangaValueMsg())
        return emb

    def showPicUtil(self):
        emb = discord.Embed(title='\U000027A1 Pictures and Gifs',description=self.pictureValueMsg())
        return emb
