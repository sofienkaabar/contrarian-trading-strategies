
# Choosing the asset
pair = 0

# Time Frame
horizon = 'H1'
lookback = 10
multiplier = 2

# Importing the asset as an array
my_data = mass_import(pair, horizon)

# Calling the indicator
my_data = keltner_channel(my_data, lookback, multiplier, 3, 4)

# Creating the signal function
def signal(data, high, low, upper_kc, lower_kc, buy, sell):

    data = add_column(data, 10)    
    
    for i in range(len(data)):  
        
       try:
           
           # Bullish signal
           if data[i, low] < data[i - 1, lower_kc] and data[i - 1, low] > data[i - 1, lower_kc]:
                  
                    data[i, buy] = 1 
                    
           # Bearish signal
           elif data[i, high] > data[i - 1, upper_kc] and data[i - 1, high] < data[i - 1, upper_kc]:
                  
                    data[i, sell] = -1 
                    
       except IndexError:
            
            pass
        
    return data

# Calling the signal function
my_data = signal(my_data, 1, 2, 4, 5, 6, 7)

# Charting the latest signals
signal_chart(my_data, 0, 6, 7, genre = 'bars', window = 250)
plt.plot(my_data[-250:, 4], color = 'blue')
plt.plot(my_data[-250:, 5], color = 'brown')

def performance_kc(data, 
                 open_price, 
                 buy_column, 
                 sell_column, 
                 long_result_col, 
                 short_result_col, 
                 total_result_col):
    
    # Variable holding period
    for i in range(len(data)):
        
        try:
            
            if data[i, buy_column] == 1:
                
                for a in range(i + 1, i + 1000):
                    
                    if data[a, sell_column] == -1:
                        
                        data[a, long_result_col] = data[a, 4] - data[i, 5]
                        
                        break
                    
                    if data[a, buy_column] == 1:
                        
                        data[a, long_result_col] = data[i, 5] - data[a, 5]
                        
                        break

                    else:                        
                        
                        continue                
                    
            else:
                
                continue
            
        except IndexError:
            
            pass
                    
    for i in range(len(data)):
        
        try:
            
            if data[i, sell_column] == -1:
                
                for a in range(i + 1, i + 1000):
                                        
                    if data[a, buy_column] == 1:
                        
                        data[a, short_result_col] = data[i, 5] - data[a, 4]
                        
                        break   
                     
                    if data[a, sell_column] == -1:
                        
                        data[a, short_result_col] = data[i, 4] - data[a, 4]
                        
                        break

                    else:                        
                        continue
                    
            else:
                continue
            
        except IndexError:
            
            pass   
        
    # Aggregating the long & short results into one column
    data[:, total_result_col] = data[:, long_result_col] + data[:, short_result_col]  
    
    # Profit factor    
    total_net_profits = data[data[:, total_result_col] > 0, total_result_col]
    total_net_losses  = data[data[:, total_result_col] < 0, total_result_col] 
    total_net_losses  = abs(total_net_losses)
    profit_factor     = round(np.sum(total_net_profits) / np.sum(total_net_losses), 2)

    # Hit ratio    
    hit_ratio         = len(total_net_profits) / (len(total_net_losses) + len(total_net_profits))
    hit_ratio         = hit_ratio * 100
    
    # Risk reward ratio
    average_gain            = total_net_profits.mean()
    average_loss            = total_net_losses.mean()
    realized_risk_reward    = average_gain / average_loss

    # Number of trades
    trades = len(total_net_losses) + len(total_net_profits)
        
    print('Hit Ratio         = ', hit_ratio)
    print('Profit factor     = ', profit_factor) 
    print('Realized RR       = ', round(realized_risk_reward, 3))
    print('Number of Trades  = ', trades)    
   
    return data

# Performance
my_data = performance_kc(my_data, 0, 6, 7, 8, 9, 10)

def signal_chart(data, position, buy_column, sell_column, genre = 'bars', window = 500):   
 
    sample = data[-window:, ]
    
    if genre == 'bars':

        fig, ax = plt.subplots(figsize = (10, 5))
        
        ohlc_plot_bars(data, window)    
    
        for i in range(len(sample)):
            
            if sample[i, buy_column] == 1:
                
                x = i
                y = sample[i - 1, 5]
            
                ax.annotate(' ', xy = (x, y), 
                            arrowprops = dict(width = 9, headlength = 11, headwidth = 11, facecolor = 'green', color = 'green'))
            
            elif sample[i, sell_column] == -1:
                
                x = i
                y = sample[i - 1, 4]
            
                ax.annotate(' ', xy = (x, y), 
                            arrowprops = dict(width = 9, headlength = -11, headwidth = -11, facecolor = 'red', color = 'red'))  

    if genre == 'candles':

        fig, ax = plt.subplots(figsize = (10, 5))
        
        ohlc_plot_candles(data, window)    
    
        for i in range(len(sample)):
            
            if sample[i, buy_column] == 1:
                
                x = i
                y = sample[i, position]
            
                ax.annotate(' ', xy = (x, y), 
                            arrowprops = dict(width = 9, headlength = 11, headwidth = 11, facecolor = 'green', color = 'green'))
            
            elif sample[i, sell_column] == -1:
                
                x = i
                y = sample[i, position]
            
                ax.annotate(' ', xy = (x, y), 
                            arrowprops = dict(width = 9, headlength = -11, headwidth = -11, facecolor = 'red', color = 'red'))  
