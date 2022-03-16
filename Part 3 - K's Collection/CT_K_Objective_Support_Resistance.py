
# Choosing the asset
pair = 2

# Time Frame
horizon = 'H1'

lookback = 144
lower_range = 0.05

# Importing the asset as an array
my_data = mass_import(pair, horizon)

# Calling the indicator
my_data = k_objective_support_resistance(my_data, lookback, lower_range, 1, 2, 4)

# Creating the signal function
def signal(data, close, k_support, k_resistance, buy, sell):
 
    data = add_column(data, 10)
    
    for i in range(len(data)):    
        
        try:    
            
            # Bullish signal
            if data[i, close] > data[i, k_support] and data[i - 1, close] < data[i - 1, k_support]:
                
                data[i + 1, buy] = 1
                     
            # Bearish signal
            elif data[i, close] < data[i, k_resistance] and data[i - 1, close] > data[i - 1, k_resistance]:
                
                data[i + 1, sell] = -1
            
        except IndexError:
             
            pass
         
    return data

# Calling the signal function
my_data = signal(my_data, 3, 5, 6, 7, 8)

# Charting the latest signals
signal_chart(my_data, 0, 7, 8, genre = 'bars', window = 500)
plt.plot(my_data[-500:, 5])
plt.plot(my_data[-500:, 6])

# Performance
my_data = performance(my_data, 0, 7, 8, 9, 10, 11)
