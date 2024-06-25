class Metric:
    
    def __init__(self, relevancy_function, calculation_function):
        self.relevancy_func = relevancy_function
        self.calculation_func = calculation_function
    
    def get_relevancy_function(self):
        return self.relevancy_func
    
    def get_calculation_function(self):
        return self.calculation_func

def route_eff_rel(play):
    if ((play["player_position"] >= 7) 
        & (play["player_position"] <= 9) 
        & (play["event_code"] == 2)).sum() == 0:
        return False
    if play[play["event_code"] == 2]["player_position"].iloc[0] < 7:
        return False
    if 4 not in play["event_code"].values:
        return False
    return True

def route_eff_score(route):
    return route.get_ideal_length() / route.get_total_length()

route_efficiency = Metric(route_eff_rel, route_eff_score)