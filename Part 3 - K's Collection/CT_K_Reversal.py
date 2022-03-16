
# Choosing the asset
pair = 0

# Time Frame
horizon = 'H1'
lookback = 100
standard_deviation = 2

# Importing the asset as an array
my_data = mass_import(pair, horizon)

# Calling the indicator
my_data = k_reversal_indicator(my_data, lookback, standard_deviation, 3, 4)

# Creating the signal function
def signal(data, open_price, close, upper_boll, lower_boll, macd_col, signal_col, buy, sell):
 
    data = add_column(data, 10)
    
    for i in range(len(data)):    
        
        # Bullish signal
        if min(data[i, open_price], data[i, close]) < data[i, lower_boll] and data[i, macd_col] > \
           data[i, signal_col] and data[i - 1, macd_col] < data[i - 1, signal_col]:
            
            data[i + 1, buy] = 1
                 
        # Bearish signal
        elif max(data[i, open_price], data[i, close]) > data[i, upper_boll] and data[i, macd_col] < \
           data[i, signal_col] and data[i - 1, macd_col] > data[i - 1, signal_col]:
            
            data[i + 1, sell] = -1
            
    return data

# Calling the signal function
my_data = signal(my_data, 0, 3, 5, 6, 7, 8, 9, 10)

# Charting the latest signals
signal_chart(my_data, 0, 9, 10, genre = 'bars', window = 1000)

# Performance
my_data = performance(my_data, 0, 9, 10, 11, 12, 13)
