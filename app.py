import streamlit as st
import pandas as pd
import smtplib
import time
import random
import re
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="Stop Web Rent | Outreach Engine", page_icon="🛡️", layout="wide")

# --- 1. PERMANENT CONNECTION (Using Secrets) ---
@st.cache_resource
def init_connection():
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    return gspread.authorize(Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scopes))

gc = init_connection()

# --- 2. SPINTAX PARSER (Instantly.ai Standard) ---
def parse_spintax(text):
    pattern = re.compile(r'\{([^{}]*)\}')
    while True:
        match = pattern.search(text)
        if not match: break
        options = match.group(1).split('|')
        text = text[:match.start()] + random.choice(options) + text[match.end():]
    return text

# --- 3. THE PROFESSIONAL HTML UI ENGINE ---
def get_html_layout(greeting, name, category, address, is_followup=False):
    # Address/Category Cleaner
    display_address = "your city" if ("(" in str(address) or str(address).lower() == "n/a") else address
    display_cat = "Dental" if str(category).lower() == "n/a" else category
    
    # Step 1: Initial Pitch Content
    content_step_1 = f"""
    <p style="font-size: 16px; line-height: 1.7; color: #334155;">
        I was recently researching on <strong>{display_cat}</strong> clinics in {display_address} and noticed that your clinic has a fantastic reputation on Google Maps.
    </p>
    <p style="font-size: 16px; line-height: 1.7; color: #334155;">
        However, I noticed you don’t have a website linked to your profile. I am reaching out because, as of 2026, <strong>Google’s algorithm has significantly increased the weight of linked websites</strong> for local rankings.
    </p>
    <div style="background-color: #fff1f2; border-left: 5px solid #f43f5e; padding: 20px; margin: 30px 0; border-radius: 4px;">
        <strong style="color: #9f1239; font-size: 17px;">⚠️ The Risk:</strong><br>
        <span style="color: #be123c;">If your competitors have a "Website" button and you don’t, Google’s AI search will eventually lower your visibility in the Map Pack.</span>
    </div>
    <h3 style="color: #0f172a; font-size: 18px; border-bottom: 2px solid #2dd4bf; display: inline-block;">The Solution: Titan Engine</h3>
    <p style="font-size: 16px; line-height: 1.7; color: #334155;">
        I build <strong>0.1s Load Speed</strong> frameworks designed to help local services dominate without "Web Rent" (monthly subscriptions).
    </p>
    <div style="text-align: center; margin: 25px 0;">
        <a href="https://hv-furniture-bit.github.io/dental-junction-behala/index.html" style="color: #0d9488; font-weight: 700; text-decoration: underline; font-size: 18px;">View the live tech demo here: Ghosh Dental Clinic</a>
    </div>
    """

    # Step 2: Follow-up Content
    content_step_2 = f"""
    <p style="font-size: 16px; line-height: 1.7; color: #334155;">
        I'm just bumping this to the top of your inbox. Did you have a chance to see my previous note about the Google Maps ranking for <strong>{name}</strong>?
    </p>
    <p style="font-size: 16px; line-height: 1.7; color: #334155;">
        In 2026, missing a high-speed website is the #1 reason clinics lose their "Top 3" spot on Google. I'd love to show you how our Titan Engine architecture can stop your "Web Rent" forever.
    </p>
    """

    main_body = content_step_2 if is_followup else content_step_1

    return f"""
    <html>
    <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Arial, sans-serif; background-color: #f8fafc; color: #1e293b;">
        <div style="max-width: 650px; margin: 20px auto; background-color: #ffffff; border-radius: 15px; overflow: hidden; box-shadow: 0 15px 35px rgba(0,0,0,0.1); border: 1px solid #e2e8f0;">
            <div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding: 45px 20px; text-align: center;">
                <h1 style="color: #2dd4bf; margin: 0; font-size: 28px; font-weight: 800; letter-spacing: 2px;">STOP WEB RENT</h1>
                <p style="color: #94a3b8; margin: 8px 0 0 0; font-size: 13px;">High-Velocity Web Architecture</p>
            </div>
            <div style="padding: 45px 40px;">
                <h2 style="color: #0f172a; font-size: 20px; margin-top: 0;">{greeting} {name} team,</h2>
                {main_body}
                
                <table style="width: 100%; border-collapse: collapse; margin: 25px 0; font-size: 13px; border: 1px solid #e2e8f0;">
                    <tr style="background-color: #0f172a; color: #ffffff;"><th style="padding: 12px; text-align: left;">Category</th><th style="padding: 12px;">Titan Engine</th><th style="padding: 12px;">Wix / Shopify</th></tr>
                    <tr><td style="padding: 12px; border-bottom: 1px solid #eee;">Monthly Rent</td><td style="padding: 12px; text-align: center; color: #0d9488; font-weight: bold;">$0</td><td style="padding: 12px; text-align: center;">$35+</td></tr>
                    <tr style="background-color: #f0fdfa;"><td style="padding: 12px; font-weight: bold;">5-Year Savings</td><td style="padding: 12px; text-align: center; font-weight: 800; color: #0d9488;">$1,841</td><td style="padding: 12px; text-align: center;">$0</td></tr>
                </table>

                <p style="font-size: 16px; font-weight: bold; color: #0f172a; text-align: center; margin-top: 30px;">
                    My Offer: A Free 24-Hour Preview (Using your logo & photos)
                </p>

                <div style="text-align: center; margin-top: 40px;">
                    <a href="https://wa.me/966572562151?text=YES" style="background-color: #0d9488; color: #ffffff; padding: 18px 35px; text-decoration: none; border-radius: 10px; font-weight: 800; display: block; font-size: 18px;">REPLY 'YES' FOR FREE DEMO</a>
                    <div style="margin-top: 20px;">
                        <a href="https://kiranmondal.gumroad.com/l/titanv50" style="color: #0d9488; font-size: 15px; font-weight: 700;">GET Your Website within 24 Hours (Buy Now)</a>
                    </div>
                </div>
            </div>
            <div style="background-color: #f8fafc; padding: 40px; text-align: center; border-top: 1px solid #e2e8f0; font-size: 12px; color: #64748b;">
                <p><strong>Kiran Deb Mondal</strong> | Principal Technologist | Stop Web Rent</p>
                <p>WhatsApp: +966 572562151 | <a href="https://www.StopWebRent.com" style="color: #0d9488;">www.StopWebRent.com</a></p>
            </div>
        </div>
    </body>
    </html>
    """

