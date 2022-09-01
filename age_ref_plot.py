from typing import Dict, List
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

REF_COLOR = "k"
FEMALE_COLOR = "C1"
MALE_COLOR = "C0"
ALL_COLOR = "C5"

GLUC_COLOR = "C0"
FOOD_COLOR = "C1"


def plot_age_ref(ax=None):
    if ax is None:
        fig, ax = plt.subplots(1,1,figsize=(8,5))

    # prep ax
    age_bins = np.arange(35, 75, 1)
    min_age = age_bins[0]
    max_age = age_bins[-1]
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.set_xlabel("Age")
    xticks = (np.sort(np.unique(np.floor(age_bins / 10) * 10))).astype(int)
    xticks = np.append(xticks, xticks[-1] + 10)
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticks)
    ax.set_xlim(xticks[0], xticks[-1] + 1)