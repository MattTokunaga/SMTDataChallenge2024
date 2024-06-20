class Player:
    
    # class variable, dictionary of existing players
    # key = player id, value = reference to player object
    pre_existing_players = {}

    def __init__(self, player_id):
        
        if player_id != int(player_id):
            print("Invalid player ID")
            return False

        self.player_id = player_id
        # format for levels_played is:
        # key = level
        # value = number of routes at that level
        self.levels_played = {}
        self.routes = []
        # format for positions is:
        # key = position
        # value = number of routes at that position
        self.positions = {}
        Player.pre_existing_players[player_id] = self

    # getter for player id
    def get_id(self):
        return self.player_id
    
    # getter for levels played at
    def get_levels(self): 
        return self.levels_played
    
    # method to add a level played at
    def add_level(self, new_level):
        if new_level not in self.get_levels():
            self.levels_played[new_level] = 0
        self.levels_played[new_level] += 1
        return True

    # getter for routes
    def get_routes(self):
        return self.routes
    
    # method to add a route
    def add_route(self, new_route):
        try:
            self.routes.append(new_route)
            return True
        except:
            return False
    
    # getter for positions
    def get_positions(self):
        return self.positions
    
    # method to add a position
    def add_position(self, new_position):
        if new_position not in self.get_positions():
            self.positions[new_position] = 0
        self.positions[new_position] += 1
        return True
        
        
    # class method to get all players
    def get_existing_players():
        return Player.pre_existing_players

    # class method to clear all players
    def clear_existing_players():
        Player.pre_existing_players = {}
        return True