# smasher-stats
Start of a python smash statistics project

Welcome to SmasherStats. This is super basic for now.

SmasherStats is written in python 3.5, so make sure you have that installed before running.

Download python 3.5 here: https://www.python.org/downloads/

# How to run the program
'python smasher-stats.py -s "\<smasher tag>" -g "\<game title>" -t \<result threshold> -y \<year> -c \<comparison>'
    
 - -s: The smasher's tag. There's only a need for quotes if the tag has a space in it.
 - -g: The game you would like results for. Again, quotes needed only if there's a space (You can be pretty flexible with what you enter).
 - -t: The results threhold. If the player places at or below this place, the tournament name will also be displayed.
 - -y: The year filter. Works in conjunction with the next flag to deliver tournaments from specific timeframes.
 - -c: The comparison string. When the program checks when a tournament took place, it will use this string to compare it to \<year>. Possible comparison strings: "==", "!=", "\<", ">", "\<=", ">="

If any of the above flags are not provided, their default value will be used:

 - Smasher Tag: prompt for user input
 - Game: Melee
 - Threshold: 5th place
 - Year: Current Year
 - Comparison: >=
