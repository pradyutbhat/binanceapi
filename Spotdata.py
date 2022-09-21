import time
import binance
import datetime
import pandas as pd

class unix:  # accept datetime or unix input
    def __init__(self, ts):
        if isinstance(ts, datetime.datetime):
            self.ts = ts
        else:  #adjustment on unix 
            self.ts = int(ts)
            if len(str(self.ts)) == 13:  #millisecond unix
                self.ts = float(self.ts) / 1000
                
    def unix_to_hkt(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.ts))
    
    def unix_to_gmt(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(self.ts))
    
class binance_api:
    def __init__(self, api_key='eJCpDAzb9NeJxp3CZZe7NZk63AbgiQLA14dFrCOA0XJ6H7Ea8QiDVrklPCuC0Y6c', api_secret='hiRvOnYeYDLgdegtJBe0l64S2sxuhnShdDyIJCmhXkn9C2PIEXWAkS3TB7BFWAUx'):
        self.key = api_key
        self.secret = api_secret
        self.client = binance.Client(self.key, self.secret)
        
    def get_spot_kline(self, ticker, interval):
        
        # request historical candle (or klines) data  
        headers = ['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 
                   'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore']
        
        bars = self.client.get_historical_klines(symbol=ticker, interval=interval, start_str="2022-08-08", end_str="2022-09-08")
        df_bars = pd.DataFrame(bars, columns=headers)
        if len(df_bars) != 0:
            df_bars['Open time (HKT)'] = df_bars['Open time'].apply(lambda x: unix(x).unix_to_hkt())
            df_bars['Close time (HKT)'] = df_bars['Close time'].apply(lambda x: unix(x).unix_to_hkt())
            df_bars['Open time (GMT)'] = df_bars['Open time'].apply(lambda x: unix(x).unix_to_gmt())
            df_bars['Close time (GMT)'] = df_bars['Close time'].apply(lambda x: unix(x).unix_to_gmt())
            
        return df_bars
#define variable & then enter the desired cryptocurrency ticker
a = binance_api().get_spot_kline(ticker='ETHUSDT', interval='1d')
