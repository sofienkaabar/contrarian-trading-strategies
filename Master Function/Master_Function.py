import datetime
import pytz
import pandas                    as pd
import MetaTrader5               as mt5
import matplotlib.pyplot         as plt
import numpy                     as np

frame_H1   = mt5.TIMEFRAME_H1
frame_D1   = mt5.TIMEFRAME_D1

now = datetime.datetime.now()

assets = ['EURUSD', 'USDCHF', 'GBPUSD', 'AUDUSD', 'USDCAD', 'XAUUSD', 'XAGUSD', 'NI225', 'SP500m'] 
     
def mass_import(asset, time_frame):
                
    if time_frame == 'H1':
        data = get_quotes(frame_H1, 2020, 1, 1, asset = assets[asset])
        data = data.iloc[:, 1:5].values
        data = data.round(decimals = 5)        
        
    if time_frame == 'D1':
        data = get_quotes(frame_D1, 2000, 1, 1, asset = assets[asset])
        data = data.iloc[:, 1:5].values
        data = data.round(decimals = 5)        
          
    return data 

def get_quotes(time_frame, year = 2005, month = 1, day = 1, asset = "EURUSD"):
        
    if not mt5.initialize():
        
        print("initialize() failed, error code =", mt5.last_error())
        
        quit()
    
    timezone = pytz.timezone("Europe/Paris")
    
    time_from = datetime.datetime(year, month, day, tzinfo = timezone)
    
    time_to = datetime.datetime.now(timezone) + datetime.timedelta(days=1)
    
    rates = mt5.copy_rates_range(asset, time_frame, time_from, time_to)
    
    rates_frame = pd.DataFrame(rates)

    return rates_frame

