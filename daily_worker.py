import smtplib, time, pandas as pd, random, json, os, re
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import gspread
from google.oauth2.service_account import Credentials

# --- 1. CONFIGURATION (Loaded from GitHub Secrets) ---
EMAIL_USER = os.environ['EMAIL_USER']
EMAIL_PASS = os.environ['EMAIL_PASS']
SHEET_URL = os.environ['SHEET_URL']
GCP_JSON = json.loads(os.environ['GCP_SERVICE_ACCOUNT'])

# --- 2. DYNAMIC WARMUP LOGIC ---
def get_daily_limit():
    start_date = datetime(2026, 3, 16) # Today
    days_since = (datetime.now() - start_date).days
    # Day 1: 50 | Day 2: 100 | Day 3: 200 | Day 4: 400 | Day 5: 800 | Day 6: 1500 | Day 7: 2000
    limits = [50, 100, 200, 400, 800, 1500, 2000]
    if days_since < 0: return 50
    if days_since >= len(limits): return 2000
    return limits[days_since]

# --- 3. CONNECTION ---
scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(GCP_JSON, scopes=scopes)
gc = gspread.authorize(creds)
sh = gc.open_by_url(SHEET_URL)
worksheet = sh.sheet1
df = pd.DataFrame(worksheet.get_all_records())

# --- 4. HIGH-END HTML TEMPLATE ---
def get_html_content(name, category, address):
    # Address Cleaner
    display_address = "your city" if ("(" in str(address) or str(address).lower() == "n/a") else address
    greeting = random.choice(["Hi", "Hello", "Greetings"])
    
    return f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f4f7f9; color: #1a2b3c; margin: 0; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 12px; overflow: hidden; border: 1px solid #e2e8f0;">
            <div style="background-color: #0f172a; padding: 30px; text-align: center;">
                <h1 style="color: #2dd4bf; margin: 0; font-size: 24px; letter-spacing: 2px;">STOP WEB RENT</h1>
            </div>
            <div style="padding: 40px;">
                <h2 style="color: #0f172a; font-size: 20px;">{greeting} {name} team,</h2>
                <p style="line-height: 1.7;">I was researching <strong>{category}</strong> services in <strong>{display_address}</strong> and noticed your clinic has an outstanding reputation. However, you are currently missing a critical asset: <strong>A "Website" button on your Google Maps profile.</strong></p>
                <div style="background-color: #fff1f2; border-left: 5px solid #f43f5e; padding: 15px; margin: 20px 0; color: #9f1239;">
                    <strong>The 2026 Ranking Risk:</strong> Google now prioritizes clinics with linked, high-speed websites. Without that button, you are losing patients to competitors daily.
                </div>
                <p>I build 0.1s speed websites with <strong>$0 monthly hosting fees</strong>. View my tech demo here: <a href="https://hv-furniture-bit.github.io/dental-junction-behala/index.html" style="color: #0d9488; font-weight: bold;">Ghosh Dental Demo</a></p>
                <div style="text-align: center; margin-top: 30px;">
                    <a href="https://wa.me/966572562151?text=YES" style="background-color: #0d9488; color: #ffffff; padding: 15px 25px; text-decoration: none; border-radius: 8px; font-weight: bold; display: block;">REPLY 'YES' FOR FREE 24-HOUR PREVIEW</a>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

# --- 5. EXECUTION ---
headers = [h.strip() for h in worksheet.row_values(1)]
col_status = headers.index("Email_Status") + 1
col_date = headers.index("Last_Sent_Date") + 1

daily_limit = get_daily_limit()
print(f"🚀 Running Daily Outreach. Limit for today: {daily_limit}")

server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.login(EMAIL_USER, EMAIL_PASS)

sent_count = 0
for index, row in df.iterrows():
    if sent_count >= daily_limit: break
    
    email = str(row.get('Email', '')).strip()
    name = str(row.get('Business Name', 'Clinic')).strip()
    cat = "Dental" if "n/a" in str(row.get('Category', '')).lower() else str(row.get('Category', ''))
    addr = str(row.get('Address', 'your area'))
    status = str(row.get('Email_Status', ''))

    if "@" in email and "Sent" not in status:
        msg = MIMEMultipart()
        msg['From'] = f"Kiran Deb Mondal <{EMAIL_USER}>"
        msg['To'] = email
        msg['Subject'] = f"Question regarding {name}'s Google Maps Profile"
        msg.attach(MIMEText(get_html_content(name, cat, addr), 'html'))

        try:
            server.send_message(msg)
            worksheet.update_cell(index + 2, col_status, "Sent")
            worksheet.update_cell(index + 2, col_date, datetime.now().strftime("%Y-%m-%d"))
            sent_count += 1
            print(f"✅ [{sent_count}] Sent to {name}")
            time.sleep(random.randint(45, 90))
        except Exception as e:
            print(f"❌ Failed for {name}: {e}")

server.quit()
print(f"🏆 Batch Finished. Total: {sent_count}")
