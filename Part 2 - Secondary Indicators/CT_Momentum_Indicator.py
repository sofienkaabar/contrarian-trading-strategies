
# Choosing the asset
pair = 0

# Time Frame
horizon = 'H1'
lookback = 14

# Importing the asset as an array
my_data = mass_import(pair, horizon)

# Calling the indicator
my_data = momentum_indicator(my_data, lookback, 3, 4)

# Charting the indicator
indicator_plot(my_data, 4, window = 500)
plt.axhline(y = 100,  color = 'black', linestyle = 'dashed', linewidth = 1)

