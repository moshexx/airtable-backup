"""
Example configurations for Airtable Backup Tool.
This file demonstrates different configuration scenarios and use cases.
"""

# Basic configuration - Daily backup at midnight
BASIC_CONFIG = {
    "schedule": {
        "frequency": "daily",
        "time": "00:00",
        "retention_days": 30
    },
    "base_id": "your_base_id",
    "backup_dir": "airtable_backups",
    "log_file": "backup.log"
}

# Weekly backup with extended retention
WEEKLY_BACKUP_CONFIG = {
    "schedule": {
        "frequency": "weekly",
        "time": "23:00",
        "retention_days": 90,
        "backup_day": "monday"  # Options: monday-sunday
    },
    "base_id": "your_base_id",
    "backup_dir": "weekly_backups",
    "log_file": "weekly_backup.log"
}

# Monthly backup with compression
MONTHLY_BACKUP_CONFIG = {
    "schedule": {
        "frequency": "monthly",
        "time": "02:00",
        "retention_days": 365,
        "backup_day": 1  # First day of the month
    },
    "base_id": "your_base_id",
    "backup_dir": "monthly_backups",
    "log_file": "monthly_backup.log",
    "compress": True,
    "compression_type": "zip"
}

# Multiple bases backup
MULTI_BASE_CONFIG = {
    "schedule": {
        "frequency": "daily",
        "time": "01:00",
        "retention_days": 30
    },
    "bases": [
        {
            "base_id": "base_id_1",
            "backup_dir": "base1_backups"
        },
        {
            "base_id": "base_id_2",
            "backup_dir": "base2_backups"
        }
    ],
    "log_file": "multi_base_backup.log"
}

# Development environment config
DEV_CONFIG = {
    "schedule": {
        "frequency": "daily",
        "time": "12:00",
        "retention_days": 7
    },
    "base_id": "dev_base_id",
    "backup_dir": "dev_backups",
    "log_file": "dev_backup.log",
    "debug_mode": True
}

# Production environment config with notifications
PROD_CONFIG = {
    "schedule": {
        "frequency": "daily",
        "time": "23:00",
        "retention_days": 90
    },
    "base_id": "prod_base_id",
    "backup_dir": "/var/backups/airtable",
    "log_file": "/var/log/airtable_backup.log",
    "notifications": {
        "enabled": True,
        "email": {
            "smtp_server": "smtp.company.com",
            "from_email": "backup@company.com",
            "to_email": ["admin@company.com"],
            "on_success": False,
            "on_failure": True
        },
        "slack": {
            "webhook_url": "your_webhook_url",
            "channel": "#backups",
            "on_success": True,
            "on_failure": True
        }
    },
    "error_retry": {
        "attempts": 3,
        "delay_seconds": 300
    }
}

# Example usage of configurations
def example_usage():
    """
    Example showing how to use different configurations
    """
    print("Available Configuration Examples:")
    print("\n1. Basic Daily Backup")
    print("   - Runs every day at midnight")
    print("   - Keeps backups for 30 days")
    print("Example usage:")
    print("from config import BASIC_CONFIG")
    print("backup_tool = AirtableBackup(BASIC_CONFIG)")
    print("backup_tool.start()")
    
    print("\n2. Weekly Backup")
    print("   - Runs every Monday at 23:00")
    print("   - Keeps backups for 90 days")
    print("Example usage:")
    print("from config import WEEKLY_BACKUP_CONFIG")
    
    print("\n3. Monthly Backup with Compression")
    print("   - Runs on the first of each month")
    print("   - Keeps backups for one year")
    print("   - Compresses backups to save space")
    
    print("\n4. Multiple Bases Backup")
    print("   - Backs up multiple bases daily")
    print("   - Separate directories for each base")
    
    print("\n5. Development Config")
    print("   - Includes debug mode")
    print("   - Shorter retention period")
    
    print("\n6. Production Config")
    print("   - Email notifications on failure")
    print("   - Slack notifications")
    print("   - Automatic retry on failure")
    print("   - Secure file paths")

if __name__ == "__main__":
    example_usage()