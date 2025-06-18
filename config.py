# config.py

import os
from dotenv import load_dotenv

# Load .env values
load_dotenv()

# Telegram API credentials
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_NAME = os.getenv("SESSION_NAME", "moca")

# Telegram bot settings
GROUP_ID = int(os.getenv("GROUP_ID"))
CHANNELS = os.getenv("CHANNELS", "solwhaletrending").split(",")

# Bot behavior settings
MAX_OPEN_POSITIONS = int(os.getenv("MAX_OPEN_POSITIONS", 5))
MIN_SCORE_TO_BUY = int(os.getenv("MIN_SCORE_TO_BUY", 5))
MAX_MARKETCAP = int(os.getenv("MAX_MARKETCAP", 100_000))
TP_MULTIPLIER = float(os.getenv("TP_MULTIPLIER", 2.0))     # 100% gain
SL_MULTIPLIER = float(os.getenv("SL_MULTIPLIER", 0.75))    # 25% loss
MOONBAG_RATIO = float(os.getenv("MOONBAG_RATIO", 0.2))     # 20% moonbag holding

# PumpPortal API
PUMPPORTAL_BASE_URL = os.getenv("PUMPPORTAL_BASE_URL", "https://api.pumpportal.io")
PUMPPORTAL_API_KEY = os.getenv("PUMPPORTAL_API_KEY")

# File path
PORTFOLIO_FILE = "portfolio.json"
STATUS_FILE = "status.json"

