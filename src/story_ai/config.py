import os
from pathlib import Path


class Config:
    DATA_ROOT = Path(os.environ.get("DATA_ROOT", 'data'))
    LOG_ROOT = DATA_ROOT / 'log'
    SERVICE_MT_OPENAI = os.environ.get("SERVICE_MT_OPENAI", "http://127.0.0.1:6599")
    SERVICE_MT_REV_OPENAI = os.environ.get("SERVICE_MT_REV_OPENAI", "http://127.0.0.1:6598")
