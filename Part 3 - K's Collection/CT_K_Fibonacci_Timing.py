
# Choosing the asset
pair = 0

# Time Frame
horizon = 'H1'

count      = 8
step       = 5
step_two   = 3

# Importing the asset as an array
my_data = mass_import(pair, horizon)

# Calling the indicator
my_data = k_fibonacci_timing_pattern(my_data, 
                                count, 
                                step, 
                                step_two, 
                                3, 
                                4, 
                                5)

# Creating the signal function
def signal(data, close, buy_pattern, sell_pattern, buy, sell):
 
    data = add_column(data, 10)
    
    for i in range(len(data)):    
        
        # Bullish signal
        if data[i, buy_pattern] == -count and data[i, close] < data[i - 1, close]:
            
            data[i + 1, buy] = 1
                 
        # Bearish signal
        elif data[i, sell_pattern] == count and data[i, close] > data[i - 1, close]:
            
            data[i + 1, sell] = -1
            
    return data

# Calling the signal function
my_data = signal(my_data, 3, 4, 5, 6, 7)

# Charting the latest signals
signal_chart(my_data, 0, 6, 7, genre = 'bars', window = 500)

# Performance
my_data = performance(my_data, 0, 6, 7, 8, 9, 10)
