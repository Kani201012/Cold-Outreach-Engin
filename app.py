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

st.set_page_config(page_title="Outreach Engine", page_icon="🚀", layout="wide")

# --- GOOGLE SHEETS CONNECTION ---
@st.cache_resource
def init_connection():
    # Looks for the secrets you pasted in Streamlit Settings
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
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

# --- APP UI ---
st.title("🚀 Professional Cold Email Engine")
st.markdown("Live Google Sheets Connection Active. No CSV uploads required.")

# 1. CREDENTIALS
with st.expander("⚙️ Settings & Credentials", expanded=True):
    col1, col2 = st.columns(2)
    smtp_user = col1.text_input("Workspace Email", value="kiran@kaydiemscriptlab.com")
    smtp_pass = col2.text_input("App Password", type="password")
    sheet_url = st.text_input("Google Sheet URL", placeholder="Paste the full URL of your WhatsApp_Leads sheet here")

# 2. CAMPAIGN BUILDER
st.subheader("📝 Sequence Builder")
tab1, tab2 = st.tabs(["Step 1: Initial Outreach", "Step 2: Follow-Up (Day 4)"])

with tab1:
    step1_sub = st.text_input("Subject Line 1", value="{Question|Inquiry} regarding [Name]")
    step1_body = st.text_area("Email Body 1", height=200, value="""{Hi|Hello|Greetings} [Name] team,

I was researching clinics in [Address] and noticed you have a great reputation! However, I noticed you don't have a website linked to your profile.

In 2026, Google is prioritizing clinics with high-speed sites. I've built a 0.1s 'High-Velocity' demo specifically for [Category] clinics that costs $0 in monthly hosting fees.

Would you be open to seeing the demo link?

{Best|Regards|Cheers},
Kiran Deb Mondal""")

with tab2:
    step2_sub = st.text_input("Subject Line 2", value="Re: {Question|Inquiry} regarding [Name]")
    step2_body = st.text_area("Email Body 2", height=200, value="""{Hi|Hello} again,

Just bumping this to the top of your inbox. Did you have a chance to read my previous email about the 0.1s website demo for [Name]?

Let me know!""")

# 3. LOAD DATABASE LIVE
if sheet_url:
    try:
        sh = gc.open_by_url(sheet_url)
        worksheet = sh.sheet1
        data = worksheet.get_all_records()
        df = pd.DataFrame(data)
        
        # Ensure tracking columns exist in the Sheet
        headers = worksheet.row_values(1)
        if 'Sequence_Step' not in headers:
            worksheet.update_cell(1, len(headers)+1, 'Sequence_Step')
            worksheet.update_cell(1, len(headers)+2, 'Last_Contact_Date')
            worksheet.update_cell(1, len(headers)+3, 'Status')
            # Reload to get new columns
            data = worksheet.get_all_records()
            df = pd.DataFrame(data)

        st.success(f"✅ Connected to Google Sheets! Total Leads: **{len(df)}**")
        st.dataframe(df.head(3))

        # 4. EXECUTION
        st.subheader("🔥 Execution")
        col3, col4, col5 = st.columns(3)
        daily_limit = col3.number_input("Daily Limit", min_value=1, max_value=2000, value=50)
        delay_min = col4.number_input("Min Delay (secs)", value=45)
        delay_max = col5.number_input("Max Delay (secs)", value=90)

        if st.button("🚀 START CAMPAIGN", type="primary"):
            if not smtp_pass:
                st.error("Please enter your App Password!")
                st.stop()

            progress_bar = st.progress(0)
            status_text = st.empty()
            sent_today = 0
            today_date = datetime.now().strftime("%Y-%m-%d")

            try:
                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server.login(smtp_user, smtp_pass)
            except Exception as e:
                st.error(f"SMTP Login Failed: {e}")
                st.stop()

            # Find column indexes for real-time updates
            col_seq = df.columns.get_loc('Sequence_Step') + 1
            col_date = df.columns.get_loc('Last_Contact_Date') + 1
            col_status = df.columns.get_loc('Status') + 1

            for index, row in df.iterrows():
                if sent_today >= daily_limit:
                    break

                email = str(row.get('Email', '')).strip()
                name = str(row.get('Business Name', 'Clinic')).strip()
                category = str(row.get('Category', 'Dental')).strip()
                address = str(row.get('Address', 'your area')).strip()
                
                step = str(row.get('Sequence_Step', '0'))
                if step == "": step = 0
                else: step = int(step)

                last_contact = str(row.get('Last_Contact_Date', ''))
                
                if "@" not in email or str(row.get('Status')) == "Replied":
                    continue

                send_email = False
                subject_to_send, body_to_send = "", ""

                # STEP 1 LOGIC
                if step == 0:
                    subject_to_send = step1_sub
                    body_to_send = step1_body
                    new_step = 1
                    send_email = True

                # STEP 2 LOGIC (Follow-up after 3 days)
                elif step == 1 and last_contact:
                    days_since = (datetime.now() - datetime.strptime(last_contact, "%Y-%m-%d")).days
                    if days_since >= 3:
                        subject_to_send = step2_sub
                        body_to_send = step2_body
                        new_step = 2
                        send_email = True

                # EXECUTE
                if send_email:
                    status_text.text(f"Sending to {name} ({email})...")
                    
                    subj = parse_spintax(subject_to_send.replace("[Name]", name).replace("[Category]", category).replace("[Address]", address))
                    body = parse_spintax(body_to_send.replace("[Name]", name).replace("[Category]", category).replace("[Address]", address))

                    msg = MIMEMultipart()
                    msg['From'] = smtp_user
                    msg['To'] = email
                    msg['Subject'] = subj
                    msg.attach(MIMEText(body, 'plain'))

                    try:
                        server.send_message(msg)
                        
                        # UPDATE GOOGLE SHEET IN REAL TIME! (+2 because sheets are 1-indexed and have headers)
                        worksheet.update_cell(index + 2, col_seq, new_step)
                        worksheet.update_cell(index + 2, col_date, today_date)
                        worksheet.update_cell(index + 2, col_status, f"Step {new_step} Sent")
                        
                        sent_today += 1
                        progress_bar.progress(sent_today / daily_limit)
                        
                        wait = random.randint(delay_min, delay_max)
                        status_text.text(f"✅ Sent! Sleeping {wait}s to mimic human...")
                        time.sleep(wait)

                    except Exception as e:
                        st.error(f"Failed to send to {email}: {e}")

            server.quit()
            st.success(f"🎉 Batch Complete! Sent {sent_today} emails today. The Google Sheet was updated automatically.")

    except Exception as e:
        st.error(f"Could not connect to Google Sheet. Check the URL and ensure it is shared with the Robot Email. Error: {e}")
