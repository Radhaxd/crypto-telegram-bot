
# Crypto Telegram Bot

A feature-rich Telegram bot for cryptocurrency enthusiasts.

## Features

- Cryptocurrency price alerts
- Trading simulation
- Crypto quiz with leaderboard
- Multi-language support
- Price conversion between cryptocurrencies
- Latest crypto news updates

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/Radhaxd/crypto-telegram-bot.git
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables in a `.env` file:
   ```
   API_ID=your_api_id
   API_HASH=your_api_hash
   BOT_TOKEN=your_bot_token
   MONGO_URI=your_mongo_uri
   ```

4. Run the bot:
   ```
   python bot.py
   ```

## Usage

- `/start` - Start the bot and see available commands
- `/convert <amount> <from_currency> <to_currency>` - Convert between cryptocurrencies
- `/price <crypto>` - Get the current price of a cryptocurrency
- `/alert <crypto> <price> <above/below>` - Set a price alert
- `/quiz` - Start a crypto quiz
- `/leaderboard` - View the quiz leaderboard
- `/news` - Get the latest crypto news
- `/portfolio` - View your simulated trading portfolio

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
