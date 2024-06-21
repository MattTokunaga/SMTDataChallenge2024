from Player import Player
from ipycanvas import Canvas
import numpy as np

class Route:

    def __init__(self, play, player_pos, ball_pos, game_info):

        self.player_position = play[play["event_code"] == 2]["player_position"].iloc[0]
        self.player_id = self.find_player_id(play, game_info)
        if self.player_id in Player.pre_existing_players:
            self.player = Player.pre_existing_players[self.player_id]
        else:
            self.player = Player(self.player_id)
        self.player.add_position(self.player_position)
        self.player.add_level(play["game_str"].iloc[0][-2:])
        self.player.add_route(self)
        self.df = self.create_df(play, player_pos)
    
    # class function for determining of a route is relevant
    def is_relevant(play):
        if ((play["player_position"] >= 7) 
            & (play["player_position"] <= 9) 
            & (play["event_code"] == 2)).sum() == 0:
            return False
        if play[play["event_code"] == 2]["player_position"].iloc[0] < 7:
            return False
        return True

    # not a getter for df instance variable
    # intended to be used to create df variable at time of initialization
    def create_df(self, play, player_pos):
        contact_timestamp = play[(play["player_position"] == 10) & (play["event_code"] == 4)]["timestamp"].iloc[0]
        retrieval_timestamp = play[(play["player_position"] == self.player_position) & (play["event_code"] == 2)]["timestamp"].iloc[0]
        return player_pos[
            (player_pos["player_position"] == self.player_position) & 
            (player_pos["timestamp"] >= contact_timestamp) & 
            (player_pos["timestamp"] <= retrieval_timestamp)]
        
    # not a getter for player id, used at initialization to find id
    def find_player_id(self, play, game_info):
        df = play.merge(game_info, on = "play_per_game")
        if self.player_position == 7:
            return int(df["left_field"].iloc[0])
        elif self.player_position == 8:
            return int(df["center_field"].iloc[0])
        elif self.player_position == 9:
            return int(df["right_field"].iloc[0])
        else:
            print("Error: Position not 7, 8, or 9")
            return False
        
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
    
    # getter for route score
    # score is defined as ideal length / total length
    # best theoretical score is 1
    # higher scores are better
    def get_score(self):
        return self.get_ideal_length() / self.get_total_length()
    
    # uses ipycanvas to visualize route
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