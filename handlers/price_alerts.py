
from pyrogram import Client, filters
from database.db import add_price_alert, remove_price_alert, get_user_alerts, get_all_active_alerts
from utils.crypto_api import get_crypto_price
from utils.i18n import i18n
from utils.logger import main_logger
import asyncio

@Client.on_message(filters.command("setalert"))
async def set_price_alert(client, message):
    try:
        _, crypto, price, condition = message.text.split()
        user_id = message.from_user.id
        
        crypto = crypto.upper()
        price = float(price)
        condition = condition.lower()

        if condition not in ['above', 'below']:
            await message.reply_text("Invalid condition. Use 'above' or 'below'.")
            return

        await add_price_alert(user_id, crypto, price, condition)
        await message.reply_text(f"Alert set for {crypto} when price is {condition} ${price}")
    except ValueError:
        await message.reply_text("Usage: /setalert <crypto> <price> <above/below>")
    except Exception as e:
        main_logger.error(f"Error in set_price_alert: {str(e)}", exc_info=True)
        await message.reply_text("An error occurred while setting the alert.")

@Client.on_message(filters.command("removealert"))
async def remove_price_alert(client, message):
    try:
        _, alert_id = message.text.split()
        user_id = message.from_user.id
        
        success = await remove_price_alert(user_id, int(alert_id))
        if success:
            await message.reply_text(f"Alert {alert_id} has been removed.")
        else:
            await message.reply_text(f"Alert {alert_id} not found or already removed.")
    except ValueError:
        await message.reply_text("Usage: /removealert <alert_id>")
    except Exception as e:
        main_logger.error(f"Error in remove_price_alert: {str(e)}", exc_info=True)
        await message.reply_text("An error occurred while removing the alert.")

@Client.on_message(filters.command("myalerts"))
async def list_user_alerts(client, message):
    try:
        user_id = message.from_user.id
        alerts = await get_user_alerts(user_id)
        
        if not alerts:
            await message.reply_text("You have no active price alerts.")
            return

        response = "Your active price alerts:\n\n"
        for alert in alerts:
            response += f"ID: {alert['id']} - {alert['crypto']} {alert['condition']} ${alert['price']}\n"
        
        await message.reply_text(response)
    except Exception as e:
        main_logger.error(f"Error in list_user_alerts: {str(e)}", exc_info=True)
        await message.reply_text("An error occurred while fetching your alerts.")

async def check_price_alerts():
    while True:
        try:
            alerts = await get_all_active_alerts()
            for alert in alerts:
                current_price = await get_crypto_price(alert['crypto'])
                if (alert['condition'] == 'above' and current_price > alert['price']) or                    (alert['condition'] == 'below' and current_price < alert['price']):
                    user_id = alert['user_id']
                    message = f"🚨 Price Alert: {alert['crypto']} is now ${current_price}, which is {alert['condition']} your alert price of ${alert['price']}."
                    await Client.send_message(user_id, message)
                    await remove_price_alert(user_id, alert['id'])
        except Exception as e:
            main_logger.error(f"Error in check_price_alerts: {str(e)}", exc_info=True)
        await asyncio.sleep(60)  # Check every minute

# Add this to your main bot file to start the price alert checker
# asyncio.create_task(check_price_alerts())
