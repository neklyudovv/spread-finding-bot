import asyncio
from config import exchanges as cfg_exchanges
from utils.parser import get_prices


async def track_price(update, context, ticker):
    while context.user_data.get('is_active', False):
        prices = get_prices(ticker, cfg_exchanges)
        message = ""
        exchanges = list(prices.keys())
        try:
            for i in range(len(exchanges)):
                for j in range(i + 1, len(exchanges)):
                    first, second = float(prices[exchanges[i]]), float(prices[exchanges[j]])
                    maxprice, minprice = max(first, second), min(first, second)
                    spread = (maxprice - minprice) / minprice * 100
                    if spread >= 2:
                        message += (f"Разница {exchanges[i]} - {exchanges[j]}: {maxprice - minprice:.2f}"
                                    f" ({spread:.2f}%)\n")
        except:
            await update.message.reply_text("no such ticker // smth went wrong")
            break
        if message:
            await update.message.reply_text(message)

        await asyncio.sleep(2)
