import asyncio
from utils.parser import get_prices


async def track_price(update, context, ticker):
    while context.user_data.get('is_active', False):
        prices = get_prices(ticker)
        print(prices)
        message = ""
        exchanges = list(prices.keys())
        try:
            for i in range(len(exchanges)):
                for j in range(i + 1, len(exchanges)):
                    first, second = float(prices[exchanges[i]]), float(prices[exchanges[j]])
                    maxprice, minprice = max(first, second), min(first, second)
                    if (maxprice - minprice) / minprice * 100 >= 2:
                        message += f"Разница {exchanges[i]} - {exchanges[j]}: {maxprice - minprice:.2f} ({(maxprice - minprice) / minprice * 100:.2f}%)\n"
        except:
            await update.message.reply_text("smth wrong idcc")
        if message:
            await update.message.reply_text(message)

        await asyncio.sleep(2)
