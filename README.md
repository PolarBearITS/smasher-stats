## smasher-stats
Start of a python smash statistics project

Welcome to SmasherStats. This is super basic for now.

SmasherStats is written in python 3.6, so make sure you have that installed before running.

Download python 3.6 here: https://www.python.org/downloads/

The default setting is to return a smasher's Melee Singles results for the current year only.

## How to run the program

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

## Dependencies

* requests
* docopt
* prettytable
* beautifulsoup4
* pysmash

You can install all these using pip by just typing `python -m pip install -r requirements.txt`

Pip comes with the latest versions of Python 2 and Python 3.
If you don't have it installed, you can download it here: https://pip.pypa.io/en/stable/installing/

## Examples

Results pulling off ssbwiki
	
	>> python script.py results -s Mang0 -t 3 -y 2016
	--------------------
	Mang0's Melee Singles results for 2016:
	Tournament names listed for placings of 3 or below.

	1st - 4
	2nd - 7

	3rd - 2
	 - Clutch City Clash
	 - Shine 2016

	4th - 4
	 - Smash Summit 2
	 - EVO 2016
	 - Smash Summit 3
	 - DreamHack Winter 2016

	13th - 1
	 - UGC Smash Open
	--------------------
	
&nbsp;
&nbsp;	
Results pulling off ssbwiki for multiple smashers

	>> python script.py results -s Armada -s Mang0 -y 2015 -t 0
	--------------------
	Mang0's Melee Singles results for 2015:
	1st - 5
	2nd - 4
	3rd - 2
	4th - 2
	5th - 3
	17th - 1
	--------------------
	Armada's Melee Singles results for 2015:
	1st - 17
	2nd - 4
	3rd - 2
	5th - 1
	--------------------
	
&nbsp;
&nbsp;	
Records pulling off smash.gg

	>> python script.py records -s Zain -y 2016
	Tournaments where specified players were present but results failed to be retrieved:
	 - Smash @ Xanadu Wednesdays 5/25
	 - Smash @ Xanadu Wednesdays 6/1
	 - Smash @ Xanadu Wednesdays 6/8
	 - EVO 2016
	 - Smash @ Xanadu Wednesdays 12/28
	+----------------------+-----------------+------------+-------+---------+
	|      Tournament      |      Round      | Zain vs. ↓ | Score | Outcome |
	+----------------------+-----------------+------------+-------+---------+
	|      Pound 2016      |      pools      |    ASL     | 2 - 0 |   WIN   |
	|                      |      pools      |  Griffith  | 2 - 0 |   WIN   |
	|                      |      pools      | MattDotZeb | 2 - 0 |   WIN   |
	|                      |      pools      |   Crush    | 0 - 2 |   LOSS  |
	|                      |                 |            |       |         |
	| Super Smash Con 2016 |      pools      |   Crush    | 0 - 2 |   LOSS  |
	|                      |      pools      |    ftgg    | 2 - 0 |   WIN   |
	|                      |      pools      |    BMC     | 2 - 0 |   WIN   |
	|                      |      pools      |  The Moon  | 0 - 2 |   LOSS  |
	|                      |                 |            |       |         |
	|   The Big House 6    | Winners Round 1 |    KJH     | 2 - 1 |   WIN   |
	|                      | Winners Round 2 |  The Moon  | 0 - 3 |   LOSS  |
	|                      |  Losers Round 4 |  PewPewU   | 0 - 3 |   LOSS  |
	+----------------------+-----------------+------------+-------+---------+

&nbsp;
&nbsp;		
Records pulling off smash.gg for specific player matchups

	>> python script.py records -s Mang0 -s Armada
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
