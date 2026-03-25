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

st.set_page_config(page_title="Stop Web Rent | Master Engine", page_icon="🛡️", layout="wide")

# --- 1. PERMANENT CONNECTION (Using Secrets) ---
@st.cache_resource
def init_connection():
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    return gspread.authorize(Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scopes))

gc = init_connection()

# --- 2. SPINTAX PARSER ---
def parse_spintax(text):
    pattern = re.compile(r'\{([^{}]*)\}')
    while True:
        match = pattern.search(text)
        if not match: break
        options = match.group(1).split('|')
        text = text[:match.start()] + random.choice(options) + text[match.end():]
    return text

# --- 3. THE 7-PHASE COPYWRITING ENGINE ---
def get_campaign_content(phase, name, category, address):
    """Returns the Subject and HTML Body for the specific phase."""
    
    greeting = random.choice(["Hi", "Hello", "Greetings", "Dear"])
    
    # Cleaners
    display_address = "your city" if ("(" in str(address) or str(address).lower() == "n/a" or not address) else address
    display_cat = "Dental" if (str(category).lower() == "n/a" or not category) else category

    if phase == 1:
        subject = parse_spintax("{Missing link|Google Maps error|Quick question} regarding [Name]").replace("[Name]", name)
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; font-size: 15px; color: #1a1a1a; line-height: 1.6;">
            <p>{greeting} {name} team,</p>
            <p>I was researching <strong>{display_cat}</strong> clinics in <strong>{display_address}</strong> and noticed your practice has a fantastic reputation. However, you are missing a critical asset: <strong>a "Website" button on your Google Maps profile.</strong></p>
            <p>Every day without that button, Google’s algorithm pushes you down the rankings, handing high-value patients to your competitors.</p>
            <p>I build 0.1s High-Velocity websites specifically for healthcare clinics. <strong>Unlike Wix or Shopify, I charge $0 in monthly hosting fees.</strong></p>
            <div style="background-color: #f8fafc; padding: 15px; border-left: 4px solid #0d9488; margin: 20px 0;">
                <strong>My Offer: A Free 24-Hour Preview</strong><br>
                I will use your current logo and photos to build a live demo. If you don't love the performance, you pay nothing.
            </div>
            <p>Reply <strong>"YES"</strong> to this email (or <a href="https://wa.me/966572562151" style="color: #0d9488; font-weight: bold;">message me on WhatsApp here</a>), and I'll send you a private link to review your new site.</p>
            <p>Best regards,<br><strong>Kiran Deb Mondal</strong><br>Principal Technologist | Stop Web Rent</p>
        </body>
        </html>
        """

    elif phase == 2:
        subject = f"Re: {name} digital preview"
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; font-size: 15px; color: #1a1a1a; line-height: 1.6;">
            <p>{greeting} again,</p>
            <p>I wanted to follow up on my last email. When I build a Titan Engine site for a clinic like {name}, it's not just a digital brochure—it's a lead generation machine.</p>
            <p><strong>Here is what your custom site will include:</strong></p>
            <ul>
                <li><strong>WhatsApp Booking:</strong> Patients can book appointments or chat with your reception desk in one tap.</li>
                <li><strong>Multilingual Support:</strong> Instantly translates to Hindi, Bengali, Spanish, French, etc.</li>
                <li><strong>Mobile-First Design:</strong> Looks and feels like a native app on your patients' phones.</li>
            </ul>
            <p><a href="https://hv-furniture-bit.github.io/dental-junction-behala/index.html" style="color: #0d9488; font-weight: bold;">You can click here to play with a live demo of a clinic we recently built.</a></p>
            <p>Would you like me to build a custom prototype for {name}? Just reply "YES".</p>
            <p>- Kiran</p>
        </body>
        </html>
        """

    elif phase == 3:
        subject = parse_spintax("{Stop paying|How to save $1,800 on} website rent")
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; font-size: 15px; color: #1a1a1a; line-height: 1.6;">
            <p>{greeting},</p>
            <p>Most business owners are trapped paying "Web Rent"—$30 to $50 every single month to Wix, Shopify, or WordPress just to keep their site online.</p>
            <p>The Titan Engine changes that. <strong>Pay a $199 one-time setup fee, and own the asset forever.</strong></p>
            
            <table style="width: 100%; max-width: 500px; border-collapse: collapse; margin: 20px 0; border: 1px solid #e2e8f0; text-align: left;">
                <tr style="background-color: #f8fafc;">
                    <th style="padding: 10px; border-bottom: 2px solid #e2e8f0;">5-Year Cost</th>
                    <th style="padding: 10px; border-bottom: 2px solid #e2e8f0; color: #0d9488;">Titan Engine</th>
                    <th style="padding: 10px; border-bottom: 2px solid #e2e8f0;">Wix / Shopify</th>
                </tr>
                <tr>
                    <td style="padding: 10px; border-bottom: 1px solid #e2e8f0;">Setup Fee</td>
                    <td style="padding: 10px; border-bottom: 1px solid #e2e8f0; font-weight: bold;">$199 (Once)</td>
                    <td style="padding: 10px; border-bottom: 1px solid #e2e8f0;">$0</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border-bottom: 1px solid #e2e8f0;">Monthly Rent</td>
                    <td style="padding: 10px; border-bottom: 1px solid #e2e8f0; font-weight: bold; color: #0d9488;">$0</td>
                    <td style="padding: 10px; border-bottom: 1px solid #e2e8f0;">$1,740</td>
                </tr>
                <tr style="background-color: #fff1f2;">
                    <td style="padding: 10px; font-weight: bold;">Total Cost</td>
                    <td style="padding: 10px; font-weight: bold; color: #0d9488;">$274 (incl. domain)</td>
                    <td style="padding: 10px; font-weight: bold; color: #e11d48;">$2,115</td>
                </tr>
            </table>
            
            <p>That is <strong>$1,841 in savings</strong>. If you want to stop renting and start owning, let's chat. <a href="https://wa.me/966572562151" style="color: #0d9488;">WhatsApp me here.</a></p>
            <p>- Kiran</p>
        </body>
        </html>
        """

    elif phase == 4:
        subject = parse_spintax("Update {name} website using Excel?")
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; font-size: 15px; color: #1a1a1a; line-height: 1.6;">
            <p>{greeting},</p>
            <p>One of the main reasons clinics don't build websites is because they don't want to learn complex dashboards or pay a developer every time they need to change a price.</p>
            <p>With our architecture, <strong>your website is hard-wired directly to a private Google Sheet.</strong></p>
            <p>If you or your receptionist can type into an Excel file, you can manage your entire website. Change a price in the spreadsheet, and your live website updates globally in seconds.</p>
            <p>Should I build a quick prototype so you can see how easy this is?</p>
            <p>- Kiran</p>
        </body>
        </html>
        """

    elif phase == 5:
        subject = parse_spintax("The 2026 Google algorithm & [Name]").replace("[Name]", name)
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; font-size: 15px; color: #1a1a1a; line-height: 1.6;">
            <p>{greeting},</p>
            <p>I am reaching out regarding the missing website link on your Google Maps profile because the rules of local SEO are changing.</p>
            <div style="background-color: #fff1f2; border-left: 4px solid #f43f5e; padding: 15px; margin: 15px 0;">
                <strong>The 2026 AI Algorithm Shift:</strong> Google’s AI search now significantly increases the weight of <i>linked, fast-loading</i> websites. Profiles without them are actively being suppressed in the Map Pack.
            </div>
            <p>Our architecture is unhackable and achieves a 100/100 Google PageSpeed score, ensuring you stay at the top of local searches.</p>
            <p>Let me build a risk-free demo to secure your ranking. Reply "YES" and I'll start immediately.</p>
            <p>- Kiran</p>
        </body>
        </html>
        """

    elif phase == 6:
        subject = "am I off base here?"
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; font-size: 15px; color: #1a1a1a; line-height: 1.6;">
            <p>{greeting},</p>
            <p>I've reached out a few times about getting a high-speed, $0 monthly fee website set up for {name}.</p>
            <p>Am I totally off base here, or is this just a really busy month for the clinic?</p>
            <p>Just let me know so I can update my notes.</p>
            <p>- Kiran</p>
        </body>
        </html>
        """

    elif phase == 7:
        subject = parse_spintax("{Closing my file|Last email} regarding [Name]").replace("[Name]", name)
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; font-size: 15px; color: #1a1a1a; line-height: 1.6;">
            <p>{greeting},</p>
            <p>Since I haven't heard back, I'll assume that fixing the missing website on your Google profile isn't a priority right now. This will be my last email.</p>
            <p>If you ever get tired of losing map traffic to competitors, or if you just want to stop paying monthly "Web Rent" to Wix or Shopify, you know where to find me.</p>
            <p>Wishing {name} a highly successful year.</p>
            <br>
            <p style="font-size: 13px; color: #64748b; border-top: 1px solid #e2e8f0; padding-top: 15px;">
                <strong>Kiran Deb Mondal</strong><br>
                Principal Technologist | Stop Web Rent<br>
                WhatsApp: <a href="https://wa.me/966572562151" style="color: #0d9488;">+966 572562151</a><br>
                Purchase Direct: <a href="https://kiranmondal.gumroad.com/l/titanv50" style="color: #0d9488;">Gumroad Link</a>
            </p>
        </body>
        </html>
        """
        
    return subject, html

# --- 4. STREAMLIT UI SIDEBAR ---
with st.sidebar:
    st.title("⚙️ Credentials")
    stored_email = st.secrets.get("EMAIL_USER", "kiran@kaydiemscriptlab.com")
    stored_pass = st.secrets.get("EMAIL_PASS", "")
    stored_url = st.secrets.get("SHEET_URL", "")

    user_email = st.text_input("Sender Email", value=stored_email)
    app_pass = st.text_input("App Password", value=stored_pass, type="password")
    sheet_url = st.text_input("Google Sheet URL", value=stored_url)
    
    if app_pass and sheet_url:
        st.success("✅ Credentials Loaded")
    else:
        st.warning("⚠️ Secrets missing")

# --- 5. MAIN LOGIC ---
st.title("🛡️ 7-Phase Master Engine")

if sheet_url:
    try:
        sh = gc.open_by_url(sheet_url)
        worksheet = sh.sheet1
        
        # --- ROBUST SPREADSHEET PARSER (Fixes the Empty Header Crash) ---
        raw_data = worksheet.get_all_values()
        if not raw_data:
            st.error("Google Sheet is completely empty!")
            st.stop()
            
        raw_headers = raw_data[0]
        clean_headers = [str(h).strip() if str(h).strip() else f"Empty_{i}" for i, h in enumerate(raw_headers)]
        df = pd.DataFrame(raw_data[1:], columns=clean_headers)
        
        st.success(f"✅ Connection Stable. {len(df)} leads loaded.")

        limit = st.number_input("Batch Send Limit (Max emails to send right now)", value=40, max_value=200)

        if st.button("🚀 IGNITE 7-PHASE CAMPAIGN", type="primary", use_container_width=True):
            
            # Ensure necessary columns exist
            required_cols = ["Email_Status", "Last_Sent_Date", "Sequence_Step"]
            for col in required_cols:
                if col not in clean_headers:
                    st.error(f"❌ Missing Column: Your sheet must have a column named exactly '{col}'")
                    st.stop()
            
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(user_email, app_pass)

            col_status_idx = clean_headers.index("Email_Status") + 1
            col_date_idx = clean_headers.index("Last_Sent_Date") + 1
            col_step_idx = clean_headers.index("Sequence_Step") + 1

            sent_count = 0
            st_progress = st.progress(0)
            st_status = st.empty()

            for index, row in df.iterrows():
                if sent_count >= limit: break
                
                email = str(row.get('Email', '')).strip()
                name = str(row.get('Business Name', 'Clinic')).strip()
                category = str(row.get('Category', 'Dental'))
                address = str(row.get('Address', 'your area'))
                
                status = str(row.get('Email_Status', '')).strip()
                step_val = str(row.get('Sequence_Step', '0')).strip()
                current_step = 0 if step_val == "" else int(float(step_val))
                last_date_str = str(row.get('Last_Sent_Date', '')).strip()

                # Check if valid email and not replied/bounced
                if "@" not in email or status.lower() in ["replied", "bounced", "unsubscribed"]:
                    continue
                
                # Campaign Complete?
                if current_step >= 7:
                    if status != "Completed":
                        worksheet.update_cell(index + 2, col_status_idx, "Completed")
                    continue

                # --- SCHEDULING LOGIC ---
                # How many days to wait based on the CURRENT step
                wait_days_map = {0: 0, 1: 3, 2: 4, 3: 4, 4: 6, 5: 6, 6: 6}
                required_wait_days = wait_days_map.get(current_step, 999)
                
                send_now = False
                
                if current_step == 0:
                    send_now = True
                elif last_date_str:
                    try:
                        last_date = datetime.strptime(last_date_str, "%Y-%m-%d")
                        days_elapsed = (datetime.now() - last_date).days
                        if days_elapsed >= required_wait_days:
                            send_now = True
                    except:
                        send_now = True # If date format is broken, force send next step

                if send_now:
                    new_step = current_step + 1
                    subject, html_body = get_campaign_content(new_step, name, category, address)

                    msg = MIMEMultipart()
                    msg['From'] = f"Kiran Deb Mondal <{user_email}>"
                    msg['To'] = email
                    msg['Subject'] = subject
                    msg.attach(MIMEText(html_body, 'html'))

                    try:
                        server.send_message(msg)
                        
                        # UPDATE SHEET
                        worksheet.update_cell(index + 2, col_status_idx, f"Phase {new_step} Sent")
                        worksheet.update_cell(index + 2, col_date_idx, datetime.now().strftime("%Y-%m-%d"))
                        worksheet.update_cell(index + 2, col_step_idx, new_step)
                        
                        sent_count += 1
                        st_progress.progress(sent_count / limit)
                        st_status.success(f"✅ [{sent_count}] Sent Phase {new_step} to {name}")
                        
                        # Anti-Spam Delay
                        if sent_count < limit:
                            time.sleep(random.randint(45, 90))
                            
                    except Exception as e:
                        st_status.error(f"❌ Failed for {email}: {e}")

            server.quit()
            st.success("🎉 Campaign Session Finished! Your Google Sheet has been updated.")
            st.balloons()
            
    except Exception as e:
        st.error(f"System Error: {e}")
