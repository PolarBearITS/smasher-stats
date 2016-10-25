import requests
import sys
import argparse
import datetime
from bs4 import BeautifulSoup as bsoup

smasher = ''
tags = []
show_t = 1

# filters
threshold = 5
year = datetime.datetime.now().year
comparison = '>='
game = 'Melee'
input_file = ''
output_file = ''

parser = argparse.ArgumentParser(description='Get tournament results of specified smasher')
name = parser.add_mutually_exclusive_group()
name.add_argument('-s', '--smasher', help='The tag of the smasher you want results for')
name.add_argument('-i', '--input_file', help='Path to input file')
parser.add_argument('-t', '--threshold', help='Tournaments where the smasher placed worse will have their names displayed', type=int)
parser.add_argument('-y', '--year', help='Specified year used in conjunction with -c')
parser.add_argument('-c', '--comparison', help='What comparison to use when comparing the date to -y')
parser.add_argument('-g', '--game', help='Specified game to get tournament results for')
parser.add_argument('-o', '--output_file', help='Path to output file')
args = parser.parse_args()
for arg in args.__dict__:
    if args.__dict__[arg] != None:
        globals()[arg] = args.__dict__[arg]

if not(str(year).isnumeric() or year == 'ALL'):
    print('Invalid year < ' + year + ' >. Defaulting to current year.')
    year = datetime.datetime.now().year
year = str(year).lstrip('0')
try:
    year = int(year)
except:
    pass
if year == datetime.datetime.now().year and '>' in comparison:
    comparison = '=='
games = [
    ['MELEE', 'SMASH MELEE',
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

if input_file != '':
    tags = [line.strip('\n') for line in open(input_file, 'r')]

if tags == [] and smasher == '':
    smasher = input('Smasher: ')
if smasher != '' and smasher.lower() not in map(str.lower, tags):
    tags += [smasher]
for tag in tags:
    output = '-'*20 + '\n'
    smasher = '_'.join([i[0].upper() + i[1:] for i in tag.split(' ')])
    page = requests.get('http://www.ssbwiki.com/Smasher:' + smasher)
    soup = bsoup(page.content, "html.parser")
    while 'There is currently no text in this page.' in soup.text:
        print('Invalid tag < ' + smasher + ' >. Try again.')
        smasher = input('Smasher: ')
        smasher = '_'.join(i[0].upper() + i[1:] for i in smasher.split(' '))
        page = requests.get('http://www.ssbwiki.com/Smasher:' + smasher)
        soup = bsoup(page.content, "html.parser")

    tables = soup.find_all('div', {'id': 'mw-content-text'})[0].contents[2].contents[1].contents[1]
    for h in tables.find_all('h3'):
        if game in h.contents[0].text:
            tables = tables.contents[tables.index(h) + 2]
    results = []
    if str(year).upper() == 'ALL':
        year = tables.contents[3].contents[3].text.split(', ')[1]

    for i in range(3, len(tables.contents), 2):
        t = tables.contents[i]

        t_name = t.contents[1].text
        t_year = int((t.contents[3].text)[-4:])
        t_place = str(t.contents[5].text).strip(' ')

        results += [[t_place, t_name, t_year]]

    output += smasher + '\'s results for year ' + comparison + ' ' + str(year) + ':\n'
    output += 'Tournament names listed for placings of ' + str(threshold) + ' or below.\n'
    results = [i for i in results if i[0] != '—' and eval(str(i[2]) + comparison + str(year))]

    s = lambda x: int(''.join([k for j in x[0] for k in j if k.isnumeric()]))
    results = sorted(results, key=s)
    for i in range(len(results)):
        r = [i[0] for i in results if i[0] != '—']
        place = results[i][0]
        if results[i - 1][0] != place:
            count = r.count(place)
            t_str = str(place) + ' - ' + str(count)
            if show_t and s([place]) >= threshold:
                for k in range(len(results)):
                    if results[k][0] == place:
                        t_str = '\n' + t_str + '\n' + results[k][1] + ' '
                        if comparison != '==':
                            t_str += '(' + str(results[k][2]) + ')'
            output += t_str + '\n'
    if output_file == '':
        print(output)
    if output_file != '':
        with open(output_file, 'a+') as f:
            if output not in open(output_file).read():
                f.write(output)
                ofile = output_file.replace('\\', ' ').replace('/', ' ').split()[-1]
                print(tag + ' written to ' + ofile)
            else:
                print(tag + ' already in ' + ofile)
