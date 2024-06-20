import Player

class Route:

    def __init__(self, play, player_pos, ball_pos, game_info):

        self.player_id = play[play["event_code"] == 2]["player_position"].iloc[0]
        if self.player_id in Player.pre_existing_players:
            self.player = Player.pre_existing_players[self.player_id]
        else:
            self.player = Player(self.player_id)
        self.df
        self.player_position 

    def create_df(self, play, player_pos, ball_pos, game_info):
        contact_timestamp = play[(play["player_position"] == 10) & (play["event_code"] == 4)]["timestamp"].iloc[0]
        
    