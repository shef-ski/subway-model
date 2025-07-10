from matplotlib import pyplot as plt


def utilization_histogram(
    data_dict,
    bins=50,
    title="Distribution from Dictionary",
    xlabel="Value",
    ylabel="Frequency",
):
    """
    Plots the distribution of float values from a dictionary as histograms.
    The dictionary keys are used as labels.

    Args:
        data_dict (dict): A dictionary where keys are integers (used as labels)
                          and values are lists of float values. Expected to have 4 entries.
        bins (int, optional): The number of bins for the histograms. Defaults to 50.
        title (str, optional): The title of the plot. Defaults to 'Distribution from Dictionary'.
        xlabel (str, optional): The label for the x-axis. Defaults to 'Value'.
        ylabel (str, optional): The label for the y-axis. Defaults to 'Frequency'.
    """
    if not isinstance(data_dict, dict) or len(data_dict) != 4:
        raise ValueError(
            "Input must be a dictionary containing exactly four key-value pairs."
        )

    # Ensure keys are integers (or can be clearly represented as labels)
    # and values are lists of numbers
    for key, sublist in data_dict.items():
        if not isinstance(key, int):
            print(
                f"Warning: Key '{key}' is not an integer. It will be converted to string for the label."
            )
        if not isinstance(sublist, list) or not all(
            isinstance(item, (int, float)) for item in sublist
        ):
            raise ValueError(f"The value for key '{key}' must be a list of numbers.")

    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]  # Standard matplotlib colors

    plt.figure(figsize=(12, 7))  # Adjust figure size as needed

    # Iterate through dictionary items, using an index for color selection
    for i, (key, sublist_data) in enumerate(data_dict.items()):
        label = str(key)  # Use the dictionary key as the label
        plt.hist(
            sublist_data,
            bins=bins,
            color=colors[i % len(colors)],
            alpha=0.7,
            label=label,
            density=True,
        )
        # Using density=True normalizes the histograms.
        # If you want raw counts, set density=False.

    plt.title(title, fontsize=16)
    plt.xlabel(xlabel, fontsize=14)
    plt.ylabel(ylabel, fontsize=14)
    plt.legend(
        title="Labels (Keys)", fontsize=12
    )  # Add a title to the legend if desired
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()  # Adjusts plot to ensure everything fits without overlapping
    plt.show()
