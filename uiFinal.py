"""
ui.py

Authors: Blake Copock, Taz Larson

This program sets up the user interface. It allows the user \n
to type in their steam name, and then see their games list and their \n
friends list. Then they can see their stats in certain games \n

Test usernames to use:
Ummm_Okay
ummm
Punkwaffl3
uk

Not every username works because in Steam there are some privacy \n
settings that if enabled can prevent the program from accessing their data. \n


"""


"""
PySimpleGUI: Allows up to set up the user interface of our program

newrequest: Imports the class and functions we
"""

import PySimpleGUI as sg
import requestFinal as rq


sg.theme('DarkBlue 9') # Add a touch of color
# Creates the collum allowing the user to enter their name
user_column = [
    [sg.Text('Enter Steam Username'), sg.InputText(), sg.Button('OK')],
    [sg.Text("Steam Username: "), sg.Text('', key='-username-')],
    [sg.Text("Steam Level: "), sg.Text('', key='-level-')]
]
# Creates the categories box with game  and social
categories = ['Game', 'Social']
subcat_choices= []
category_column = [
    [sg.Text("Category"),
    sg.Combo(categories,
            key='-cat-',
            enable_events=True,
            default_value=categories[0]),
    sg.Button("Refresh")],
    [sg.Listbox(subcat_choices,
                key='-subcat-',
                enable_events=True,
                select_mode="LISTBOX_SELECT_MODE_SINGLE",
                s=(30,5))]]

stat_choices = []
statchoice_column = [
    [sg.Text("Stats"), sg.Button('Reload')],
    [sg.Listbox(stat_choices,
    key='-stat-',
    enable_events=True,
    select_mode='LISTBOX_SELECT_MODE_SINGLE',
    s=(30,5))]]

# All the stuff inside your window.
layout = [  [sg.Column(user_column, vertical_alignment='top'), sg.Column(category_column)],
            [sg.Button('Quit')],
            [sg.Text("_"*120)],
            [sg.Column(statchoice_column, vertical_alignment='top')]]

#Create the Window
window = sg.Window('Steam Graphing Program', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read(timeout=1000)
    # closes program
    if event == sg.WIN_CLOSED or event == 'Quit': # if user closes window or clicks quit
        break
    #OK button is pressed
    if event == 'OK':
        #error handling
        try:
            #gets the user name and creates a user object
            username = values[0]
            window['-username-'].update(values[0])
            user_obj = rq.objectify_user(username)
            level = user_obj.get_level()
            window['-level-'].update(level['player_level'])
            games = user_obj.get_games()
            friends = user_obj.get_friends()
        except TypeError:
            window['-username-'].update('Error')
        except:
            pass
    #Display games in listbox
    try: 
        if values['-cat-'] == 'Game' and event == 'Refresh':
            window['-subcat-'].update(games.keys())
    except AttributeError:
            no_games = ["No Games"]
            window['-subcat-'].update(no_games)
    #Display friends in listbox
    try:
        if values['-cat-'] == 'Social' and event == 'Refresh':
            window['-subcat-'].update(values= friends.keys())
    except AttributeError:
        no_friends = ["No Friends"]
        window['-subcat-'].update(no_friends)
    
    # if they click on a game in the game category
    if event == '-subcat-':
        
        if values['-cat-'] == 'Game':
            # gets the game stats
            game_choice = games[values['-subcat-'][0]]
            choice_stats = game_choice.app_stats(user_obj.steam_id)
            choice_stats_list = []

            # creats list of game stats
            try:
                for choice in choice_stats:
                    choice_stats_list.append(choice)
                    choice_stats_list.append(choice_stats[choice])
            except TypeError:
                pass
            #Adds the list to the winwo
            try:
                window['-stat-'].update(choice_stats_list)
            except AttributeError:
                no_stats = ['No Stats']
                window['-stat-'].update(no_stats)
        
        if values['-cat-'] == 'Social':
            friend_id = friends[values['-subcat-'][0]].steam_id
            
    if event == '-stat-' and values['-stat-'] != "No Stats":
        friends_own = rq.friends_have(game_choice, friends)
        

window.close()
