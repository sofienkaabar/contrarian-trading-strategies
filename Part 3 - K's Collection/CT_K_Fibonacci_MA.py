
# Choosing the asset
pair = 4

# Time Frame
horizon = 'H1'

# Importing the asset as an array
my_data = mass_import(pair, horizon)

# Calling the indicator
my_data = fma(my_data, 4)

# Creating the signal function
def signal(data, high, low, close, upper_ma, lower_ma, buy, sell):
 
    data = add_column(data, 10)
    
    for i in range(len(data)):
        
        if data[i, low] < data[i, upper_ma] and data[i, low] > data[i, lower_ma] and data[i - 1, low] > \
           data[i - 1, upper_ma] and data[i, close] < data[i, upper_ma] and data[i, buy] == 0:
               
               data[i + 1, buy] = 1

        elif data[i, high] < data[i, upper_ma] and data[i, high] > data[i, lower_ma] and data[i - 1, high] < \
             data[i - 1, lower_ma] and data[i, close] > data[i, lower_ma] and data[i, sell] == 0:
               
               data[i + 1, sell] = -1
               
    return data

# Calling the signal function
my_data = signal(my_data, 1, 2, 3, 4, 5, 6, 7)

# Charting the latest signals
signal_chart(my_data, 0, 6, 7, genre = 'bars', window = 500)
plt.plot(my_data[-500:, 4])
plt.plot(my_data[-500:, 5])

# Performance
my_data = performance(my_data, 0, 6, 7, 8, 9, 10)
