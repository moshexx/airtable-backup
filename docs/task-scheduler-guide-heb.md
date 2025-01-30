# הגדרת Task Scheduler לגיבוי אוטומטי

מדריך זה יסביר כיצד להגדיר גיבוי יומי אוטומטי שיפעל ברקע ב-Windows באמצעות Task Scheduler.

## הכנות מקדימות
לפני שמתחילים, וודאו שיש לכם:
- Python מותקן במחשב
- הפרויקט מותקן ועובד
- משתני סביבה מוגדרים:
  - `AIRTABLE_API_KEY`
  - `AIRTABLE_BASE_ID`

## שלבי ההגדרה

### 1. פתיחת Task Scheduler
1. לחץ על `Windows + R`
2. הקלד `taskschd.msc`
3. לחץ OK

### 2. יצירת משימה חדשה
1. בחלון Task Scheduler, לחץ על "Create Basic Task" בצד ימין
2. הזן את הפרטים הבאים:
   - Name: `Airtable Backup`
   - Description: `גיבוי אוטומטי של נתוני Airtable`
3. לחץ Next

### 3. הגדרת תזמון
1. בחר "Daily"
2. לחץ Next
3. הגדר:
   - Start: התאריך של היום
   - Time: `23:00` (או שעה אחרת לבחירתך)
4. לחץ Next

### 4. הגדרת הפעולה
1. בחר "Start a Program"
2. לחץ Next
3. מלא את השדות:
```
Program/script: pythonw
Add arguments: "C:\path\to\your\backup.py"  # קובץ הגיבוי הבודד
Start in: C:\path\to\your\project\folder
```
> חשוב: החלף את הנתיבים בנתיבים האמיתיים במחשב שלך

### 5. הגדרות מתקדמות
1. בסיום האשף, סמן "Open the Properties dialog"
2. לחץ Finish
3. בחלון Properties:
   - לשונית "General":
     - סמן "Run with highest privileges"
   - לשונית "Conditions":
     - בטל "Start the task only if the computer is on AC power"
   - לשונית "Settings":
     - סמן "Run task as soon as possible after a scheduled start is missed"
     - סמן "If the task fails, restart every:" והגדר ל-5 דקות עם מקסימום 3 נסיונות

### 6. בדיקה
1. אתר את המשימה בחלון Task Scheduler הראשי
2. לחץ קליק ימני ובחר "Run"
3. בדוק בתיקיית הגיבויים שנוצר קובץ גיבוי חדש
4. בדוק את תיקיית הלוגים:
   ```
   C:\path\to\your\project\folder\logs
   ```

## מבנה תיקיות וקבצים

```
project_folder/
├── logs/                # קבצי לוג
├── airtable_backups/    # תיקיית גיבויים
└── src/
    └── backup.py       # קובץ הגיבוי שמריצים
```

## פתרון בעיות נפוצות

### המשימה לא רצה
- בדוק שהנתיבים נכונים
- וודא שמשתני הסביבה מוגדרים:
  ```cmd
  # בדיקת משתני סביבה
  echo %AIRTABLE_API_KEY%
  echo %AIRTABLE_BASE_ID%
  
  # הגדרת משתני סביבה אם חסרים
  setx AIRTABLE_API_KEY your_key_here
  setx AIRTABLE_BASE_ID your_base_id_here
  ```
- בדוק הרשאות בתיקיית הגיבוי

### שגיאת "Access Denied"
1. פתח Task Scheduler כמנהל
2. וודא שסימנת "Run with highest privileges"
3. בדוק שהמשתמש שמריץ את המשימה הוא מנהל

### לא נוצרים גיבויים
1. הרץ את הגיבוי ידנית מהטרמינל לבדיקה:
   ```cmd
   python src/backup.py
   ```
2. בדוק את קובץ הלוג
3. וודא שיש מספיק מקום בדיסק
4. בדוק שה-API key תקין

## פקודות שימושיות ב-Task Scheduler

### הפעלה ידנית של המשימה
```cmd
SCHTASKS /RUN /TN "AirtableBackup"
```

### בדיקת סטטוס המשימה
```cmd
SCHTASKS /QUERY /TN "AirtableBackup"
```

### עדכון זמן הריצה
```cmd
SCHTASKS /CHANGE /TN "AirtableBackup" /ST 23:00
```

### מחיקת המשימה
```cmd
SCHTASKS /DELETE /TN "AirtableBackup" /F
```

## תמיכה

אם נתקלתם בבעיה שלא מופיעה במדריך זה:
1. הריצו את הגיבוי ידנית לבדיקה
2. בדקו את קובץ הלוג
3. פתחו issue חדש בGitHub
4. צרפו:
   - הודעת שגיאה מלאה
   - תוכן קובץ הלוג
   - צילום מסך של הגדרות ה-Task