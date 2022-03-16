
# Choosing the asset
pair = 0

# Time Frame
horizon = 'H1'
lookback_fisher = 14
lookback_rsi = 5
lower_barrier = 15
upper_barrier = 85

# Importing the asset as an array
my_data = mass_import(pair, horizon)

# Calling the indicator
my_data = fisher_transform(my_data, lookback_fisher, 1, 2, 3, 4)
my_data = rsi(my_data, lookback_rsi, 4, 5)

# Creating the signal function
def signal(data, fisher_rsi_column, buy, sell):
    
    data = add_column(data, 10)
    
    for i in range(len(data)):    
        
        # Bullish signal
        if data[i, fisher_rsi_column] < lower_barrier and data[i - 1, fisher_rsi_column] > lower_barrier:
            
            data[i + 1, buy] = 1
                 
        # Bearish signal
        elif data[i, fisher_rsi_column] > upper_barrier and data[i - 1, fisher_rsi_column] < upper_barrier:
            
            data[i + 1, sell] = -1
            
    return data

# Calling the signal function
my_data = signal(my_data, 5, 6, 7)

# Charting the latest signals
signal_chart_indicator_plot(my_data, 0, 5, 6, 7, barriers = True, window = 500)

# Performance
my_data = performance(my_data, 0, 6, 7, 8, 9, 10)


