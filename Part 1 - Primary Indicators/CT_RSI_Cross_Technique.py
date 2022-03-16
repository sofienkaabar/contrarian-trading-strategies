
# Choosing the asset
pair = 0

# Time Frame
horizon = 'H1'
lookback_rsi = 14
lookback_ma = 9
lower_barrier = 30
upper_barrier = 70

# Importing the asset as an array
my_data = mass_import(pair, horizon)

# Calling the indicator
my_data = rsi(my_data, lookback_rsi, 3, 4)
my_data = ma(my_data, lookback_ma, 4, 5)

# Creating the signal function
def signal(data, rsi_column, ma_column, buy, sell):
 
    data = add_column(data, 10)
    
    for i in range(len(data)):    
        
        try:
        
            # Bullish signal
            if data[i, rsi_column] > data[i, ma_column] and data[i - 1, rsi_column] < data[i - 1, ma_column] and \
               data[i, rsi_column] < 50:
                   
                data[i + 1, buy] = 1
                     
            # Bearish signal
            elif data[i, rsi_column] < data[i, ma_column] and data[i - 1, rsi_column] > data[i - 1, ma_column] and \
                 data[i, rsi_column] > 50:
                            
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


