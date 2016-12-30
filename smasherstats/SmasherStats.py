"""
Usage:
    smasherstats.py results [-s <tag>]... [-y <year>] [-y <year>] [options]
    smasherstats.py records [-s <tag>] [-s <tag>] [-y <year>] [-y <year>] [options]
    smasherstats.py settable [-s <tag>]... [-y <year>] [-y <year>] [options]
    smasherstats.py -h | --help

Get tournament results of specified smasher

Options:
  -h, --help                Show this help message and exit
  -s, --smasher <tag>       The tag of the smasher you want results for
  -i, --input_file <path>   Path to input file where tags are stored
  -o, --output_file <path>  Path to output file where results are put
  -t, --threshold <place>   Tournaments where the smasher placed worse will have
                            their names displayed
  -y, --year <year>         Specified year used to filter tournament dates
                            List 1 specific year or 2 to define a range
  -g, --game <game>         Specified game to get tournament results for
                            [default: Melee]
  -e, --event <event>       What event to pull results for
                            [default: Singles]
  --debug                   Run in debug mode
"""

import requests
import datetime
import sys
import prettytable
from prettytable import PrettyTable
from docopt import docopt
from bs4 import BeautifulSoup as bsoup
import pysmash

CURRENT_YEAR = datetime.datetime.now().year
smash = pysmash.SmashGG()


def nums_from_string(string):
    nums = ''
    for char in string:
        if char.isnumeric():
            nums += char
    return int(nums)

def getResults(tag, year):
    res = []
    smasher = '_'.join(i for i in tag.split())
    page = requests.get('http://www.ssbwiki.com/Smasher:' + smasher)
    if page.status_code == 404:
        page = requests.get('http://www.ssbwiki.com/' + smasher)
    soup = bsoup(page.content, "html.parser")
    while page.status_code == 404:
        print(f'Invalid tag \'{smasher}\'. Try again.')
        tag = input('Smasher: ')
        tag = ' '.join(i[0].upper() + i[1:] for i in tag.split())
        smasher = '_'.join(i for i in tag.split())
        page = requests.get('http://www.ssbwiki.com/Smasher:' + smasher)
        if page.status_code == 404:
            page = requests.get('http://www.ssbwiki.com/' + smasher)
        soup = bsoup(page.content, "html.parser")

    tables = soup.find_all('div', {'id': 'mw-content-text'})[0].contents[2].contents[1].contents[1]
    for header in tables.find_all('h3'):
        if game in header.contents[0].text:
            tables = tables.contents[tables.index(header) + 2]
    if str(year[0]).upper() == 'ALL':
        year = [int(tables.contents[3].contents[3].text.split(', ')[1]), CURRENT_YEAR]

    for i in range(3, len(tables.contents), 2):
        t = tables.contents[i]
        t_name = t.contents[1].text
        t_year = int((t.contents[3].text).strip(' ')[-4:])
        if event == 'Singles':
            t_place = str(t.contents[5].text).strip(' ')
        elif event == 'Doubles':
            t_place = str(t.contents[7].text).strip(' ')
        res += [[t_place, t_name, t_year]]
    res = [i for i in res if i[0] not in ['—', ''] and int(year[0]) <= i[2] <= int(year[-1])]
    return [res, year]

def getRecord(tags, results):
    print(f'{tags[0]} vs. {tags[1]}')
    tournaments = [r[1] for res in results for r in res[1] if res[0] in tags]
    t = []
    m = tournaments.count(max(set(tournaments), key=tournaments.count))
    for tournament in tournaments:
        if tournaments.count(tournament) == m and tournament not in t:
            t += [tournament]
    tournaments = t

    setcounts = [0, 0]
    gamecounts = [0, 0]

    fail_tournaments = []
    pt = PrettyTable()
    pt.field_names = ['Tournament', 'Round', f'{tags[0]} - {tags[1]}', 'Winner']
    pretty_tournaments = []
    pt_rows = []
    for tournament in tournaments:
        sys.stdout.write('\r')
        sys.stdout.write(f'Retrieving tournament {tournaments.index(tournament)+1}/{len(tournaments)}...')
        havePlayed = 0
        try:
            players = []
            b = 0
            tournament_name = '-'.join(tournament.replace('.', '').split())
            t = smash.tournament_show_event_brackets(tournament_name, 'melee-singles')
            while not all(tag.lower() in [player['tag'].lower() for player in players] for tag in tags):
                b -= 1
                sets = smash.bracket_show_sets(t['bracket_ids'][b])
                players = smash.bracket_show_players(t['bracket_ids'][b])
        except:
            fail_tournaments.append(tournament)
            continue

        player_ids = ['', '']
        for p in players:
            if p['tag'] in tags:
                player_ids[tags.index(p['tag'])] = p['entrant_id']
        
        for s in sets:
            if all(str(n) != 'None' for n in s.values()):
                ids = [int(s['entrant_1_id']), int(s['entrant_2_id'])]
                scores = [s['entrant_1_score'], s['entrant_2_score']]
                if all(i in player_ids for i in ids):
                    havePlayed = 1
                    if ids != player_ids:
                        ids.reverse()
                        scores.reverse()
                    for i in range(len(gamecounts)):
                        gamecounts[i] += scores[i]
                    setcounts[scores.index(max(scores))] += 1
                    res = [tournament, s['full_round_text'], f'{scores[0]} - {scores[1]}', tags[player_ids.index(int(s['winner_id']))]]
                    pt_rows.append(res)
                    if tournament not in pretty_tournaments:
                        pretty_tournaments.append(tournament)
    for i in range(len(pt_rows)):
        row = pt_rows[i]
        r_name = row[0]
        if r_name == pt_rows[i-1][0]:
            r_name = ''
        elif i > 0:
            pt.add_row(['' for _ in range(len(pt.field_names))])
        pt.add_row([r_name] + row[1:])
    return pt, setcounts, gamecounts, fail_tournaments

