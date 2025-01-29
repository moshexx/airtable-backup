# src/config.py
"""
Configuration file for Airtable Backup Tool.
Contains all configurable parameters and settings.
"""

BACKUP_CONFIG = {
    "schedule": {
        "frequency": "daily",     # Options: daily, weekly, monthly
        "time": "23:00",         # Format: HH:MM
        "retention_days": 30      # How many days to keep backups
    },
    "base_id": "your_base_id",   # Your Airtable base ID
    "backup_dir": "airtable_backups",
    "log_file": "backup.log"
}

# API Configuration
API_VERSION = "v0"
API_BASE_URL = "https://api.airtable.com"

# Logging Configuration
LOG_CONFIG = {
    "format": "%(asctime)s - %(levelname)s - %(message)s",
    "level": "INFO",
    "date_format": "%Y-%m-%d %H:%M:%S"
}

# Console Output Configuration
CONSOLE_COLORS = {
    "info": "\033[94m",    # Blue
    "success": "\033[92m", # Green
    "warning": "\033[93m", # Yellow
    "error": "\033[91m",   # Red
    "reset": "\033[0m"     # Reset
}