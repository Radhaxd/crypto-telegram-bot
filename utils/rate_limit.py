
import time
from collections import defaultdict
from utils.logger import main_logger

class RateLimiter:
    def __init__(self, max_calls, time_frame):
        self.max_calls = max_calls
        self.time_frame = time_frame
        self.calls = defaultdict(list)

    def is_allowed(self, user_id):
        current_time = time.time()
        self.calls[user_id] = [call for call in self.calls[user_id] if current_time - call <= self.time_frame]
        
        if len(self.calls[user_id]) >= self.max_calls:
            return False
        
        self.calls[user_id].append(current_time)
        return True

rate_limiter = RateLimiter(max_calls=5, time_frame=60)  # 5 calls per minute

def rate_limit(func):
    async def wrapper(client, message):
        if rate_limiter.is_allowed(message.from_user.id):
            return await func(client, message)
        else:
            main_logger.warning(f"Rate limit exceeded for user {message.from_user.id}")
            await message.reply_text("You're using this command too frequently. Please wait a moment and try again.")
    return wrapper
