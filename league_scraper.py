# Isaac Wen
# This program emulates the functionality of websites and programs like
# op.gg, u.gg, and blitz.gg to enhance the experience of League of Legends
# players


import urllib.request
from bs4 import BeautifulSoup
import string


# Lists of the ids and the names of the shards, as of patch 10.25.1
#   - this is to manually add the shards into the rune dictionary, as the
#     shards are not currently in the runes database
shard_ids = ['5008', '5005', '5007', '5002', '5003', '5001']
shard_names = ['Adaptive Force', 'Attack Speed', 'Ability Haste',
               'Armor', 'Magic Resist', 'Health']


# List of champions which have multiple forms, that is, where their data on
# leagueoflegends.fandom.com is stored on multiple unique web domains
#   - NOTE***: This code only works while shapeshifters only vary in their
#     Q,W, and E abilities
shapeshifters = ['Elise', 'Gnar', 'Jayce', 'Nidalee', 'Kled']
# A list of the forms of the champions in the previous list, as they
# appear in a URL
shapeshifter_forms = [['Human Form', 'Spider Form'],
                      ['Mini Gnar', 'Mega Gnar'],
                      ['Mercury Hammer', 'Mercury Cannon'],
                      ['Human Form', 'Cougar Form'],
                      ['Mounted', 'Dismounted']]
# A tuple indicating the range of html sections that contain the secondary
# skills for the associated champions from the results for when the html is
# parsed by div with classes that contain the string 'skill'
shapeshifter_html = [(4,7),(4,7),(6,9),(4,7)]


# Checks if the data that has been stored is of the current patch, and if it
# is not, then it calls all relevant functions that will update the stored
# data
def update_data():
    url = "https://ddragon.leagueoflegends.com/api/versions.json"
    data = urllib.request.urlopen(url)
    data = str(data.read())
    split_html = data.split('\"')
    version = split_html[1]
    up_to_date = True
    # Tries to open the file and compare the stored version with the most
    # recently received version; if it is not the case or if the file does
    # not yet exist, then the file will be rewritten, or written, to include
    # the most recent version
    try:
        version_file = open('version.txt', 'r')
        stored_version = str(version_file.read())
        if version != stored_version:
            up_to_date = False
        version_file.close()
    except FileNotFoundError:
        up_to_date = False
    # If the version recorded is not the same as the most recent, then all
    # stored data that may need to be updated will be
    if up_to_date == False:
        # This rewrites the file, or writes the file if it does not yet exist
        version_file = open('version.txt', 'w')
        version_file.write(version)
        version_file.close()
        champ_keys(version)
        rune_keys(version)


# Writes the champion keys and their associated champion into a file
def champ_keys(version):
    url = "http://ddragon.leagueoflegends.com/cdn/" + version \
          + "/data/en_US/champion.json"
    data = urllib.request.urlopen(url)
    data = str(data.read())
    # Creates a list of all the champion keys for the champions in
    # alphabetical order
    key_split = data.split('\"key\":\"')
    all_keys = []
    for i in key_split[1:]:
        key_beta = i[:3]
        list = key_beta.split('\"')
        all_keys.append(list[0])
    # Creates a list of all the champion names for the champions in
    # alphabetical order
    name_split = data.split('\"name\":\"')
    all_names = []
    for i in name_split[1:]:
        # Constant for a number for which all champion names are shorter than
        longest_champ_name = 20
        name_beta = i[:longest_champ_name]
        list = name_beta.split('\"')
        all_names.append(list[0])
    # Writes all the champion keys and names into a file
    champ_file = open('champions.txt', 'w')
    champ_file.write(version + '\n')
    num_champs = len(all_keys)
    for i in range(num_champs):
        champ_file.write(all_keys[i] + ';' + all_names[i] + '\n')
    champ_file.close()
    return


