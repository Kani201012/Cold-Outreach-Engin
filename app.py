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

st.set_page_config(page_title="Stop Web Rent | Professional Outreach", page_icon="🛡️", layout="wide")

# --- GOOGLE SHEETS CONNECTION ---
@st.cache_resource
def init_connection():
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    credentials = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scopes)
    return gspread.authorize(credentials)

gc = init_connection()

# --- SPINTAX PARSER ---
def parse_spintax(text):
    pattern = re.compile(r'\{([^{}]*)\}')
    while True:
        match = pattern.search(text)
        if not match: break
        options = match.group(1).split('|')
        text = text[:match.start()] + random.choice(options) + text[match.end():]
    return text

# --- HTML UI ENGINE (Fixed Curly Bracket Bug) ---
def get_professional_template(greeting, name, category, address):
    # Clean the address: if it contains a rating like 4.7(39), hide it
    if "(" in address and "." in address:
        display_address = "your area"
    else:
        display_address = address

    html = f"""
    <html>
    <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Arial, sans-serif; background-color: #f0f2f5; color: #1a1a1a;">
        <div style="max-width: 600px; margin: 20px auto; background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.08); border: 1px solid #e1e4e8;">
            <div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding: 40px 20px; text-align: center;">
                <h1 style="color: #2dd4bf; margin: 0; font-size: 28px; font-weight: 800; text-transform: uppercase; letter-spacing: 2px;">STOP WEB RENT</h1>
                <p style="color: #94a3b8; margin: 8px 0 0 0; font-size: 14px;">High-Velocity Web Architecture</p>
            </div>
            <div style="padding: 40px 35px;">
                <h2 style="color: #0f172a; font-size: 22px; margin-top: 0;">{greeting} {name} team,</h2>
                <p style="font-size: 16px; line-height: 1.7; color: #475569;">
                    I was recently researching <strong>{category}</strong> services in <strong>{display_address}</strong> and noticed your clinic has an outstanding reputation. However, you are currently missing a critical asset: <strong>A "Website" button on your Google Maps profile.</strong>
                </p>
                <div style="background-color: #fff1f2; border-left: 5px solid #f43f5e; padding: 20px; margin: 30px 0;">
                    <strong style="color: #9f1239;">The 2026 Ranking Risk:</strong><br>
                    <span style="color: #be123c;">Google now prioritizes clinics with linked, high-speed websites. Without that button, you are losing high-value patients to competitors every single day.</span>
                </div>
                <table style="width: 100%; border-collapse: collapse; margin: 25px 0; font-size: 14px; border: 1px solid #e2e8f0;">
                    <tr style="background-color: #f8fafc;">
                        <th style="padding: 12px; text-align: left; border-bottom: 2px solid #e2e8f0;">Cost Category</th>
                        <th style="padding: 12px; text-align: center; border-bottom: 2px solid #e2e8f0; color: #0d9488;">Titan Engine</th>
                        <th style="padding: 12px; text-align: center; border-bottom: 2px solid #e2e8f0;">Wix/Shopify</th>
                    </tr>
                    <tr>
                        <td style="padding: 12px; border-bottom: 1px solid #e2e8f0;">Annual Rent</td>
                        <td style="padding: 12px; text-align: center; border-bottom: 1px solid #e2e8f0; font-weight: bold; color: #0d9488;">$0</td>
                        <td style="padding: 12px; text-align: center; border-bottom: 1px solid #e2e8f0;">$348+</td>
                    </tr>
                    <tr style="background-color: #f0fdfa;">
                        <td style="padding: 12px; font-weight: bold;">5-Year Total</td>
                        <td style="padding: 12px; text-align: center; font-weight: 800; color: #0d9488;">$274</td>
                        <td style="padding: 12px; text-align: center;">$2,115</td>
                    </tr>
                </table>
                <div style="text-align: center; margin-top: 35px;">
                    <a href="https://wa.me/966572562151?text=YES" style="background-color: #0d9488; color: #ffffff; padding: 16px 30px; text-decoration: none; border-radius: 8px; font-weight: 700; display: block; margin-bottom: 15px; font-size: 16px;">REPLY 'YES' FOR FREE DEMO</a>
                    <a href="https://kiranmondal.gumroad.com/l/titanv50" style="color: #0d9488; font-size: 14px; font-weight: 600;">GET Your Website within 24 Hours (Direct Purchase)</a>
                </div>
            </div>
            <div style="background-color: #f8fafc; padding: 35px; text-align: center; border-top: 1px solid #e2e8f0; font-size: 12px; color: #64748b;">
                <p><strong>Kiran Deb Mondal</strong> | Principal Business Technologist</p>
                <p><a href="https://www.StopWebRent.com" style="color: #0d9488; text-decoration: none;">www.StopWebRent.com</a></p>
            </div>
        </div>
    </body>
    </html>
    """
    return html

# --- STREAMLIT APP ---
st.title("🛡️ Stop Web Rent Outreach Engine")

with st.expander("⚙️ Settings & Credentials", expanded=True):
    col1, col2 = st.columns(2)
    smtp_user = col1.text_input("Workspace Email", value="kiran@kaydiemscriptlab.com")
    smtp_pass = col2.text_input("App Password", type="password")
    sheet_url = st.text_input("Google Sheet URL")

if sheet_url:
    try:
        sh = gc.open_by_url(sheet_url)
        worksheet = sh.sheet1
        data = worksheet.get_all_records()
        df = pd.DataFrame(data)
        
        st.success(f"✅ Connected to Sheet! {len(df)} leads found.")
        limit = st.number_input("Send Limit", value=50)
        
        if st.button("🚀 LAUNCH CAMPAIGN", type="primary"):
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(smtp_user, smtp_pass)
            
            # --- FIXED COLUMN MAPPING ---
            headers = [h.strip() for h in worksheet.row_values(1)]
            col_status_idx = headers.index("Email_Status") + 1 if "Email_Status" in headers else 15
            col_date_idx = headers.index("Last_Sent_Date") + 1 if "Last_Sent_Date" in headers else 16

            sent = 0
            for index, row in df.iterrows():
                if sent >= limit: break
                
                email = str(row.get('Email', '')).strip()
                name = str(row.get('Business Name', 'Clinic')).strip()
                cat = str(row.get('Category', 'Dental')).strip()
                addr = str(row.get('Address', 'your area')).strip()
                status = str(row.get('Email_Status', ''))

                if "@" not in email or "Sent" in status: continue
                
                # Logic Fixes
                greeting = random.choice(["Hi", "Hello", "Greetings"])
                subject = parse_spintax("{Quick question|Inquiry} regarding " + name)
                
                html_body = get_professional_template(greeting, name, cat, addr)
                
                msg = MIMEMultipart()
                msg['From'] = f"Kiran Deb Mondal <{smtp_user}>"
                msg['To'] = email
                msg['Subject'] = subject
                msg.attach(MIMEText(html_body, 'html'))
                
                try:
                    server.send_message(msg)
                    # --- FIXED UPDATE LOGIC ---
                    worksheet.update_cell(index + 2, col_status_idx, "Sent")
                    worksheet.update_cell(index + 2, col_date_idx, datetime.now().strftime("%Y-%m-%d"))
                    
                    sent += 1
                    st.write(f"✅ [{sent}] Sent to {name}")
                    time.sleep(random.randint(60, 100))
                except Exception as e:
                    st.error(f"Error sending to {email}: {e}")

            server.quit()
            st.success("Batch Complete!")
            st.balloons()
            
    except Exception as e:
        st.error(f"Error: {e}")
