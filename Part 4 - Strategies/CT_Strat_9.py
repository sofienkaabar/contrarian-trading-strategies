
# Choosing the asset
pair = 0

# Time Frame
horizon = 'H1'
lookback_slope = 14
lookback_rsi   = 14
upper_barrier  = 70
lower_barrier  = 30

# Importing the asset as an array
my_data = mass_import(pair, horizon)

# Calling the indicator
my_data = bounded_slope_indicator(my_data, lookback_slope, lookback_rsi, 3, 4)

# Creating the signal function
def signal(data, bsi_column, buy, sell):
    
    data = add_column(data, 10)
    
    for i in range(len(data)):    
        
        try:
        
            # Bullish signal
            if data[i, bsi_column] > lower_barrier and data[i - 1, bsi_column] < lower_barrier:
                
                data[i + 1, buy] = 1
                     
            # Bearish signal
            elif data[i, bsi_column] < upper_barrier and data[i - 1, bsi_column] > upper_barrier:
                
                data[i + 1, sell] = -1
            
        except IndexError:
             
            pass
         
    return data

# Calling the signal function
my_data = signal(my_data, 5, 6, 7)

# Charting the latest signals
signal_chart_indicator_plot(my_data, 0, 5, 6, 7, barriers = True, window = 500)

# Performance
my_data = performance(my_data, 0, 6, 7, 8, 9, 10)


