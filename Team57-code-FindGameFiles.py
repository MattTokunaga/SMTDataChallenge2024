import os
from pathlib import Path

# function for finding all game files
# returns a list of tuples of form:
# (player_pos, ball_pos, game_info, game_events)
def FindGameFiles():
    files = []
    for season in os.listdir(r"2024_SMT_Data_Challenge\ball_pos"):
        for team in os.listdir(rf"2024_SMT_Data_Challenge\ball_pos\{season}"):
            for vis in os.listdir(rf"2024_SMT_Data_Challenge\ball_pos\{season}\{team}"):
                for day in os.listdir(rf"2024_SMT_Data_Challenge\ball_pos\{season}\{team}\{vis}"):
                    p = Path(f"{season}\{team}\{vis}\{day}")
                    # player position
                    pp = Path("2024_SMT_Data_Challenge/player_pos") / p / Path("player_pos.csv")
                    # ball position
                    bp = Path("2024_SMT_Data_Challenge/ball_pos") / p / Path("ball_pos.csv")
                    # game info
                    gi = Path("2024_SMT_Data_Challenge/game_info") / p / Path("game_info.csv")
                    # game events
                    ge = Path("2024_SMT_Data_Challenge/game_events") / p / Path("game_events.csv")

                    files.append((pp, bp, gi, ge))
    return files
