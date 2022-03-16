
# Choosing the asset
pair = 1

# Time Frame
horizon = 'H1'

lookback   = 20
multiplier = 2

# Importing the asset as an array
my_data = mass_import(pair, horizon)

# Calling the indicator
my_data = k_volatility_band(my_data, lookback, multiplier, 1, 2, 3, 4)

# Creating the signal function
def signal(data, close, upper_band, lower_band, buy, sell):
 
    data = add_column(data, 10)
    
    for i in range(len(data)):    
        
        # Bullish signal
        if data[i, close] < data[i, lower_band] and data[i - 1, close] > data[i - 1, lower_band]:
            
            data[i + 1, buy] = 1
                 
        # Bearish signal
        elif data[i, close] > data[i, upper_band] and data[i - 1, close] < data[i - 1, upper_band]:
            
            data[i + 1, sell] = -1
            
    return data

# Calling the signal function
my_data = signal(my_data, 3, 5, 6, 7, 8)

# Charting the latest signals
signal_chart(my_data, 0, 7, 8, genre = 'bars', window = 500)
plt.plot(my_data[-500:, 4], color = 'blue')
plt.plot(my_data[-500:, 5], color = 'orange')
plt.plot(my_data[-500:, 6], color = 'purple')

# Performance
my_data = performance(my_data, 0, 7, 8, 9, 10, 11)
