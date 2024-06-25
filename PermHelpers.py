import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None

# given a dataframe, calculates the
# total variation distance from
# a uniform distribution of given average
# dataframe should NOT already be grouped
def calc_TVD(df, col):
    grouped = df[[col, "score"]].groupby(col).mean()
    av = df["score"].mean()
    return .5*(np.abs(grouped["score"] - av)).sum()


# does a permutation test
def permutation_tester(df, col, N):
    df = df[[col, "score"]]
    observed_stat = calc_TVD(df, col)
    more_extreme = 0
    total = 0
    for _ in range(N):
        df["shuffled"] = df[col].sample(frac = 1).values
        stat = calc_TVD(df, "shuffled")
        if stat >= observed_stat:
            more_extreme += 1
        total += stat
    p_val = more_extreme/N
    print(f"Out of {N} permutations, {more_extreme} had a test statistic at least as extreme as the observed test statistic.")
    print(f"This give a p-value of {p_val}.")
    print(f"The observed statistic was {observed_stat}.")
    print(f"The average test statistic was {total / N}")
    return df