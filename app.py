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

st.set_page_config(page_title="Stop Web Rent | Professional Engine", page_icon="🛡️", layout="wide")

# --- GOOGLE SHEETS CONNECTION ---
@st.cache_resource
def init_connection():
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"], scopes=scopes
    )
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

# --- MODERN HTML UI ENGINE ---
def get_html_layout(greeting, name, category, address, is_followup=False):
    # Address Cleaner
    display_address = "your area" if ("(" in address or address.lower() == "n/a") else address
    
    # Step 1 Content
    content_initial = f"""
    <p style="font-size: 16px; line-height: 1.7; color: #475569;">
        I was recently researching <strong>{category}</strong> services in <strong>{display_address}</strong> and noticed your clinic has an outstanding reputation. However, you are currently missing a critical asset: <strong>A "Website" button on your Google Maps profile.</strong>
    </p>
    <div style="background-color: #fff1f2; border-left: 5px solid #f43f5e; padding: 20px; margin: 30px 0;">
        <strong style="color: #9f1239; font-size: 16px;">The 2026 Ranking Risk:</strong><br>
        <span style="color: #be123c;">Google now prioritizes clinics with linked, high-speed websites. Without that button, you are losing high-value patients to competitors every single day.</span>
    </div>
    """
    
    # Step 2 Content (Follow-up)
    content_followup = f"""
    <p style="font-size: 16px; line-height: 1.7; color: #475569;">
        I'm just bumping this to the top of your inbox. Did you have a chance to see my previous note about the Google Maps ranking for <strong>{name}</strong>?
    </p>
    <p style="font-size: 16px; line-height: 1.7; color: #475569;">
        In 2026, the absence of a 'Website' button on your profile is the #1 reason for dropping out of the Top 3 Map Pack.
    </p>
    """

    main_text = content_followup if is_followup else content_initial

    return f"""
    <html>
    <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Arial, sans-serif; background-color: #f4f7f9;">
        <div style="max-width: 600px; margin: 20px auto; background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
            <div style="background-color: #0f172a; padding: 35px; text-align: center;">
                <h1 style="color: #2dd4bf; margin: 0; font-size: 26px; letter-spacing: 2px;">STOP WEB RENT</h1>
                <p style="color: #94a3b8; margin: 5px 0 0 0; font-size: 13px;">High-Velocity Web Frameworks</p>
            </div>
            <div style="padding: 40px;">
                <h2 style="color: #0f172a; font-size: 20px;">{greeting} {name} team,</h2>
                {main_text}
                <table style="width: 100%; border-collapse: collapse; margin: 25px 0; font-size: 14px; border: 1px solid #e2e8f0;">
                    <tr style="background-color: #f8fafc;">
                        <th style="padding: 12px; text-align: left;">Category</th>
                        <th style="padding: 12px; text-align: center; color: #0d9488;">Titan Engine</th>
                        <th style="padding: 12px; text-align: center;">Wix/Shopify</th>
                    </tr>
                    <tr>
                        <td style="padding: 12px; border-top: 1px solid #eee;">Monthly Rent</td>
                        <td style="padding: 12px; text-align: center; font-weight: bold; color: #0d9488; border-top: 1px solid #eee;">$0</td>
                        <td style="padding: 12px; text-align: center; border-top: 1px solid #eee;">$35+</td>
                    </tr>
                    <tr style="background-color: #f0fdfa;">
                        <td style="padding: 12px; font-weight: bold;">5-Year Savings</td>
                        <td style="padding: 12px; text-align: center; font-weight: 800; color: #0d9488;">$1,841</td>
                        <td style="padding: 12px; text-align: center;">$0</td>
                    </tr>
                </table>
                <div style="text-align: center; margin-top: 35px;">
                    <a href="https://wa.me/966572562151?text=YES" style="background-color: #0d9488; color: #ffffff; padding: 16px 30px; text-decoration: none; border-radius: 8px; font-weight: bold; display: block;">REPLY 'YES' FOR FREE DEMO</a>
                    <br>
                    <a href="https://kiranmondal.gumroad.com/l/titanv50" style="color: #0d9488; font-weight: 600;">GET Your Website within 24 Hours</a>
                </div>
            </div>
            <div style="background-color: #f8fafc; padding: 30px; text-align: center; font-size: 12px; color: #64748b; border-top: 1px solid #eee;">
                <p>Kiran Deb Mondal | Principal Business Technologist</p>
                <p>To opt-out, please reply STOP</p>
            </div>
        </div>
    </body>
    </html>
    """

