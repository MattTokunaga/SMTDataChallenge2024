# SMTDataChallenge2024

IMPORTANT!!

The only file that is intended to be run is the file named "Team57_code_Analysis_and_Vis.ipynb" 
The other files that end in .py are simply for classes that I use in the analysis.
I wanted to put the skills I've learned in classes to the test, so I made heavy use of object oriented programming.

ALSO IMPORTANT!! (probably even more important)

I did NOT use the starter code at all. I used an original function to sift through the files for relevant plays.
This probably makes my code quite slow, especially when I first load in the data.
I did this because honestly I did not know what the starter code was doing and I felt comfortable writing functions for file navigation.
THE CORRECT DIRECTORY FORMAT IS AS FOLLOWS:
In the same folder as all the other files, I had a folder called 2024_SMT_Data_Challenge, which is the data as downloaded.
In the 2024_SMT_Data_Challenge folder there were four folders and one file: ball_pos, game_events, game_info, player_pos, team_info.csv
This should be the exact same format as the data when I initially downloaded it. 

Because of this inefficiency, I wouldn't really recommend running any of my code unless you have a five minutes or so to spare.

Miscellaneous notes:
I had to rename some of my files to submit. 
The original import statements are commented out instead of deleted so that in case of an error due to the renaming you can see what it looked like originally.

The playground.ipynb file is where I did a lot of informal analysis. As such it is very messy and wouldn't run properly due to cells being in the wrong order and the file renaming. Any analysis that lead to visualizations was cleaned up and put in the other notebook file. 

The results.csv is a table of all the "subroutes." A "subroute" is simply one snapshot of a play. It has the four variables that get inputted into the DCP model: distance remaining, hang time remaining, updated direction, speed in correct direction, as well as some additional information. The unique IDs for each route are NOT in number order. Subroutes with the same unique route ID come from the same play. The "new_route" column is true if that subroute is the first one of that play and false otherwise. The variable "orig_hang_time" refers to the hang time of the whole play. 