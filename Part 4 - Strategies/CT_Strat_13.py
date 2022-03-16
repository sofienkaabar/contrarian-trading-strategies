
# Choosing the asset
pair = 0

# Time Frame
horizon = 'H1'
lookback_rsi = 13
upper_barrier = 70
lower_barrier = 30

# Importing the asset as an array
my_data = mass_import(pair, horizon)

# Calling the indicator
my_data = rsi(my_data, lookback_rsi, 3, 4)
my_data = fibonacci_retracement(my_data, 0.618, 4, upper_barrier, lower_barrier, 5)

# Charting the latest signals
signal_chart_indicator_plot(my_data, 0, 4, 9, 10, barriers = True, window = 500)

# Performance
my_data = performance(my_data, 0, 9, 10, 11, 12, 13)


