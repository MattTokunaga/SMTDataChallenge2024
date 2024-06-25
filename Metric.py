
from Route import Route
import PermHelpers

class Metric:
    
    def __init__(self, relevancy_function, calculation_function):
        self.relevancy_func = relevancy_function
        self.calculation_func = calculation_function
    
    def get_relevancy_function(self):
        return self.relevancy_func
    
    def get_calculation_function(self):
        return self.calculation_func
    
    def test_metric(self, N = 1000):
        Route.find_all_relevant(self)
        df = Route.get_all_routes_df()
        home_only = df[df["player_id"].apply(lambda x: len(str(x)) == 3)]
        PermHelpers.permutation_tester(home_only, "player_id", N)

def outfielder_retrieve_or_catch(play):
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

route_efficiency = Metric(outfielder_retrieve_or_catch, route_eff_score)