
# Choosing the asset
pair = 0

# Time Frame
horizon = 'H1'
lookback = 5
upper_barrier = 75
lower_barrier = 25

# Importing the asset as an array
my_data = mass_import(pair, horizon)

# Calling the indicator
my_data = psychological_levels_scanner(my_data, 3, 4)
my_data = stochastic_oscillator(my_data, 
                             lookback, 
                             1, 
                             2, 
                             3, 
                             5)

# Creating the signal function
def signal(data, psychological_column, stoch_column, buy, sell):

    data = add_column(data, 5)    
    
    for i in range(len(data)):  
        
       try:
           
           # Bullish signal
           if data[i, psychological_column] == 1 and data[i, stoch_column] <= lower_barrier:
                  
                    data[i + 1, buy] = 1 
                    
           # Bearish signal
           elif data[i, psychological_column] == 1 and data[i, stoch_column] >= upper_barrier:
                  
                    data[i + 1, sell] = -1 
                    
       except IndexError:
            
            pass
        
    return data



# Calling the signal function
my_data = signal(my_data, 4, 5, 6, 7)

# Charting the latest signals
signal_chart(my_data, 0, 6, 7, genre = 'bars', window = 500)

# Performance
my_data = performance(my_data, 0, 6, 7, 8, 9, 10)


