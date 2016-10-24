## smasher-stats
Start of a python smash statistics project

Welcome to SmasherStats. This is super basic for now.

SmasherStats is written in python 3.5, so make sure you have that installed before running.

Download python 3.5 here: https://www.python.org/downloads/

## How to run the program
usage: smasherstats.py [-h] (-s SMASHER | -i INPUT_FILE) [-t THRESHOLD]
                       [-y YEAR] [-c COMPARISON] [-g GAME] [-o OUTPUT_FILE]

Get tournament results of specified smasher

optional arguments:
  -h, --help            show a help message and exit
  -s SMASHER, --smasher SMASHER
                        The tag of the smasher you want results for; NOTE: THIS IS REQUIRED
  -i INPUT_FILE, --input_file INPUT_FILE
                        Path to input file
  -t THRESHOLD, --threshold THRESHOLD
                        Tournaments where the smasher placed worse will have
                        their names displayed
  -y YEAR, --year YEAR  Specified year used in conjunction with -c
  -c COMPARISON, --comparison COMPARISON
                        What comparison to use when comparing the date to -y
  -g GAME, --game GAME  Specified game to get tournament results for
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        Path to output file

Possible comparison strings:
 - ==
 - !=
 - <
 - >
 - <=
 - >=

If any of the above flags are not provided, their default value will be used:

 - Game: Melee
 - Threshold: 5th place
 - Year: Current Year
 - Comparison: >=
