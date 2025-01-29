# src/schedule_backup.py
"""
Scheduler for Airtable Backup Tool.
Handles automated backup scheduling.
"""

import schedule
import time
from datetime import datetime
import logging
from backup import backup_airtable_to_csv, print_status, setup_logging
from config import BACKUP_CONFIG

def run_backup():
    """Wrapper function to run backup with error handling"""
    print_status(f"\n=== Starting scheduled backup at {datetime.now()} ===\n", "start")
    try:
        backup_airtable_to_csv()
    except Exception as e:
        print_status(f"Scheduled backup failed: {str(e)}", "error")

def schedule_backup():
    """Configure and start the backup schedule"""
    config = BACKUP_CONFIG["schedule"]
    backup_time = config["time"]
    frequency = config["frequency"]
    
    if frequency == "daily":
        schedule.every().day.at(backup_time).do(run_backup)
    elif frequency == "weekly":
        schedule.every().monday.at(backup_time).do(run_backup)
    elif frequency == "monthly":
        # Run on the first day of each month
        schedule.every().day.at(backup_time).do(
            lambda: run_backup() if datetime.now().day == 1 else None
        )
    else:
        raise ValueError(f"Invalid frequency: {frequency}")
    
    print_status(f"Backup scheduled to run {frequency} at {backup_time}", "info")

def main():
    """Main scheduler function"""
    setup_logging()
    print_status("Starting Airtable Backup Scheduler", "start")
    
    try:
        schedule_backup()
        
        # Run first backup immediately
        run_backup()
        
        # Keep the scheduler running
        while True:
            schedule.run_pending()
            time.sleep(60)
            
    except KeyboardInterrupt:
        print_status("\nScheduler stopped by user", "info")
    except Exception as e:
        print_status(f"Scheduler error: {str(e)}", "error")
        raise

if __name__ == "__main__":
    main()