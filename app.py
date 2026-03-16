import streamlit as st
import pandas as pd
import smtplib
import time
import random
import re
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

st.set_page_config(page_title="Outreach Engine", page_icon="🚀", layout="wide")

# --- SPINTAX PARSER ---
# Converts "{Hi|Hello|Hey}" into a random choice
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
st.markdown("100% Instantly.ai Compliant: Spintax, Sequences, and Batch Warming.")

# 1. CREDENTIALS
with st.expander("⚙️ SMTP Settings & Credentials", expanded=False):
    col1, col2 = st.columns(2)
    smtp_user = col1.text_input("Workspace Email", value="kiran@kaydiemscriptlab.com")
    smtp_pass = col2.text_input("App Password", type="password")

# 2. CAMPAIGN BUILDER
st.subheader("📝 Campaign Builder")
tab1, tab2 = st.tabs(["Step 1: Initial Outreach", "Step 2: Follow-Up (Day 4)"])

with tab1:
    st.info("Variables allowed: [Name], [Category], [Address]. Spintax allowed: {word1|word2}")
    step1_sub = st.text_input("Subject Line 1", value="{Question|Inquiry} regarding [Name]")
    step1_body = st.text_area("Email Body 1", height=200, value="""{Hi|Hello|Greetings} [Name] team,

I was researching clinics in [Address] and noticed you have a great reputation! However, I noticed you don't have a website linked to your profile.

In 2026, Google is prioritizing clinics with high-speed sites. I've built a 0.1s 'High-Velocity' demo specifically for [Category] clinics that costs $0 in monthly hosting fees.

Would you be open to seeing the demo link?

{Best|Regards|Cheers},
Kiran Deb Mondal""")

with tab2:
    st.info("This sends ONLY to leads who received Step 1 more than 3 days ago.")
    step2_sub = st.text_input("Subject Line 2", value="Re: {Question|Inquiry} regarding [Name]")
    step2_body = st.text_area("Email Body 2", height=200, value="""{Hi|Hello} again,

Just bumping this to the top of your inbox. Did you have a chance to read my previous email about the 0.1s website demo for [Name]?

Let me know!""")

# 3. DATABASE UPLOAD
st.subheader("📂 Upload Leads Database")
uploaded_file = st.file_uploader("Upload your CSV (Must contain 'Email', 'Business Name', 'Category', 'Address')", type=['csv'])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    # Initialize tracking columns if they don't exist (Like Instantly does)
    if 'Sequence_Step' not in df.columns: df['Sequence_Step'] = 0
    if 'Last_Contact_Date' not in df.columns: df['Last_Contact_Date'] = ""
    if 'Status' not in df.columns: df['Status'] = "Uncontacted"

    st.write(f"Total Leads: **{len(df)}**")
    st.dataframe(df.head(3))

    # 4. SENDING CONTROLS
    st.subheader("🔥 Execution")
    col3, col4, col5 = st.columns(3)
    daily_limit = col3.number_input("Daily Limit (Warmup)", min_value=1, max_value=2000, value=50)
    delay_min = col4.number_input("Min Delay (secs)", value=45)
    delay_max = col5.number_input("Max Delay (secs)", value=90)

    if st.button("🚀 START CAMPAIGN", type="primary"):
        if not smtp_pass:
            st.error("Please enter your App Password in the Settings!")
            st.stop()

        progress_bar = st.progress(0)
        status_text = st.empty()
        
        sent_today = 0
        today_date = datetime.now().strftime("%Y-%m-%d")

        # Connect to Server
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(smtp_user, smtp_pass)
        except Exception as e:
            st.error(f"SMTP Login Failed: {e}")
            st.stop()

        # LOOP THROUGH LEADS
        for index, row in df.iterrows():
            if sent_today >= daily_limit:
                break

            email = str(row.get('Email', '')).strip()
            name = str(row.get('Business Name', 'Clinic')).strip()
            category = str(row.get('Category', 'Dental')).strip()
            address = str(row.get('Address', 'your area')).strip()
            
            step = int(row.get('Sequence_Step', 0))
            last_contact = str(row.get('Last_Contact_Date', ''))
            
            if "@" not in email or str(row.get('Status')) == "Replied":
                continue

            # Determine which email to send
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

            # EXECUTE SEND
            if send_email:
                status_text.text(f"Sending to {name} ({email})...")
                
                # Replace Variables
                subj = subject_to_send.replace("[Name]", name).replace("[Category]", category).replace("[Address]", address)
                body = body_to_send.replace("[Name]", name).replace("[Category]", category).replace("[Address]", address)
                
                # Apply Spintax
                subj = parse_spintax(subj)
                body = parse_spintax(body)

                msg = MIMEMultipart()
                msg['From'] = smtp_user
                msg['To'] = email
                msg['Subject'] = subj
                msg.attach(MIMEText(body, 'plain'))

                try:
                    server.send_message(msg)
                    
                    # Update Dataframe
                    df.at[index, 'Sequence_Step'] = new_step
                    df.at[index, 'Last_Contact_Date'] = today_date
                    df.at[index, 'Status'] = f"Step {new_step} Sent"
                    
                    sent_today += 1
                    progress_bar.progress(sent_today / daily_limit)
                    
                    # Random Human Delay
                    wait = random.randint(delay_min, delay_max)
                    status_text.text(f"Sleeping for {wait} seconds to mimic human...")
                    time.sleep(wait)

                except Exception as e:
                    st.error(f"Failed to send to {email}: {e}")

        server.quit()
        st.success(f"🎉 Batch Complete! Sent {sent_today} emails today.")
        
        # DOWNLOAD UPDATED DATABASE
        st.subheader("📥 Download Updated Database")
        st.info("IMPORTANT: Download this file and upload it again tomorrow so the app remembers who it already emailed!")
        
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Updated Leads CSV",
            data=csv_data,
            file_name=f"Campaign_DB_{today_date}.csv",
            mime='text/csv',
            type="primary"
        )
