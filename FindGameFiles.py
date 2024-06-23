import os
from pathlib import Path

def FindGameFiles():
    files = []
    for season in os.listdir(r"2024_SMT_Data_Challenge\ball_pos"):
        for team in os.listdir(rf"2024_SMT_Data_Challenge\ball_pos\{season}"):
            for vis in os.listdir(rf"2024_SMT_Data_Challenge\ball_pos\{season}\{team}"):
                for day in os.listdir(rf"2024_SMT_Data_Challenge\ball_pos\{season}\{team}\{vis}"):
                    p = Path(f"{season}\{team}\{vis}\{day}")
                    pp = Path("2024_SMT_Data_Challenge/player_pos") / p / Path("player_pos.csv")
                    bp = Path("2024_SMT_Data_Challenge/ball_pos") / p / Path("ball_pos.csv")
                    gi = Path("2024_SMT_Data_Challenge/game_info") / p / Path("game_info.csv")
                    ge = Path("2024_SMT_Data_Challenge/game_events") / p / Path("game_events.csv")

                    files.append((pp, bp, gi, ge))
    return files