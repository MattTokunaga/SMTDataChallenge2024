class Player:
    
    pre_existing_players = {}

    def __init__(self, player_id):
        
        self.player_id = player_id
        self.levels_played = []
        self.routes = []
        self.positions = []
        Player.pre_existing_players[player_id] = self

    def get_id(self):
        return self.player_id
    
    def get_levels(self): 
        return self.levels_played
    
    def add_level(self, new_level):
        try:
            self.levels_played.append(new_level)
            return True
        except:
            return False
    
    def get_routes(self):
        return self.routes
    
    def add_route(self, new_route):
        try:
            self.routes.append(new_route)
            return True
        except:
            return False
        
    def get_positions(self):
        return self.positions
    
    def add_position(self, new_position):
        try:
            self.positions.append(new_position)
            return True
        except:
            return False