# Writes the rune keys and their associated runes into a file
def rune_keys(version):
    url = "http://ddragon.leagueoflegends.com/cdn/" + version \
          + "/data/en_US/runesReforged.json"
    data = urllib.request.urlopen(url)
    data = str(data.read())
    # Creates a list of all the rune names in the order that they are recorded
    # on the database
    name_split = data.split('\"name\":\"')
    all_names = []
    for i in name_split[1:]:
        # Constant for a number for which all rune names are shorter than
        longest_rune_name = 30
        name_beta = i[:longest_rune_name]
        list = name_beta.split('\"')
        all_names.append(list[0])
    # Creates a list of all the rune id's in the order that they are recorded
    # on the database
    id_split = data.split('\"id\":')
    all_ids = []
    for i in id_split[1:]:
        # Constant for the longest rune id
        #   - as all of them are 4 digits, this is set to 4 currently
        longest_rune_id = 4
        id_beta = i[:longest_rune_id]
        list = id_beta.split('\"')
        all_ids.append(list[0])
    # Writes all the rune names and ids into a file
    rune_file = open('runes.txt', 'w')
    rune_file.write(version + '\n')
    num_runes = len(all_names)
    for i in range(num_runes):
        rune_file.write(all_ids[i] + ';' + all_names[i] + '\n')
    # Adds the ids for the shards, as they are not currently listed in the
    # database
    num_shards = len(shard_ids)
    for i in range(num_shards):
        rune_file.write(shard_ids[i] + ';' + shard_names[i] + '\n')
    rune_file.close()
    return


# Takes a list of champion id's and returns a list of champion names
# corresponding to those champion id's in the same order
def champ_names(ids):
    # Calls on the txt file where all the champ id and name information is
    # stored and makes a dictionary with that information
    champ_file = open('champions.txt', 'r')
    file_lines = champ_file.readlines()
    champ_dict = {}
    # The first line of the file contains the version so we want all the
    # lines past that one
    for line in file_lines[1:]:
        id_name = line.split(';')
        format_name = id_name[1].strip()
        # The keys of the dictionary will be the id, and the values will be
        # the champion which is associated with that id
        champ_dict[id_name[0]] = format_name
    champ_file.close()
    # Creates a list of names based on the id's
    champs = []
    for id in ids:
        champs.append(champ_dict[id])
    return champs


# Takes a list of the rune keys and returns a list of rune names
# corresponding to those rune keys in the same order
def rune_names(keys):
    # Calls on the txt file where all the rune keys and name information is
    # stored and makes a dictionary with that information
    rune_file = open('runes.txt', 'r')
    file_lines = rune_file.readlines()
    rune_dict = {}
    # The first line of the file contains the version so we want all the
    # lines past that one
    for line in file_lines[1:]:
        key_name = line.split(';')
        format_name = key_name[1].strip()
        # The key of the dictionary will be the key, and the values will be
        # the rune which is associated with that id
        rune_dict[key_name[0]] = format_name
    rune_file.close()
    # Creates a list of names based on the id's
    runes = []
    for key in keys:
        runes.append(rune_dict[key])
    return runes

# This takes a champion as a parameter and produces a dictionary where each
# of the keys represents a skill (P, Q, W, E, or R), and the value is a list
# containing all of the info pertaining to that skill
#   - if the champion only has one form, that is, it is not a shapeshifter,
#     then by default only one dictionary will be returned
#   - however, if the champion has multiple forms, as indicated when the
#     second parameter is True, then two dictionaries will be returned, one
#     for the main set of abilities and the other for the secondary
#   - NOTE***: This code only works while shapeshifters only vary in their
#     Q,W, and E abilities
def champ_skills(champion, shapeshifter = False):
    url = "https://leagueoflegends.fandom.com/wiki/" + champion
    data = urllib.request.urlopen(url)
    soup = BeautifulSoup(data, 'html.parser')
    # Finds the HTML sections relating to all 5 of the champion's skills
    skills = soup.find_all('div', class_='skill')
    total_info = {}
    # Counts through all 5 of the skills that a champion has
    skill_count = 0
    for skill in ['Passive', 'Q', 'W', 'E', 'R']:
        skill_info = \
            skills[skill_count].find_all('div', class_='ability-info')
        all_info = []
        for info in skill_info:
            all_info.append(info.get_text())
        total_info[skill] = all_info
        skill_count += 1
    if shapeshifter == False:
        return total_info
    # This covers the edge case of Kled, whose abilities change but doesn't
    # have coding that resembles the other shapeshifters
    #   - this code replicates the above code, however it has slight
    #     modifications in order to parse the specific sections that contain
    #     the abilities that are desired
    elif shapeshifter == True and champion == 'Kled':
        kled_skills = soup.find_all('div', id='item-2')
        kled_skills2 = kled_skills[0].find_all('div', class_='skill')
        kled_skill_name = ['Q', 'W']
        skill_count = 0
        kled_total_info = {}
        for i in range(1,3):
            kled_skill_info =\
                kled_skills2[i].find_all('div', class_='ability-info')
            kled_all_info = []
            for k in kled_skill_info:
                kled_all_info.append(k.get_text())
            kled_total_info[kled_skill_name[skill_count]] = kled_all_info
            skill_count += 1
        return (total_info, kled_total_info)
    # This covers the edge cases of shapeshifters in general, as they have
    # secondary forms with different ability descriptions
    #   - as with the Kled section, this code replicates the above code with
    #     some slight adjustments
    else:
        index = shapeshifters.index(champion)
        sec_skills = soup.find_all('div', class_='skill')
        sec_total_info = {}
        sec_skill_name = ['Q', 'W', 'E']
        (range_lower, range_higher) = shapeshifter_html[index]
        for i in range(range_lower, range_higher):
            sec_skill_info = \
                sec_skills[i].find_all('div', class_='ability-info')
            sec_all_info = []
            for sec_info in sec_skill_info:
                sec_all_info.append(sec_info.get_text())
            sec_total_info[sec_skill_name[i - range_lower]] = sec_all_info
        return (total_info, sec_total_info)



