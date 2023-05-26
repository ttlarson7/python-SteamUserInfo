"""
request.py

Authors: Blake Copock, Taz Larson

This program sets up the backend for the user interface, it \n
creates two classes, SteamUser and SteamGame. In addition there are \n
multiple functions as well that set up dictionarys and lists used in the \n
front end 
"""

"""
Import Config:
    Allows us to create an environment that stores the steam api key
Import Steam:
    reuired to access the steam api, also creates easier methods to access information
"""


from decouple import config
from steam import Steam

# Gets access to steam
KEY = config("STEAM_KEY")
steam = Steam(KEY)


class SteamUser:
    '''Steam user class that stores persona (a sort of temporary
    username allowed on Steam) and steamid. The class also
    methodizes Steam API calls, allowing calls to be made on a per-user
    basis.
    '''
    def __init__(self, steam_id):
        '''
        Gives the class attributes that the methods can use \n
        Arg:
        - steam_id - string: the user's steam_id number
        '''
        #confers the passed-in steamid
        self.steam_id = int(steam_id)
        self.persona_name = steam.users.get_user_details(steam_id)['player']['personaname']
    def get_friends(self):
        '''
        Query Steam for user's friends, return list \n
        of dicts each including name, steamid, and more\n
        '''
        try:
            friendlist = steam.users.get_user_friends_list(self.steam_id)["friends"]
            friend_dict = {}
            for friend in friendlist:
                friend_dict[friend['personaname']] = friend
            for friend in friend_dict.copy():
                friend_dict[friend] = SteamUser(friend_dict[friend]['steamid'])
            return friend_dict
        except:
            pass

    def get_games(self):
        '''
        Returns a list of dictionaries of the user's owned games, each \n
        including game name, game id, playtime, and last time played.
        '''
        try: 
            games = steam.users.get_owned_games(self.steam_id)['games']
            game_dict = {}
            for game in games:
                game_dict[game['name']] = game
            for game in game_dict.copy():
                game_dict[game] = SteamGame(game_dict[game]['appid'],game_dict[game]['name'])
                #if not game_dict[game].app_stats(self.steam_id):
                    #del game_dict[game]
            return game_dict
        except KeyError:
            pass

    def get_level(self):
        '''
        Get request to get the user's steam levels and returns the user's level
        '''
        return steam.users.get_user_steam_level(self.steam_id)


class SteamGame:
    '''
    This class creates a SteamGame object that allows access to app stats, \n
    along with app_achievments.
    '''
    def __init__(self, app_id, name):
        '''
        Gives the class an identifying attribute that the methods can use \n
        Arg:
        - steam_id - string: the user's steam_id number
        '''
        self.app_id = int(app_id)
        self.game_name = name

    def app_stats(self, steam_id):
        '''get SteamUser stats for SteamGame object
        Arg:
            steam_id - string - steam_id of the user whose stats are being requested.
        '''
        try:
            stats = steam.apps.get_user_stats(steam_id, self.app_id)
            stat_list = stats['playerstats']['stats']
            stat_dict = {}
            for stat in stat_list:
                stat_dict[stat['name']] = stat['value']
            return stat_dict
        except Exception:
            no_stats = ["No Stats"]
            return no_stats
    
    def app_achievements(self, steam_id):
        '''get SteamUser achievements for SteamGame object
        Arg:
            steam_id - string - steam_id of the user whose stats are being requested.
        '''
        #api request stored in variable in case additional parsing is needed.
        achievements = steam.apps.get_user_stats(steam_id, self.app_id)
        return achievements


def objectify_user(user_name):
    '''
    Gets the steam user id and returns the SteamUser Object
    Arg:
        user_name - string - the username associated with the account.
    '''
    user = steam.users.search_user(user_name)
    # gets the steam id number from user dict
    user_steam_id = user['player']['steamid']
    return SteamUser(user_steam_id)



def friend_has(gamename, friend):
    '''Check a friend's Steam library for a particular game. Return
    boolean.
    Arg:
        gamename: id of game to check friend's library for.
        friend: friend SteamUser to conduct library search on.
    Test:
        umok = objectify_user("Ummm_Okay")
        d2 = umok.get_games()['Destiny 2']
        wrath = umok.get_friends()['Wrath']
        print(friend_has(d2.game_name, wrath))
    '''
    try:
        friend_games = friend.get_games()
        if gamename in friend_games.keys():
            return True
        return False
    #When friend has no games, friend_games is NoneType object instead of dict.
    #Since gameless friends dont have games, they don't have the game with name
    #gamename, so we can safely return false.
    except AttributeError:
        return False

def friends_have(gamename, friends):
    '''
    Collects the friends who have a particular game into a dict.
    Arg:
        Friends: dictionary of SteamUser objects.
        Gamename: name of the game to check friends' libraries for.
    '''
    friends_own = {}
    for friend in friends:
        if friend_has(gamename, friends[friend]):
            friends_own[friend] = friends[friend]
    return friends_own

