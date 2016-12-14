## smasher-stats
Start of a python smash statistics project

Welcome to SmasherStats. This is super basic for now.

SmasherStats is written in python 3.5, so make sure you have that installed before running.

Download python 3.5 here: https://www.python.org/downloads/

The default setting is to return a smasher's Melee Singles results for the current year only.

## How to run the program

    Usage:
        smasherstats.py results [-s <tag>]... [-y <year>] [-y <year>] [options]
        smasherstats.py records [-s <tag>] [-s <tag>] [-y <year>] [-y <year>] [options]
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

## Dependencies

* requests
* docopt
* beautifulsoup4
* pysmash

You can install all these using pip by just typing `python -m pip install -r requirements.txt`

Pip comes with the latest versions of Python 2 and Python 3.
If you don't have it installed, you can download it here: https://pip.pypa.io/en/stable/installing/

## Examples

* Results pulling off ssbwiki
	
	asdf
	
* Results pulling off ssbwiki for multiple smashers
* Records pulling off smash.gg
* Records pulling off smash.gg for specific player matchups