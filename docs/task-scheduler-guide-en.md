# Setting Up Automatic Backup with Task Scheduler

This guide will explain how to set up automatic daily backups to run in the background on Windows using Task Scheduler.

## Prerequisites
Before starting, ensure you have:
- Python installed on your computer
- The project installed and working
- Environment variables set:
  - `AIRTABLE_API_KEY`
  - `AIRTABLE_BASE_ID`

## Setup Steps

### 1. Opening Task Scheduler
1. Press `Windows + R`
2. Type `taskschd.msc`
3. Click OK

### 2. Creating a New Task
1. In the Task Scheduler window, click "Create Basic Task" on the right
2. Enter the following details:
   - Name: `Airtable Backup`
   - Description: `Automatic backup of Airtable data`
3. Click Next

### 3. Setting the Schedule
1. Select "Daily"
2. Click Next
3. Set:
   - Start: Today's date
   - Time: `23:00` (or another time of your choice)
4. Click Next

### 4. Setting the Action
1. Select "Start a Program"
2. Click Next
3. Fill in the fields:
```
Program/script: pythonw
Add arguments: "C:\path\to\your\backup.py"  # Single backup file
Start in: C:\path\to\your\project\folder
```
> Important: Replace the paths with the actual paths on your computer

### 5. Advanced Settings
1. At the end of the wizard, check "Open the Properties dialog"
2. Click Finish
3. In the Properties window:
   - "General" tab:
     - Check "Run with highest privileges"
   - "Conditions" tab:
     - Uncheck "Start the task only if the computer is on AC power"
   - "Settings" tab:
     - Check "Run task as soon as possible after a scheduled start is missed"
     - Check "If the task fails, restart every:" and set to 5 minutes with maximum 3 attempts

### 6. Testing
1. Locate the task in the main Task Scheduler window
2. Right-click and select "Run"
3. Check the backup folder for a new backup file
4. Check the logs folder:
   ```
   C:\path\to\your\project\folder\logs
   ```

## Folder Structure and Files

```
project_folder/
├── logs/                # Log files
├── airtable_backups/    # Backup directory
└── src/
    └── backup.py       # Backup file to run
```

## Common Issues and Solutions

### Task Not Running
- Check that paths are correct
- Verify environment variables are set:
  ```cmd
  # Check environment variables
  echo %AIRTABLE_API_KEY%
  echo %AIRTABLE_BASE_ID%
  
  # Set environment variables if missing
  setx AIRTABLE_API_KEY your_key_here
  setx AIRTABLE_BASE_ID your_base_id_here
  ```
- Check backup directory permissions

### "Access Denied" Error
1. Open Task Scheduler as administrator
2. Ensure "Run with highest privileges" is checked
3. Verify the user running the task has admin rights

### No Backups Being Created
1. Run the backup manually from the terminal to check:
   ```cmd
   python src/backup.py
   ```
2. Check the log file
3. Verify enough disk space
4. Check API key validity

## Useful Task Scheduler Commands

### Run Task Manually
```cmd
SCHTASKS /RUN /TN "AirtableBackup"
```

### Check Task Status
```cmd
SCHTASKS /QUERY /TN "AirtableBackup"
```

### Update Run Time
```cmd
SCHTASKS /CHANGE /TN "AirtableBackup" /ST 23:00
```

### Delete Task
```cmd
SCHTASKS /DELETE /TN "AirtableBackup" /F
```

## Support

If you encounter an issue not covered in this guide:
1. Run the backup manually for testing
2. Check the log file
3. Open a new issue on GitHub
4. Include:
   - Full error message
   - Log file contents
   - Screenshot of Task settings

## Troubleshooting Examples

### Example 1: Task Shows "Last Run Result: 0x1"
This usually means there's a Python environment issue:
1. Verify Python is in PATH
2. Try running manually first
3. Check environment variables

### Example 2: "Could not find the directory"
This means the Start in path is incorrect:
1. Double-check all paths
2. Use full paths instead of relative
3. Verify folder permissions

### Example 3: "The system cannot find the specified file"
Common causes:
1. Wrong path to backup.py
2. Python not properly installed
3. Environment variables not set correctly

## Best Practices

1. **Regular Testing**
   - Run manual backup weekly
   - Check log files regularly
   - Verify backup file contents

2. **Maintenance**
   - Update API keys periodically
   - Clean old backup files
   - Monitor disk space

3. **Security**
   - Keep API keys secure
   - Use minimal permissions
   - Regularly audit task settings