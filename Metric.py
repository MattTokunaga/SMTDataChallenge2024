
from Route import Route
import PermHelpers

# class for metrics
class Metric:
    
    def __init__(self, relevancy_function, calculation_function):
        self.relevancy_func = relevancy_function
        self.calculation_func = calculation_function
    
    # gets function to determine if a play is relevant based on game events table
    # returns another function
    def get_relevancy_function(self):
        return self.relevancy_func
    
    # gets function actually calculate associated score
    # returns another function
    def get_calculation_function(self):
        return self.calculation_func
    
    # tests the metric to see if it is significantly different from being random
    def test_metric(self, N = 1000):
        Route.find_all_relevant(self)
        df = Route.get_all_routes_df()
        home_only = df[df["player_id"].apply(lambda x: len(str(x)) == 3)]
        PermHelpers.permutation_tester(home_only, "player_id", N)

# relevancy function for any metric that involves any outfielder catching or
# receiving a ball
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

# route efficiency calculation
def route_eff_score(route):
    return route.get_ideal_length() / route.get_total_length()

# route efficiency as a Metric object
route_efficiency = Metric(outfielder_retrieve_or_catch, route_eff_score)


# measures the break a player gets on a route
# defined as highest acceleration magnitude in first 5 timestamps
def break_score(route):
    accels = route.get_accel_tuples()
    mags = list(map(lambda x: x[2], accels[:5]))
    return max(mags)

break_metric = Metric(outfielder_retrieve_or_catch, break_score)

# simply uses player id as the metric
# should be literally the most statistically significant
def id_score(route):
    return route.get_player_id()

id_metric = Metric(outfielder_retrieve_or_catch, id_score)