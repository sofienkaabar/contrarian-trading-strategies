
# Choosing the asset
pair = 0

# Time Frame
horizon = 'H1'
lookback = 20
standard_deviation = 2
lower_barrier = 0
upper_barrier = 1
width = 60

# Importing the asset as an array
my_data = mass_import(pair, horizon)

# Calling the indicator
my_data = bollinger_bands(my_data, lookback, standard_deviation, 3, 4)
my_data = bollinger_percentage_bands(my_data, 3, 5, 6, 7)

# Creating the signal function
def divergence(data, indicator, lower_barrier, upper_barrier, width, buy, sell):
    data = add_column(data, 10)
    for i in range(len(data)):
        try:
            if data[i, indicator] < lower_barrier:
                for a in range(i + 1, i + width):
                    if data[a, indicator] > lower_barrier and data[a, indicator] < upper_barrier:
                        for r in range(a + 1, a + width):
                            if data[r, indicator] < lower_barrier and \
                            data[r, indicator] > data[i, indicator] and data[r, 3] < data[i, 3]:
                                for s in range(r + 1, r + width):
                                    if data[s, indicator] > lower_barrier:
                                        data[s + 1, buy] = 1
                                        break
                                    else:
                                        break
                            else:
                                break
                        else:
                            break
                    else:
                        break
        except IndexError:
            pass
    for i in range(len(data)):
        try:
            if data[i, indicator] > upper_barrier:
                for a in range(i + 1, i + width):
                    if data[a, indicator] < upper_barrier  and data[a, indicator] > lower_barrier:
                        for r in range(a + 1, a + width):
                            if data[r, indicator] > upper_barrier and \
                            data[r, indicator] < data[i, indicator] and data[r, 3] > data[i, 3]:
                                for s in range(r + 1, r + width):
                                    if data[s, indicator] < upper_barrier:
                                        data[s + 1, sell] = -1
                                        break
                                    else:
                                        break
                            else:
                                break
                        else:
                            break
                    else:
                        break
        except IndexError:
            pass 
    return data

# Calling the signal function
my_data = divergence(my_data, 7, lower_barrier, upper_barrier, width, 8, 9)

# Charting the latest signals
signal_chart_indicator_plot(my_data, 0, 7, 8, 9, barriers = True, window = 250)

# Performance
my_data = performance(my_data, 0, 8, 9, 10, 11, 12)


