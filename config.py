
# Crypto Telegram Bot Configuration

# Bot settings
BOT_NAME = "CryptoHelper"
BOT_USERNAME = "your_bot_username"

# Feature toggles
ENABLE_PRICE_ALERTS = True
ENABLE_TRADING_SIMULATION = True
ENABLE_CRYPTO_QUIZ = True
ENABLE_NEWS_UPDATES = True

# Quiz settings
QUIZ_QUESTIONS_PER_ROUND = 5
QUIZ_TIME_LIMIT = 30  # seconds

# Trading simulation settings
INITIAL_BALANCE = 10000  # USD
TRANSACTION_FEE = 0.001  # 0.1%

# News update frequency
NEWS_UPDATE_INTERVAL = 3600  # seconds (1 hour)

# Supported languages
SUPPORTED_LANGUAGES = ["en", "es"]

# API endpoints
CRYPTO_PRICE_API = "https://api.coingecko.com/api/v3/simple/price"
CRYPTO_NEWS_API = "https://cryptopanic.com/api/v1/posts/"

# Maximum number of price alerts per user
MAX_ALERTS_PER_USER = 10

# Leaderboard settings
LEADERBOARD_TOP_USERS = 10

# Logging level
LOG_LEVEL = "INFO"