# globals
smasher = ''
tags = []
threshold = 1
year = [CURRENT_YEAR]
game = 'Melee'
event = ''
input_file = ''
output_file = ''
valid = 0

args = docopt(__doc__)
if args['--debug']:
    print(args)
for arg in args:
    if args[arg] != None:
        globals()[arg.strip('-')] = args[arg]

for y in year:
    if not str(y).isnumeric() and y.upper() != 'ALL':
        print('Invalid year \'{y}\'. Defaulting to current year.')
        y = CURRENT_YEAR
    y = str(y).lstrip('0')
    try:
        y = int(y)
    except:
        pass
if year == []:
    year = [CURRENT_YEAR]

games = [
    ['MELEE',
     'SMASH MELEE',
     'SMASH BROS MELEE',
     'Super Smash Bros. Melee',
     ''],

    ['64',
     'SMASH 64',
     'SUPER SMASH BROS 64',
     'Super Smash Bros.',
     ''],

    ['BRAWL',
     'SMASH BROS BRAWL',
     'SMASH BRAWL',
     'Super Smash Bros. Brawl',
     ''],

    ['SM4SH',
     'SMASH 4',
     'SMASH WII U',
     'SMASH BROS 4',
     'SMASH BROS WII U',
     'SMASH BROS 4',
     'SUPER SMASH BROS 4',
     'Super Smash Bros. for Wii U',
     ''],

    ['PM',
     'PROJECT MELEE',
     'SUPER SMASH BROS PROJECT M',
     'SUPER SMASH BROS PM',
     'Project M',
     '']
]
for g in games:
    if game.strip('.').upper() in g:
        game = g[-2]
        valid = 1
if not valid:
    print('Invalid game \'{game}\'. Defaulting to Melee.')
    game = 'Super Smash Bros. Melee'

events = [
    ['SINGLES',
     'Singles'],

    ['DOUBLES',
     'Doubles']
]

for e in events:
    if event.upper() in e:
        event = e[-1]
        valid = 1
if not valid:
    print('Invalid event \'{event}\'. Defaulting to Singles.')
    event = 'Singles'

if input_file != '':
    tags = [line.strip('\n') for line in open(input_file, 'r')]
if tags == [] and smasher == []:
    smasher = [input('Smasher: ')]
for tag in smasher:
    if tag != '' and tag.lower() not in map(str.lower, tags):
        tags += [tag]

results = []
tags = [' '.join(i[0].upper() + i[1:] for i in tag.split()) for tag in tags]
for tag in tags:
    r = getResults(tag, year)
    results.append([tag, r[0]])
    year = r[1]

if args['results']:
    for i in range(len(tags)):
        tag = tags[i]
        res = results[i][1]
        output = '-'*20 + '\n'
        output += f'{tag}\'s results for '
        if len(year) == 1:
            output += str(year[0])
        elif len(year) == 2:
            output += f'<{year[0]}, {year[1]}>'
        output += ':'
        if int(threshold) not in [0, 1]:
            output += f'\nTournament names listed for placings of {threshold} or below.\n'

        res = [x for x in res if any(c.isdigit() for c in x[0])]
        res = sorted(res, key=lambda x: nums_from_string(x[0]))

        # sorted by place
        # formatted like so: [[place, name, year], ...]
        for i in range(len(res)):
            r = [i[0] for i in res]
            place = res[i][0]
            if res[i - 1][0] != place:
                output += '\n'
                count = r.count(place)
                t_str = f'{place} - {count}'
                if nums_from_string(place) >= int(threshold) > 0:
                    for k in range(len(res)):
                        if res[k][0] == place:
                            t_name = res[k][1]
                            t_year = str(res[k][2])
                            if t_str[0] != '\n':
                                t_str = '\n' + t_str
                            t_str += '\n - ' + t_name + ' '
                            if len(year) != 1 and t_year not in t_name:
                                t_str += f'({t_year})'
                output += t_str
        output += '\n' + '-'*20
        if output_file == '':
            print(output)
        else:
            with open(output_file, 'a+') as f:
                ofile = output_file.replace('\\', ' ').replace('/', ' ').split()[-1]
                if output not in open(output_file).read():
                    f.write(output)
                    print(f'{tag} written to {ofile}')
                else:
                    print(f'{tag} already in {ofile}')