# Formats a champion's name to the equivalent in a URL
#   - this will be used in both u.gg and leagueoflegends.fandom.com
#   - as of patch 10.25.1, both of these sites accept URLs with spaces as
#     underscores, ' as %27, and periods as periods
def format_champ(champion):
    format1 = champion.replace(' ', '_')
    format2 = format1.replace('\'', '%27')
    return format2


# This takes a champion and a game more (either 'norm' or 'aram') as a
# parameter and produces information that might help in playing the game as
# that champion, including:
#   - runes
#   - skill order
def champ_info(champion, gamemode):
    formatted = format_champ(champion)
    if gamemode == 'norm':
        url = 'https://u.gg/lol/champions/' + formatted + '/build'
    else:
        url = 'https://u.gg/lol/champions/aram/' + formatted + '-aram'
    data = urllib.request.urlopen(url)
    soup = BeautifulSoup(data, 'html.parser')
    # Finds the HTML sections relating to all of the recommended runes for a
    # given champion
    rune_set = soup.find_all('div', class_='rune-trees-container-2 media-que'
                                           'ry media-query_MOBILE_LARGE__DES'
                                           'KTOP_LARGE')
    # This will return False if the entered champion is not a valid champion
    # name
    if rune_set == []:
        return False
    # Finds the main runes
    runes_html = rune_set[0].find_all('div', class_="perk-active")
    # Finds the shards
    shards_html = rune_set[0].find_all('div', class_="shard-active")
    # As the page contains two sets of data for this rune,
    rune_list = []
    for html in runes_html:
        split = str(html).split('alt=\"')
        rune_plus = split[1].split('\"')
        rune = rune_plus[0]
        if rune.startswith('The Rune '):
            rune_list.append(rune[9:])
        else:
            rune_list.append(rune[13:])
    for html in shards_html:
        split = str(html).split('alt=\"')
        shard_plus = split[1].split('\"')
        shard = shard_plus[0]
        rune_list.append(shard[4:-6])
    # Finds the HTML sections relating to the skill path
    skill_path = soup.find_all('div', class_='skill-priority-path')[0]\
        .get_text()
    return (rune_list, skill_path)


# Prints the information for each champion in a list of champions, which is
# taken as input from the user through champion names separated by
# semi-colons
#   - this prints the champions SKILLS, as from champ_skills()
def print_champions(champions):
    list_champs = champions.split(';')
    for champ in list_champs:
        # Capitalizes every word in champ
        capital_champ = string.capwords(champ)
        print('Champion: ' + capital_champ)
        # This formats the champion names to what would be their equivalents
        # in a URL
        formatted = format_champ(capital_champ)
        if capital_champ in shapeshifters:
            (info1, info2) = champ_skills(formatted, True)
            index = shapeshifters.index(capital_champ)
            print(shapeshifter_forms[index][0])
            print_champions_dict(info1)
            print(shapeshifter_forms[index][1])
            print_champions_dict(info2)
        else:
            info = champ_skills(formatted)
            print_champions_dict(info)
    return


# Prints the dictionaries generated by print_champions
def print_champions_dict(info):
    for key in info.keys():
        if info[key] == []:
            continue
        information = key + ': '
        len_info = len(info[key])
        for i in range(len_info):
            information = information + info[key][i]
            if i < (len_info - 1):
                information = information + '--- '
        print(information)
    return


