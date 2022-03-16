
# Choosing the asset
pair = 8

# Time Frame
horizon = 'H1'
lookback_volatility_short = 20
lookback_volatility_long = 100 
lookback_stoch = 20
lookback_volatility = 30
std = 3
lower_barrier = 20
upper_barrier = 80

# Importing the asset as an array
my_data = mass_import(pair, horizon)

# Calling the indicator
my_data = vama_bands(my_data, lookback_volatility_short, lookback_volatility_long, lookback_volatility, std, 3, 4)
my_data = stochastic_oscillator(my_data, lookback_stoch, 1, 2, 3, 7)

# Creating the signal function
def signal(data, high, low, upper_vama_band, lower_vama_band, stoch_column, buy, sell):

    data = add_column(data, 5)    
    
    for i in range(len(data)):  
        
       try:
           
           # Bullish signal
           if data[i, low] < data[i - 1, lower_vama_band] and data[i - 1, low] > data[i - 1, lower_vama_band] and \
              data[i, stoch_column] < lower_barrier:
                  
                    data[i, buy] = 1 
                    
           # Bearish signal
           elif data[i, high] > data[i - 1, upper_vama_band] and data[i - 1, high] < data[i - 1, upper_vama_band] and \
              data[i, stoch_column] > upper_barrier:
                  
                    data[i, sell] = -1 
                    
       except IndexError:
            
            pass
        
    return data

# Calling the signal function
my_data = signal(my_data, 1, 2, 5, 6, 7, 8, 9)
my_data = delete_column(my_data, 4, 1)

# Charting the latest signals
signal_chart_indicator_plot(my_data, 0, 6, 7, 8, barriers = True, window = 500)

def performance_vama(data, 
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
my_data = performance_vama(my_data, 0, 7, 8, 9, 10, 11)

def signal_chart_indicator_plot(data, 
                                    position, 
                                    second_panel, 
                                    buy_column, 
                                    sell_column, 
                                    barriers = False,  
                                    window = 250):   
 
    fig, ax = plt.subplots(2, figsize = (10, 5))

    sample = data[-window:, ]
    
    for i in range(len(sample)):
        
        ax[0].vlines(x = i, ymin = sample[i, 2], ymax = sample[i, 1], color = 'black', linewidth = 1)  
        
        if sample[i, 3] > sample[i, 0]:
            
            ax[0].vlines(x = i, ymin = sample[i, 0], ymax = sample[i, 3], color = 'black', linewidth = 1)  

        if sample[i, 3] < sample[i, 0]:
            
            ax[0].vlines(x = i, ymin = sample[i, 3], ymax = sample[i, 0], color = 'black', linewidth = 1)  
            
        if sample[i, 3] == sample[i, 0]:
            
            ax[0].vlines(x = i, ymin = sample[i, 3], ymax = sample[i, 0] + 0.00003, color = 'black', linewidth = 1.00)  
            
    ax[0].grid() 
    ax[0].plot(data[-500:, 4], color = 'blue')
    ax[0].plot(data[-500:, 5], color = 'purple')


    for i in range(len(sample)):
        
        if sample[i, buy_column] == 1:
            
            x = i
            y = sample[i - 1, 5]
        
            ax[0].annotate(' ', xy = (x, y), 
                        arrowprops = dict(width = 9, headlength = 11, headwidth = 11, facecolor = 'green', color = 'green'))
        
        elif sample[i, sell_column] == -1:
            
            x = i
            y = sample[i - 1, 4]
        
            ax[0].annotate(' ', xy = (x, y), 
                        arrowprops = dict(width = 9, headlength = -11, headwidth = -11, facecolor = 'red', color = 'red'))  

    ax[1].plot(sample[:, second_panel], color = 'royalblue', linewidth = 1)
    ax[1].grid()
    
    if barriers == True:
        
        plt.axhline(y = lower_barrier, color = 'black', linestyle = 'dashed', linewidth = 1)
        plt.axhline(y = upper_barrier, color = 'black', linestyle = 'dashed', linewidth = 1)



