class userInfo(object):
    def __init__(self,name=''):
        self.username = name
        self.include = []
        self.exclude = []
        self.search = {'show_amount': 1, 'order_by': 'rating'}

    def addInclude(self, item):
        self.include.append(item)


########
#Used to keep track of all of the users using this bot
########

class user_collection(object):
    def __init__(self):
        self.all_search_options = ['rating', 'year', 'title']
        self.all_genres = ['action', 'adult', 'adventure', 'comedy', 'doujinshi', 'drama', 'ecchi', 'fantasy',
                           'gender bender', 'harem', 'hentai', 'historical', 'horror', 'josei', 'lolicon',
                           'martial arts', 'mature', 'mecha', 'mystery', 'psychological', 'romance', 'school life',
                           'sci-fi', 'seinen', 'shotacon', 'shoujo', 'shoujo ai', 'shounen', 'shounen ai',
                           'slice of life', 'smut', 'sports', 'supernatural', 'tragedy', 'yaoi', 'yuri']
        self.all_users = []
        self.all_users_pref = {}

    def set_show_amount(self, name, val):
        if val > 5 and val < 1:
            return None
        tmp = self.all_users_pref.get(name)
        tmp.search['show_amount'] = val

    def set_order_by(self, name, op):
        print("Here:" ,op.lower())
        if op.lower() not in self.all_search_options:
            return None
        print("Here2")
        tmp = self.all_users_pref.get(name)
        tmp.search['order_by'] = op.lower()
        return True

    def createProfile(self, name):
        assert name is not str
        if name not in self.all_users:
            self.all_users.append(name)

        tmp = userInfo(name=name)


        self.all_users_pref[name] = tmp
    def insertPrefInclude(self, name, pref):

        if name not in self.all_users:
            return None
        tmp = self.all_users_pref.get(name)
        failed_insert = []

        for i in pref:
            i = " ".join(i.lower().split('_'))
            if i in self.all_genres and i not in tmp.include and i not in tmp.exclude:

                print("In here: ",i.lower())
                tmp.addInclude(i.lower())
            else:
                failed_insert.append(i.lower())

        return failed_insert

    def insertPrefExclude(self, name, pref):
        if name not in self.all_users:
            return None

        tmp = self.all_users_pref.get(name)
        failed_insert = []
        for i in pref:
            i = " ".join(i.lower().split('_'))
            if i in self.all_genres and i not in tmp.include and i not in tmp.exclude:
                print(i.lower())
                tmp.exclude.append(i.lower())
            else:
                failed_insert.append(i.lower())

        return failed_insert

    def removePrefExclude(self, name, pref):
        if name not in self.all_users:
            return None

        tmp = self.all_users_pref.get(name)
        failed_remove = []
        for i in pref:
            i = " ".join(i.lower().split('_'))
            if i in tmp.exclude:
                print(i.lower())
                tmp.exclude.remove(i.lower())
            else:
                failed_remove.append(i.lower())

        return failed_remove

    def removePrefInclude(self, name, pref):
        if name not in self.all_users:
            return None

        tmp = self.all_users_pref.get(name)
        failed_remove = []
        for i in pref:
            i = " ".join(i.lower().split('_'))
            if i in tmp.include:
                print(i.lower())
                tmp.include.remove(i.lower())
            else:
                failed_remove.append(i.lower())

        return failed_remove

    def resetAll(self, name):
        if name not in self.all_users:
            return None
        tmp = self.all_users_pref.get(name)
        tmp.include.clear()
        tmp.exclude.clear()

        self.all_users_pref[name] = tmp

    def resetInclude(self, name):
        if name not in self.all_users:
            return None
        tmp = self.all_users_pref.get(name)
        tmp.include.clear()

        self.all_users_pref[name] = tmp

    def resetExclude(self, name):
        if name not in self.all_users:
            return None
        tmp = self.all_users_pref.get(name)
        tmp.exclude.clear()

        self.all_users_pref[name] = tmp

    def getPref(self, name):
        if name not in self.all_users:
            return None
        tmp = self.all_users_pref.get(name)
        ret = {'name': tmp.username, 'include': tmp.include, 'exclude': tmp.exclude, 'options': tmp.search}
        return ret

    def getAllUsersFile(self):
        try:
            read = open('storage/users.txt', 'r')

            line = read.readline()
            while line:
                self.all_users.append(line.strip('\n'))
                self.createProfile(line.strip('\n'))
                line = read.readline()

        except FileNotFoundError:
            create = open('storage/users.txt', 'w')
            create.close()
        print("All Users: ", self.all_users)
        print("All user profile: ", self.all_users_pref)

    def writeAllUsersFile(self):
        write_file = open('storage/users.txt', 'w')
        for i in self.all_users:
            write_file.write(i + '\n')
        write_file.close()

    def getUserFile(self):
        for i in self.all_users:
            try:

                i = i.strip('\n')
                read_file = open('storage/' + i + '.txt', 'r')
                isInclude = True
                self.createProfile(i)
                tmp = self.all_users_pref.get(i)
                print(tmp)

                line = read_file.readline()
                while line:
                    if line.strip('\n') == 'include':
                        line = read_file.readline()
                        continue

                    if line.strip('\n') == 'exclude':
                        isInclude = False
                        line = read_file.readline()
                        continue

                    if isInclude == True:
                        tmp.include.append(line.strip('\n'))
                    else:
                        tmp.exclude.append(line.strip('\n'))
                    line = read_file.readline()
                read_file.close()
            except FileNotFoundError:
                create = open('storage/' + i + '.txt', 'r')
                create.close()

    def writeUserFile(self):
        for i in self.all_users:
            write_file = open('storage/' + i + '.txt', 'w')
            tmp = self.all_users_pref.get(i)
            write_file.write("include\n")
            for j in tmp.include:
                write_file.write(j + '\n')
            write_file.write("exclude\n")
            for k in tmp.exclude:
                write_file.write(k + '\n')
            write_file.close()