# Returns the information that one might desire to know about the live game
# that they are in (or returns False if the user is not currently in a live
# game), such as:
#   - opponent rank, WR, champion, role, and whether they are playing on role
#     or not
def live_game_info(player):
    formatted = format_champ(player)
    url = 'https://u.gg/lol/profile/na1/' + formatted + '/live-game'
    data = urllib.request.urlopen(url)
    data = str(data.read())
    data_split = data.split('getLiveGame')
    player_live = True
    if len(data_split) == 1:
        player_live = False
    if player_live == False:
        return False
    teams_info = data_split[1].split('team')
    teamA = teams_info[1]
    if player in teamA:
        opponent_team = teams_info[2]
    else:
        opponent_team = teamA
    # Gets all of the information in the following lists, where each list
    # contains one type of information
    opp_ranked = []
    opp_names = []
    opp_tier = []
    opp_rank = []
    opp_champs = []
    opp_roles = []
    opp_onrole = []
    opp_runes = []
    info_order = ["seasonRankScore", "summonerName", "tier", "rank",
                  "championId", "currentRole", "onRole", "summonerRuneData"]
    list_order = [opp_ranked, opp_names, opp_tier, opp_rank,
                  opp_champs, opp_roles, opp_onrole, opp_runes]
    # This splits the HTML code such that the desired parts of the HTML code
    # can be extracted
    for i in range(len(info_order)):
        info = info_order[i]
        split = opponent_team.split(info + "\":")
        if info == 'summonerRuneData':
            for j in range(1,6):
                rune_info = split[j].split(']')
                opp_runes.append(rune_info[0] + ']')
        elif info == 'tier' or info == 'rank':
            count = 1
            for j in range(1,6):
                if opp_ranked[j-1] == 'null':
                    list_order[i].append('null')
                else:
                    info_list = split[count].split(',')
                    info_strip = info_list[0].strip('\"')
                    list_order[i].append(info_strip)
                    count += 1
        else:
            for j in range(1,6):
                info_list = split[j].split(',')
                info_strip = info_list[0].strip('\"')
                list_order[i].append(info_strip)
    # Puts all of the information into a dictionary, where the keys are the
    # player names and the values are a list of the corresponding data
    player_dict = {}
    for i in range(5):
        player_dict[opp_names[i]] = [string.capwords(opp_tier[i]),
                                     opp_rank[i].upper(), opp_champs[i],
                                     opp_roles[i].upper(), opp_onrole[i],
                                     opp_runes[i]]
    return player_dict


# Prints the result from live_player_game() nicely
def print_player_dict(player):
    player_dict = live_game_info(player)
    if player_dict == False:
        print(player + ' is not currently in a live game, or does not exist '
                       'on this server.')
        return
    print('Note that if player\'s IGN have non-alphabetic or non-numeric '
          'characters, it may not appear as intended.\n')
    keys = list(player_dict.keys())
    # Creates a list of all the champion ids that need to be searched and
    # searches up which champions they refer to
    champion_ids = []
    for key in keys:
        champion_ids.append(player_dict[key][2])
    champions = champ_names(champion_ids)
    # Goes through each player (the keys in the player_dict) and print all
    # the associated information for each of them
    for i in range(len(keys)):
        print('Player Name: ' + keys[i])
        info = player_dict[keys[i]]
        # Prints the player rank if they have a rank
        if info[0] == 'Null':
            rank = 'N/A'
        else:
            rank = info[0] + ' ' + info[1]
        # Takes the runes from the dictionary, turns it into a list of rune
        # ids, and searches them up
        runes = rune_names(info[5][1:-1].split(','))
        # Puts all of the runes that are searched up into a formatted string
        print_runes = 'Runes: '
        for j in range(len(runes)):
            if j != (len(runes) - 1):
                print_runes += runes[j] + ', '
            else:
                print_runes += runes[j]
        # Prints all of the information nicely
        print('Rank:', rank, '--- Role:', info[3], '--- Main Role:',
              string.capwords(info[4]))
        print(print_runes)
        print_champions(champions[i])
        print('')
    return

# ===========================================================================
# Code past this point is only concerned with the display element of this
# program in the console, and of the running of the previously defined
# functions
# ===========================================================================

