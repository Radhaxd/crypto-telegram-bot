
from pyrogram import Client, filters
from database.db import get_user_balance, update_user_balance, add_trade, get_user_trades
from utils.crypto_api import get_crypto_price
from utils.i18n import i18n
from utils.logger import main_logger

@Client.on_message(filters.command("balance"))
async def check_balance(client, message):
    try:
        user_id = message.from_user.id
        balance = await get_user_balance(user_id)
        await message.reply_text(f"Your current balance: ${balance:.2f}")
    except Exception as e:
        main_logger.error(f"Error in check_balance: {str(e)}", exc_info=True)
        await message.reply_text("An error occurred while checking your balance.")

@Client.on_message(filters.command("buy"))
async def buy_crypto(client, message):
    try:
        _, crypto, amount = message.text.split()
        user_id = message.from_user.id
        
        crypto = crypto.upper()
        amount = float(amount)

        price = await get_crypto_price(crypto)
        cost = price * amount
        
        balance = await get_user_balance(user_id)
        if balance < cost:
            await message.reply_text("Insufficient funds for this purchase.")
            return

        new_balance = balance - cost
        await update_user_balance(user_id, new_balance)
        await add_trade(user_id, 'buy', crypto, amount, price)

        await message.reply_text(f"Successfully bought {amount} {crypto} at ${price:.2f} each. New balance: ${new_balance:.2f}")
    except ValueError:
        await message.reply_text("Usage: /buy <crypto> <amount>")
    except Exception as e:
        main_logger.error(f"Error in buy_crypto: {str(e)}", exc_info=True)
        await message.reply_text("An error occurred while processing your purchase.")

@Client.on_message(filters.command("sell"))
async def sell_crypto(client, message):
    try:
        _, crypto, amount = message.text.split()
        user_id = message.from_user.id
        
        crypto = crypto.upper()
        amount = float(amount)

        price = await get_crypto_price(crypto)
        value = price * amount
        
        # Check if user has enough of the crypto to sell
        trades = await get_user_trades(user_id)
        crypto_balance = sum(trade['amount'] for trade in trades if trade['crypto'] == crypto and trade['type'] == 'buy') -                          sum(trade['amount'] for trade in trades if trade['crypto'] == crypto and trade['type'] == 'sell')
        
        if crypto_balance < amount:
            await message.reply_text(f"Insufficient {crypto} balance for this sale.")
            return

        balance = await get_user_balance(user_id)
        new_balance = balance + value
        await update_user_balance(user_id, new_balance)
        await add_trade(user_id, 'sell', crypto, amount, price)

        await message.reply_text(f"Successfully sold {amount} {crypto} at ${price:.2f} each. New balance: ${new_balance:.2f}")
    except ValueError:
        await message.reply_text("Usage: /sell <crypto> <amount>")
    except Exception as e:
        main_logger.error(f"Error in sell_crypto: {str(e)}", exc_info=True)
        await message.reply_text("An error occurred while processing your sale.")

@Client.on_message(filters.command("portfolio"))
async def view_portfolio(client, message):
    try:
        user_id = message.from_user.id
        trades = await get_user_trades(user_id)
        
        portfolio = {}
        for trade in trades:
            if trade['crypto'] not in portfolio:
                portfolio[trade['crypto']] = 0
            if trade['type'] == 'buy':
                portfolio[trade['crypto']] += trade['amount']
            else:
                portfolio[trade['crypto']] -= trade['amount']

        response = "Your current portfolio:\n\n"
        total_value = 0
        for crypto, amount in portfolio.items():
            if amount > 0:
                price = await get_crypto_price(crypto)
                value = price * amount
                total_value += value
                response += f"{crypto}: {amount:.6f} (${value:.2f})\n"

        balance = await get_user_balance(user_id)
        total_value += balance
        response += f"\nCash balance: ${balance:.2f}\n"
        response += f"Total portfolio value: ${total_value:.2f}"

        await message.reply_text(response)
    except Exception as e:
        main_logger.error(f"Error in view_portfolio: {str(e)}", exc_info=True)
        await message.reply_text("An error occurred while fetching your portfolio.")