if args['records']:
    if len(tags) == 1:
        tournaments = [r[1] for res in results for r in res[1] if res[0] in tags]
        fail_tournaments = []
        t = []
        m = tournaments.count(max(set(tournaments), key=tournaments.count))
        for tournament in tournaments:
            if tournaments.count(tournament) == m and tournament not in t:
                t += [tournament]
        tournaments = t

        # print(tournaments)

        setcount1 = 0
        setcount2 = 0
        gamecount1 = 0
        gamecount2 = 0
        winner = ''
        
        for tournament in tournaments:
            print(tournament, end = ' ... ')
            output = '\n'
            havePlayed = 0
            tournament_name = '-'.join(tournament.replace('.', '').split())
            players = []
            b = 0

            try:
                t = smash.tournament_show_event_brackets(tournament_name, 'melee-singles')
                while not all(tag.lower() in [player['tag'].lower() for player in players] for tag in tags):
                    b -= 1
                    sets = smash.bracket_show_sets(t['bracket_ids'][b])
                    players = smash.bracket_show_players(t['bracket_ids'][b])
            except:
                fail_tournaments += [tournament]
                print('FAIL')
                continue

            output += tournament + '\n' + '-'*len(tournament) + '\n'
            outcome = ''

            wincount = 0
            losscount = 0

            for s in sets:
                pt = []
                if all(str(n) != 'None' for n in list(s.values())):
                    ids = [int(s['entrant_1_id']), int(s['entrant_2_id'])]
                    scores = [int(s['entrant_1_score']), int(s['entrant_2_score'])]
                    p_tags = ['', '']
                    # Generate tag pair for each set
                    for p in players:
                        for i in range(len(ids)):
                            if ids[i] == int(p['entrant_id']):
                                p_tags[i] = p['tag']
                    if p_tags[0] != tags[0]:
                        p_tags.reverse()
                        scores.reverse()
                    if all(tag.lower() in [p.lower() for p in p_tags] for tag in tags):
                        havePlayed = 1
                        wincount += scores[0]
                        losscount += scores[1]
                        if scores[0] > scores[1]:
                            outcome = 'WIN'
                        else:
                            outcome = 'LOSS'
                        output += f"{s['full_round_text']} - {p_tags[0]} vs. {p_tags[1]} {scores[0]} - {scores[1]} {outcome}\n"
            print('DONE')
            output += f'Game Count: {wincount} - {losscount}\n'
            if havePlayed:
                if output_file == '':
                    print(output, end='')
                else:
                    with open(output_file, 'a+') as f:
                        ofile = output_file.replace('\\', ' ').replace('/', ' ').split()[-1]
                        if output not in open(output_file).read():
                            f.write(output)
                            print(f'{tournament} written to {ofile}')
                        else:
                            print(f'{tournament} written to {ofile}')
        if len(fail_tournaments) > 0:
            print('\nTournaments where specified players were present but results failed to be retrieved:')
            for f in fail_tournaments:
                print(f' - {f}')
            print()
    elif len(tags) == 2:
        record = getRecord(tags, results)
        print('\nTournaments where specified players were present but results failed to be retrieved:')
        for f in record[3]:
            print(f' - {f}')
        print(record[0])
        print()
        print(f'Set Count: {tags[0]} {record[1][0]} - {record[1][1]} {tags[1]}')
        print(f'Game Count: {tags[0]} {record[2][0]} - {record[2][1]} {tags[1]}')
if args['settable']:
    settable = PrettyTable(hrules=prettytable.ALL)
    settable.field_names = ['↓ vs. →'] + tags
    st = [['-' for _ in range(len(tags))] for _ in range(len(tags))]
    for i in range(len(tags)):
        for j in range(i+1, len(tags)):
            record = getRecord([tags[i], tags[j]], results)[1]
            print('\n')
            st[i][j] = f'{record[0]} - {record[1]}'
            st[j][i] = f'{record[1]} - {record[0]}'
    for i in range(len(st)):
        settable.add_row([tags[i]] + st[i])   
    print(settable)
