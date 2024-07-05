
from Route import Route
import PermHelpers

# class for metrics
class Metric:
    
    def __init__(self, relevancy_function, calculation_function, name):
        self.relevancy_func = relevancy_function
        self.calculation_func = calculation_function
        self.name = name
    
    # gets function to determine if a play is relevant based on game events table
    # returns another function
    def get_relevancy_function(self):
        return self.relevancy_func
    
    # gets function actually calculate associated score
    # returns another function
    def get_calculation_function(self):
        return self.calculation_func
    
    # getter for name
    def get_name(self):
        return self.name
    
    # tests the metric to see if it is significantly different from being random
    def test_metric(self, N = 1000):
        Route.find_all_relevant([self])
        df = Route.get_all_routes_df()
        home_only = df[df["player_id"].apply(lambda x: len(str(x)) == 3)]
        PermHelpers.permutation_tester(home_only, "player_id", N, self.get_name())

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
    outfielderidx = play[(play["player_position"] == 7) 
                         | (play["player_position"] == 8)
                         | (play["player_position"] == 9)].index[0]
    truncated = play.loc[:outfielderidx]
    if ((truncated["player_position"] > 1)
        & (truncated["player_position"] < 7)).sum() != 0:
        return False
    return True

# route efficiency calculation
def route_eff_score(route):
    return route.get_ideal_length() / route.get_total_length()

# route efficiency as a Metric object
route_efficiency = Metric(outfielder_retrieve_or_catch, route_eff_score, "route efficiency")


# measures the break a player gets on a route
# defined as highest acceleration magnitude in first 5 timestamps
def break_score(route):
    accels = route.get_accel_tuples()
    mags = list(map(lambda x: x[2], accels[:5]))
    return max(mags)

break_metric = Metric(outfielder_retrieve_or_catch, break_score, "acc mag break")

# simply uses player id as the metric
# should be literally the most statistically significant
def id_score(route):
    return route.get_player_id()

id_metric = Metric(outfielder_retrieve_or_catch, id_score, "id test")

# jump metric as defined by statcast
# at least how I assume its calculated
def jump_score(route):
    df = route.get_df()
    if df.shape[0] < 60:
        return -1
    start = route.get_start_coords()
    retrieve = route.get_retrieval_coords()
    three_sec_coords_x = df["field_x"].iloc[59]
    three_sec_coords_y = df["field_y"].iloc[59]
    total_vec = (retrieve[0] - start[0], retrieve[1] - start[1])
    three_vec = (three_sec_coords_x - start[0], three_sec_coords_y - start[1])
    total_length = route.get_ideal_length()
    dotprod = three_vec[0] * total_vec[0] + three_vec[1] * total_vec[1]
    return dotprod / total_length


statcast_jump = Metric(outfielder_retrieve_or_catch, jump_score, "statcast jump")

# reaction metric
# same as jump but for first 1.5 seconds instead of 3
def reaction_score(route):
    df = route.get_df()
    if df.shape[0] < 30:
        return -1
    start = route.get_start_coords()
    retrieve = route.get_retrieval_coords()
    one_half_sec_coords_x = df["field_x"].iloc[29]
    one_half_sec_coords_y = df["field_y"].iloc[29]
    total_vec = (retrieve[0] - start[0], retrieve[1] - start[1])
    three_vec = (one_half_sec_coords_x - start[0], one_half_sec_coords_y - start[1])
    total_length = route.get_ideal_length()
    dotprod = three_vec[0] * total_vec[0] + three_vec[1] * total_vec[1]
    return dotprod / total_length

statcast_reaction = Metric(outfielder_retrieve_or_catch, reaction_score, "statcast reaction")