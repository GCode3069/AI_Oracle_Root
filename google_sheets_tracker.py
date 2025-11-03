#!/usr/bin/env python3
"""
GOOGLE SHEETS TRACKER FOR ABRAHAM LINCOLN VIDEOS
Auto-tracks: Episode, Headline, Upload Date, YouTube URL, Views, Retention
"""
import os
from pathlib import Path
from datetime import datetime

def setup_google_sheets():
    """
    Setup Google Sheets API
    Instructions: https://developers.google.com/sheets/api/quickstart/python
    """
    instructions = """
GOOGLE SHEETS TRACKING SETUP:

1. Go to: https://console.cloud.google.com/
2. Create new project: "Abraham Lincoln Tracker"
3. Enable Google Sheets API
4. Create Service Account
5. Download credentials JSON
6. Save to: config/google_sheets_credentials.json
7. Create Google Sheet, share with service account email
8. Set environment variable: GOOGLE_SHEETS_ID=your_sheet_id

SHEET STRUCTURE:
- Column A: Episode Number
- Column B: Headline
- Column C: Upload Date
- Column D: Script Length (words)
- Column E: Video Path
- Column F: YouTube URL
- Column G: Views (manual update or API)
- Column H: Retention % (manual update or API)
- Column I: Status (Active/Archived)
"""
    print(instructions)

def log_video_to_sheets(episode_num, headline, script_length, video_path, youtube_url=""):
    """Log video generation to Google Sheets"""
    try:
        from google.oauth2.service_account import Credentials
        from googleapiclient.discovery import build
        
        # Paths
        base_dir = Path("F:/AI_Oracle_Root/scarify")
        creds_file = base_dir / "config" / "google_sheets_credentials.json"
        
        if not creds_file.exists():
            print("[Sheets] Credentials not found. Run setup_google_sheets() for instructions.")
            # Fallback: Log to local CSV
            return log_to_csv(episode_num, headline, script_length, video_path, youtube_url)
        
        # Get Sheet ID from environment
        sheet_id = os.getenv('GOOGLE_SHEETS_ID', '')
        if not sheet_id:
            print("[Sheets] GOOGLE_SHEETS_ID not set. Using local CSV fallback.")
            return log_to_csv(episode_num, headline, script_length, video_path, youtube_url)
        
        # Authenticate
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        creds = Credentials.from_service_account_file(str(creds_file), scopes=SCOPES)
        service = build('sheets', 'v4', credentials=creds)
        
        # Prepare data
        row_data = [[
            episode_num,
            headline[:100],  # Truncate long headlines
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            script_length,
            str(video_path),
            youtube_url if youtube_url else 'Pending',
            '',  # Views (manual update)
            '',  # Retention (manual update)
            'Active'
        ]]
        
        # Append to sheet
        body = {'values': row_data}
        result = service.spreadsheets().values().append(
            spreadsheetId=sheet_id,
            range='Sheet1!A:I',
            valueInputOption='USER_ENTERED',
            insertDataOption='INSERT_ROWS',
            body=body
        ).execute()
        
        print(f"[Sheets] [OK] Logged episode #{episode_num} to Google Sheets")
        return True
        
    except Exception as e:
        print(f"[Sheets] Error: {e}")
        return log_to_csv(episode_num, headline, script_length, video_path, youtube_url)

def log_to_csv(episode_num, headline, script_length, video_path, youtube_url=""):
    """Fallback: Log to local CSV file"""
    try:
        base_dir = Path("F:/AI_Oracle_Root/scarify")
        csv_file = base_dir / "video_tracking.csv"
        
        # Create CSV if doesn't exist
        if not csv_file.exists():
            with open(csv_file, 'w', encoding='utf-8') as f:
                f.write("Episode,Headline,Upload Date,Script Length,Video Path,YouTube URL,Views,Retention,Status\n")
        
        # Append row
        with open(csv_file, 'a', encoding='utf-8') as f:
            row = (
                f"{episode_num},"
                f'"{headline[:100]}",'
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')},"
                f"{script_length},"
                f'"{video_path}",'
                f"{youtube_url if youtube_url else 'Pending'},"
                f"0,0,Active\n"
            )
            f.write(row)
        
        print(f"[CSV] [OK] Logged episode #{episode_num} to CSV")
        return True
    except Exception as e:
        print(f"[CSV] Error: {e}")
        return False

def update_video_metrics(episode_num, views, retention):
    """Update views and retention for a video (requires Sheet ID)"""
    try:
        from google.oauth2.service_account import Credentials
        from googleapiclient.discovery import build
        
        base_dir = Path("F:/AI_Oracle_Root/scarify")
        creds_file = base_dir / "config" / "google_sheets_credentials.json"
        sheet_id = os.getenv('GOOGLE_SHEETS_ID', '')
        
        if not creds_file.exists() or not sheet_id:
            print("[Sheets] Not configured")
            return False
        
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        creds = Credentials.from_service_account_file(str(creds_file), scopes=SCOPES)
        service = build('sheets', 'v4', credentials=creds)
        
        # Find row with episode number
        result = service.spreadsheets().values().get(
            spreadsheetId=sheet_id,
            range='Sheet1!A:I'
        ).execute()
        
        values = result.get('values', [])
        for i, row in enumerate(values):
            if row and str(row[0]) == str(episode_num):
                # Update views (column G) and retention (column H)
                row_num = i + 1
                service.spreadsheets().values().update(
                    spreadsheetId=sheet_id,
                    range=f'Sheet1!G{row_num}:H{row_num}',
                    valueInputOption='USER_ENTERED',
                    body={'values': [[views, retention]]}
                ).execute()
                print(f"[Sheets] [OK] Updated episode #{episode_num}: {views} views, {retention}% retention")
                return True
        
        print(f"[Sheets] Episode #{episode_num} not found")
        return False
    except Exception as e:
        print(f"[Sheets] Error: {e}")
        return False

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "setup":
        setup_google_sheets()
    else:
        # Test logging
        log_video_to_sheets(
            episode_num=9999,
            headline="Test Headline for Tracking",
            script_length=35,
            video_path="test/path/video.mp4",
            youtube_url="https://youtube.com/watch?v=TEST123"
        )

