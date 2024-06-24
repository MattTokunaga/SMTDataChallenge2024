from Player import Player
from ipycanvas import Canvas
import numpy as np
# import pygame
from FindGameFiles import FindGameFiles
import pandas as pd

class Route:

    all_routes = []
    there_but_nan = 0
    not_there_at_all = 0
    something_else = 0

    def __init__(self, play, player_pos, ball_pos, game_info):

        self.play = play
        self.player_position = play[play["event_code"] == 2]["player_position"].iloc[0]
        self.player_id = self.find_player_id(play, game_info)
        if self.player_id in Player.pre_existing_players:
            self.player = Player.pre_existing_players[self.player_id]
        else:
            self.player = Player(self.player_id)
        self.player.add_position(self.player_position)
        self.player.add_level(play["game_str"].iloc[0][-2:])
        self.start_coords = False
        self.player.add_route(self)
        self.df = self.create_df(play, player_pos)
        try: 
            self.start_coords = self.get_start_coords()
            Route.add_to_all_routes(self)
        except:
            print("no start coords")
            self.player.remove_last_route()
    
    # class function for determining of a route is relevant
    def is_relevant(play):
        if ((play["player_position"] >= 7) 
            & (play["player_position"] <= 9) 
            & (play["event_code"] == 2)).sum() == 0:
            return False
        if play[play["event_code"] == 2]["player_position"].iloc[0] < 7:
            return False
        if 4 not in play["event_code"].values:
            return False
        return True
    
    # class function for finding all relevant routes
    # uses FindGameFiles.py
    # doesn't return anything tangible
    # instantiates Player and Route objects
    # very much not efficient, the idea is to only use this once for each analysis
    def find_all_relevant():
        Player.clear_existing_players()
        Route.clear_all_routes()

        # Route.there_but_nan = 0
        # Route.not_there_at_all = 0
        # Route.something_else = 0

        files = FindGameFiles()
        total = len(files)
        for i in range(total):
            game = files[i]
            try:
                relevant = pd.read_csv(game[3]).groupby("play_per_game").filter(Route.is_relevant)
            except:
                print("game skipped")
                continue
            pp = pd.read_csv(game[0]) 
            bp = pd.read_csv(game[1])
            gi = pd.read_csv(game[2])
            for play_num in relevant["play_per_game"].unique():
                Route(relevant[relevant["play_per_game"] == play_num], pp, bp, gi)
            print(f"Finished game {i} of {total}")
        return True
    
    def clear_all_routes():
        Route.all_routes = []
        print("Routes cleared")
        return True
    
    def get_all_routes():
        return Route.all_routes
    
    def get_total_num_routes():
        return len(Route.get_all_routes())
    
    def add_to_all_routes(route):
        Route.all_routes.append(route)
        return True

    # not a getter for df instance variable
    # intended to be used to create df variable at time of initialization
    def create_df(self, play, player_pos):
        contact_timestamp = play[(play["player_position"] == 10) & (play["event_code"] == 4)]["timestamp"].iloc[0]
        retrieval_timestamp = play[(play["player_position"] == self.get_current_player_position()) & (play["event_code"] == 2)]["timestamp"].iloc[0]
        return player_pos[
            (player_pos["player_position"] == self.get_current_player_position()) & 
            (player_pos["timestamp"] >= contact_timestamp) & 
            (player_pos["timestamp"] <= retrieval_timestamp)]
        
    # not a getter for player id, used at initialization to find id
    # returns -1 if no player id is found
    def find_player_id(self, play, game_info):
        df = play.merge(game_info, on = "play_per_game")
        try:
            if self.player_position == 7:
                return int(df["left_field"].iloc[0])
            elif self.player_position == 8:
                return int(df["center_field"].iloc[0])
            elif self.player_position == 9:
                return int(df["right_field"].iloc[0])
            else:
                print("Error: Position not 7, 8, or 9")
                return False
        except:
            try:
                if df.shape[0] == 0:
                    print("worked at least once")
                    Route.not_there_at_all += 1
                elif not df["left_field"].iloc[0] > 0:
                    Route.there_but_nan += 1
            except:
                Route.something_else += 1
            return -1
        
    # getter for play from game_events
    def get_play(self):
        return self.play

    # getter for player id
    # goes through player object
    def get_player_id(self):
        return self.player.get_id()
    
    # getter for player's position during this route
    # does not go through player object
    def get_current_player_position(self):
        return self.player_position

    # getter for player's positions
    # goes through player object
    def get_player_positions(self):
        return self.player.get_positions()
    
    # getter for dataframe
    def get_df(self):
        return self.df

    # getter for coordinate tuples
    # not a pre-existing instance variable
    # created from df instance variable
    def get_coord_tuples(self):
        df = self.get_df()
        return list(zip(list(df["field_x"]), list(df["field_y"])))
    
    # getter for list of x coordinates
    # not a pre-existing instance variable
    # created from df instance variable
    def get_x_coords(self):
        return list(self.get_df()["field_x"])
    
    # getter for list of x coordinates
    # not a pre-existing instance variable
    # created from df instance variable
    def get_y_coords(self):
        return list(self.get_df()["field_y"])
    
    # getter for starting coordinates
    # not a pre-existing instance variable
    def get_start_coords(self):
        if self.start_coords:
            return self.start_coords
        return (self.get_df()["field_x"].iloc[0], self.get_df()["field_y"].iloc[0])

    
    # getter for retrieval coordinates
    # not a pre-existing instance variable
    def get_retrieval_coords(self):
        return (self.get_df()["field_x"].iloc[-1], self.get_df()["field_y"].iloc[-1])
    
    # getter for total route length
    # linearly interpolates between points
    # not a pre-existing instance variable
    def get_total_length(self):
        coords = self.get_coord_tuples()
        total = 0
        for i in range(len(coords) - 1):
            total += ((coords[i][0] - coords[i+1][0])**2 + (coords[i][1] - coords[i+1][1])**2)**.5
        return total
    
    # getter for ideal length
    # straight line distance from start coords to retrieval coords
    # not a pre-existing instance variable
    def get_ideal_length(self):
        start = self.get_start_coords()
        retrieve = self.get_retrieval_coords()
        return ((start[0] - retrieve[0])**2 + (start[1] - retrieve[1])**2)**.5
    
    # getter for ideal route vector direction
    # angle in radians
    def get_direction(self):
        start = self.get_start_coords()
        retrieve = self.get_retrieval_coords()
        return np.arccos((retrieve[0] - start[0]) / self.get_ideal_length())

    # getter for route score
    # score is defined as ideal length / total length
    # best theoretical score is 1
    # higher scores are better
    def get_score(self):
        return self.get_ideal_length() / self.get_total_length()
    
    # getter for if the ball was caught
    # not a pre-existing instance variable
    def get_was_caught(self):
        df = self.get_play()
        df = df.head((df.reset_index()["event_code"] == 2).idxmax())
        non_catches = set([9, 10, 16])
        events = set(list(df["event_code"]))
        intersection = non_catches.intersection(events)
        return len(intersection) == 0
    
    # uses pygame to visualize route
    def visualize(self):
        coords = self.get_coord_tuples()
        num_coords = len(coords)
        canv = Canvas(width  = 400, height = 400)
        canv.scale(x = 1, y = -1)
        canv.translate(x = canv.width / 2, y = -canv.height)
        colors = np.array(range(num_coords)) * 255 / num_coords
        colors = list(map(lambda x: ([255 - x, 255 - x, 255]), colors))
        canv.fill_styled_circles(np.array(self.get_x_coords()), np.array(self.get_y_coords()), color = colors, radius = 1)
        return canv
    
    def get_all_routes_df():
        routes = Route.get_all_routes()
        out = pd.DataFrame(columns= ["player_id", "position", "level", "ideal_length", "direction", "score"])
        for i in range(len(routes)):
            r = routes[i]
            p_id = r.get_player_id()
            pos = r.get_current_player_position()
            lev = r.get_df()["game_str"].iloc[0][-2:]
            idl_len = r.get_ideal_length()
            dir = r.get_direction()
            sc = r.get_score()
            out.loc[i] = (p_id, pos, lev, idl_len, dir, sc)
        return out