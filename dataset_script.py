import requests
import pandas as pd
import time
import os
import datetime

def main(symbol, new_data):
    if os.path.exists(f'data/{symbol}.csv'):
        expand_dataset(symbol, new_data)
    else:
        create_dataset(symbol)

# AI, FIS, MDT, DATA, VIDT
        
def create_dataset(symbol, save=True):
    # TODO: Implement dataset creation for new coins
    base_url = 'https://api.binance.com/api/v3/klines'
    
    params = {
        'symbol':  symbol,
        'interval': '15m',
        'limit': 1000
    }
    
    response = requests.get(base_url, params=params).json()
    
    df = pd.DataFrame(response)
    df.columns = ['Open Time', 'Open Price', 'High Price', 'Low Price', 'Close Price', 'Volume', 'Close Time', 
              'Quote Asset Volume', 'Number of Trades', 'Total base asset purchased by takers', 'Total quote asset sold by takers', 'Ignore']
    
    df = df.drop('Ignore', axis=1)
    
    df['Open Time'] = pd.to_datetime(df['Open Time'], unit='ms')
    df['Close Time'] = pd.to_datetime(df['Close Time'], unit='ms')
    
    # Adjust data types
    columns_not_to_convert = ['Open Time', 'Close Time']

    for col in df.columns:
        if (col not in columns_not_to_convert) and (col != 'Number of Trades'):
            df[col] = df[col].astype('float32')
        elif col == 'Number of Trades':
            df[col] = df[col].astype('int32')
        
    if save:
        df.to_csv(f'data/{symbol}.csv')

def expand_dataset(symbol, new_data):
    df = pd.read_csv(f'data/{symbol}.csv')
    
    if new_data:
        last_timestamp = df.iloc[-1]['Close Time']
        last_timestamp = pd.to_datetime(last_timestamp)
        last_timestamp_utc = last_timestamp.tz_localize('UTC')
        last_timestamp_as_unix = int(last_timestamp_utc.timestamp() * 1000)
     
        params = {
        'symbol': symbol,
        'interval': '15m',
        'limit': 1000,
        'startTime': last_timestamp_as_unix
        }
    else:
        first_timestamp = df.iloc[0]['Open Time']
        first_timestamp = pd.to_datetime(first_timestamp)
        first_timestamp_utc = first_timestamp.tz_localize('UTC')
        first_timestamp_as_unix = int(first_timestamp_utc.timestamp() * 1000)
        
        params = {
            'symbol': symbol,
            'interval': '15m',
            'limit': 1000,
            'endTime': first_timestamp_as_unix
        }
    
    # TODO: Implement api limits /response etc
    
    base_url = 'https://api.binance.com/api/v3/klines'
    response = requests.get(base_url, params=params)
    
    new_df = clean_df(response.json())
    
    # Reset indices
    df = df.reset_index(drop=True)
    new_df = new_df.reset_index(drop=True)
    
    if new_data:
        df_updated = pd.concat([df, new_df], ignore_index=True)
        df_updated = df_updated.loc[:, ~df_updated.columns.str.contains('^Unnamed')]
    else:
        df_updated = pd.concat([new_df, df], ignore_index=True)
        df_updated = df_updated.loc[:, ~df_updated.columns.str.contains('^Unnamed')]
    
    df_updated.to_csv(f'data/{symbol}.csv')
    

    
def clean_df(response):
    df = pd.DataFrame(response)
    df.columns = ['Open Time', 'Open Price', 'High Price', 'Low Price', 'Close Price', 'Volume', 'Close Time', 
              'Quote Asset Volume', 'Number of Trades', 'Total base asset purchased by takers', 'Total quote asset sold by takers', 'Ignore']
    df = df.drop('Ignore', axis=1)  
    
    df['Open Time'] = pd.to_datetime(df['Open Time'], unit='ms')
    df['Close Time'] = pd.to_datetime(df['Close Time'], unit='ms')
    
    columns_not_to_convert = ['Open Time', 'Close Time']

    for col in df.columns:
        if (col not in columns_not_to_convert) and (col != 'Number of Trades'):
            df[col] = df[col].astype('float32')
        elif col == 'Number of Trades':
            df[col] = df[col].astype('int32')
            
    return df
            
if __name__ == '__main__':
    symbol = 'AIUSDT'
    new_data = False
    main(symbol=symbol, new_data=new_data)