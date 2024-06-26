from Player import Player
from ipycanvas import Canvas
import numpy as np
# import pygame
from FindGameFiles import FindGameFiles
import pandas as pd
from Metric import Metric

class Route:

    score_func = None
    relevancy_func = None

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
    def is_relevant():
        return Route.relevancy_func
        # if ((play["player_position"] >= 7) 
        #     & (play["player_position"] <= 9) 
        #     & (play["event_code"] == 2)).sum() == 0:
        #     return False
        # if play[play["event_code"] == 2]["player_position"].iloc[0] < 7:
        #     return False
        # if 4 not in play["event_code"].values:
        #     return False
        # return True
    
    # class function for finding all relevant routes
    # uses FindGameFiles.py
    # doesn't return anything tangible
    # instantiates Player and Route objects
    # very much not efficient, the idea is to only use this once for each analysis
    def find_all_relevant(Metric):
        Player.clear_existing_players()
        Route.clear_all_routes()
        Route.relevancy_func = Metric.get_relevancy_function()
        Route.score_func = Metric.get_calculation_function()

        # Route.there_but_nan = 0
        # Route.not_there_at_all = 0
        # Route.something_else = 0

        print("Starting file search")
        files = FindGameFiles()
        print("Files accumulated")
        total = len(files)
        for i in range(total):
            game = files[i]
            try:
                relevant = pd.read_csv(game[3]).groupby("play_per_game").filter(Route.is_relevant())
            except:
                # print(1/0)
                print("game skipped")
                continue
            pp = pd.read_csv(game[0]) 
            bp = pd.read_csv(game[1])
            gi = pd.read_csv(game[2])
            for play_num in relevant["play_per_game"].unique():
                Route(relevant[relevant["play_per_game"] == play_num], pp, bp, gi)
            if i % 10 == 0:
                print(f"Finished game {i+1} of {total}")
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
                    # print("worked at least once")
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
    # 0 means straight back, pi means straight in
    # symmetric with respect to going left or right
    def get_direction(self):
        start = self.get_start_coords()
        retrieve = self.get_retrieval_coords()
        dotprod = start[0] * (retrieve[0] - start[0]) + start[1] * (retrieve[1] - start[1])
        startlen = (start[0]**2 + start[1]**2)**.5
        angle = np.arccos(dotprod / (self.get_ideal_length() * startlen))
        if angle <= np.pi:
            return angle
        return 2*np.pi - angle

    # getter for route score
    # score is defined as ideal length / total length
    # best theoretical score is 1
    # higher scores are better
    def get_score(self):
        return Route.score_func(self)
        # return self.get_ideal_length() / self.get_total_length()
    
    # getter for if the ball was caught
    # not a pre-existing instance variable
    def get_was_caught(self):
        df = self.get_play()
        df = df.head((df.reset_index()["event_code"] == 2).idxmax())
        non_catches = set([9, 10, 16])
        events = set(list(df["event_code"]))
        intersection = non_catches.intersection(events)
        return len(intersection) == 0
    
    # uses ipycanvas to visualize route
    def visualize(self):
        # get coords
        coords = self.get_coord_tuples()
        num_coords = len(coords)
        # initialize canvas
        canv = Canvas(width  = 400, height = 400)
        # transform to fit coordinate orientation
        canv.scale(x = 1, y = -1)
        canv.translate(x = canv.width / 2, y = -canv.height)
        # draw field lines
        canv.stroke_line(0, 0, 62.58, 63.64)
        canv.stroke_line(0, 0, -62.58, 63.64)
        # create colors (white is start, gets darker thru time)
        colors = np.array(range(num_coords)) * 255 / num_coords
        colors = list(map(lambda x: ([255 - x, 255 - x, 255]), colors))
        # draws circles
        canv.fill_styled_circles(np.array(self.get_x_coords()), np.array(self.get_y_coords()), color = colors, radius = 1)
        return canv
    
    # function to get velocity tuples (just subtracting consecutive positions)
    # (x velocity, y velocity, magnitude)
    # returns a list
    def get_vel_tuples(self):
        coords = self.get_coord_tuples()
        vel = []
        for i in range(len(coords)-1):
            velvec = (coords[i+1][0] - coords[i][0], coords[i+1][1]-coords[i][1])
            vel.append((velvec[0], velvec[1], (velvec[0]**2 + velvec[1]**2)**.5))
        return vel

    # same but for acceleration (just subtracting consecutive velocities)
    def get_accel_tuples(self):
        vel = self.get_vel_tuples()
        acc = []
        for i in range(len(vel)-1):
            accvec = (vel[i+1][0] - vel[i][0], vel[i+1][1]-vel[i][1])
            acc.append((accvec[0], accvec[1], (accvec[0]**2 + accvec[1]**2)**.5))
        return acc
        

    # function using ipycanvas to visualize acceleration
    def visualize_accel(self, type = "mag"):
        acc = self.get_accel_tuples()
        accdf = pd.DataFrame(columns= ["xacc", "yacc", "mag"], data  = acc)
        accdf = accdf.reset_index()
        if type == "mag":
            accdf = accdf.sort_values("mag").iloc[:-10]
            accdf = accdf.sort_values("index")
            return accdf.plot(kind = "line", x = "index", y = "mag")
            
    # returns a dataframe with every route
    def get_all_routes_df():
        # gets list of route objects
        routes = Route.get_all_routes()
        datalist = []

        #loops through every route object
        for i in range(len(routes)):
            # route object itself
            r = routes[i]
            # player id
            p_id = r.get_player_id()
            # player position (during that play)
            pos = r.get_current_player_position()
            # game string
            gs = r.get_df()["game_str"].iloc[0]
            # level (1A, 2A, 3A, 4A)
            lev = gs[-2:]
            # gets euclidean distance to retrieval spot from start
            idl_len = r.get_ideal_length()
            # gets direction, angle in radians
            dir = r.get_direction()
            # gets score for this route
            sc = r.get_score()
            datalist.append([r, gs, p_id, pos, lev, idl_len, dir, sc])

        # creates dataframe
        out = pd.DataFrame(columns= ["route_obj", "game_str", "player_id", "position", "level", "ideal_length", "direction", "score"], data = datalist)
        return out