import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

REF_COLOR = "k"
FEMALE_COLOR = "C1"
MALE_COLOR = "C0"
ALL_COLOR = "C5"

GLUC_COLOR = "C0"
FOOD_COLOR = "C1"


def plot_age_ref(
    iglu_var, gender, ref_df=None, ax=None, perc_plot_list=[3, 10, 50, 90, 97]
):

    if ref_df is None:
        fname = "../CGMap/iglu_reference_values/age_gender_percentiles_df.csv"
        ref_df = pd.read_csv(fname, index_col=0)
    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=(8, 5))

    # filter reference_df
    df = ref_df.loc[(ref_df["Value"] == iglu_var) & (ref_df["Gender"] == gender)]

    # prep ax
    age_bins = np.arange(40, 71, 1)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.set_xlabel("Age")
    ax.set_ylabel(iglu_var)
    xticks = (np.sort(np.unique(np.floor(age_bins / 10) * 10))).astype(int)
    # xticks = np.append(xticks, xticks[-1] + 10)
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticks)
    ax.set_xlim(xticks[0], xticks[-1] + 1)

    # plot percentiles
    for perc in perc_plot_list:
        perc_str = str(perc)
        perc_vec = df.loc[:, perc_str]
        age_vec = df.loc[:, "Age group"]
        ax.plot(
            age_vec,
            perc_vec,
            color=REF_COLOR,
            alpha=0.1,
            lw=1,
            ls="-",
        )
        ax.text(
            x=age_vec.iloc[-1]+0.5,
            y=perc_vec.iloc[-1],
            s=perc_str,
            alpha=0.5,
        )
    ax.fill_between(
        age_vec,
        df.loc[:, str(10)],
        df.loc[:, str(90)],
        alpha=0.1,
        color=REF_COLOR,
    )
    ax.fill_between(
        age_vec,
        df.loc[:, str(3)],
        df.loc[:, str(97)],
        alpha=0.05,
        color=REF_COLOR,
    )

    return ax
