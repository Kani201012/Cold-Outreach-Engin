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

# --- PROFESSIONAL HTML UI ENGINE ---
def get_professional_html(name, category, address):
    # Data Cleaning for UI
    display_address = "your city" if ("(" in str(address) or str(address).lower() == "n/a") else address
    
    html = f"""
    <html>
    <body style="margin: 0; padding: 0; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #f4f7f9; color: #1a2b3c;">
        <div style="max-width: 650px; margin: 20px auto; background-color: #ffffff; border-radius: 15px; overflow: hidden; box-shadow: 0 15px 35px rgba(30, 41, 59, 0.1); border: 1px solid #e2e8f0;">
            
            <!-- Tech Header -->
            <div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding: 45px 20px; text-align: center;">
                <h1 style="color: #2dd4bf; margin: 0; font-size: 30px; font-weight: 800; letter-spacing: 3px; text-transform: uppercase;">STOP WEB RENT</h1>
                <p style="color: #94a3b8; margin: 10px 0 0 0; font-size: 14px; font-weight: 600;">HIGH-VELOCITY WEB ARCHITECTURE</p>
            </div>

            <!-- Content Body -->
            <div style="padding: 45px 40px;">
                <h2 style="color: #0f172a; font-size: 20px; margin-top: 0;">Hi {name},</h2>
                
                <p style="font-size: 16px; line-height: 1.7; color: #334155;">
                    I was recently researching on <strong>{category}</strong> clinics in {display_address} and noticed that your clinic has a fantastic reputation on Google Maps.
                </p>

                <p style="font-size: 16px; line-height: 1.7; color: #334155;">
                    However, I noticed you don’t have a website linked to your profile. I am reaching out because, as of 2026, <strong>Google’s algorithm has significantly increased the weight of linked websites</strong> for local rankings.
                </p>

                <div style="background-color: #fff1f2; border-left: 5px solid #f43f5e; padding: 20px; margin: 30px 0; border-radius: 4px;">
                    <strong style="color: #9f1239; font-size: 17px;">⚠️ The Risk:</strong><br>
                    <span style="color: #be123c; font-size: 15px;">If your competitors have a "Website" button and you don’t, Google’s AI search will eventually lower your visibility in the Map Pack, making it harder for new customers to find you.</span>
                </div>

                <h3 style="color: #0f172a; font-size: 18px; border-bottom: 2px solid #2dd4bf; display: inline-block;">The Solution: Hyper-Static Architecture</h3>
                <p style="font-size: 16px; line-height: 1.7; color: #334155;">
                    I have developed a specialized High-Velocity Web Framework designed specifically to help local services dominate their local area without the high costs of traditional web design.
                </p>

                <div style="text-align: center; margin: 25px 0;">
                    <a href="https://hv-furniture-bit.github.io/dental-junction-behala/index.html" style="color: #0d9488; font-weight: 700; text-decoration: underline; font-size: 18px;">View the live tech demo here: Ghosh Dental Clinic</a>
                    <p style="font-size: 13px; color: #64748b; margin-top: 5px;">Stop paying website rent. $0 monthly forever.</p>
                </div>

                <p style="font-weight: 700; color: #0f172a; margin-bottom: 10px;">Why this is better than Wix / Squarespace / Shopify or WordPress:</p>
                <div style="background-color: #f8fafc; padding: 20px; border-radius: 8px; margin-bottom: 30px;">
                    <ul style="margin: 0; padding-left: 20px; color: #475569; line-height: 2;">
                        <li>💰 <strong>Zero Monthly Hosting:</strong> Pay once, own the asset forever.</li>
                        <li>🚀 <strong>0.1s Speed:</strong> It loads instantly (Google's #1 ranking factor).</li>
                        <li>🛡️ <strong>Unhackable:</strong> No database, nothing for hackers to break.</li>
                        <li>📲 <strong>WhatsApp Leads:</strong> Customers chat with you in one tap.</li>
                    </ul>
                </div>

                <!-- Financial Comparison Table -->
                <table style="width: 100%; border-collapse: collapse; font-size: 13px; border: 1px solid #e2e8f0;">
                    <thead>
                        <tr style="background-color: #0f172a; color: #ffffff;">
                            <th style="padding: 12px; text-align: left;">Expense Category</th>
                            <th style="padding: 12px; text-align: center;">Titan Engine</th>
                            <th style="padding: 12px; text-align: center;">Wix / Shopify</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td style="padding: 12px; border-bottom: 1px solid #e2e8f0;">Initial Setup</td>
                            <td style="padding: 12px; text-align: center; border-bottom: 1px solid #e2e8f0;">$199 (One-time)</td>
                            <td style="padding: 12px; text-align: center; border-bottom: 1px solid #e2e8f0;">$0 (DIY)</td>
                        </tr>
                        <tr>
                            <td style="padding: 12px; border-bottom: 1px solid #e2e8f0;">Annual Hosting</td>
                            <td style="padding: 12px; text-align: center; border-bottom: 1px solid #e2e8f0; font-weight: bold; color: #0d9488;">$0</td>
                            <td style="padding: 12px; text-align: center; border-bottom: 1px solid #e2e8f0;">$348 ($29/mo)</td>
                        </tr>
                        <tr style="background-color: #f0fdfa;">
                            <td style="padding: 12px; font-weight: bold;">TOTAL (5 YEARS)</td>
                            <td style="padding: 12px; text-align: center; font-weight: 800; color: #0d9488;">$274</td>
                            <td style="padding: 12px; text-align: center;">$2,115</td>
                        </tr>
                    </tbody>
                </table>
                <p style="text-align: center; color: #0d9488; font-weight: 800; margin-top: 10px;">Your 5-Year Savings: $1,841</p>

                <p style="font-size: 16px; line-height: 1.7; color: #334155; margin-top: 35px;">
                    <strong>The 24-Hour Deployment:</strong> If you like the performance of the demo link above, I can customize a version with <strong>your logo, photos, and phone number</strong> and have it live on your own domain within 24 hours.
                </p>

                <p style="font-size: 16px; line-height: 1.7; color: #0f172a; font-weight: bold; text-align: center;">
                    My Offer: A Free 24-Hour Preview. If you don't love it, you pay nothing.
                </p>

                <!-- CTA Buttons -->
                <div style="text-align: center; margin-top: 40px;">
                    <a href="https://wa.me/966572562151?text=YES" style="background-color: #0d9488; color: #ffffff; padding: 20px 40px; text-decoration: none; border-radius: 10px; font-weight: 800; display: block; font-size: 18px; box-shadow: 0 4px 15px rgba(13, 148, 136, 0.4);">REPLY 'YES' FOR FREE DEMO</a>
                    <div style="margin-top: 20px;">
                        <a href="https://kiranmondal.gumroad.com/l/titanv50" style="color: #0d9488; font-size: 15px; font-weight: 700; text-decoration: underline;">GET Your Website within 24 Hours (Direct Purchase)</a>
                    </div>
                </div>
            </div>

            <!-- Footer -->
            <div style="background-color: #f8fafc; padding: 40px; text-align: center; border-top: 1px solid #e2e8f0; font-size: 12px; color: #64748b;">
                <p style="margin: 0; font-weight: bold; font-size: 15px; color: #1e293b;">Kiran Deb Mondal</p>
                <p style="margin: 5px 0;">Principal Business Technologist | Stop Web Rent</p>
                <p style="margin: 15px 0;">
                    <a href="https://www.StopWebRent.com" style="color: #0d9488; text-decoration: none; font-weight: bold;">www.StopWebRent.com</a> | 
                    <a href="https://wa.me/966572562151" style="color: #0d9488; text-decoration: none; font-weight: bold;">WhatsApp</a>
                </p>
                <p style="margin-top: 30px; opacity: 0.5;">To opt-out of future updates, please reply STOP.</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html

# --- STREAMLIT APP ---
st.title("🛡️ Stop Web Rent Master Outreach")

with st.sidebar:
    st.header("⚙️ Credentials")
    smtp_user = st.text_input("Email", value="kiran@kaydiemscriptlab.com")
    smtp_pass = st.text_input("App Password", type="password")
    sheet_url = st.text_input("Sheet URL")

if sheet_url:
    try:
        sh = gc.open_by_url(sheet_url)
        worksheet = sh.sheet1
        df = pd.DataFrame(worksheet.get_all_records())
        
        st.success(f"✅ Leads Loaded: {len(df)}")
        limit = st.number_input("Batch Limit", value=50)

        if st.button("🚀 START PROFESSIONAL CAMPAIGN", type="primary"):
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(smtp_user, smtp_pass)

            # Auto-Find Columns
            headers = [h.strip() for h in worksheet.row_values(1)]
            col_status = headers.index("Email_Status") + 1
            col_date = headers.index("Last_Sent_Date") + 1
            col_step = headers.index("Sequence_Step") + 1

            sent = 0
            for index, row in df.iterrows():
                if sent >= limit: break
                
                email = str(row.get('Email', '')).strip()
                name = str(row.get('Business Name', 'Clinic')).strip()
                cat = str(row.get('Category', 'Dental')).strip()
                addr = str(row.get('Address', 'your area')).strip()
                status = str(row.get('Email_Status', ''))

                if "@" not in email or "Sent" in status: continue
                
                # HTML Preparation
                html_content = get_professional_html(name, cat, addr)
                subject = f"Question regarding {name}'s Google Maps Profile"
                
                msg = MIMEMultipart()
                msg['From'] = f"Kiran Deb Mondal <{smtp_user}>"
                msg['To'] = email
                msg['Subject'] = subject
                msg.attach(MIMEText(html_content, 'html'))
                
                try:
                    server.send_message(msg)
                    # Real-time Sheet Update
                    worksheet.update_cell(index + 2, col_status, "Sent")
                    worksheet.update_cell(index + 2, col_date, datetime.now().strftime("%Y-%m-%d"))
                    worksheet.update_cell(index + 2, col_step, 1)
                    
                    sent += 1
                    st.write(f"✅ Sent to {name}")
                    time.sleep(random.randint(60, 110))
                except:
                    st.write(f"❌ Failed for {name}")

            server.quit()
            st.success("Campaign Finished!")
            
    except Exception as e:
        st.error(f"Error: {e}")
