import pandas as pd
import seaborn as sns
import matplotlib

matplotlib.use("TkAgg")  # Use TkAgg backend for interactive plots
from matplotlib import pyplot as plt


def plot_ridership_by_hour(
    df: pd.DataFrame,
    x: str = "hour_of_day",
    y: str = "estimated_ridership",
    col: str = "day_of_week",
    hue: str = "Month",
) -> None:
    """
    Generate a relational plot of estimated ridership by hour of the day,
    separated by day of the week and colored by month.

    NOTE: Seaborn documentation: https://seaborn.pydata.org/tutorial/relational.html
    The default behavior in seaborn is to aggregate the multiple measurements at each x value by plotting the mean and the 95% confidence interval around the mean:


    Parameters:
    - df (pd.DataFrame): The DataFrame containing the data to plot.
    - x (str): The name of the column to be used for the x-axis (default is "hour_of_day").
    - y (str): The name of the column to be used for the y-axis (default is "estimated_ridership").
    - col (str): The name of the column to create separate plots for each unique value (default is "day_of_week").
    - hue (str): The name of the column to color the lines by (default is "Month").

    Returns:
    - None: This function displays the plot and does not return any value.
    """
    sns.relplot(data=df, x=x, y=y, col=col, hue=hue, kind="line")

    plt.show()


# Load the dataset
df = pd.read_csv("data/line_outputs/Crosstown/direction_estimates.csv")

# Usage:
# plot_ridership_by_hour(df)

if __name__ == "__main__":
    plot_ridership_by_hour(df)
    # # Save the plot to a file
    # plt.savefig("ridership_by_hour.png")
    # print("Plot saved as ridership_by_hour.png")
