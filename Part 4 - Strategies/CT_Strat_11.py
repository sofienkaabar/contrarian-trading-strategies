
# Choosing the asset
pair = 0

# Time Frame
horizon = 'H1'
lookback = 14
upper_barrier = 70
lower_barrier = 30
width = 40

# Importing the asset as an array
my_data = mass_import(pair, horizon)

# Calling the indicator
my_data = rsi(my_data, lookback, 3, 4)
my_data = double_top_bottom(my_data, 4, lower_barrier, upper_barrier, width, 5, 6)

# Charting the latest signals
signal_chart_indicator_plot(my_data, 0, 4, 5, 6, barriers = True, window = 500)

# Performance
my_data = performance(my_data, 0, 5, 6, 7, 8, 9)


