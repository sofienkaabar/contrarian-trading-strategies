
# Choosing the asset
pair = 0

# Time Frame
horizon = 'H1'
lookback_rsi = 14
lookback_boll = 20
std_lookback  = 2
upper_barrier = 70
lower_barrier = 30

# Importing the asset as an array
my_data = mass_import(pair, horizon)

# Calling the indicator
my_data = rsi(my_data, lookback_rsi, 3, 4)
my_data = bollinger_bands(my_data, lookback_boll, std_lookback, 3, 5)

# Creating the signal function
def signal(data, close, rsi_column, upper_bollinger, lower_bollinger, buy, sell):
    
    data = add_column(data, 10)
    
    for i in range(len(data)):
        
        try:
        
            # Bullish signal
            if data[i, rsi_column] < lower_barrier and data[i - 1, rsi_column] > lower_barrier and \
               data[i, close] < data[i, lower_bollinger]:
                
                data[i + 1, buy] = 1
                     
            # Bearish signal
            elif data[i, rsi_column] > upper_barrier and data[i - 1, rsi_column] < upper_barrier and \
               data[i, close] > data[i, upper_bollinger]:
                
                data[i + 1, sell] = -1
                
        except IndexError:
             
            pass
         
    return data

# Calling the signal function
my_data = signal(my_data, 3, 4, 6, 7, 8, 9)

# Charting the latest signals
signal_chart(my_data, 0, 8, 9, genre = 'bars', window = 500)

# Performance
my_data = performance(my_data, 0, 8, 9, 10, 11, 12)


