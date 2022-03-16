
# Choosing the asset
pair = 0

# Time Frame
horizon = 'H1'
lookback = 20
lookback_trend = 100

# Importing the asset as an array
my_data = mass_import(pair, horizon)

# Calling the indicator
my_data = mandi(my_data, lookback, lookback_trend, 3, 4)

# Creating the signal function
def signal(data, close, ma_column, mandi_column, trend_column, buy, sell):
    
    data = add_column(data, 10)
    
    for i in range(len(data)):    
        
        try:
        
            # Bullish signal
            if data[i, mandi_column] == 100 and data[i - 1, mandi_column] < 100 and \
               data[i, close] > data[i, trend_column] and data[i, close] < data[i, ma_column]:
                
                data[i + 1, buy] = 1
                     
            # Bearish signal
            elif data[i, mandi_column] == 100 and data[i - 1, mandi_column] < 100 and \
                 data[i, close] < data[i, trend_column] and data[i, close] > data[i, ma_column]:
                
                data[i + 1, sell] = -1
            
        except IndexError:
             
            pass
         
    return data

# Calling the signal function
my_data = signal(my_data, 3, 4, 5, 6, 7, 8)

# Charting the latest signals
signal_chart_indicator_plot(my_data, 0, 5, 7, 8, barriers = False, window = 500)

# Performance
my_data = performance(my_data, 0, 7, 8, 9, 10, 11)


