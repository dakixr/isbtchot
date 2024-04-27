import pandas as pd
from isbtchot.model import btc_power_law
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter, NullFormatter


df = btc_power_law()
df["delta"] = df.price / df.power_law


# Plotting the data
plt.figure(figsize=(10, 6))

# Plot both 'price' and 'power_law' on a log-log scale
plt.plot(df['days'], df['price'], label='Price')
plt.plot(df['days'], df['power_law'], label='Power Law')
plt.plot(df['days'], df['power_law_bottom'], label='Power Law Bottom')
plt.plot(df['days'], df['power_law_top'], label='Power Law Top')

# Setting log scale for both x and y axis
plt.xscale('log')
plt.yscale('log')

# Find the date range
date_range = pd.date_range(start=df.index.min(), end=df.index.max(), freq='4YS')

# Calculate the number of days since the start for each year start
xticks_yearly = [(date - df.index.min()).days for date in date_range]

# Generate yearly labels from the date_range
xticklabels_yearly = [date.strftime('%Y') for date in date_range]

# Setting ticks on the x-axis to correspond to the start of each year
plt.xticks(ticks=xticks_yearly, labels=xticklabels_yearly, rotation=45, ha='right')

# Setting the axis labels
plt.xlabel('Year')
plt.ylabel('Price ($)')

# Set the formatter for the y-axis to plain (no scientific notation)
plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:.0f}'))
plt.gca().yaxis.set_minor_formatter(NullFormatter())

# Adding legend and grid
plt.legend()
plt.grid(True, which="both", ls="--")

# Adding limits
plt.xlim(left=500)
plt.ylim(bottom=0.01)

# Show the plot
plt.tight_layout()  # Adjust the padding between and around subplots.
plt.show()