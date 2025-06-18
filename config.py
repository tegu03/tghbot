import os
from dotenv import load_dotenv

# Load .env values
load_dotenv()

# ========== Telegram API ==========
API_ID = int(os.getenv("API_ID", "0"))  # wajib diisi
API_HASH = os.getenv("API_HASH", "")
SESSION_NAME = os.getenv("SESSION_NAME", "moca")

# ========== Telegram BOT ==========
GROUP_ID = int(os.getenv("GROUP_ID", "0"))  # wajib diisi jika pakai grup
CHANNELS = os.getenv("CHANNELS", "solwhaletrending").split(",")

# ========== Bot Logic Rules ==========
MAX_OPEN_POSITIONS = int(os.getenv("MAX_OPEN_POSITIONS", 5))       # max token dibeli
MIN_SCORE_TO_BUY = int(os.getenv("MIN_SCORE_TO_BUY", 5))           # min skor untuk beli
MAX_MARKETCAP = int(os.getenv("MAX_MARKETCAP", 100_000))           # max marketcap ($)

TP_MULTIPLIER = float(os.getenv("TP_MULTIPLIER", 2.0))             # contoh: 2.0 = 100% profit
SL_MULTIPLIER = float(os.getenv("SL_MULTIPLIER", 0.75))            # contoh: 0.75 = cut loss 25%
MOONBAG_RATIO = float(os.getenv("MOONBAG_RATIO", 0.2))             # contoh: 20% sisa disimpan

# ========== External API ==========
PUMPPORTAL_BASE_URL = os.getenv("PUMPPORTAL_BASE_URL", "https://api.pumpportal.io")
PUMPPORTAL_API_KEY = os.getenv("PUMPPORTAL_API_KEY", "")

# ========== File Paths ==========
PORTFOLIO_FILE = "portfolio.json"
STATUS_FILE = "status.json"
