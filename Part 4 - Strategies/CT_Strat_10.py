
# Choosing the asset
pair = 0

# Time Frame
horizon = 'H1'

# Importing the asset as an array
my_data = mass_import(pair, horizon)

# Calling the indicator
my_data = rob_booker_reversal(my_data, 1, 2, 3, 4, 6, 7)

# Charting the latest signals
signal_chart(my_data, 0, 6, 7, genre = 'bars', window = 500)

# Performance
my_data = performance(my_data, 0, 6, 7, 8, 9, 10)


