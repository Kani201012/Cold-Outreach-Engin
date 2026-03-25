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

# --- 3. THE 7-PHASE COPYWRITING ENGINE (ULTRA-MODERN UI) ---
def get_campaign_content(phase, name, category, address):
    """Returns the Subject and HTML Body for the specific phase."""
    
    greeting = random.choice(["Hi", "Hello", "Greetings", "Dear"])
    
    # Cleaners
    display_address = "your city" if ("(" in str(address) or str(address).lower() == "n/a" or not address) else address
    display_cat = "Dental" if (str(category).lower() == "n/a" or not category) else category

    # Global CSS Variables (Inline)
    font_family = "'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Arial, sans-serif"
    bg_body = "#f3f4f6"
    bg_card = "#ffffff"
    text_main = "#334155"
    text_dark = "#0f172a"
    accent = "#0d9488" # Teal
    accent_light = "#f0fdfa"
    warning = "#e11d48" # Crimson
    warning_light = "#fff1f2"

    # Common Footer
    footer = f"""
    <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #e2e8f0; font-size: 13px; color: #64748b; text-align: center;">
        <strong style="color: {text_dark}; font-size: 14px;">Kiran Deb Mondal</strong><br>
        Principal Technologist | Stop Web Rent<br>
        <span style="display: inline-block; margin-top: 8px;">
            <a href="https://wa.me/966572562151" style="color: {accent}; text-decoration: none;">WhatsApp: +966 572562151</a> | 
            <a href="https://www.stopwebrent.com" style="color: {accent}; text-decoration: none;">StopWebRent.com</a>
        </span>
    </div>
    """

    if phase == 1:
        subject = parse_spintax("{Action Required|Google Maps alert|Missing link} for [Name]").replace("[Name]", name)
        html = f"""
        <html>
        <body style="margin: 0; padding: 20px; background-color: {bg_body}; font-family: {font_family};">
            <div style="max-width: 600px; margin: 0 auto; background-color: {bg_card}; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: 1px solid #e5e7eb;">
                <div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding: 30px 20px; text-align: center;">
                    <h1 style="color: #2dd4bf; margin: 0; font-size: 24px; font-weight: 800; letter-spacing: 1.5px; text-transform: uppercase;">STOP WEB RENT</h1>
                    <p style="color: #94a3b8; margin: 5px 0 0 0; font-size: 13px; font-weight: 500;">High-Velocity Web Architecture</p>
                </div>
                <div style="padding: 35px 30px;">
                    <h2 style="color: {text_dark}; font-size: 20px; margin-top: 0;">{greeting} {name} team,</h2>
                    <p style="font-size: 16px; line-height: 1.6; color: {text_main};">
                        I was researching <strong>{display_cat}</strong> clinics in <strong>{display_address}</strong> and noticed your practice has a fantastic reputation. However, you are missing a critical digital asset:
                    </p>
                    <div style="background-color: {warning_light}; border-left: 4px solid {warning}; padding: 16px; margin: 25px 0; border-radius: 0 8px 8px 0;">
                        <strong style="color: #9f1239; font-size: 16px;">⚠️ Missing Element:</strong><br>
                        <span style="color: {warning}; font-size: 15px;">You do not have a <strong>"Website"</strong> button on your Google Maps profile. Every day, Google’s algorithm is handing your high-value patients to competitors who do.</span>
                    </div>
                    <p style="font-size: 16px; line-height: 1.6; color: {text_main};">
                        I build 0.1s High-Velocity websites specifically for healthcare clinics. <strong>Unlike Wix or Shopify, I charge $0 in monthly hosting fees.</strong>
                    </p>
                    <div style="background-color: {accent_light}; border: 1px solid #ccfbf1; padding: 20px; margin: 25px 0; border-radius: 8px; text-align: center;">
                        <strong style="color: #0f766e; font-size: 16px;">My Offer: A Free 24-Hour Preview</strong><br>
                        <p style="color: #0d9488; font-size: 14px; margin: 8px 0 0 0;">I will use your current logo and photos to build a live demo. If you don't love the performance, you pay nothing.</p>
                    </div>
                    <div style="text-align: center; margin-top: 30px;">
                        <a href="https://wa.me/966572562151?text=YES" style="background-color: {accent}; color: #ffffff; padding: 16px 32px; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 16px; display: inline-block;">REPLY 'YES' FOR FREE DEMO</a>
                    </div>
                    {footer}
                </div>
            </div>
        </body>
        </html>
        """

    elif phase == 2:
        subject = f"Re: {name} digital preview"
        html = f"""
        <html>
        <body style="margin: 0; padding: 20px; background-color: {bg_body}; font-family: {font_family};">
            <div style="max-width: 600px; margin: 0 auto; background-color: {bg_card}; border-radius: 12px; padding: 35px 30px; border: 1px solid #e5e7eb;">
                <h2 style="color: {text_dark}; font-size: 18px; margin-top: 0;">{greeting} again,</h2>
                <p style="font-size: 15px; line-height: 1.6; color: {text_main};">
                    I wanted to follow up on my last email. When I build a Titan Engine site for a clinic like <strong>{name}</strong>, it's not just a digital brochure—it's a high-conversion lead generation machine.
                </p>
                <div style="background-color: #f8fafc; padding: 20px; border-radius: 8px; margin: 25px 0;">
                    <h3 style="color: {text_dark}; font-size: 16px; margin-top: 0;">⚡ Here is what your custom site includes:</h3>
                    <ul style="color: {text_main}; font-size: 15px; line-height: 1.8; margin-bottom: 0; padding-left: 20px;">
                        <li><strong>WhatsApp Booking:</strong> Patients book appointments in one tap.</li>
                        <li><strong>Multilingual Support:</strong> Instantly translates to local languages.</li>
                        <li><strong>Zero-DB Architecture:</strong> 100% unhackable and secure.</li>
                    </ul>
                </div>
                <div style="text-align: center; margin: 30px 0;">
                    <a href="https://hv-furniture-bit.github.io/dental-junction-behala/index.html" style="color: {accent}; font-weight: bold; font-size: 16px; text-decoration: underline;">👉 Click here to play with a live demo of a clinic we recently built</a>
                </div>
                <p style="font-size: 15px; line-height: 1.6; color: {text_main}; text-align: center;">
                    Would you like me to build a custom prototype for {name}? Just reply "YES".
                </p>
                {footer}
            </div>
        </body>
        </html>
        """

    elif phase == 3:
        subject = parse_spintax("{Stop paying|How to save $1,800 on} website rent")
        html = f"""
        <html>
        <body style="margin: 0; padding: 20px; background-color: {bg_body}; font-family: {font_family};">
            <div style="max-width: 600px; margin: 0 auto; background-color: {bg_card}; border-radius: 12px; padding: 35px 30px; border: 1px solid #e5e7eb;">
                <h2 style="color: {text_dark}; font-size: 20px; margin-top: 0; text-align: center;">Stop Renting. Start Owning.</h2>
                <p style="font-size: 15px; line-height: 1.6; color: {text_main}; text-align: center;">
                    Most business owners are trapped paying $30-$50 every single month to Wix or Shopify. The Titan Engine changes that. <strong>Pay a $199 one-time setup fee, and own it forever.</strong>
                </p>
                
                <div style="border-radius: 8px; overflow: hidden; margin: 30px 0; border: 1px solid #e2e8f0;">
                    <table style="width: 100%; border-collapse: collapse; font-size: 14px; text-align: center;">
                        <tr style="background-color: #f8fafc;">
                            <th style="padding: 15px; border-bottom: 2px solid #e2e8f0; text-align: left;">5-Year Cost</th>
                            <th style="padding: 15px; border-bottom: 2px solid #e2e8f0; background-color: {accent_light}; color: {accent};">Titan Engine</th>
                            <th style="padding: 15px; border-bottom: 2px solid #e2e8f0; color: #64748b;">Wix / Shopify</th>
                        </tr>
                        <tr>
                            <td style="padding: 15px; border-bottom: 1px solid #e2e8f0; text-align: left; font-weight: 500;">Setup Fee</td>
                            <td style="padding: 15px; border-bottom: 1px solid #e2e8f0; background-color: {accent_light}; font-weight: bold;">$199 <span style="font-size: 11px; font-weight: normal;">(Once)</span></td>
                            <td style="padding: 15px; border-bottom: 1px solid #e2e8f0; color: #64748b;">$0</td>
                        </tr>
                        <tr>
                            <td style="padding: 15px; border-bottom: 1px solid #e2e8f0; text-align: left; font-weight: 500;">Monthly Rent</td>
                            <td style="padding: 15px; border-bottom: 1px solid #e2e8f0; background-color: {accent_light}; font-weight: bold; color: {accent};">$0</td>
                            <td style="padding: 15px; border-bottom: 1px solid #e2e8f0; color: #64748b;">$1,740</td>
                        </tr>
                        <tr style="background-color: #0f172a; color: white;">
                            <td style="padding: 15px; text-align: left; font-weight: bold;">Total Cost</td>
                            <td style="padding: 15px; font-weight: bold; color: #2dd4bf;">$274 <span style="font-size: 11px; font-weight: normal;">(w/ domain)</span></td>
                            <td style="padding: 15px; font-weight: bold; color: #f87171;">$2,115</td>
                        </tr>
                    </table>
                </div>
                
                <div style="text-align: center; margin-top: 25px;">
                    <p style="font-size: 16px; color: {text_dark}; font-weight: bold;">That is $1,841 in savings.</p>
                    <a href="https://wa.me/966572562151" style="display: inline-block; margin-top: 10px; background-color: {text_dark}; color: #ffffff; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: 600;">Message me to start saving</a>
                </div>
                {footer}
            </div>
        </body>
        </html>
        """

    elif phase == 4:
        subject = parse_spintax("Update {name} website using Excel?")
        html = f"""
        <html>
        <body style="margin: 0; padding: 20px; background-color: {bg_body}; font-family: {font_family};">
            <div style="max-width: 600px; margin: 0 auto; background-color: {bg_card}; border-radius: 12px; padding: 35px 30px; border: 1px solid #e5e7eb;">
                <h2 style="color: {text_dark}; font-size: 18px; margin-top: 0;">{greeting},</h2>
                <p style="font-size: 15px; line-height: 1.6; color: {text_main};">
                    One of the main reasons clinics don't build websites is because they don't want to learn complex dashboards or pay a developer every time they need to change a price.
                </p>
                <div style="background-color: #f0fdf4; border: 1px solid #bbf7d0; padding: 20px; border-radius: 8px; margin: 25px 0;">
                    <h3 style="color: #166534; font-size: 16px; margin: 0 0 10px 0;">📊 The Spreadsheet CMS</h3>
                    <p style="color: #15803d; font-size: 14px; margin: 0; line-height: 1.5;">
                        With our architecture, <strong>your website is hard-wired directly to a private Google Sheet.</strong> If you or your receptionist can type into an Excel file, you can manage your entire website. 
                    </p>
                </div>
                <p style="font-size: 15px; line-height: 1.6; color: {text_main};">
                    Change a price in the spreadsheet, and your live website updates globally in seconds. Should I build a quick prototype so you can see how easy this is?
                </p>
                {footer}
            </div>
        </body>
        </html>
        """

    elif phase == 5:
        subject = parse_spintax("The 2026 Google algorithm & [Name]").replace("[Name]", name)
        html = f"""
        <html>
        <body style="margin: 0; padding: 20px; background-color: {bg_body}; font-family: {font_family};">
            <div style="max-width: 600px; margin: 0 auto; background-color: {bg_card}; border-radius: 12px; padding: 35px 30px; border: 1px solid #e5e7eb; border-top: 5px solid {warning};">
                <h2 style="color: {text_dark}; font-size: 18px; margin-top: 0;">Urgent Ranking Notice for {name}</h2>
                <p style="font-size: 15px; line-height: 1.6; color: {text_main};">
                    {greeting}, I am reaching out regarding the missing website link on your Google Maps profile because the rules of local SEO are officially changing.
                </p>
                <div style="background-color: {warning_light}; padding: 20px; border-radius: 8px; margin: 25px 0;">
                    <strong style="color: #be123c; font-size: 16px;">The 2026 AI Algorithm Shift:</strong>
                    <p style="color: #9f1239; font-size: 14px; margin: 8px 0 0 0; line-height: 1.5;">
                        Google’s AI search now significantly increases the weight of <i>linked, fast-loading</i> websites. Profiles without them are actively being suppressed and hidden from patients in the Map Pack.
                    </p>
                </div>
                <p style="font-size: 15px; line-height: 1.6; color: {text_main};">
                    Our architecture achieves a <strong>100/100 Google PageSpeed score</strong>, ensuring you stay at the top of local searches.
                </p>
                <div style="text-align: center; margin-top: 30px;">
                    <a href="https://wa.me/966572562151?text=YES" style="background-color: {text_dark}; color: #ffffff; padding: 14px 28px; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 15px;">SECURE YOUR RANKING (FREE DEMO)</a>
                </div>
                {footer}
            </div>
        </body>
        </html>
        """

    elif phase == 6:
        # Phase 6 stays visually clean and simple to look like a personal follow-up.
        subject = "am I off base here?"
        html = f"""
        <html>
        <body style="margin: 0; padding: 20px; background-color: {bg_body}; font-family: {font_family};">
            <div style="max-width: 600px; margin: 0 auto; background-color: {bg_card}; border-radius: 12px; padding: 35px 30px; border: 1px solid #e5e7eb;">
                <p style="font-size: 15px; line-height: 1.6; color: {text_main}; margin-top: 0;">{greeting},</p>
                <p style="font-size: 15px; line-height: 1.6; color: {text_main};">
                    I've reached out a few times about getting a high-speed, $0 monthly fee website set up for {name}.
                </p>
                <p style="font-size: 15px; line-height: 1.6; color: {text_main};">
                    Am I totally off base here, or is this just a really busy month for the clinic? Just let me know so I can update my notes.
                </p>
                {footer}
            </div>
        </body>
        </html>
        """

    elif phase == 7:
        subject = parse_spintax("{Closing my file|Last email} regarding [Name]").replace("[Name]", name)
        html = f"""
        <html>
        <body style="margin: 0; padding: 20px; background-color: {bg_body}; font-family: {font_family};">
            <div style="max-width: 600px; margin: 0 auto; background-color: {bg_card}; border-radius: 12px; padding: 35px 30px; border: 1px solid #e5e7eb;">
                <div style="text-align: center; margin-bottom: 25px;">
                    <span style="display: inline-block; background-color: #f1f5f9; color: #475569; padding: 6px 16px; border-radius: 20px; font-size: 12px; font-weight: bold; letter-spacing: 1px; text-transform: uppercase;">File Closed</span>
                </div>
                <p style="font-size: 15px; line-height: 1.6; color: {text_main}; margin-top: 0;">{greeting},</p>
                <p style="font-size: 15px; line-height: 1.6; color: {text_main};">
                    Since I haven't heard back, I'll assume that fixing the missing website on your Google profile isn't a priority right now. This will be my last email.
                </p>
                <p style="font-size: 15px; line-height: 1.6; color: {text_main};">
                    If you ever get tired of losing map traffic to competitors, or if you just want to stop paying monthly "Web Rent" to Wix or Shopify, you know where to find me. Wishing {name} a highly successful year.
                </p>
                <div style="margin-top: 35px; padding: 25px; background-color: #f8fafc; border-radius: 8px; text-align: center; border: 1px dashed #cbd5e1;">
                    <strong style="color: {text_dark}; font-size: 16px;">Ready to deploy your site instantly?</strong><br>
                    <a href="https://kiranmondal.gumroad.com/l/titanv50" style="display: inline-block; margin-top: 15px; background-color: {accent}; color: #ffffff; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 14px;">Purchase Direct via Gumroad</a>
                </div>
                {footer}
            </div>
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
