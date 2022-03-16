
# Choosing the asset
pair = 0

# Time Frame
horizon = 'H1'
width = 60

# Importing the asset as an array
my_data = mass_import(pair, horizon)

# Calling the indicator
my_data = macd(my_data, 3, 26, 12, 9, 4)

def signal(data, macd_line, macd_signal, width, buy, sell):
    
    data = add_column(data, 10)
    
    for i in range(len(data)):
        
        try:
            
            if data[i, macd_line] < data[i, macd_signal] and data[i, macd_line] < 0:
                
                for a in range(i + 1, i + width):
                    
                    if data[a, macd_line] > data[a, macd_signal] and data[a, macd_line] < 0:
                        
                        for r in range(a + 1, a + width):
                            
                            if data[r, macd_line] < data[r, macd_signal] and data[r, macd_line] < 0 and \
                            data[r, macd_line] > data[i, macd_line] and data[r, 3] < data[i, 3]:
                                
                                for s in range(r + 1, r + width):
                                    
                                    if data[s, macd_line] > data[s, macd_signal] and data[s, macd_line] < 0:
                                        
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
            
            if data[i, macd_line] > data[i, macd_signal] and data[i, macd_line] > 0:
                
                for a in range(i + 1, i + width):
                    
                    if data[a, macd_line] < data[a, macd_signal]  and data[a, macd_line] > 0:
                        
                        for r in range(a + 1, a + width):
                            
                            if data[r, macd_line] > data[r, macd_signal] and data[r, macd_line] > 0 and \
                            data[r, macd_line] < data[i, macd_line] and data[r, 3] > data[i, 3]:
                                
                                for s in range(r + 1, r + width):
                                    
                                    if data[s, macd_line] < data[s, macd_signal] and data[s, macd_line] > 0:
                                        
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
my_data = signal(my_data, 4, 5, width, 6, 7)

# Charting the latest signals
signal_chart_indicator_plot(my_data, 0, 4, 6, 7, barriers = False, window = 500)
plt.plot(my_data[-500:, 5], color = 'orange', linewidth = 1)
plt.axhline(y = 0, color = 'black', linestyle = 'dashed', linewidth = 1)

# Performance
my_data = performance(my_data, 0, 6, 7, 8, 9, 10)


