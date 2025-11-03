from pathlib import Path
from typing import List, Tuple
import csv
import io
import requests

def _get_creds_path() -> Path:
    # Default location for the Google service account JSON
    return Path(r"F:\AI_Oracle_Root\scarify\config\credentials\google\service_account.json")

def read_sheet_rows(sheet_id: str, tab_name: str = "Sheet1", max_rows: int = 200) -> List[List[str]]:
    """Read rows from a Google Sheet using a service account (read-only).

    Returns a list of rows (each row is List[str]), skipping the header row.
    """
    try:
        import gspread
        from google.oauth2.service_account import Credentials

        scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
        creds_path = _get_creds_path()
        creds = Credentials.from_service_account_file(str(creds_path), scopes=scopes)
        gc = gspread.authorize(creds)
        ws = gc.open_by_key(sheet_id).worksheet(tab_name)
        rows = ws.get_all_values()
        return [r for r in rows[1:max_rows+1] if any(c.strip() for c in r)]
    except Exception as e:
        # If service account path missing or auth fails, attempt public CSV access
        print(f"    [WARNING] Sheets auth failed, trying public link: {e}")
        try:
            # Public CSV export (works if sheet is shared: Anyone with link)
            url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={tab_name}"
            resp = requests.get(url, timeout=20)
            if resp.status_code == 200 and resp.content:
                text = resp.content.decode('utf-8', errors='ignore')
                reader = csv.reader(io.StringIO(text))
                rows = list(reader)
                return [r for r in rows[1:max_rows+1] if any((c or '').strip() for c in r)]
        except Exception as ee:
            print(f"    [WARNING] Public CSV read failed: {ee}")
        return []

def read_headlines(sheet_id: str, tab_name: str = "Sheet1", max_rows: int = 200) -> Tuple[List[str], List[str], List[str]]:
    """Return (headlines, prompts, tags) from columns A, B, C respectively."""
    rows = read_sheet_rows(sheet_id, tab_name, max_rows)
    headlines = []
    prompts = []
    tags = []
    for r in rows:
        if len(r) >= 1 and r[0].strip():
            headlines.append(r[0].strip())
        if len(r) >= 2 and r[1].strip():
            prompts.append(r[1].strip())
        if len(r) >= 3 and r[2].strip():
            tags.append(r[2].strip())
    return headlines, prompts, tags


