
# Choosing the asset
pair = 0

# Time Frame
horizon = 'H1'
lookback = 14
lower_barrier = 20
upper_barrier = 80

# Importing the asset as an array
my_data = mass_import(pair, horizon)

# Calling the indicator
psar = sar(my_data, af = 0.02, amax = 0.2)
psar = np.array(psar)
psar = np.reshape(psar, (-1, 1))
my_data = np.concatenate((my_data, psar), axis = 1)
my_data = rsi(my_data, lookback, 4, 5)
my_data = delete_column(my_data, 4, 1)

# Creating the signal function
def signal(data, rsi_column, buy, sell):
 
    data = add_column(data, 10)
    
    for i in range(len(data)):   
        
        try:
            
            # Bullish signal
            if data[i, rsi_column] < lower_barrier and data[i - 1, rsi_column] > lower_barrier:
                
                data[i + 1, buy] = 1
                     
            # Bearish signal
            elif data[i, rsi_column] > upper_barrier and data[i - 1, rsi_column] < upper_barrier:
                
                data[i + 1, sell] = -1
            
        except IndexError:
             
            pass
         
    return data

# Calling the signal function
my_data = signal(my_data, 4, 5, 6)

# Charting the latest signals
signal_chart_indicator_plot(my_data, 0, 4, 5, 6, barriers = True, window = 250)

# Performance
my_data = performance(my_data, 0, 5, 6, 7, 8, 9)



