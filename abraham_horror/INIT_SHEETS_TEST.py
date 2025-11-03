"""
Populate the shared Google Sheet with headers and sample rows.

Prefers service-account auth; falls back to OAuth desktop client if present.

Sheet: AI Oracle Integration
Tab: Sheet1
Columns:
  A: headline
  B: prompt
  C: tags (comma-separated)
"""
from pathlib import Path
from datetime import datetime

SHEET_ID = "1jvWP95U0ksaHw97PrPZsrh6ZVllviJJof7kQ2dV0ka0"
TAB_NAME = "Sheet1"

CREDS_SA = Path(r"F:\AI_Oracle_Root\scarify\config\credentials\google\service_account.json")
CLIENT_OAUTH = Path(r"F:\AI_Oracle_Root\scarify\config\credentials\google\oauth_client.json")
TOKEN_OAUTH = Path(r"F:\AI_Oracle_Root\scarify\abraham_horror\google_sheets_token.json")

def _gc_service_account():
    import gspread
    from google.oauth2.service_account import Credentials
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file(str(CREDS_SA), scopes=scopes)
    return gspread.authorize(creds)

def _gc_oauth():
    import gspread
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]

    creds = None
    if TOKEN_OAUTH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_OAUTH), scopes)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_OAUTH), scopes)
            creds = flow.run_local_server(port=0)
        TOKEN_OAUTH.write_text(creds.to_json())
    return gspread.authorize(creds)

def get_gc():
    try:
        if CREDS_SA.exists():
            return _gc_service_account()
    except Exception as e:
        print(f"[WARN] Service account auth failed: {e}")
    # OAuth fallback
    if CLIENT_OAUTH.exists():
        return _gc_oauth()
    raise FileNotFoundError("No Google auth found. Place service_account.json or oauth_client.json.")

def main():
    import gspread
    gc = get_gc()
    ws = gc.open_by_key(SHEET_ID).worksheet(TAB_NAME)

    # Write headers
    headers = [["headline", "prompt", "tags"]]
    ws.update("A1:C1", headers)

    # Append a few sample rows
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rows = [
        [f"Senate advances bill at {now}", "Punch-up and punch-down equally", "Politics,Lincoln,Satire"],
        ["Tech CEO says AI solves hunger by making ads better", "Chappelle style opener", "Tech,AI,Roast"],
        ["Markets rally on vibes and memes", "Carlin observation about marketing democracy", "Economy,Carlin"]
    ]
    ws.append_rows(rows, value_input_option="RAW")
    print("[OK] Sheet initialized with headers and sample rows.")

if __name__ == "__main__":
    main()





