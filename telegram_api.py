from telegram import Bot
import json 

async def send_message(top_gainers):
    with open('config.json') as config_file:
        config = json.load(config_file)
        
    chat_id = config['chat_id']
    group_chat_id = config['group_chat_id']
    bot_token = config['bot_token']
    
    bot = Bot(token=bot_token)
    
    print(top_gainers)
    
    for gainer in top_gainers:
        symbol = gainer['symbol']
        price_change = gainer['price_change']
        current_price = gainer['current_price']
        previous_price = gainer['previous_price']
        buy_wall_price = gainer['buy_wall_price']
        buy_wall_volume = gainer['buy_wall_volume']
        sell_wall_price = gainer['sell_wall_price']
        sell_wall_volume = gainer['sell_wall_volume']
        
        message = (
            "🚨**Price Change Alert!**\n\n🚨"
            f"The trading pair **{symbol}** has experienced a change of **{price_change:+.2f}%** since the last update!\n\n"
            f"📊 **Current Price**: ${current_price:,.4f}\n"
            f"📉 **Previous Price**: ${previous_price:,.4f}\n\n"
            f"**Buy/Sell Walls**: {buy_wall_volume}x ${buy_wall_price:,.3f} and {sell_wall_volume}x ${sell_wall_price:,.3f}\n" 
        )
    
        await bot.send_message(chat_id=group_chat_id, text=message, parse_mode='Markdown')
