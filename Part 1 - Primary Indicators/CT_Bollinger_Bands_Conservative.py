
# Choosing the asset
pair = 0

# Time Frame
horizon = 'H1'
lookback = 20
standard_deviation = 2

# Importing the asset as an array
my_data = mass_import(pair, horizon)

# Calling the indicator
my_data = bollinger_bands(my_data, lookback, standard_deviation, 3, 4)

# Creating the signal function
def signal(data, close, middle_boll, upper_boll, lower_boll, buy, sell):
 
    data = add_column(data, 10)
    
    for i in range(len(data)):   
        
        try:
            
            # Bullish signal
            if data[i, close] > data[i, lower_boll] and data[i - 1, close] < data[i - 1, lower_boll] and \
               data[i, close] < data[i, middle_boll]:
                
                data[i + 1, buy] = 1
                     
            # Bearish signal
            elif data[i, close] < data[i, upper_boll] and data[i - 1, close] > data[i - 1, upper_boll]  and \
                 data[i, close] > data[i, middle_boll]:
                
                data[i + 1, sell] = -1
                
        except IndexError:
                 
            pass
         
    return data

# Calling the signal function
my_data = signal(my_data, 3, 4, 5, 6, 7, 8)

# Charting the latest signals
signal_chart(my_data, 0, 7, 8, genre = 'bars', window = 250)
plt.plot(my_data[-250:, 4], color = 'grey', linestyle = 'dashed')
plt.plot(my_data[-250:, 5], color = 'blue')
plt.plot(my_data[-250:, 6], color = 'purple')

# Performance
my_data = performance(my_data, 0, 7, 8, 9, 10, 11)


