from Player import Player

class Route:

    def __init__(self, play, player_pos, ball_pos, game_info):

        self.player_position = play[play["event_code"] == 2]["player_position"].iloc[0]
        self.player_id = self.find_player_id(play, game_info)
        if self.player_id in Player.pre_existing_players:
            self.player = Player.pre_existing_players[self.player_id]
        else:
            self.player = Player(self.player_id)
        self.df = self.create_df(play, player_pos)

    def create_df(self, play, player_pos):
        contact_timestamp = play[(play["player_position"] == 10) & (play["event_code"] == 4)]["timestamp"].iloc[0]
        retrieval_timestamp = play[(play["player_position"] == self.player_position) & (play["event_code"] == 2)]["timestamp"].iloc[0]
        return player_pos[
            (player_pos["player_position"] == self.player_position) & 
            (player_pos["timestamp"] >= contact_timestamp) & 
            (player_pos["timestamp"] <= retrieval_timestamp)]
        
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