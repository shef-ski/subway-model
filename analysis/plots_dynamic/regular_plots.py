from matplotlib import pyplot as plt
import pandas as pd


def create_basic_plot(results):

    # Create a DataFrame from the results
    df=pd.DataFrame(results)

    # Visualize the results - simple plot
    df.plot()

    plt.title("Utilization rates")
    plt.xlabel('Simulations')
    plt.ylabel('Utilization rate (ranging from 0 to 1)') 

    plt.legend(title='Maximum train capacity'#, loc='upper left'
            ) 
    plt.show()


