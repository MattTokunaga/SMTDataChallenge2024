class Player:
    
    # class variable, dictionary of existing players
    # key = player id, value = reference to player object
    pre_existing_players = {}

    def __init__(self, player_id):
        
        if player_id != int(player_id):
            print("Invalid player ID")
            return False

        self.player_id = player_id
        self.levels_played = set([])
        self.routes = []
        self.positions = set([])
        Player.pre_existing_players[player_id] = self

    def get_id(self):
        return self.player_id
    
    def get_levels(self): 
        return self.levels_played
    
    def add_level(self, new_level):
        try:
            self.levels_played.add(new_level)
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
            if int(new_position) != new_position:
                print("Error: Invalid position")
                return False
            self.positions.add(int(new_position))
            return True
        except:
            return False
        
    # class method
    def get_existing_players():
        return Player.pre_existing_players

    # class method
    def clear_existing_players():
        Player.pre_existing_players = {}
        return True