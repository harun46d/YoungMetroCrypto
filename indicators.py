import requests

def dynamic_price_change():
    pass

def buy_sell_walls(order_books, top_gainers):
    gainers = []
    for order_book, gainer in zip(order_books, top_gainers):
        symbol = gainer['symbol']

        bids = order_book['bids']
        asks = order_book['asks']
        
        highest_bid_volume = max(bids, key=lambda x: float(x[1]))
        gainer['buy_wall_price'] = float(highest_bid_volume[0])
        gainer['buy_wall_volume'] = float(highest_bid_volume[1])
        
        highest_ask_volume = max(asks, key=lambda x: float(x[1]))
        gainer['sell_wall_price'] = float(highest_ask_volume[0])
        gainer['sell_wall_volume'] = float(highest_ask_volume[1])
        
        gainers.append(gainer)
    
    return gainers


def get_order_book(gainers):
    base_url = 'https://api.binance.com/api/v3/depth'
    order_books = []
    
    for gainer in gainers:    
        symbol = gainer['symbol']
        params = {
                'symbol': symbol
        }
        order_book = requests.get(base_url, params=params).json()
        
        order_books.append({'symbol': symbol,
                            'bids': order_book['bids'],
                            'asks': order_book['asks']})
        
    return order_books
        
        