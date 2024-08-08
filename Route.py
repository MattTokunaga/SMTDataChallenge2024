from Player import Player
from ipycanvas import Canvas
import numpy as np
# import pygame
from FindGameFiles import FindGameFiles
import pandas as pd
from Animation import plot_animation

class Route:

    score_funcs = {}
    relevancy_func = None

    all_routes = []

    # these are for debugging purposes, ignore em
    there_but_nan = 0
    not_there_at_all = 0
    something_else = 0
    no_ball_info = 0

    def __init__(self, play, player_pos, ball_pos, game_info):

        self.play = play
        self.player_position = play[play["event_code"] == 2]["player_position"].iloc[0]
        self.player_id = self.find_player_id(play, game_info)
        if self.player_id in Player.get_existing_players():
            self.player = Player.get_existing_players()[self.player_id]
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
        
        self.play_id = play["play_id"].iloc[0]
        self.ball_pos = ball_pos[ball_pos["play_id"] == self.play_id]
        self.player_pos = player_pos[player_pos["play_id"] == self.play_id]
    
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
    def find_all_relevant(Metrics):
        from Metric import Metric
        Player.clear_existing_players()
        Route.clear_all_routes()
        Route.relevancy_func = Metrics[0].get_relevancy_function()
        for metric in Metrics:
            Route.score_funcs[metric.get_name()] = metric.get_calculation_function()

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
                relevant = pd.read_csv(game[3]).groupby("play_id").filter(Route.is_relevant())
            except:
                #print(1/0)
                print("game skipped")
                continue
            pp = pd.read_csv(game[0]) 
            bp = pd.read_csv(game[1])
            gi = pd.read_csv(game[2])
            for play_num in relevant["play_id"].unique():
                Route(relevant[relevant["play_id"] == play_num], pp, bp, gi)
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
    
    # # getter for ideal route vector direction
    # # angle in radians
    # # 0 is straight back, pi/2 is straight left
    # # pi is straight forward, 3pi/2 is straight right
    # def get_raw_angle(self):
    #     start = self.get_start_coords()
    #     retrieve = self.get_retrieval_coords()
    #     direcvec = (retrieve[0] - start[0], retrieve[1] - start[1])
    #     angle = np.arctan2(start[1], start[0]) - np.arctan2(direcvec[1], direcvec[0])
    #     if angle < 0:
    #         return angle + 2 * np.pi
    #     return angle

    # gets general direction WHERE BALL IS RETRIEVED
    # 90 degree quadrants
    def get_retrieval_direction(self):
        return Route.find_direction(self.get_start_coords(), self.get_retrieval_coords())


    # getter for hang time
    # in milliseconds, subtracts timestamps
    def get_hang_time(self):
        play = self.get_play()
        play = play.loc[(play["event_code"] == 4).idxmax():(play["event_code"] == 2).idxmax()]
        if 255 not in play["player_position"].values:
            return play["timestamp"].iloc[-1] - play["timestamp"].iloc[0]
        else:
            bounceonly = play.loc[:(play["player_position"] == 255).idxmax()]
            return bounceonly["timestamp"].iloc[-1] - bounceonly["timestamp"].iloc[0]
        
    # getter for ball position dataframe
    def get_ball_pos(self):
        return self.ball_pos
    
    # getter for coordinates where ball lands or is caught
    def get_landing_coords(self):
        if self.get_was_caught():
            return self.get_retrieval_coords()
        bounce_time = self.get_landing_time()
        ballpos = self.get_ball_pos()
        try:
            bounce_ser = ballpos[ballpos["timestamp"] == bounce_time].iloc[0]
        except:
            Route.no_ball_info += 1
            return self.get_retrieval_coords()
        ballx = bounce_ser["ball_position_x"]
        bally = bounce_ser["ball_position_y"]
        return (ballx, bally)

    # getter for timestamp when ball either lands or is caught
    def get_landing_time(self):
        play = self.get_play()
        idx = play[play["player_position"] == 10].index[0]
        play = play.loc[idx:].iloc[1:]
        bounce_time = play["timestamp"].iloc[0]
        return bounce_time
    
    # helper function for finding discretized direction between two points
    def find_direction(start, end):
        direcvec = (end[0] - start[0], end[1] - start[1])
        angle = np.arctan2(start[1], start[0]) - np.arctan2(direcvec[1], direcvec[0])
        if angle < 0:
            angle = angle + 2 * np.pi
        if angle <= np.pi / 4 or angle > 7 * np.pi / 4:
            return "back"
        elif angle <= 3 *np.pi / 4:
            return "left"
        elif angle <= 5 * np.pi / 4:
            return "forward"
        else:
            return "right"

    # getter for landing direction
    # direction where ball hits ground or is caught, could be different
    # from actual retrieval direction
    def get_direction(self):
        return Route.find_direction(self.get_start_coords(), self.get_landing_coords())


    # getter for whether the player got to the ball
    # defined as either catching the ball or being within 3 feet
    def get_got_to(self):
        if self.get_was_caught():
            return True
        ballx, bally = self.get_landing_coords()
        bounce_time = self.get_landing_time()
        playpos = self.get_df()
        bounce_time_df = playpos[np.abs(playpos["timestamp"] - bounce_time) < 20]
        playerx = bounce_time_df["field_x"].mean()
        playery = bounce_time_df["field_y"].mean()
        dist = np.sqrt((playerx - ballx)**2 + (playery - bally)**2)
        return dist <= 3

    # getter for route score
    # score is defined as ideal length / total length
    # best theoretical score is 1
    # higher scores are better
    def get_scores(self):
        out = {}
        play = self.get_play()
        scorefuncs = Route.get_score_funcs()
        for metric in scorefuncs:
            out[metric] = scorefuncs[metric](play)
        return out
        # return self.get_ideal_length() / self.get_total_length()
    
    # getter for score functions
    def get_score_funcs():
        return Route.score_funcs
    
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
    def visualize(self, save = False):
        # # get coords
        # coords = self.get_coord_tuples()
        # num_coords = len(coords)
        # # initialize canvas
        # canv = Canvas(width  = 400, height = 400)
        # # transform to fit coordinate orientation
        # canv.scale(x = 1, y = -1)
        # canv.translate(x = canv.width / 2, y = -canv.height)
        # # draw field lines
        # canv.stroke_line(0, 0, 62.58, 63.64)
        # canv.stroke_line(0, 0, -62.58, 63.64)
        # # create colors (white is start, gets darker thru time)
        # colors = np.array(range(num_coords)) * 255 / num_coords
        # colors = list(map(lambda x: ([255 - x, 255 - x, 255]), colors))
        # # draws circles
        # canv.fill_styled_circles(np.array(self.get_x_coords()), np.array(self.get_y_coords()), color = colors, radius = 1)
        # return canv
        return plot_animation(self.player_pos, self.ball_pos, self.play_id, save_gif = save)

    
    # function to get velocity tuples (just subtracting consecutive positions)
    # (x velocity, y velocity, magnitude)
    # returns a list
    def get_vel_tuples(self):
        coords = pd.DataFrame(self.get_coord_tuples())
        xvels = coords[0].shift(-1) - coords[0]
        yvels = coords[1].shift(-1) - coords[1]
        mags = (xvels**2 + yvels**2)**.5
        return list(zip(xvels, yvels, mags))

    # same but for acceleration (just subtracting consecutive velocities)
    def get_accel_tuples(self):
        vel = pd.DataFrame(self.get_vel_tuples())
        xaccs = vel[0].shift(-1) - vel[0]
        yaccs = vel[1].shift(-1) - vel[1]
        mags = (xaccs**2 + yaccs**2)**.5
        return list(zip(xaccs, yaccs, mags))
        

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
            # gets distance from starting position to bounce/catch position
            startx, starty = r.get_start_coords()
            landx, landy = r.get_landing_coords()
            bd = ((startx - landx)**2 + (starty - landy)**2)**.5
            datalist.append([r, gs, p_id, pos, lev, idl_len, dir, bd])

        # creates dataframe
        out = pd.DataFrame(columns= ["route_obj", "game_str", "player_id", "position", "level", "ideal_length", "direction", "bounce_dist"], data = datalist)

        # finds scores
        for metric in Route.get_score_funcs():
            scores = []
            for i in range(len(routes)):
                r = routes[i]
                scores.append(Route.get_score_funcs()[metric](r))
            scores = pd.Series(scores).rename(metric)
            out = pd.concat([out, scores], axis = 1)
        return out
    
    # gets all subroutes for one route
    def get_subroutes(self):
        velo_interval = 5 # quarter second
        rdf = self.get_df()
        rdf = rdf.iloc[::velo_interval]
        rdf = rdf[rdf["timestamp"] <= self.get_landing_time()]
        rdf["distance_remaining"] = np.linalg.norm(rdf[["field_x", "field_y"]].to_numpy() - self.get_landing_coords(), axis = 1)
        rdf["hang_time_remaining"] = self.get_landing_time() - rdf["timestamp"]
        rdf["current_coords"] = list(zip(rdf["field_x"], rdf["field_y"]))
        land_coords = self.get_landing_coords()
        rdf["updated_direction"] = rdf["current_coords"].apply(lambda x: Route.find_direction(x, land_coords))
        frame_shift = 1
        rdf["quarter_sec_ago_coords"] = rdf["current_coords"].shift(frame_shift)
        rdf.loc[rdf.index[:frame_shift], "quarter_sec_ago_coords"] = rdf["current_coords"].iloc[:frame_shift]
        rdf["quarter_sec_ago_x"] = rdf["field_x"].shift(frame_shift)
        rdf["quarter_sec_ago_y"] = rdf["field_y"].shift(frame_shift)
        rdf.loc[rdf.index[:frame_shift], "quarter_sec_ago_x"] = rdf["field_x"].iloc[:frame_shift]
        rdf.loc[rdf.index[:frame_shift], "quarter_sec_ago_y"] = rdf["field_y"].iloc[:frame_shift]

        # pure velo
        #rdf["quarter_sec_velo"] = np.linalg.norm(rdf[["field_x", "field_y"]].to_numpy() - rdf[["quarter_sec_ago_x", "quarter_sec_ago_y"]].to_numpy(), axis = 1) * 
        
        # velo in correct direction
        a = np.array(list(zip(rdf["field_x"] - rdf["quarter_sec_ago_x"], rdf["field_y"] - rdf["quarter_sec_ago_y"])))
        b = np.array(list(zip(land_coords[0] - rdf["field_x"], land_coords[1] - rdf["field_y"])))
        rdf["quarter_sec_velo"] = np.sum(a*b, axis = 1) / np.linalg.norm(list(zip(land_coords[0] - rdf["field_x"], land_coords[1] - rdf["field_y"])), axis =1 ) * 4
        if rdf["quarter_sec_velo"].isna().sum() > 0:
            print("hi")
            rdf["quarter_sec_velo"].iloc[-1] = rdf["distance_remaining"].iloc[-2] * 4

        rdf["was_caught"] = [self.get_was_caught()]*rdf.shape[0]
        rdf["route_obj"] = self
        return rdf[["route_obj", "distance_remaining", "hang_time_remaining", "updated_direction", "quarter_sec_velo", "was_caught"]]
    
    def get_all_subroutes_df():
        to_concat = []
        for route in Route.get_all_routes():
            to_concat.append(route.get_subroutes())
        return pd.concat(to_concat)