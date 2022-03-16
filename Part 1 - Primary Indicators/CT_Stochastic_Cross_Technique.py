
# Choosing the asset
pair = 5

# Time Frame
horizon = 'H1'
lookback = 14
lookback_ma = 9
lower_barrier = 20
upper_barrier = 80

# Importing the asset as an array
my_data = mass_import(pair, horizon)

# Calling the indicator
my_data = stochastic_oscillator(my_data, lookback, 1, 2, 3, 4, slowing = True, 
                                smoothing = True, smoothing_period = 3, slowing_period = 3)
my_data = delete_column(my_data, 4, 1)

# Creating the signal function
def signal(data, stoch_column, ma_column, buy, sell):
 
    data = add_column(data, 10)
    
    for i in range(len(data)):   
        
        try:
            
            # Bullish signal
            if data[i, stoch_column] > data[i, ma_column] and data[i - 1, stoch_column] < data[i - 1, ma_column] and \
               data[i, stoch_column] < lower_barrier:
                   
                data[i + 1, buy] = 1
                     
            # Bearish signal
            elif data[i, stoch_column] < data[i, ma_column] and data[i - 1, stoch_column] > data[i - 1, ma_column] and \
                 data[i, stoch_column] > upper_barrier:
                            
                data[i + 1, sell] = -1
                
        except IndexError:
             
            pass
         
    return data

# Calling the signal function
my_data = signal(my_data, 4, 5, 6, 7)

# Charting the latest signals
signal_chart_indicator_plot(my_data, 0, 4, 6, 7, barriers = True, window = 250)
plt.plot(my_data[-250:, 5], color = 'orange', linewidth = 1)

# Performance
my_data = performance(my_data, 0, 6, 7, 8, 9, 10)



