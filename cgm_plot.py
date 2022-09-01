from typing import Dict, List
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


GLUC_COLOR = "C0"
DIET_COLOR = "brown"
SLEEP_COLOR = "purple"
FONTSIZE = 14


class CGMPlot:
    def __init__(
        self,
        cgm_df: pd.DataFrame,
        diet_df: pd.DataFrame = None,
        cgm_date_col: str = "Date",
        gluc_col: str = "glucose",
        diet_date_col: str = "Date",
        diet_text_col: str = "shortname_eng",
        ax: plt.axes = None,
        smooth: bool = False,
        sleep_tuples=None,
    ) -> None:
        self.cgm_df = cgm_df
        self.diet_df = diet_df
        self.cgm_date_col = cgm_date_col
        self.gluc_col = gluc_col
        self.diet_date_col = diet_date_col
        self.diet_text_col = diet_text_col
        self.smooth = smooth
        self.n_points = len(self.cgm_df[self.gluc_col])
        self.gluc_color = GLUC_COLOR
        self.diet_color = DIET_COLOR
        self.datetime_start = self.cgm_df[self.cgm_date_col].iloc[0]
        self.sleep_tuples = sleep_tuples

        if ax is None:
            fig, ax = plt.subplots(1, 1, figsize=(18, 5))
        self.ax = ax

    def prep_plot(self):
        self.ax.spines["right"].set_visible(False)
        self.ax.spines["top"].set_visible(False)

    def plot_gluc(self):
        ax = self.ax
        y = self.cgm_df[self.gluc_col]
        x = self.cgm_df[self.cgm_date_col]
        if self.smooth:
            # smoothing
            smoothed = (
                self.cgm_df.set_index(self.cgm_date_col)
                .asfreq(freq="60S")
                .interpolate(method="cubicspline")
            )
            ax.plot(
                smoothed.index,
                smoothed[self.gluc_col],
                ls="-",
                lw=4,
                color=self.gluc_color,
                alpha=0.8,
            )
        else:
            ax.plot(x, y, ls="-", lw=4, color=self.gluc_color, alpha=0.9)
        ax.scatter(x, y, s=60, color=self.gluc_color, alpha=0.6, label="Glucose")

    def plot_diet(self):
        ax = self.ax
        x_offset = pd.to_timedelta(-5, "minutes")
        max_y = ax.get_ylim()[1]
        min_y = ax.get_ylim()[0]
        ax.set_ylim(min(60, min_y), max(150, max_y))

        for i, (food_datetime, group) in enumerate(
            self.diet_df.groupby(self.diet_date_col)
        ):
            food_str = "\n".join(group[self.diet_text_col])

            txt_x = food_datetime - pd.to_timedelta(7.5, "m")
            if i % 2 == 0:
                txt_y = max(150, max_y) + 1
                # verticalalignment="bottom"
                horizontalalignment = "center"
            else:
                # txt_y = ax.get_ylim()[0] - 8
                txt_y = max(150, max_y) + 5
                # verticalalignment="top"
                horizontalalignment = "center"

            ax.axvline(food_datetime, color=self.diet_color, alpha=0.5, ls=":")
            ax.scatter(
                x=food_datetime,
                y=max(150, max_y) - 2,
                marker="v",
                s=100,
                color=self.diet_color,
            )
            ax.text(
                x=txt_x,
                y=txt_y,
                s=(food_str),
                color=self.diet_color,
                horizontalalignment=horizontalalignment,
                fontsize=10,
            )

    def plot_sleep(self):
        ax = self.ax
        for sleep_start, sleep_end in self.sleep_tuples:
            ax.fill_between(
                [sleep_start, sleep_end],
                ax.get_ylim()[0],
                ax.get_ylim()[1],
                color=SLEEP_COLOR,
                alpha=0.05,
            )

    def plot(self):
        self.prep_plot()
        self.plot_gluc()
        if self.diet_df is not None:
            self.plot_diet()
        if self.sleep_tuples is not None:
            self.plot_sleep()


class AGP:
    def __init__(
        self,
        cgm_df: pd.DataFrame,
        cgm_date_col: str = "Date",
        gluc_col: str = "glucose",
        ax: plt.axes = None,
    ) -> None:
        self.cgm_df = cgm_df
        self.cgm_date_col = cgm_date_col
        self.gluc_col = gluc_col
        self.gluc_color = GLUC_COLOR

        if ax is None:
            fig, ax = plt.subplots(1, 1, figsize=(18, 5))
        self.ax = ax

        agp_df = (
            cgm_df.set_index("Date")
            .asfreq(freq="60S")
            .interpolate(method="cubicspline")
            .reset_index()
        )
        agp_df["minute_in_day"] = 60 * agp_df.Date.dt.hour + agp_df.Date.dt.minute
        self.agp_df = agp_df

    def plot(self):
        ax = self.ax
        agp_df = self.agp_df
        median = agp_df.groupby("minute_in_day")["glucose"].median()
        lo_5 = agp_df.groupby("minute_in_day")["glucose"].quantile(0.05)
        hi_95 = agp_df.groupby("minute_in_day")["glucose"].quantile(0.95)
        lo_25 = agp_df.groupby("minute_in_day")["glucose"].quantile(0.25)
        hi_75 = agp_df.groupby("minute_in_day")["glucose"].quantile(0.75)

        ax.plot(median, color="k", lw=3)
        ax.fill_between(median.index.values, lo_25, hi_75, color="navy", alpha=0.3)
        ax.fill_between(median.index.values, lo_5, hi_95, color="navy", alpha=0.1)

        xticks = [m for m in median.index.values if m % 180 == 0]
        xticks += [24 * 60]
        xticklabels = [f"{int(m/60)}:00" for m in xticks]
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticklabels)

        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.set_ylabel("Glucose (mg\dL)", fontsize=14)
