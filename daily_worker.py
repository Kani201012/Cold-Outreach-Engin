import smtplib, time, pandas as pd, random, json, os
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import gspread
from google.oauth2.service_account import Credentials

# --- 1. CONFIGURATION (Loaded from GitHub Secrets) ---
EMAIL_USER = os.environ['EMAIL_USER']
EMAIL_PASS = os.environ['EMAIL_PASS']
SHEET_URL = os.environ['SHEET_URL']
# The JSON key for the Robot User
GCP_JSON = json.loads(os.environ['GCP_SERVICE_ACCOUNT'])

# --- 2. DYNAMIC WARMUP LOGIC ---
# Day 1: 50 | Day 2: 100 | Day 3: 200 | Day 4: 400 | Day 5: 800 | Day 6: 1500 | Day 7: 2000
def get_daily_limit():
    start_date = datetime(2026, 3, 16) # Set this to today's date
    days_since_start = (datetime.now() - start_date).days
    limits = [50, 100, 200, 400, 800, 1500, 2000]
    if days_since_start < 0: return 50
    if days_since_start >= len(limits): return 2000
    return limits[days_since_start]

# --- 3. CONNECTION ---
scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(GCP_JSON, scopes=scopes)
gc = gspread.authorize(creds)
sh = gc.open_by_url(SHEET_URL)
worksheet = sh.sheet1
df = pd.DataFrame(worksheet.get_all_records())

# --- 4. TEMPLATE ENGINE ---
def get_html_body(name, category, address):
    # (Use the professional HTML template code from our previous chat here)
    # For brevity, I'm assuming you'll paste the 'get_professional_html' function here
    pass 

# --- 5. EXECUTION ---
headers = [h.strip() for h in worksheet.row_values(1)]
col_status = headers.index("Email_Status") + 1
col_date = headers.index("Last_Sent_Date") + 1
col_step = headers.index("Sequence_Step") + 1

daily_limit = get_daily_limit()
print(f"🚀 Day {(datetime.now() - datetime(2026, 3, 16)).days + 1} Outreach. Limit: {daily_limit}")

server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.login(EMAIL_USER, EMAIL_PASS)

sent_count = 0
for index, row in df.iterrows():
    if sent_count >= daily_limit: break
    
    email = str(row.get('Email', '')).strip()
    status = str(row.get('Email_Status', ''))
    
    if "@" in email and "Sent" not in status:
        # Send Logic (MIMEMultipart, etc.)
        # ... [Same sending logic as app.py] ...
        
        # Update Sheet
        worksheet.update_cell(index + 2, col_status, "Sent")
        worksheet.update_cell(index + 2, col_date, datetime.now().strftime("%Y-%m-%d"))
        worksheet.update_cell(index + 2, col_step, 1)
        
        sent_count += 1
        print(f"✅ Sent to {email}")
        time.sleep(random.randint(60, 100))

server.quit()
print(f"🏆 Batch Finished. Total sent: {sent_count}")
