# src/backup.py
"""
Main backup script for Airtable Backup Tool.
Handles data retrieval and backup creation.
"""

import requests
import pandas as pd
from datetime import datetime
import os
from typing import List, Dict
import json
import logging
from pathlib import Path
from colorama import init, Fore, Style
import emoji
from config import BACKUP_CONFIG, API_BASE_URL, API_VERSION, LOG_CONFIG, CONSOLE_COLORS

# Initialize colorama
init()

def setup_logging():
    """Configure logging settings"""
    logging.basicConfig(
        level=getattr(logging, LOG_CONFIG["level"]),
        format=LOG_CONFIG["format"],
        datefmt=LOG_CONFIG["date_format"],
        handlers=[
            logging.FileHandler(BACKUP_CONFIG["log_file"]),
            logging.StreamHandler()
        ]
    )

def print_status(message: str, status: str = 'info', indent: int = 0) -> None:
    """Print formatted status message with emoji and color"""
    prefix = "  " * indent
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    icons = {
        'start': '🚀',
        'success': '✅',
        'error': '❌',
        'info': 'ℹ️',
        'table': '📊',
        'file': '📁',
        'warning': '⚠️'
    }
    
    color = CONSOLE_COLORS.get(status, CONSOLE_COLORS['reset'])
    icon = icons.get(status, icons['info'])
    
    print(f"{color}{prefix}{icon} [{timestamp}] {message}{CONSOLE_COLORS['reset']}")
    logging.info(message)

def get_tables(base_id: str, api_key: str) -> List[Dict]:
    """Get all tables from an Airtable base"""
    url = f"{API_BASE_URL}/{API_VERSION}/meta/bases/{base_id}/tables"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get("tables", [])
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to get tables: {str(e)}")
        raise

def backup_table(base_id: str, table_name: str, api_key: str) -> pd.DataFrame:
    """Backup a single table to DataFrame"""
    url = f"{API_BASE_URL}/{API_VERSION}/{base_id}/{table_name}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    all_records = []
    params = {}
    
    while True:
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            records = data.get("records", [])
            all_records.extend([record["fields"] for record in records])
            
            # Check for pagination
            if "offset" in data:
                params["offset"] = data["offset"]
            else:
                break
                
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to get records for {table_name}: {str(e)}")
            raise
    
    return pd.DataFrame(all_records)

def cleanup_old_backups(backup_dir: str, retention_days: int) -> None:
    """Remove backups older than retention_days"""
    try:
        current_time = datetime.now()
        backup_path = Path(backup_dir)
        
        for file in backup_path.glob("*.csv"):
            file_time = datetime.fromtimestamp(file.stat().st_mtime)
            age = (current_time - file_time).days
            
            if age > retention_days:
                file.unlink()
                print_status(f"Removed old backup: {file.name}", "info", 1)
    except Exception as e:
        logging.error(f"Error during cleanup: {str(e)}")
        raise

def backup_airtable_to_csv():
    """Main backup function"""
    try:
        setup_logging()
        print_status("Starting Airtable Backup Process", "start")
        
        # Get API key
        API_KEY = os.getenv("AIRTABLE_API_KEY")
        if not API_KEY:
            raise ValueError("Missing AIRTABLE_API_KEY environment variable")
        
        BASE_ID = BACKUP_CONFIG["base_id"]
        
        # Get all tables
        tables = get_tables(BASE_ID, API_KEY)
        print_status(f"Found {len(tables)} tables", "info")
        
        # Create backup directory
        today = datetime.now().strftime("%Y-%m-%d")
        backup_dir = BACKUP_CONFIG["backup_dir"]
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
            print_status(f"Created backup directory: {backup_dir}", "file")
        
        # Process each table
        successful_backups = 0
        for table in tables:
            try:
                table_name = table["name"]
                print_status(f"Processing table: {table_name}", "table", 1)
                
                # Get data
                df = backup_table(BASE_ID, table_name, API_KEY)
                print_status(f"Found {len(df)} records", "info", 2)
                
                if not df.empty:
                    # Save to CSV
                    filename = f"{backup_dir}/{table_name}_{today}.csv"
                    df.to_csv(filename, index=False, encoding="utf-8-sig")
                    print_status(f"Saved: {filename}", "success", 2)
                    successful_backups += 1
                else:
                    print_status("Table is empty", "warning", 2)
                    
            except Exception as e:
                print_status(f"Error backing up {table_name}: {str(e)}", "error", 2)
        
        # Cleanup old backups
        cleanup_old_backups(backup_dir, BACKUP_CONFIG["schedule"]["retention_days"])
        
        print_status(
            f"Backup completed! {successful_backups}/{len(tables)} tables backed up successfully",
            "success"
        )
        
    except Exception as e:
        print_status(f"Critical error during backup process: {str(e)}", "error")
        logging.error(f"Backup failed: {str(e)}")
        raise

if __name__ == "__main__":
    backup_airtable_to_csv()