def performance(data, 
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
                    
                    if data[a, buy_column] == 1 or data[a, sell_column] == -1:
                        
                        data[a, long_result_col] = data[a, open_price] - data[i, open_price]
                        
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
                                        
                    if data[a, buy_column] == 1 or data[a, sell_column] == -1:
                        
                        data[a, short_result_col] = data[i, open_price] - data[a, open_price]
                        
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

def add_column(data, times):
    
    for i in range(1, times + 1):
    
        new = np.zeros((len(data), 1), dtype = float)
        
        data = np.append(data, new, axis = 1)

    return data

def delete_column(data, index, times):
    
    for i in range(1, times + 1):
    
        data = np.delete(data, index, axis = 1)

    return data

def delete_row(data, number):
    
    data = data[number:, ]
    
    return data

def rounding(data, how_far):
    
    data = data.round(decimals = how_far)
    
    return data

def ma(data, lookback, close, position): 
    
    data = add_column(data, 1)
    
    for i in range(len(data)):
           
            try:
                
                data[i, position] = (data[i - lookback + 1:i + 1, close].mean())
            
            except IndexError:
                
                pass
            
    data = delete_row(data, lookback)
    
    return data

def ema(data, alpha, lookback, close, position):
    
    alpha = alpha / (lookback + 1.0)
    
    beta  = 1 - alpha
    
    data = ma(data, lookback, close, position)

    data[lookback + 1, position] = (data[lookback + 1, close] * alpha) + (data[lookback, position] * beta)

    for i in range(lookback + 2, len(data)):
        
            try:
                
                data[i, position] = (data[i, close] * alpha) + (data[i - 1, position] * beta)
        
            except IndexError:
                
                pass
            
    return data 

def smoothed_ma(data, alpha, lookback, close, position):
    
    lookback = (2 * lookback) - 1
    
    alpha = alpha / (lookback + 1.0)
    
    beta  = 1 - alpha
    
    data = ma(data, lookback, close, position)

    data[lookback + 1, position] = (data[lookback + 1, close] * alpha) + (data[lookback, position] * beta)

    for i in range(lookback + 2, len(data)):
        
            try:
                
                data[i, position] = (data[i, close] * alpha) + (data[i - 1, position] * beta)
        
            except IndexError:
                
                pass
            
    return data

def volatility(data, lookback, close, position):
    
    data = add_column(data, 1)
    
    for i in range(len(data)):
        
        try:
            
            data[i, position] = (data[i - lookback + 1:i + 1, close].std())
    
        except IndexError:
            
            pass
     
    data = delete_row(data, lookback)    
     
    return data

def atr(data, lookback, high, low, close, position):
    
    data = add_column(data, 1)
      
    for i in range(len(data)):
        
        try:
            
            data[i, position] = max(data[i, high] - data[i, low], abs(data[i, high] - data[i - 1, close]), abs(data[i, low]  - data[i - 1, close]))
            
        except ValueError:
            
            pass
        
    data[0, position] = 0   
      
    data = smoothed_ma(data, 2, lookback, position, position + 1)

    data = delete_column(data, position, 1)
    
    data = delete_row(data, lookback)
    
    return data

def ohlc_plot_bars(data, window):
     
    sample = data[-window:, ]
    
    for i in range(len(sample)):
        
        plt.vlines(x = i, ymin = sample[i, 2], ymax = sample[i, 1], color = 'black', linewidth = 1)  
        
        if sample[i, 3] > sample[i, 0]:
            
            plt.vlines(x = i, ymin = sample[i, 0], ymax = sample[i, 3], color = 'black', linewidth = 1)  

        if sample[i, 3] < sample[i, 0]:
            
            plt.vlines(x = i, ymin = sample[i, 3], ymax = sample[i, 0], color = 'black', linewidth = 1)  
            
        if sample[i, 3] == sample[i, 0]:
            
            plt.vlines(x = i, ymin = sample[i, 3], ymax = sample[i, 0] + 0.00003, color = 'black', linewidth = 1.00)  
            
    plt.grid()
    
def ohlc_plot_candles(data, window):
      
    sample = data[-window:, ]
    
    for i in range(len(sample)):
        
        plt.vlines(x = i, ymin = sample[i, 2], ymax = sample[i, 1], color = 'black', linewidth = 1)  
        
        if sample[i, 3] > sample[i, 0]:
            
            plt.vlines(x = i, ymin = sample[i, 0], ymax = sample[i, 3], color = 'green', linewidth = 3)  

        if sample[i, 3] < sample[i, 0]:
            
            plt.vlines(x = i, ymin = sample[i, 3], ymax = sample[i, 0], color = 'red', linewidth = 3)  
            
        if sample[i, 3] == sample[i, 0]:
            
            plt.vlines(x = i, ymin = sample[i, 3], ymax = sample[i, 0] + 0.00003, color = 'black', linewidth = 1.00)  
            
    plt.grid()   

def signal_chart(data, position, buy_column, sell_column, genre = 'bars', window = 500):   
 
    sample = data[-window:, ]
    
    if genre == 'bars':

        fig, ax = plt.subplots(figsize = (10, 5))
        
        ohlc_plot_bars(data, window)    
    
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

def indicator_plot(data, second_panel, window = 250):

    fig, ax = plt.subplots(2, figsize = (10, 5))

    sample = data[-window:, ]
    
    for i in range(len(sample)):
        
        ax[0].vlines(x = i, ymin = sample[i, 2], ymax = sample[i, 1], color = 'black', linewidth = 1)  
        
        if sample[i, 3] > sample[i, 0]:

            ax[0].vlines(x = i, ymin = sample[i, 0], ymax = sample[i, 3], color = 'black', linewidth = 1.5)  

        if sample[i, 3] < sample[i, 0]:
            
            ax[0].vlines(x = i, ymin = sample[i, 3], ymax = sample[i, 0], color = 'black', linewidth = 1.5)  
            
        if sample[i, 3] == sample[i, 0]:
            
            ax[0].vlines(x = i, ymin = sample[i, 3], ymax = sample[i, 0], color = 'black', linewidth = 1.5)  
   
    ax[0].grid() 
     
    ax[1].plot(sample[:, second_panel], color = 'royalblue', linewidth = 1)
    ax[1].grid()

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

    for i in range(len(sample)):
        
        if sample[i, buy_column] == 1:
            
            x = i
            y = sample[i, position]
        
            ax[0].annotate(' ', xy = (x, y), 
                        arrowprops = dict(width = 9, headlength = 11, headwidth = 11, facecolor = 'green', color = 'green'))
        
        elif sample[i, sell_column] == -1:
            
            x = i
            y = sample[i, position]
        
            ax[0].annotate(' ', xy = (x, y), 
                        arrowprops = dict(width = 9, headlength = -11, headwidth = -11, facecolor = 'red', color = 'red'))  

    ax[1].plot(sample[:, second_panel], color = 'royalblue', linewidth = 1)
    ax[1].grid()
    
    if barriers == True:
        
        plt.axhline(y = lower_barrier, color = 'black', linestyle = 'dashed', linewidth = 1)
        plt.axhline(y = upper_barrier, color = 'black', linestyle = 'dashed', linewidth = 1)

def rsi(data, lookback, close, position):
    
    data = add_column(data, 5)
    
    for i in range(len(data)):
        
        data[i, position] = data[i, close] - data[i - 1, close]
     
    for i in range(len(data)):
        
        if data[i, position] > 0:
            
            data[i, position + 1] = data[i, position]
            
        elif data[i, position] < 0:
            
            data[i, position + 2] = abs(data[i, position])
            
    data = smoothed_ma(data, 2, lookback, position + 1, position + 3)
    data = smoothed_ma(data, 2, lookback, position + 2, position + 4)

    data[:, position + 5] = data[:, position + 3] / data[:, position + 4]
    
    data[:, position + 6] = (100 - (100 / (1 + data[:, position + 5])))

    data = delete_column(data, position, 6)
    data = delete_row(data, lookback)

    return data
    
def stochastic_oscillator(data, 
                             lookback, 
                             high, 
                             low, 
                             close, 
                             position, 
                             slowing = False, 
                             smoothing = False, 
                             slowing_period = 1, 
                             smoothing_period = 1):
            
    data = add_column(data, 1)
        
    for i in range(len(data)):
            
        try:
            
            data[i, position] = (data[i, close] - min(data[i - lookback + 1:i + 1, low])) / (max(data[i - lookback + 1:i + 1, high]) - min(data[i - lookback + 1:i + 1, low]))
            
        except ValueError:
            
            pass
        
    data[:, position] = data[:, position] * 100  
            
    if slowing == True and smoothing == False:
        
        data = ma(data, slowing_period, position, position + 1)
    
    if smoothing == True and slowing == False:
        
        data = ma(data, smoothing_period, position, position + 1)
        
    if smoothing == True and slowing == True:
    
        data = ma(data, slowing_period, position,   position + 1)
        
        data = ma(data, smoothing_period, position + 1, position + 2)        
       
    data = delete_row(data, lookback)

    return data

def normalized_index(data, lookback, close, position):
            
    data = add_column(data, 1)
        
    for i in range(len(data)):
            
        try:
            
            data[i, position] = (data[i, close] - min(data[i - lookback + 1:i + 1, close])) / (max(data[i - lookback + 1:i + 1, close]) - min(data[i - lookback + 1:i + 1, close]))
            
        except ValueError:
            
            pass
        
    data[:, position] = data[:, position] * 100  
            
    data = delete_row(data, lookback)

    return data

def fisher_transform(data, lookback, high, low, close, position):
    
   data = add_column(data, 1)
   
   data = stochastic_oscillator(data, lookback, high, low, close, position)
   
   data[:, position] = data[:, position] / 100
   
   data[:, position] = (2 * data[:, position]) - 1
   
   for i in range(len(data)):
       
       if data[i, position] == 1:
           
           data[i, position] = 0.999
           
       if data[i, position] == -1:
           
           data[i, position] = -0.999
           
   for i in range(len(data)):
       
      data[i, position + 1] = 0.5 * (np.log((1 + data[i, position]) / (1 - data[i, position])))
   
   data = delete_column(data, position, 1)   
   
   return data

def momentum_indicator(data, lookback, close, position):
    
    data = add_column(data, 1)
    
    for i in range(len(data)):
        
        data[i, position] = data[i, close] / data[i - lookback, close] * 100       
    
    data = delete_row(data, lookback)
    
    return data

def k_fibonacci_timing_pattern(data, 
                                count, 
                                step, 
                                step_two, 
                                close, 
                                position_long, 
                                position_short):
        
    data = add_column(data, 2)
    
    counter = -1 

    for i in range(len(data)):
        
        if data[i, close] < data[i - step, close] and \
           data[i, close] < data[i - step_two, close]:
            
            data[i, position_long] = counter
            
            counter += -1   
            
            if counter == -count - 1:
                
                counter = 0
                
            else:
                
                continue  
            
        elif data[i, close] >= data[i - step, close] or \
             data[i, close] >= data[i - step_two, close]:
            
            counter = -1 
            
            data[i, position_long] = 0 
        
    counter = 1 
    
    for i in range(len(data)):
        
        if data[i, close] > data[i - step, close] and \
           data[i, close] > data[i - step_two, close]:
            
            data[i, position_short] = counter 
            
            counter += 1      
            
            if counter == count + 1: 
                
                counter = 0     
                
            else:
                
                continue        
            
        elif data[i, close] <= data[i - step, close] or \
             data[i, close] <= data[i - step_two, close]:
            
            counter = 1 
            
            data[i, position_short] = 0 
        
    return data

def rvi(data, lookback, opening, high, low, close, position):
 
    data = add_column(data, 4)

    # Numerator
    for i in range(len(data)):
        
        data[i, position] = (data[i, close] - data[i, opening]) + \
                            (2 * (data[i, close] - data[i - 1, opening])) + \
                            (2 * (data[i, close] - data[i - 2, opening])) + \
                            (data[i, close] - data[i - 3, opening])
    
    data[:, position] = data[:, position] / 6
    data = ma(data, lookback, position, position + 1)
    
    # Denominator
    for i in range(len(data)):
        
        data[i, position + 2] = (data[i, high] - data[i, low]) + \
                                (2 * (data[i, high] - data[i - 1, low])) + \
                                (2 * (data[i, high] - data[i - 2, low])) + \
                                (data[i, high] - data[i - 3, low])
    
    data[:, position] = data[:, position] / 6
    data = ma(data, lookback, position + 2, position + 3)
    
    # RVI
    data[:, position + 4] = data[:, position + 1] / data[:, position + 3]
    
    # Signal
    for i in range(len(data)):
    
        data[i, position + 5] = ((data[i, position + 4]) + \
                                (2 * (data[i - 1, position + 4])) + \
                                (2 * (data[i - 2, position + 4])) + \
                                (data[i - 3, position + 4])) / 6 
    
    data = delete_column(data, position, 4)
    data = delete_row(data, lookback + 10)
    
    return data

def macd(data, close, long_ema, short_ema, signal_ema, position):
    
    data = add_column(data, 1)
    
    data = ema(data, 2, long_ema,  close, position)
    data = ema(data, 2, short_ema, close, position + 1)
    
    data[:, position + 2] = data[:, position + 1] - data[:, position]

    data = delete_row(data, long_ema)
    data = ema(data, 2, signal_ema, position + 2, position + 3)
    
    data = delete_column(data, position, 2)   
    data = delete_row(data, signal_ema)
    
    return data

def sar(s, af = 0.02, amax = 0.2):
    
    s = pd.DataFrame(s)
    s.columns = ['open','high','low','close']
    
    high, low = s.high, s.low

    # Starting values
    sig0, xpt0, af0 = True, high[0], af
    sar = [low[0] - (high - low).std()]
    for i in range(1, len(s)):
        sig1, xpt1, af1 = sig0, xpt0, af0
        lmin = min(low[i - 1], low[i])
        lmax = max(high[i - 1], high[i])
        if sig1:
            sig0 = low[i] > sar[-1]
            xpt0 = max(lmax, xpt1)
        else:
            sig0 = high[i] >= sar[-1]
            xpt0 = min(lmin, xpt1)
        if sig0 == sig1:
            sari = sar[-1] + (xpt1 - sar[-1])*af1
            af0 = min(amax, af1 + af)
            if sig0:
                af0 = af0 if xpt0 > xpt1 else af1
                sari = min(sari, lmin)
            else:
                af0 = af0 if xpt0 < xpt1 else af1
                sari = max(sari, lmax)
        else:
            af0 = af
            sari = xpt0
        sar.append(sari)        
        s = np.array(s)
        s = np.reshape(s, (-1, 1))

    return sar

def bollinger_bands(data, lookback, standard_deviation, close, position):
       
    data = add_column(data, 2)
    
    # Calculating means
    data = ma(data, lookback, close, position)

    data = volatility(data, lookback, close, position + 1)
    
    data[:, position + 2] = data[:, position] + (standard_deviation * data[:, position + 1])
    data[:, position + 3] = data[:, position] - (standard_deviation * data[:, position + 1])
    
    data = delete_row(data, lookback)
    
    data = delete_column(data, position + 1, 1)
        
    return data

def fma(data, position):
    
    data = add_column(data, 2)

    # Calculating Different Moving Averages
    data = ema(data, 2, 5,    1, position)    
    data = ema(data, 2, 8,    1, position + 1)    
    data = ema(data, 2, 13,   1, position + 2)    
    data = ema(data, 2, 21,   1, position + 3)    
    data = ema(data, 2, 34,   1, position + 4)    
    data = ema(data, 2, 55,   1, position + 5)    
    data = ema(data, 2, 89,   1, position + 6)    
    data = ema(data, 2, 144,  1, position + 7)    
    data = ema(data, 2, 233,  1, position + 8)    
    data = ema(data, 2, 377,  1, position + 9)    
    data = ema(data, 2, 610,  1, position + 10)    
    data = ema(data, 2, 987,  1, position + 11)    
    data = ema(data, 2, 1597, 1, position + 12) 
    data = ema(data, 2, 2584, 1, position + 13) 
    data = ema(data, 2, 4181, 1, position + 14) 

    # Calculating the High FMA
    data[:, position + 15] = (data[:, position]      + \
                          data[:,  position + 1]  + \
                          data[:,  position + 2]  + \
                          data[:,  position + 3]  + \
                          data[:,  position + 4]  + \
                          data[:,  position + 5]  + \
                          data[:,  position + 6]  + \
                          data[:,  position + 7]  + \
                          data[:,  position + 8]  + \
                          data[:,  position + 9]  + \
                          data[:,  position + 10] + \
                          data[:,  position + 11] + \
                          data[:,  position + 12] + \
                          data[:,  position + 13] + \
                          data[:,  position + 14]) / 15
    
    data = delete_column(data, position, 15)
    
    # Calculating Different Moving Averages
    data = ema(data, 2, 5,    2, position + 1)    
    data = ema(data, 2, 8,    2, position + 2)    
    data = ema(data, 2, 13,   2, position + 3)    
    data = ema(data, 2, 21,   2, position + 4)    
    data = ema(data, 2, 34,   2, position + 5)    
    data = ema(data, 2, 55,   2, position + 6)    
    data = ema(data, 2, 89,   2, position + 7)    
    data = ema(data, 2, 144,  2, position + 8)    
    data = ema(data, 2, 233,  2, position + 9)    
    data = ema(data, 2, 377,  2, position + 10)    
    data = ema(data, 2, 610,  2, position + 11)    
    data = ema(data, 2, 987,  2, position + 12)    
    data = ema(data, 2, 1597, 2, position + 13) 
    data = ema(data, 2, 2584, 2, position + 14) 
    data = ema(data, 2, 4181, 2, position + 15) 

    # Calculating the High FMA
    data[:, position + 16] = (data[:, position + 1]  + \
                          data[:,  position + 2]  + \
                          data[:,  position + 3]  + \
                          data[:,  position + 4]  + \
                          data[:,  position + 5]  + \
                          data[:,  position + 6]  + \
                          data[:,  position + 7]  + \
                          data[:,  position + 8]  + \
                          data[:,  position + 9]  + \
                          data[:,  position + 10] + \
                          data[:,  position + 11] + \
                          data[:,  position + 12] + \
                          data[:,  position + 13] + \
                          data[:,  position + 14] + \
                          data[:,  position + 15]) / 15
    
    data = delete_column(data, position + 1, 15)
    
    return data

def divergence(data, indicator, lower_barrier, upper_barrier, width, buy, sell):
    data = add_column(data, 10)
    for i in range(len(data)):
        try:
            if data[i, indicator] < lower_barrier:
                for a in range(i + 1, i + width):
                    # First trough
                    if data[a, indicator] > lower_barrier:
                        for r in range(a + 1, a + width):
                            if data[r, indicator] < lower_barrier and \
                            data[r, indicator] > data[i, indicator] and data[r, 3] < data[i, 3]:
                                for s in range(r + 1, r + width):
                                    # Second trough
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
                    # First trough
                    if data[a, indicator] < upper_barrier:
                        for r in range(a + 1, a + width):
                            if data[r, indicator] > upper_barrier and \
                            data[r, indicator] < data[i, indicator] and data[r, 3] > data[i, 3]:
                                for s in range(r + 1, r + width):
                                    # Second trough
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

def keltner_channel(data, lookback, multiplier, close, position):
    
    data = add_column(data, 2)
    
    data = ema(data, 2, lookback, close, position)
    
    data = atr(data, lookback, 2, 1, 3, position + 1)
    
    data[:, position + 2] = data[:, position] + (data[:, position + 1] * multiplier)
    data[:, position + 3] = data[:, position] - (data[:, position + 1] * multiplier)

    data = delete_column(data, position, 2)
    data = delete_row(data, lookback)

    return data

def psychological_levels_scanner(data, close, position):
    
    data = add_column(data, 10)
    
    # Rounding for ease of use
    data = rounding(data, 4)
    
    # Threshold
    level = 0
    
    # Scanning for Psychological Levels
    for i in range(len(data)):
        
        for i in range(len(data)):
            
            if data[i, close] == level:
                    
                data[i, position] = 1
                
        level = round(level + 0.01, 2)
        if level > 5:
            break
    
    return data

def time_up(data, width, close, position):
    
    data = add_column(data, 4)
    
    # Calculating the difference in prices
    for i in range(len(data)):
        
        data[i, position] = data[i, close] - data[i - width, close]
        
    # Upward timing    
    for i in range(len(data)):
        
        data[0, position + 1] = 1
        
        if data[i, position] > 0:
            
            data[i, position + 1] = data[i - width, position + 1] + 1
        else:
            data[i, position + 1] = 0
            
    # Downward timing    
    for i in range(len(data)):
            
        data[0, position + 2] = 1
            
        if data[i, position] < 0:
                
            data[i, position + 2] = data[i - width, position + 2] + 1
        else:
            data[i, position + 2] = 0
                
    # Changing signs
    for i in range(len(data)):
            
        if data[i, position + 2] != 0:
                
            data[i, position + 2] = -1 * data[i, position + 2]
        
    # Time's up indicator
    data[:, position + 3] = data[:, position + 1] + data[:, position + 2]
        
    # Cleaning rows/columns
    data = delete_column(data, position, 3)
        
    return data

def rob_booker_reversal(data, high, low, close, position, buy, sell):
    
    # Calling the MACD function
    data = macd(data, close, 26, 12, 9, position)
    
    # Removing the MACD signal line
    data = delete_column(data, position + 1, 1)
    
    # Calling the stochastic function
    data = stochastic_oscillator(data, 70, high, low, close, position + 1, 
                             slowing = True, 
                             smoothing = True, 
                             slowing_period = 10, 
                             smoothing_period = 10)
    
    # Removing the unnecessary columns
    data = delete_column(data, position + 1, 2)
    
    data = add_column(data, 5)
    
    # Creating the Rob Booker reversal indicator
    for i in range(len(data)):
        
        if data[i, position] > 0 and data[i - 1, position] < 0 and data[i, position + 1] < 30:
           
            data[i + 1, buy] = 1
        
        elif data[i, position] < 0 and data[i - 1, position] > 0 and data[i, position + 1] > 70:
                          
            data[i + 1, sell] = -1

    return data

def volatility_adjusted_moving_average(data, lookback_volatility_short, lookback_volatility_long, close, position):
    
    data = add_column(data, 2)
    
    # Calculating Standard Deviations
    data = volatility(data, lookback_volatility_short, close, position)
    data = volatility(data, lookback_volatility_long, close, position + 1)
    
    # Calculating Alpha
    for i in range(len(data)):
        
        data[i, position + 2] = 0.2 * (data[i, position] / data[i, position + 1])
   
    # Calculating the First Value of VAMA
    data[1, position + 3] = (data[1, position + 2] * data[1, close]) + ((1 - data[1, position + 2]) * data[0, close])
        
    # Calculating the Rest of VAMA
    for i in range(2, len(data)):
        
        data[i, position + 3] = (data[i, position + 2] * data[i, close]) + ((1 - data[i, position + 2]) * data[i - 1, position + 3])
    
    # Cleaning
    data = delete_column(data, position, 3) 
    data = delete_row(data, 1)
    
    return data

def vama_bands(data, lookback_volatility_short, lookback_volatility_long, lookback_volatility, std, close, position):
    
    data = volatility_adjusted_moving_average(data, lookback_volatility_short, lookback_volatility_long, close, position)
    
    data = volatility(data, lookback_volatility, close, position + 1)
    
    data = add_column(data, 2)
    
    data[:, position + 2] = data[:, position] + (std * data[:, position + 1])
    data[:, position + 3] = data[:, position] - (std * data[:, position + 1])
    
    data = delete_row(data, lookback_volatility)
    data = delete_column(data, position + 1, 1)
    
    return data

def bollinger_percentage_bands(data, close, upper_boll, lower_boll, position):
    
    data = add_column(data, 1)
    
    # Calculating the Bollinger percentage bands
    for i in range(len(data)):
        
        data[i, position] = (data[i, close] - data[i, lower_boll]) / (data[i, upper_boll] - data[i, lower_boll])
        
    return data

def detrended_price_oscillator(data, lookback, close, position):
    
    # Calculating the moving average
    data = ma(data, lookback, close, position)
    
    data = add_column(data, 1)
    
    # Calculating the detrended price oscillator
    for i in range(len(data)):
        
        x = int((lookback / 2) + 1)
        data[i, position + 1] = (data[i - x, close] - data[i, position]) * 100
        
    # Cleaning
    data = delete_column(data, position, 1)    
        
    return data

def demarker(data, lookback, high, low, position):
    
    data = add_column(data, 3)
    
    # Calculating DeMAX
    for i in range(len(data)):
        
        if data[i, high] > data[i - 1, high]:
            data[i, position] = data[i, high] - data[i - 1, high]
        else:
            data[i, position] = 0
    
    # Calculating the moving average on DeMAX
    data = ma(data, lookback, position, position + 1)        
            
    # Calculating DeMIN
    for i in range(len(data)):
        
        if data[i - 1, low] > data[i, low]:
            data[i, position + 2] = data[i - 1, low] - data[i, low]
        else:
            data[i, position + 2] = 0    
    
    # Calculating the moving average on DeMIN
    data = ma(data, lookback, position + 2, position + 3)        
   
    
    # Calculating Demarker
    for i in range(len(data)):
        
        data[i, position + 4] = data[i, position + 1] / (data[i, position + 1] + data[i, position + 3]) 
    
    # Cleaning
    data = delete_column(data, position, 4)
    
    return data

def k_reversal_indicator(data, lookback_boll, standard_deviation, close, position):
    
    data = bollinger_bands(data, lookback_boll, standard_deviation, close, position)
    
    data = macd(data, close, 26, 12, 9, position + 3)
    
    return data

def k_objective_support_resistance(data, lookback, lower_range, high, low, position):
    
    data = add_column(data, 3)
    
    # Calculating the maximum range
    for i in range(len(data)):
        
        try:
            
            data[i, position] = (max(data[i - lookback + 1:i + 1, high]) - min(data[i - lookback + 1:i + 1, low]))
            
        except ValueError:
            
            pass
        
    # Calculating support
    for i in range(len(data)):
        
        try:
            
            data[i, position + 1] = min(data[i - lookback + 1:i + 1, low]) + (data[i, position] * lower_range)
            
        except ValueError:
            
            pass
    
    # Calculating resistance
    for i in range(len(data)):
        
        try:
            
            data[i, position + 2] = max(data[i - lookback + 1:i + 1, high]) - (data[i, position] * lower_range)
            
        except ValueError:
            
            pass
    
    return data

def k_envelopes(data, lookback, high, low, position):
    
    # Calculating the upper moving average
    data = ma(data, lookback, high, position)
    
    # Calculating the lower moving average
    data = ma(data, lookback, low, position + 1)    
    
    return data

def k_volatility_band(data, lookback, multiplier, high, low, close, position):
    
    data = add_column(data, 6)
    
    # Calculating the median line
    for i in range(len(data)):
        
        try:
            
            data[i, position] = max(data[i - lookback + 1:i + 1, high]) 
            data[i, position + 1] = min(data[i - lookback + 1:i + 1, low]) 
            data[i, position + 2] = (data[i, position] + data[i, position + 1]) / 2
            
        except ValueError:
            
            pass

    # Cleaning
    data = delete_column(data, position, 2)

    # Calculating maximum volatility
    data = volatility(data, lookback, close, position + 1)
    
    for i in range(len(data)):
        
        try:
            
            data[i, position + 2] = max(data[i - lookback + 1:i + 1, position + 1]) 
            
        except ValueError:
            
            pass   
        
    # Cleaning
    data = delete_column(data, position + 1, 1)
    
    # Calculating the bands
    data[:, position + 2] = data[:, position] + (multiplier * data[:, position + 1])    
    data[:, position + 3] = data[:, position] - (multiplier * data[:, position + 1])

    # Cleaning
    data = delete_column(data, position + 1, 1)    
        
    return data

def stochastic_rsi(data, lookback_rsi, lookback_stoch, close, position, slowing_period = 1, smoothing_period = 1):
            
    data = rsi(data, lookback_rsi, close, position)    
    
    data = add_column(data, 1)
        
    for i in range(len(data)):
            
        try:
            
            data[i, position + 1] = (data[i, position] - min(data[i - lookback_stoch + 1:i + 1, position])) / (max(data[i - lookback_stoch + 1:i + 1, position]) - min(data[i - lookback_stoch + 1:i + 1, position]))
            
        except ValueError:
            
            pass
    
    data = delete_column(data, position, 1)
    
    data[:, position] = data[:, position] * 100  
                 
    data = ma(data, slowing_period, position, position + 1)
    
    data = ma(data, smoothing_period, position + 1, position + 2)    
       
    return data

def rsi_atr(data, lookback_rsi, lookback_atr, lookback_rsi_atr, high, low, close, position):
    
    data = rsi(data, lookback_rsi, close, position)
    
    data = atr(data, lookback_atr, high, low, close, position + 1)
    
    data = add_column(data, 1)
    
    data[:, position + 2] = data[:, position] / data[:, position + 1]
    
    data = rsi(data, lookback_rsi_atr, position + 2, position + 3)
    
    data = delete_column(data, position, 3)
    
    return data

def chande_momentum_oscillator(data, lookback, close, position):
    
    data = add_column(data, 5)
    
    # Calculating the number of higher closes
    for i in range(len(data)):
        
        if data[i, close] > data[i - 1, close]:
            
            data[i, position] = data[i, close] - data[i - 1, close]
    
    # Calculating the number of lower closes
    for i in range(len(data)):
        
        if data[i, close] < data[i - 1, close]:
            
            data[i, position + 1] = abs(data[i, close] - data[i - 1, close])
    
    # Calculating the sum of higher closes
    for i in range(len(data)):
    
        data[i, position + 2] = data[i - lookback + 1:i + 1, position].sum()           
    
    # Calculating the sum of lower closes
    for i in range(len(data)):
        
        data[i, position + 3] = data[i - lookback + 1:i + 1, position + 1].sum()   
        
    # Calculating the CMO
    for i in range(len(data)):
           
        data[i, position + 4] = (data[i, position + 2] - data[i, position + 3]) / (data[i, position + 2] + data[i, position + 3]) * 100 
    
    # Cleaning
    data = delete_column(data, 4, 4)
    
    return data

def fibonacci_retracement(data, retracement, rsi_col, upper_barrier, lower_barrier, position): 

    data = add_column(data, 10)    
    
    for i in range(len(data)):
     
        if data[i, rsi_col] > lower_barrier and data[i - 1, rsi_col] < lower_barrier:
            
            for a in range(i + 1, len(data)):
                
                if data[a, rsi_col] < upper_barrier and data[a - 1, rsi_col] > upper_barrier:
                    
                    data[a - 1, position] = 1 # Marking the top
                    data[a - 1, position + 1] = (data[a - 1, rsi_col] - data[i - 1, rsi_col])
                    data[a - 1, position + 1] = (data[a - 1, position + 1] * (1 - retracement)) + data[i - 1, rsi_col]
                    break
                
                else:
                    continue
        else:
            continue

    for i in range(len(data)):
     
        if data[i, rsi_col] < upper_barrier and data[i - 1, rsi_col] > upper_barrier:
            
            for a in range(i + 1, len(data)):
                
                if data[a, rsi_col] > lower_barrier and data[a - 1, rsi_col] < lower_barrier:
                    
                    data[a - 1, position + 2] = -1 # Marking the bottom
                    data[a - 1, position + 3] = (data[i - 1, rsi_col] - data[a - 1, rsi_col])
                    data[a - 1, position + 3] = data[a - 1, rsi_col] + (data[a - 1, position + 3] * retracement) 
                    break
                
                else:
                    continue
        else:
            continue

    for i in range(len(data)):

        if data[i, position] == 1:
            
            for a in range(i + 1, len(data)):
                if data[a, rsi_col] <= data[i, position + 1]:
                    data[a + 1, position + 4] = 1
                    break
                else:
                    continue
        else:
            continue        

    for i in range(len(data)):

        if data[i, position + 2] == -1:
            
            for a in range(i + 1, len(data)):
                if data[a, rsi_col] >= data[i, position + 3]:
                    data[a + 1, position + 5] = -1
                    break
                else:
                    continue
        else:
            continue   


    return data

def mandi(data, lookback, lookback_trend, close, position):
    
    data = ma(data, lookback, close, position)
    
    data = add_column(data, 1)
    
    data[:, position + 1] = abs(data[:, close] - data[:, position])
    
    data = normalized_index(data, lookback, position + 1, position + 2)
    
    data = delete_column(data, position + 1, 1)
    
    data = ma(data, lookback_trend, close, position + 2)   
    
    return data

def double_top_bottom(data, indicator, lower_barrier, upper_barrier, width, buy, sell):
    data = add_column(data, 10)
    for i in range(len(data)):
        try:
            if data[i, indicator] < lower_barrier:
                for a in range(i + 1, i + width):
                    if data[a, indicator] > lower_barrier:
                        for r in range(a + 1, a + width):
                            if data[r, indicator] < lower_barrier and data[r, indicator] >= data[i, indicator]:
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
                    if data[a, indicator] < upper_barrier:
                        for r in range(a + 1, a + width):
                            if data[r, indicator] > upper_barrier and data[r, indicator] <= data[i, indicator]:
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

def bounded_slope_indicator(data, lookback_slope, lookback_rsi, close, position):
    
    data = add_column(data, 1)
    
    for i in range(len(data)):
        
        data[i, position] = (data[i, close] - data[i - lookback_slope, close]) / lookback_slope
        
    data = rsi(data, lookback_rsi, position, position + 1)
    
    return data

def directional_probability_index(data, lookback, open_column, close, position):
    
    data = add_column(data, 3)
    
    # Calculating the DPI
    for i in range(len(data)):
        
        if data[i, close] > data[i, open_column]:
            
            data[i, position] = 1
            
    for i in range(len(data)):
        
        data[i, position + 1] = data[i - lookback + 1:i + 1, position].sum()
        
    data[:, position + 2] = (data[:, position + 1] / lookback) * 100
    
    data = delete_column(data, position, 2)
    
    return data

# Example of a signal function on a moving average Cross (To be used in case of a moving average crossover strategy) on OHLC array
def signal_MA_crossover(data, close, ma_col, buy, sell):
     
     data = add_column(data, 2)
     
     for i in range(len(data)):
          
          if data[i, close] > data[i, ma_col] and data[i - 1, close] < data[i - 1, ma_col]:
               
               data[i + 1, buy] = 1
          if data[i, close] < data[i, ma_col] and data[i - 1, close] > data[i - 1, ma_col]:
               
               data[i + 1, sell] = -1
     
     return data
