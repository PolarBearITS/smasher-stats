"""
Usage:
    script.py results [-s <tag>]... [-y <year>] [-y <year>] [options]
    script.py records [-s <tag>] [-s <tag>] [-y <year>] [-y <year>] [options]
    script.py settable [-s <tag>]... [-y <year>] [-y <year>] [options]
    script.py -h | --help

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

from smasherstats import *
from prettytable import PrettyTable, ALL

def nums_from_string(string):
    nums = ''
    for char in string:
        if char.isnumeric():
            nums += char
    return int(nums)

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
    if args[arg] is not None:
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
    r = getResults(tag, year, game, event)
    results.append([tag, r[0]])
    year = r[1]

if args['results']:
    for i in range(len(tags)):
        tag = tags[i]
        res = results[i][1]
        output = '-'*20 + '\n'
        output += f'{tag}\'s {event} results for '
        if len(year) == 1:
            output += str(year[0])
        elif len(year) == 2:
            output += f'<{year[0]}, {year[1]}>'
        output += ':'
        if int(threshold) not in [0, 1]:
            output += f'\nTournament names listed for placings of {threshold} or below.\n'

        res = [r for r in res if any(c.isdigit() for c in r[0])]
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
        if i == len(tags) - 1:
            output += '-'*20 + '\n'
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
    record = getRecord(tags, results)
    print('\n\nTournaments where specified players were present but results failed to be retrieved:')
    for f in record[3]:
        print(f' - {f}')
    print()

    pt = PrettyTable()
    if len(tags) == 1:
        pt.field_names = ['Tournament', 'Round', f'{tags[0]} vs. ↓', 'Score', 'Outcome']
    elif len(tags) == 2:
        pt.field_names = ['Tournament', 'Round', f'{tags[0]} - {tags[1]}', 'Winner']

    pt_rows = record[0]
    for i in range(len(pt_rows)):
        row = pt_rows[i]
        r_name = row[0]
        if r_name == pt_rows[i-1][0]:
            r_name = ''
        elif i > 0:
            pt.add_row(['' for _ in range(len(pt.field_names))])
        pt.add_row([r_name] + row[1:])
    print(pt)

    if len(tags) == 2:
        print(f'Total Set Count: {tags[0]} {record[1][0]} - {record[1][1]} {tags[1]}')
        print(f'Total Game Count: {tags[0]} {record[2][0]} - {record[2][1]} {tags[1]}')

if args['settable']:
    settable = PrettyTable(hrules=ALL)
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
