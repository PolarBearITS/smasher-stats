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

Results pulling off ssbwiki
	
	>> python smasherstats.py results -s Mang0 -t 3
	--------------------
	Mang0's results for 2016:
	Tournament names listed for placings of 3 or below.

	1st - 4
	2nd - 7

	3rd - 2
	Clutch City Clash
	Shine 2016

	4th - 4
	Smash Summit 2
	EVO 2016
	Smash Summit 3
	DreamHack Winter 2016

	13th - 1
	UGC Smash Open
	--------------------
	
&nbsp;
&nbsp;	
Results pulling off ssbwiki for multiple smashers

	>> python smasherstats.py results -s Armada -s Mang0 -y 2015 -t 0
	--------------------
	Armada's results for 2015:
	1st - 16
	2nd - 4
	3rd - 2
	5th - 1
	--------------------
	Mang0's results for 2015:
	1st - 5
	2nd - 4
	3rd - 2
	4th - 2
	5th - 3
	17th - 1
	--------------------
	
&nbsp;
&nbsp;	
Records pulling off smash.gg

	>> python smasherstats.py records -s Zain
	Pound 2016
	----------
	pools - Zain vs. ASL 2 - 0 WIN
	pools - Griffith vs. Zain 0 - 2 WIN
	pools - MattDotZeb vs. Zain 0 - 2 WIN
	pools - Zain vs. Crush 0 - 2 LOSS
	Game Count: 6 - 2

	Super Smash Con 2016
	--------------------
	pools - Zain vs. Crush 0 - 2 LOSS
	pools - Zain vs. ftgg 2 - 0 WIN
	pools - Zain vs. BMC 2 - 0 WIN
	pools - The Moon vs. Zain 2 - 0 LOSS
	Game Count: 4 - 4

	The Big House 6
	---------------
	Winners Round 1 - Zain vs. KJH 2 - 1 WIN
	Winners Round 2 - Zain vs. The Moon 0 - 3 LOSS
	Losers Round 4 - Zain vs. PewPewU 0 - 3 LOSS
	Game Count: 2 - 7

&nbsp;
&nbsp;		
Records pulling off smash.gg for specific player matchups

	>> python smasherstats.py records -s Mang0 -s Armada
	GENESIS 3
	---------
	Grand Final - Armada vs. Mang0 1 - 3
	Grand Final - Mang0 vs. Armada 1 - 3


	Battle of the Five Gods
	-----------------------
	Losers Final - Armada vs. Mang0 2 - 3


	Smash Summit 2
	--------------
	Losers Semi-Final - Armada vs. Mang0 3 - 0


	Get On My Level 2016
	--------------------
	Losers Quarter-Final - Armada vs. Mang0 1 - 3


	WTFox 2
	-------
	Winners Final - Armada vs. Mang0 1 - 3
	Grand Final - Mang0 vs. Armada 3 - 0


	The Big House 6
	---------------
	Winners Semi-Final - Armada vs. Mang0 2 - 3
	Grand Final - Mang0 vs. Armada 1 - 3
	Grand Final - Armada vs. Mang0 2 - 3


	Tournaments where specified players were present but results failed to be retrieved:
	 - Enthusiast Gaming Live Expo
	 - EVO 2016

	Set Count: Mang0 7 - 3 Armada
	Game Count: Mang0 23 - 18 Armada