# Function that initiates the start screen, changing depending on whether the
# user has saved their IGN already or not
def start_screen():
    # This prints the opening message, with edits depending on whether the
    # user has saved their IGN before or not
    print('\nWelcome to op.gg, Python Edition!')
    have_ign = True
    try:
        name_file = open('ign.txt', 'r')
        ign = str(name_file.read())
        ign_msg = 'Your currently saved IGN: ' + ign + '\n'
    except FileNotFoundError:
        have_ign = False
    options_msg = 'Select one of the options below by typing in the ' +\
                  'number for the option:\n'
    option1a_msg = '1 - Set your IGN\n'
    option1b_msg = '1 - Change your saved IGN\n'
    option2_msg = '2 - Champion Runes and Skill Order\n'
    option3_msg = '3 - Summoner Live Game (displays opponent ranks, ' +\
                  'current role, whether they are playing on their main ' +\
                  'role, their runes, and their champion\'s information)\n'
    option4_msg = '4 - Your Live Game (displays the information for a ' +\
                  'Summoner Live Game for your current live game)\n'
    if have_ign:
        print(ign_msg + options_msg + option1b_msg + option2_msg +
              option3_msg + option4_msg)
    else:
        print(options_msg + option1a_msg + option2_msg + option3_msg)
    option = input('Enter selection, or press ENTER to terminate the '
                   'program: ')
    # Terminates the program
    if option == '':
        return
    # Calls on the appropriate screens depending on the option
    elif option == '1':
        set_ign_screen()
    elif option == '2':
        champ_screen()
    elif option == '3':
        live_game_screen()
    elif have_ign and option == '4':
        your_live_screen(ign)
    else:
        print('You did not enter a valid input.')
        start_screen()
    return


# Initiates the set IGN screen
def set_ign_screen():
    print('\nEntry specifications:')
    print('  - Currently only supports players on the NA server, and with '
          'IGN with strictly alphabetic and numeric characters\n')
    ign = input('Enter your IGN to set it, or press ENTER to cancel: ')
    if ign == '':
        start_screen()
        return
    else:
        ign_file = open('ign.txt', 'w')
        ign_file.write(ign)
        ign_file.close()
        start_screen()
    return


# Initiates the search champion page
def champ_screen():
    print('\nEntry specifications:')
    print('  - Champion names can be capitalized or entirely lowercase')
    print('  - Enter champions names with spaces included (e.g. enter'
          ' \'Twisted Fate\', not \'TwistedFate\')')
    print('  - Enter a champion with or without the apostrophe, if relevant '
          '(e.g. both Kaisa and Kai\'sa are acceptable)')
    print('  - Multiple champion names are permitted; separate each champion '
          'name with a semi-colon, with no spaces (e.g. \'Malphite;Jayce\')')
    champs = input('\nEnter champion name(s), or press ENTER to cancel: ')
    if champs == '':
        start_screen()
        return
    champ_list = champs.split(';')
    select_gamemode_screen(champ_list)
    return


# Initiates the select gamemode page
def select_gamemode_screen(champ_list):
    print('\nWhat gamemode would you like the information for? Enter the '
          'number for the gamemode.')
    print('1 - Summoner\'s Rift (Normal, Ranked)\n2 - ARAM')
    gamemode = input('Enter your selection, or press ENTER to cancel: ')
    if gamemode == '':
        start_screen()
        return
    elif gamemode == '1' or gamemode == '2':
        for champ in champ_list:
            if gamemode == '1':
                info = champ_info(champ, 'norm')
            else:
                info = champ_info(champ, 'aram')
            if info == False:
                print('\nThe champion', champ, 'does not exist.')
            else:
                # Prints the runes and skill order info nicely
                runes = info[0]
                print_runes = 'Runes: '
                for i in range(len(runes)):
                    if i != (len(runes) - 1):
                        print_runes += runes[i] + ', '
                    else:
                        print_runes += runes[i]
                print_skills = 'Skill Order: ' + info[1]
                print('\nChampion: ' + champ + '\n' + print_runes + '\n' +
                      print_skills)
        start_screen()
    else:
        print('You did not enter a valid input.')
        select_gamemode_screen(champ_list)
    return


# Initializes the screen for looking up player's live games
def live_game_screen():
    print('\nEntry specifications:')
    print('  - Currently only supports players on the NA server, and with '
          'IGN with strictly alphabetic and numeric characters\n')
    ign = input('Enter the IGN of a player, or press ENTER to cancel: ')
    print()
    print_player_dict(ign)
    start_screen()
    return


# Initializes the screen to show your live game information
def your_live_screen(ign):
    print('')
    print_player_dict(ign)
    start_screen()
    return


# The main function of the program that uses all previous functions to
# initialize and run the program as intended
def main():
    update_data()
    start_screen()
    return

main()