import streamlit as st
import pandas as pd
import smtplib
import time
import random
import re
import json
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="Stop Web Rent | Outreach", page_icon="🛡️", layout="wide")

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

# --- PROFESSIONAL HTML TEMPLATE ---
def get_html_template(name, category, address):
    # This is the modern UI layout
    html = f"""
    <html>
    <body style="margin: 0; padding: 0; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #f4f7f9; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
            <!-- Header -->
            <div style="background-color: #1a2b3c; padding: 30px; text-align: center;">
                <h1 style="color: #20c997; margin: 0; font-size: 24px; letter-spacing: 1px;">STOP WEB RENT</h1>
                <p style="color: #ffffff; margin: 5px 0 0 0; font-size: 14px; opacity: 0.8;">High-Velocity Web Architecture</p>
            </div>

            <!-- Body -->
            <div style="padding: 40px;">
                <h2 style="color: #1a2b3c; margin-top: 0;">{{Greeting}} {name} team,</h2>
                <p style="line-height: 1.6; font-size: 16px;">
                    I was recently researching <strong>{category}</strong> clinics in <strong>{address}</strong> and noticed your clinic has a fantastic reputation on Google Maps. 
                </p>
                <p style="line-height: 1.6; font-size: 16px;">
                    However, I noticed you don’t have a website linked to your profile. As of 2026, Google’s AI significantly prioritizes profiles with high-speed linked sites for local rankings.
                </p>

                <!-- Risk Alert -->
                <div style="background-color: #fff5f5; border-left: 4px solid #ff4d4f; padding: 15px; margin: 25px 0;">
                    <strong style="color: #cf1322;">The Risk:</strong> If your competitors have a "Website" button and you don’t, Google will eventually lower your visibility in the Map Pack.
                </div>

                <h3 style="color: #1a2b3c;">The Solution: Titan Engine</h3>
                <p style="line-height: 1.6; font-size: 16px;">
                    I have developed a specialized framework designed to help local services dominate without "Web Rent" (monthly subscriptions).
                </p>

                <!-- Features List -->
                <ul style="padding-left: 20px; line-height: 2;">
                    <li>🚀 <strong>0.1s Speed:</strong> Ranked #1 by Google algorithms.</li>
                    <li>💰 <strong>Zero Hosting:</strong> Pay once, own it forever.</li>
                    <li>🛡️ <strong>Unhackable:</strong> No database, zero security risk.</li>
                </ul>

                <!-- Financial Table -->
                <div style="margin: 30px 0;">
                    <table style="width: 100%; border-collapse: collapse; font-size: 14px; text-align: left;">
                        <thead>
                            <tr style="background-color: #1a2b3c; color: #ffffff;">
                                <th style="padding: 12px; border: 1px solid #ddd;">Category</th>
                                <th style="padding: 12px; border: 1px solid #ddd;">Titan Engine</th>
                                <th style="padding: 12px; border: 1px solid #ddd;">Wix / Shopify</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td style="padding: 12px; border: 1px solid #ddd; background-color: #f9f9f9;">Annual Sub.</td>
                                <td style="padding: 12px; border: 1px solid #ddd; font-weight: bold; color: #20c997;">$0</td>
                                <td style="padding: 12px; border: 1px solid #ddd;">$348+</td>
                            </tr>
                            <tr style="background-color: #e6fffa;">
                                <td style="padding: 12px; border: 1px solid #ddd;"><strong>5-Year Cost</strong></td>
                                <td style="padding: 12px; border: 1px solid #ddd;"><strong>$274</strong></td>
                                <td style="padding: 12px; border: 1px solid #ddd;"><strong>$2,115</strong></td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <!-- Call to Action -->
                <div style="text-align: center; margin-top: 40px;">
                    <p style="font-weight: bold; font-size: 18px;">Ready to secure your Google rank?</p>
                    <a href="https://wa.me/966572562151?text=YES" style="background-color: #20c997; color: white; padding: 18px 35px; text-decoration: none; border-radius: 50px; font-weight: bold; display: inline-block; box-shadow: 0 4px 10px rgba(32, 201, 151, 0.3);">YES, SEND THE DEMO</a>
                </div>
            </div>

            <!-- Footer -->
            <div style="background-color: #f8f9fa; padding: 30px; text-align: center; border-top: 1px solid #eee; font-size: 12px; color: #777;">
                <p><strong>Kiran Deb Mondal</strong><br>Principal Business Technologist | Stop Web Rent</p>
                <p>WhatsApp: +966 572562151 | <a href="https://www.StopWebRent.com" style="color: #20c997;">www.StopWebRent.com</a></p>
                <p style="margin-top: 20px;">If you'd rather not receive these, please reply "STOP".</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html

# --- STREAMLIT APP ---
st.title("🛡️ Stop Web Rent Outreach Engine")
st.markdown("Modern HTML Outreach System | Permanent Sheet Connection")

# 1. SETTINGS
with st.expander("⚙️ SMTP & Sheet Settings", expanded=True):
    col1, col2 = st.columns(2)
    smtp_user = col1.text_input("Workspace Email", value="kiran@kaydiemscriptlab.com")
    smtp_pass = col2.text_input("App Password", type="password")
    sheet_url = st.text_input("Google Sheet URL")

# 2. SEQUENCE
st.subheader("📝 Sequence Details")
subject_line = st.text_input("Subject Line", value="{Quick question|Important note} regarding [Name]")

# 3. EXECUTION
if sheet_url:
    try:
        sh = gc.open_by_url(sheet_url)
        worksheet = sh.sheet1
        df = pd.DataFrame(worksheet.get_all_records())
        
        st.success(f"✅ Connected! Ready to send to **{len(df)}** leads.")
        
        col3, col4 = st.columns(2)
        limit = col3.number_input("Send Limit", value=50)
        
        if st.button("🚀 LAUNCH CAMPAIGN", type="primary"):
            if not smtp_pass: st.error("Enter App Password!"); st.stop()
            
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(smtp_user, smtp_pass)
            
            sent = 0
            for index, row in df.iterrows():
                if sent >= limit: break
                
                email = str(row.get('Email', '')).strip()
                name = str(row.get('Business Name', 'Clinic')).strip()
                cat = str(row.get('Category', 'Dental')).strip()
                addr = str(row.get('Address', 'your area')).strip()
                
                if "@" not in email or "Sent" in str(row.get('Status', '')): continue
                
                # Prepare Content
                subj = parse_spintax(subject_line.replace("[Name]", name))
                greeting = random.choice(["Hi", "Hello", "Greetings", "Hey there"])
                html_body = get_html_template(name, cat, addr).replace("{{Greeting}}", greeting)
                
                # Send Email
                msg = MIMEMultipart()
                msg['From'] = f"Kiran Deb Mondal <{smtp_user}>"
                msg['To'] = email
                msg['Subject'] = subj
                msg.attach(MIMEText(html_body, 'html'))
                
                server.send_message(msg)
                
                # Update Sheet (Assume Status is column 17/Q)
                worksheet.update_cell(index + 2, 17, "Sent")
                
                sent += 1
                st.write(f"✅ [{sent}] Sent to {name}")
                time.sleep(random.randint(45, 90))
                
            server.quit()
            st.balloons()
            st.success("Batch Complete!")
            
    except Exception as e:
        st.error(f"Error: {e}")
