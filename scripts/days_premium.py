from isbtchot.model import btc_power_law
import numpy as np
import matplotlib.pyplot as plt

# Assuming btc_power_law is a function that returns a DataFrame.
df = btc_power_law()
prices = df["price"].values
power_law_bottoms = df["power_law_bottom"].values
dates = df.index.to_series().reset_index(drop=True)
days_premium = np.full(df.shape[0], np.nan)
price_went_below = np.full(df.shape[0], False)

# Avoid nested loops by processing in a more efficient manner
for i in range(len(prices)):
    curr_price = prices[i]

    condition_met = np.where(curr_price - power_law_bottoms[i:] < 0)[0]
    if condition_met.size > 0:
        first_met_index = condition_met[0] + i
        days_premium[i] = (dates[first_met_index] - dates[i]).days
        # days_premium_price = power_law_bottoms[first_met_index]

    condition_met = np.where(prices[i:] / power_law_bottoms[i:] < 1.1)[0]
    if condition_met.size > 0:
        first_met_index = condition_met[0] + i
        price_went_below[i] = curr_price > prices[first_met_index]


df["days_premium"] = days_premium
df["extension_from_power_law_bottom"] = (df["price"] / df["power_law_bottom"]) - 1
df["price_went_below"] = price_went_below

# Assuming df is predefined and has been cleaned up as per your provided script
df = df.dropna(
    subset=["days_premium", "extension_from_power_law_bottom", "price_went_below"]
)
price_went_below_false = df[df["price_went_below"] == False]

plt.figure(figsize=(14, 8))  # Larger figure size for better visibility

# Adjusting the opacity and edge color of the main data points
plt.scatter(
    price_went_below_false.index,
    price_went_below_false["days_premium"],
    label="Days Premium (Price Never Went Below)",
    color="green",
    edgecolor="black",
    s=50,  # Smaller markers for a clearer view
    alpha=0.6,  # Adjusting transparency for less dense appearance
)

# The main line plot for days premium with reduced opacity
plt.plot(
    df.index,
    df["days_premium"],
    label="Days Premium - All Data",
    color="grey",
    alpha=0.4,
)

# Adding a distinct marker for the last value in the days_premium series
last_index = df.index[-1]  # Getting the last index
last_days_premium = df["days_premium"].iloc[
    -1
]  # Getting the last value of days_premium

plt.scatter(
    [last_index],
    [last_days_premium],
    color="red",  # A distinct color for the last point
    edgecolor="black",
    s=100,  # Larger size for visibility
    label=f"Current Days Premium: {int(last_days_premium)}",
    zorder=5,  # Ensuring the dot is on top of other elements
)

# Adding labels with increased font size for better readability
plt.xlabel("Years", fontsize=14)
plt.ylabel("Days Premium", fontsize=14)

# Adding a title with increased font size
plt.title("Visual Analysis of Days Premium and Price Went Below Status", fontsize=16)

# Adjust the tick parameters for better visibility
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

# Enable grid, but make it lighter and less obtrusive
plt.grid(True, which="both", linestyle="--", linewidth=0.5, color="gainsboro")

# Opt for a tight layout to use space effectively
plt.tight_layout()

# Show the legend with an updated location to prevent blocking data points
plt.legend(loc="upper left")

# Show the plot
plt.show()