# --- 4. STREAMLIT UI SIDEBAR (PRE-FILLED) ---
with st.sidebar:
    st.title("⚙️ Credentials")
    
    # We pull from st.secrets and use it as the 'value'
    stored_email = st.secrets.get("EMAIL_USER", "kiran@kaydiemscriptlab.com")
    stored_pass = st.secrets.get("EMAIL_PASS", "")
    stored_url = st.secrets.get("SHEET_URL", "")

    user_email = st.text_input("Sender Email", value=stored_email)
    app_pass = st.text_input("App Password", value=stored_pass, type="password")
    sheet_url = st.text_input("Google Sheet URL", value=stored_url)
    
    if app_pass and sheet_url:
        st.success("✅ Credentials Loaded from Secrets")
    else:
        st.warning("⚠️ Some secrets are missing in Streamlit Settings")

# --- 5. MAIN LOGIC ---
st.title("🛡️ Master Outreach Engine")

if sheet_url:
    try:
        sh = gc.open_by_url(sheet_url)
        worksheet = sh.sheet1
        
        # --- ROBUST SPREADSHEET PARSER ---
        # 1. Get all raw data as a list of lists instead of dicts
        raw_data = worksheet.get_all_values()
        
        if not raw_data:
            st.error("Google Sheet is completely empty!")
            st.stop()
            
        # 2. Extract Row 1 (Headers)
        raw_headers = raw_data[0]
        
        # 3. Clean headers (give generic names to empty/duplicate columns)
        clean_headers = []
        for i, h in enumerate(raw_headers):
            h_str = str(h).strip()
            if not h_str:
                clean_headers.append(f"EmptyColumn_{i}")
            else:
                clean_headers.append(h_str)
                
        # 4. Create the Pandas DataFrame safely
        df = pd.DataFrame(raw_data[1:], columns=clean_headers)
        st.success(f"✅ Connection Stable. {len(df)} leads loaded.")

        limit = st.number_input("Batch Send Limit", value=50)

        if st.button("🚀 LAUNCH PROFESSIONAL CAMPAIGN", type="primary"):
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(user_email, app_pass)

            # Auto-Mapping Headers
            headers = [h.strip() for h in worksheet.row_values(1)]
            col_status = headers.index("Email_Status") + 1
            col_date = headers.index("Last_Sent_Date") + 1
            col_step = headers.index("Sequence_Step") + 1

            sent_count = 0
            for index, row in df.iterrows():
                if sent_count >= limit: break
                
                email = str(row.get('Email', '')).strip()
                name = str(row.get('Business Name', 'Clinic')).strip()
                category = str(row.get('Category', 'Dental'))
                address = str(row.get('Address', 'your area'))
                
                status = str(row.get('Email_Status', ''))
                step = str(row.get('Sequence_Step', '0'))
                step = 0 if step == "" else int(step)
                last_date_str = str(row.get('Last_Sent_Date', ''))

                # --- SEQUENCE LOGIC ---
                send_now = False
                is_followup = False
                new_step = step

                if step == 0 and "Sent" not in status:
                    send_now = True
                    new_step = 1
                elif step == 1 and last_date_str and status != "Replied":
                    last_date = datetime.strptime(last_date_str, "%Y-%m-%d")
                    if (datetime.now() - last_date).days >= 3:
                        send_now = True
                        is_followup = True
                        new_step = 2

                if "@" in email and send_now:
                    greeting = parse_spintax("{Hi|Hello|Greetings|Hey there}")
                    subject_prefix = "{Follow up:|Update:|Re:}" if is_followup else "{Question|Inquiry|Important note}"
                    subject = parse_spintax(f"{subject_prefix} regarding {name}'s Google Maps Profile")
                    
                    html_body = get_html_layout(greeting, name, category, address, is_followup)

                    msg = MIMEMultipart()
                    msg['From'] = f"Kiran Deb Mondal <{user_email}>"
                    msg['To'] = email
                    msg['Subject'] = subject
                    msg.attach(MIMEText(html_body, 'html'))

                    try:
                        server.send_message(msg)
                        # UPDATE SHEET IN REAL-TIME
                        worksheet.update_cell(index + 2, col_status, f"Step {new_step} Sent")
                        worksheet.update_cell(index + 2, col_date, datetime.now().strftime("%Y-%m-%d"))
                        worksheet.update_cell(index + 2, col_step, new_step)
                        
                        sent_count += 1
                        st.write(f"✅ [{sent_count}] Sent Step {new_step} to {name}")
                        time.sleep(random.randint(60, 110))
                    except:
                        st.write(f"❌ Failed for {name}")

            server.quit()
            st.success("Campaign Session Finished!")
            st.balloons()
            
    except Exception as e:
        st.error(f"Error: {e}")
