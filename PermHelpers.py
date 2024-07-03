import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None

# given a dataframe, calculates the
# total variation distance from
# a uniform distribution of given average
# dataframe should NOT already be grouped
def calc_TVD(df, col, score_col):
    grouped = df[[col, score_col]].groupby(col).mean()
    av = df[score_col].mean()
    return .5*(np.abs(grouped[score_col] - av)).sum()


# does a permutation test
def permutation_tester(df, col, N, score_col):
    df = df[[col, score_col]]
    # calculates observed stat (TVD)
    observed_stat = calc_TVD(df, col)
    more_extreme = 0
    total = 0
    # shuffles N times
    for _ in range(N):
        # creates shuffled column
        df["shuffled"] = df[col].sample(frac = 1).values
        # calculates test statistic as if shuffled column was real
        stat = calc_TVD(df, "shuffled")
        # records if the test stat was as or more extreme than observed
        if stat >= observed_stat:
            more_extreme += 1
        total += stat
    p_val = more_extreme/N
    print(f"Out of {N} permutations, {more_extreme} had a test statistic at least as extreme as the observed test statistic.")
    print(f"This give a p-value of {p_val}.")
    if p_val < 0.05:
        print("This would be considered statistically significant")
    else:
        print("This would NOT be considered statistically signifiant")
    print("-----")
    print(f"The observed statistic was {observed_stat}.")
    print(f"The average test statistic was {total / N}")

    return df