"""
Usage:
  smasherstats.py [-s <tag>]... [-y <year>] [-y <year>] [options]
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
  --rank                    Rank players by results
                            Player rank = sum of (1/place)^2
"""

import requests
import sys
import datetime
from docopt import docopt
from bs4 import BeautifulSoup as bsoup

# globals
smasher = ''
tags = []
threshold = 0
year = [datetime.datetime.now().year]
game = 'Melee'
event = ''
input_file = ''
output_file = ''
valid = 0
rank = 0
ranks = []

args = docopt(__doc__)
if args['--debug']:
    print(args)
for arg in args:
    if args[arg] != None:
        globals()[arg[2:]] = args[arg]

for y in year:
    if not str(y).isnumeric() and y.upper() != 'ALL':
        print('Invalid year < ' + y + ' >. Defaulting to current year.')
        y = datetime.datetime.now().year
    y = str(y).lstrip('0')
    try:
        y = int(y)
    except:
        pass
if year == []:
    year = [datetime.datetime.now().year]

games = [
    ['MELEE',
     'SMASH MELEE',
     'SMASH BROS MELEE',
     'Super Smash Bros. Melee'],

    ['64',
     'SMASH 64',
     'SUPER SMASH BROS 64',
     'Super Smash Bros.'],

    ['BRAWL',
     'SMASH BROS BRAWL',
     'SMASH BRAWL',
     'Super Smash Bros. Brawl'],

    ['SM4SH',
     'SMASH 4',
     'SMASH WII U',
     'SMASH BROS 4',
     'SMASH BROS WII U',
     'SMASH BROS 4',
     'SUPER SMASH BROS 4',
     'Super Smash Bros. for Wii U'],

    ['PM',
     'PROJECT MELEE',
     'SUPER SMASH BROS PROJECT M',
     'SUPER SMASH BROS PM',
     'Project M']
]
for g in games:
    if game.strip('.').upper() in g:
        game = g[-1]
        valid = 1
if not valid:
    print('Invalid game < ' + game + ' >. Defaulting to Melee.')
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
    print('Invalid event < ' + event + ' >. Defaulting to Singles.')
    event = 'Singles'

if input_file != '':
    tags = [line.strip('\n') for line in open(input_file, 'r')]
if tags == [] and smasher == []:
    smasher = [input('Smasher: ')]
for tag in smasher:
    if tag != '' and tag.lower() not in map(str.lower, tags):
        tags += [tag]
for tag in tags:
    output = '-'*20 + '\n'
    smasher = '_'.join(i[0].upper() + i[1:] for i in tag.split(' '))
    page = requests.get('http://www.ssbwiki.com/Smasher:' + smasher)
    soup = bsoup(page.content, "html.parser")
    while 'There is currently no text in this page.' in soup.text:
        print('Invalid tag < ' + smasher + ' >. Try again.')
        tag = input('Smasher: ')
        smasher = '_'.join(i[0].upper() + i[1:] for i in tag.split(' '))
        page = requests.get('http://www.ssbwiki.com/Smasher:' + smasher)
        soup = bsoup(page.content, "html.parser")

    tables = soup.find_all('div', {'id': 'mw-content-text'})[0].contents[2].contents[1].contents[1]
    for header in tables.find_all('h3'):
        if game in header.contents[0].text:
            tables = tables.contents[tables.index(header) + 2]
    results = []
    if str(year[0]).upper() == 'ALL':
        year = [tables.contents[3].contents[3].text.split(', ')[1], datetime.datetime.now().year]

    for i in range(3, len(tables.contents), 2):
        t = tables.contents[i]

        t_name = t.contents[1].text
        t_year = int((t.contents[3].text)[-4:])
        if event == 'Singles':
            t_place = str(t.contents[5].text).strip(' ')
        elif event == 'Doubles':
            t_place = str(t.contents[7].text).strip(' ')

        results += [[t_place, t_name, t_year]]
    output += tag + '\'s results for year '
    if len(year) == 1:
        output += '= ' + str(year[0])
    elif len(year) == 2:
        output += 'in range = <' + str(year[0]) + ', ' + str(year[1]) + '>'
    output += ':\n'
    if threshold != 0:
        output += 'Tournament names listed for placings of ' + str(threshold) + ' or below.\n'
    results = [i for i in results if i[0] not in ['—', ''] and int(year[0]) <= i[2] <= int(year[-1])]

    s = lambda x: int(''.join([k for j in x[0] for k in j if k.isnumeric()]))
    results = sorted(results, key=s)
    ranks += [tag, sum(1/(r**2) for r in [s(i) for i in results])]
    for i in range(len(results)):
        r = [i[0] for i in results if i[0] != '—']
        place = results[i][0]
        if results[i - 1][0] != place:
            count = r.count(place)
            t_str = str(place) + ' - ' + str(count)
            if s([place]) >= int(threshold) > 0:
                for k in range(len(results)):
                    if results[k][0] == place:
                        t_name = results[k][1]
                        t_year = str(results[k][2])
                        if t_str[0] != '\n':
                            t_str = '\n' + t_str
                        t_str += '\n' + t_name + ' '
                        if len(year) != 1 and t_year not in t_name:
                            t_str += '(' + t_year + ')'
            output += t_str + '\n'
    if output_file == '':
        print(output)
        print(ranks)
    else:
        with open(output_file, 'a+') as f:
            ofile = output_file.replace('\\', ' ').replace('/', ' ').split()[-1]
            if output not in open(output_file).read():
                f.write(output)
                print(tag + ' written to ' + ofile)
            else:
                print(tag + ' already in ' + ofile)
