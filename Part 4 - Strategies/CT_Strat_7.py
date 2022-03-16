
# Choosing the asset
pair = 0

# Time Frame
horizon = 'H1'
lookback_first_rsi = 14
lookback_second_rsi = 5
lower_barrier = 20
upper_barrier = 80
width = 60

# Importing the asset as an array
my_data = mass_import(pair, horizon)

# Calling the indicator
my_data = rsi(my_data, lookback_first_rsi, 3, 4)
my_data = rsi(my_data, lookback_second_rsi, 4, 5)

# Creating the signal function
my_data = divergence(my_data, 5, lower_barrier, upper_barrier, width, 6, 7)

# Charting the latest signals
signal_chart_indicator_plot(my_data, 0, 5, 6, 7, barriers = True, window = 500)

# Performance
my_data = performance(my_data, 0, 6, 7, 8, 9, 10)


