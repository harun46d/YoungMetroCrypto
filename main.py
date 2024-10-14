from trigger import get_usd_pairs
from db import save_pairs_to_db
from telegram_api import send_message
from indicators import buy_sell_walls, get_order_book
import asyncio
import logging

logging.basicConfig(
    filename='logfile.log',
    level=logging.INFO,  
    format='%(asctime)s - %(levelname)s - %(message)s'  
)

def main():
    try:
        usd_pairs = get_usd_pairs()
        logging.info(f'Erfolgreich {len(usd_pairs)} Handelspaare abgerufen.')
        
        gainers = save_pairs_to_db(usd_pairs)
        logging.info("Daten erfolgreich in die Datenbank eingefügt.")

        if gainers is not None:
            logging.info(f"Es wurden {len(gainers)} Top-Gainer gefunden.")
            order_books = get_order_book(gainers)
            gainers = buy_sell_walls(order_books, gainers)
            asyncio.run(send_message(gainers))
            logging.info("Nachrichten an Telegram gesendet.")
        else:
            logging.info("Keinen Top Gainer gefunden.")
            
    except Exception as e:
        logging.exception(f"Fehler während der Verarbeitung: {str(e)}")

if __name__ == '__main__':
    main()
    