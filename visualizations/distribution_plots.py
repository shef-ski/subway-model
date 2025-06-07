# compare utilization rates in 5 simulations
import seaborn as sns
from matplotlib import pyplot as plt


def create_distribution_plot(df):
    """Create a joint plot with distributions"""

    sns.jointplot(df, 
                #   kind="kde"
                )
    plt.show()

