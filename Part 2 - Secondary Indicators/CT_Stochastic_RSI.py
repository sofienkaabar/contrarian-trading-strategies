
# Choosing the asset
pair = 0

# Time Frame
horizon = 'H1'
lookback_rsi = 14
lookback_stoch = 14
lower_barrier = 5
upper_barrier = 95

# Importing the asset as an array
my_data = mass_import(pair, horizon)

# Calling the indicator
my_data = stochastic_rsi(my_data, lookback_rsi, lookback_stoch, 3, 4, slowing_period = 3, smoothing_period = 3)

# Creating the signal function
def signal(data, stoch_rsi_column, buy, sell):
 
    data = add_column(data, 10)
    
    for i in range(len(data)):   
        
        try:
            
            # Bullish signal
            if data[i, stoch_rsi_column] < lower_barrier and data[i - 1, stoch_rsi_column] > lower_barrier:
                
                data[i + 1, buy] = 1
                     
            # Bearish signal
            elif data[i, stoch_rsi_column] > upper_barrier and data[i - 1, stoch_rsi_column] < upper_barrier:
                
                data[i + 1, sell] = -1
                
        except IndexError:
             
            pass
         
    return data

# Calling the signal function
my_data = signal(my_data, 6, 7, 8)

# Charting the latest signals
signal_chart_indicator_plot(my_data, 0, 5, 7, 8, barriers = True, window = 250)
plt.plot(my_data[-250:, 6], color = 'orange', linewidth = 1)

# Performance
my_data = performance(my_data, 0, 7, 8, 9, 10, 11)