# --- STREAMLIT APP ---
st.title("🛡️ Professional Outreach Engine")

with st.expander("⚙️ Settings & Credentials", expanded=True):
    col1, col2 = st.columns(2)
    smtp_user = col1.text_input("Workspace Email", value="kiran@kaydiemscriptlab.com")
    smtp_pass = col2.text_input("App Password", type="password")
    sheet_url = st.text_input("Google Sheet URL")

if sheet_url:
    try:
        sh = gc.open_by_url(sheet_url)
        worksheet = sh.sheet1
        df = pd.DataFrame(worksheet.get_all_records())
        st.success(f"✅ Connection Stable. {len(df)} leads loaded.")

        limit = st.number_input("Batch Send Limit", value=50)

        if st.button("🚀 LAUNCH CAMPAIGN"):
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(smtp_user, smtp_pass)

            # Mapping columns
            headers = [h.strip() for h in worksheet.row_values(1)]
            col_status = headers.index("Email_Status") + 1
            col_date = headers.index("Last_Sent_Date") + 1
            col_step = headers.index("Sequence_Step") + 1

            sent_count = 0
            for index, row in df.iterrows():
                if sent_count >= limit: break
                
                email = str(row.get('Email', '')).strip()
                name = str(row.get('Business Name', 'Clinic')).strip()
                cat = str(row.get('Category', 'Dental')).strip()
                addr = str(row.get('Address', 'your area')).strip()
                
                status = str(row.get('Email_Status', ''))
                step = str(row.get('Sequence_Step', '0'))
                step = 0 if step == "" else int(step)
                last_date = str(row.get('Last_Sent_Date', ''))

                # INSTANTLY LOGIC: Step Check
                send_now = False
                is_followup = False
                if step == 0:
                    send_now = True
                    new_step = 1
                elif step == 1 and last_date:
                    days_ago = (datetime.now() - datetime.strptime(last_date, "%Y-%m-%d")).days
                    if days_ago >= 3 and status != "Replied":
                        send_now = True
                        is_followup = True
                        new_step = 2
                
                if "@" in email and send_now:
                    greeting = random.choice(["Hi", "Hello", "Greetings"])
                    subject = f"{'Follow up:' if is_followup else 'Quick question:'} regarding {name}"
                    html_body = get_html_layout(greeting, name, cat, addr, is_followup)

                    msg = MIMEMultipart()
                    msg['From'] = f"Kiran Deb Mondal <{smtp_user}>"
                    msg['To'] = email
                    msg['Subject'] = subject
                    msg.attach(MIMEText(html_body, 'html'))

                    server.send_message(msg)
                    
                    # UPDATE SHEET
                    worksheet.update_cell(index + 2, col_status, "Sent")
                    worksheet.update_cell(index + 2, col_date, datetime.now().strftime("%Y-%m-%d"))
                    worksheet.update_cell(index + 2, col_step, new_step)
                    
                    sent_count += 1
                    st.write(f"✅ Sent Step {new_step} to {name}")
                    time.sleep(random.randint(60, 100))

            server.quit()
            st.success(f"Mission Complete! Sent {sent_count} emails.")
            st.balloons()
            
    except Exception as e:
        st.error(f"Error: {e}")
