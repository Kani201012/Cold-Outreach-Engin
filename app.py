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

# --- 1. PERMANENT CONNECTION ---
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

# --- 3. THE HIGH-VISUAL NEWSLETTER UI (MATCHING SCREENSHOT) ---
def get_campaign_content(phase, name, category, address):
    greeting = random.choice(["Hi", "Hello", "Greetings", "Dear"])
    
    display_address = "your city" if ("(" in str(address) or str(address).lower() == "n/a" or not address) else address
    display_cat = "Dental" if (str(category).lower() == "n/a" or not category) else category

    # UI Colors from your screenshot
    bg_outer = "#f4f5f7"
    bg_inner = "#ffffff"
    color_header_bg = "#1e293b"    # Dark slate
    color_header_txt = "#14b8a6"   # Cyan/Teal
    color_text = "#475569"         # Slate text
    color_dark = "#0f172a"         # Deep black/slate
    color_teal = "#0d9488"         # Button/Links
    color_red_bg = "#fff1f2"
    color_red_border = "#f43f5e"
    color_red_text = "#e11d48"

    # --- SHARED UI COMPONENTS ---
    header = f"""
    <tr>
        <td style="background-color: {color_header_bg}; text-align: center; padding: 40px 20px;">
            <h1 style="color: {color_header_txt}; margin: 0; font-family: Arial, sans-serif; font-size: 24px; font-weight: 900; letter-spacing: 2px; text-transform: uppercase;">STOP WEB RENT</h1>
            <p style="color: #94a3b8; margin: 8px 0 0 0; font-family: Arial, sans-serif; font-size: 12px; font-style: italic;">High-Velocity Web Architecture</p>
        </td>
    </tr>
    """

    footer = f"""
    <tr>
        <td style="background-color: #f8fafc; padding: 30px; text-align: center; border-top: 1px solid #e2e8f0;">
            <p style="margin: 0; font-family: Arial, sans-serif; font-size: 11px; color: #64748b; font-weight: bold;">
                <span style="color: #334155;">Kiran Deb Mondal</span> | Principal Technologist | Stop Web Rent
            </p>
            <p style="margin: 8px 0 0 0; font-family: Arial, sans-serif; font-size: 11px; color: #64748b;">
                WhatsApp: +966 572562151 | <a href="https://www.StopWebRent.com" style="color: {color_teal}; font-weight: bold; text-decoration: underline;">www.StopWebRent.com</a>
            </p>
        </td>
    </tr>
    """

    def wrap_html(content_body):
        return f"""
        <html>
        <body style="margin: 0; padding: 30px 15px; background-color: {bg_outer};">
            <table width="100%" border="0" cellspacing="0" cellpadding="0">
                <tr>
                    <td align="center">
                        <table width="600" border="0" cellspacing="0" cellpadding="0" style="background-color: {bg_inner}; border: 1px solid #e2e8f0; border-radius: 6px; overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                            {header}
                            <tr>
                                <td style="padding: 40px 30px;">
                                    {content_body}
                                </td>
                            </tr>
                            {footer}
                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """

    # -------------------------------------------------------------------------
    # PHASE 1: EXACT MATCH TO YOUR SCREENSHOT
    # -------------------------------------------------------------------------
    if phase == 1:
        subject = parse_spintax("{Action Required|Google Maps alert|Missing link} for [Name]").replace("[Name]", name)
        body = f"""
        <h2 style="color: {color_dark}; font-family: Arial, sans-serif; font-size: 18px; margin-top: 0;">{greeting} {name} team,</h2>
        
        <p style="font-family: Arial, sans-serif; font-size: 14px; color: {color_text}; line-height: 1.7;">
            I was recently researching on <strong>{display_cat}</strong> clinics in {display_address} and noticed that your clinic has a fantastic reputation on Google Maps.
        </p>
        
        <p style="font-family: Arial, sans-serif; font-size: 14px; color: {color_text}; line-height: 1.7;">
            However, I noticed you don't have a website linked to your profile. I am reaching out because, as of 2026, <strong>Google's algorithm has significantly increased the weight of linked websites</strong> for local rankings.
        </p>

        <!-- RED WARNING BOX -->
        <div style="background-color: {color_red_bg}; border-left: 4px solid {color_red_border}; padding: 16px; margin: 25px 0;">
            <strong style="color: #9f1239; font-family: Arial, sans-serif; font-size: 15px;">⚠️ The Risk:</strong>
            <p style="color: {color_red_text}; font-family: Arial, sans-serif; font-size: 13px; margin: 5px 0 0 0; line-height: 1.5;">
                If your competitors have a "Website" button and you don't, Google's AI search will eventually lower your visibility in the Map Pack.
            </p>
        </div>

        <!-- SUBHEADING -->
        <h3 style="color: {color_dark}; font-family: Arial, sans-serif; font-size: 16px; border-bottom: 2px solid {color_teal}; display: inline-block; padding-bottom: 4px; margin-bottom: 15px;">The Solution: Titan Engine</h3>

        <p style="font-family: Arial, sans-serif; font-size: 14px; color: {color_text}; line-height: 1.7;">
            I build <strong>0.1s Load Speed</strong> frameworks designed to help local services dominate without "Web Rent" (monthly subscriptions).
        </p>

        <div style="text-align: center; margin: 25px 0;">
            <a href="https://hv-furniture-bit.github.io/dental-junction-behala/index.html" style="color: {color_teal}; font-family: Arial, sans-serif; font-size: 16px; font-weight: bold; text-decoration: underline;">View the live tech demo here: Ghosh Dental Clinic</a>
        </div>

        <!-- DARK TABLE -->
        <table width="100%" border="0" cellspacing="0" cellpadding="0" style="border: 1px solid #e2e8f0; font-family: Arial, sans-serif; font-size: 13px; margin-bottom: 30px;">
            <tr>
                <th style="background-color: {color_dark}; color: #ffffff; padding: 12px; text-align: left;">Category</th>
                <th style="background-color: {color_dark}; color: #ffffff; padding: 12px; text-align: center;">Titan Engine</th>
                <th style="background-color: {color_dark}; color: #ffffff; padding: 12px; text-align: center;">Wix / Shopify</th>
            </tr>
            <tr>
                <td style="padding: 12px; border-bottom: 1px solid #e2e8f0; color: {color_text};">Monthly Rent</td>
                <td style="padding: 12px; border-bottom: 1px solid #e2e8f0; text-align: center; color: {color_teal}; font-weight: bold;">$0</td>
                <td style="padding: 12px; border-bottom: 1px solid #e2e8f0; text-align: center; color: {color_text};">$35+</td>
            </tr>
            <tr style="background-color: #f0fdfa;">
                <td style="padding: 12px; font-weight: bold; color: {color_dark};">5-Year Savings</td>
                <td style="padding: 12px; text-align: center; color: {color_teal}; font-weight: bold; font-size: 14px;">$1,841</td>
                <td style="padding: 12px; text-align: center; color: {color_text};">$0</td>
            </tr>
        </table>

        <p style="text-align: center; font-family: Arial, sans-serif; font-size: 14px; font-weight: bold; color: {color_dark}; margin-bottom: 20px;">
            My Offer: A Free 24-Hour Preview (Using your logo & photos)
        </p>

        <!-- MASSIVE CTA BUTTON -->
        <a href="https://wa.me/966572562151?text=YES" style="display: block; background-color: {color_teal}; color: #ffffff; text-align: center; padding: 18px 0; font-family: Arial, sans-serif; font-size: 16px; font-weight: 900; text-decoration: none; border-radius: 6px; letter-spacing: 1px;">
            REPLY 'YES' FOR FREE DEMO
        </a>

        <div style="text-align: center; margin-top: 15px;">
            <a href="https://kiranmondal.gumroad.com/l/titanv50" style="color: {color_teal}; font-family: Arial, sans-serif; font-size: 13px; font-weight: bold; text-decoration: underline;">GET Your Website within 24 Hours (Buy Now)</a>
        </div>
        """
        html = wrap_html(body)

    # -------------------------------------------------------------------------
    # PHASE 2: VISUAL PROOF
    # -------------------------------------------------------------------------
    elif phase == 2:
        subject = f"Re: {name} digital preview"
        body = f"""
        <h2 style="color: {color_dark}; font-family: Arial, sans-serif; font-size: 18px; margin-top: 0;">{greeting} again,</h2>
        
        <p style="font-family: Arial, sans-serif; font-size: 14px; color: {color_text}; line-height: 1.7;">
            I wanted to follow up on my last email. When I build a Titan Engine site for a clinic like <strong>{name}</strong>, it's not just a digital brochure—it's a lead generation machine.
        </p>

        <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 20px; margin: 25px 0;">
            <strong style="color: {color_dark}; font-family: Arial, sans-serif; font-size: 15px;">⚡ Technical Specifications Included:</strong>
            <ul style="font-family: Arial, sans-serif; font-size: 14px; color: {color_text}; line-height: 1.8; margin-top: 10px; margin-bottom: 0;">
                <li><strong>WhatsApp Routing:</strong> Patients book in one tap.</li>
                <li><strong>Multilingual:</strong> Instantly translates to local languages.</li>
                <li><strong>Mobile-Native:</strong> Installs directly to patient's phones.</li>
            </ul>
        </div>

        <p style="text-align: center; font-family: Arial, sans-serif; font-size: 14px; font-weight: bold; color: {color_dark}; margin-bottom: 20px;">
            Would you like me to build a custom prototype for {name}?
        </p>

        <a href="https://wa.me/966572562151?text=YES" style="display: block; background-color: {color_teal}; color: #ffffff; text-align: center; padding: 18px 0; font-family: Arial, sans-serif; font-size: 16px; font-weight: 900; text-decoration: none; border-radius: 6px; letter-spacing: 1px;">
            YES, BUILD MY PROTOTYPE
        </a>
        
        <div style="text-align: center; margin-top: 15px;">
            <a href="https://hv-furniture-bit.github.io/dental-junction-behala/index.html" style="color: {color_teal}; font-family: Arial, sans-serif; font-size: 14px; font-weight: bold; text-decoration: underline;">Click here to view the Live Demo Environment</a>
        </div>
        """
        html = wrap_html(body)

    # -------------------------------------------------------------------------
    # PHASE 3: FINANCIAL FOCUS
    # -------------------------------------------------------------------------
    elif phase == 3:
        subject = parse_spintax("{Stop paying|How to save $1,800 on} website rent")
        body = f"""
        <h2 style="color: {color_dark}; font-family: Arial, sans-serif; font-size: 18px; margin-top: 0; text-align: center;">Stop Renting. Start Owning.</h2>
        
        <p style="font-family: Arial, sans-serif; font-size: 14px; color: {color_text}; line-height: 1.7; text-align: center;">
            Most clinics are trapped paying $30-$50 every month to Wix or Shopify. The Titan Engine changes that. <strong>Pay a one-time setup fee, and own it forever.</strong>
        </p>

        <table width="100%" border="0" cellspacing="0" cellpadding="0" style="border: 1px solid #e2e8f0; font-family: Arial, sans-serif; font-size: 14px; margin: 30px 0;">
            <tr>
                <th style="background-color: {color_dark}; color: #ffffff; padding: 15px; text-align: left;">5-Year Projection</th>
                <th style="background-color: {color_teal}; color: #ffffff; padding: 15px; text-align: center;">Titan Engine</th>
                <th style="background-color: #334155; color: #ffffff; padding: 15px; text-align: center;">Wix / Shopify</th>
            </tr>
            <tr>
                <td style="padding: 15px; border-bottom: 1px solid #e2e8f0; color: {color_text};">Setup Fee</td>
                <td style="padding: 15px; border-bottom: 1px solid #e2e8f0; text-align: center; font-weight: bold; color: {color_dark};">$199</td>
                <td style="padding: 15px; border-bottom: 1px solid #e2e8f0; text-align: center; color: {color_text};">$0</td>
            </tr>
            <tr>
                <td style="padding: 15px; border-bottom: 1px solid #e2e8f0; color: {color_text};">Monthly Rent</td>
                <td style="padding: 15px; border-bottom: 1px solid #e2e8f0; text-align: center; font-weight: bold; color: {color_teal};">$0</td>
                <td style="padding: 15px; border-bottom: 1px solid #e2e8f0; text-align: center; color: {color_text};">$1,740</td>
            </tr>
            <tr style="background-color: #f0fdfa;">
                <td style="padding: 15px; font-weight: bold; color: {color_dark};">Total Cost</td>
                <td style="padding: 15px; text-align: center; font-weight: bold; color: {color_teal}; font-size: 16px;">$274</td>
                <td style="padding: 15px; text-align: center; font-weight: bold; color: {color_red_text};">$2,115</td>
            </tr>
        </table>

        <p style="text-align: center; font-family: Arial, sans-serif; font-size: 16px; font-weight: bold; color: {color_dark}; margin-bottom: 25px;">
            That is $1,841 in direct savings.
        </p>

        <a href="https://wa.me/966572562151" style="display: block; background-color: {color_teal}; color: #ffffff; text-align: center; padding: 18px 0; font-family: Arial, sans-serif; font-size: 16px; font-weight: 900; text-decoration: none; border-radius: 6px; letter-spacing: 1px;">
            CLAIM YOUR $1,841 SAVINGS
        </a>
        """
        html = wrap_html(body)

    # -------------------------------------------------------------------------
    # PHASES 4, 5, 6, 7 (Using the exact same visual wrapper framework)
    # -------------------------------------------------------------------------
    elif phase == 4:
        subject = parse_spintax("Update {name} website using Excel?")
        body = f"""
        <h2 style="color: {color_dark}; font-family: Arial, sans-serif; font-size: 18px; margin-top: 0;">{greeting},</h2>
        <p style="font-family: Arial, sans-serif; font-size: 14px; color: {color_text}; line-height: 1.7;">Clinics avoid building websites because they hate complex dashboards and paying web developers.</p>
        
        <div style="background-color: #f0fdf4; border-left: 4px solid #16a34a; padding: 20px; margin: 25px 0;">
            <strong style="color: #166534; font-family: Arial, sans-serif; font-size: 16px;">📊 The Spreadsheet CMS</strong>
            <p style="color: #15803d; font-family: Arial, sans-serif; font-size: 14px; margin: 8px 0 0 0; line-height: 1.6;">
                Your website is hard-wired directly to a private Google Sheet. If your receptionist can type into Excel, they can manage your entire website. Change a price, and it updates globally in 1 second.
            </p>
        </div>

        <p style="text-align: center; font-family: Arial, sans-serif; font-size: 15px; font-weight: bold; color: {color_dark}; margin-bottom: 20px;">Should I build a quick prototype so you can see how easy this is?</p>
        <a href="https://wa.me/966572562151?text=YES" style="display: block; background-color: {color_teal}; color: #ffffff; text-align: center; padding: 18px 0; font-family: Arial, sans-serif; font-size: 16px; font-weight: 900; text-decoration: none; border-radius: 6px;">YES, BUILD PROTOTYPE</a>
        """
        html = wrap_html(body)

    elif phase == 5:
        subject = parse_spintax("The 2026 Google algorithm & [Name]").replace("[Name]", name)
        body = f"""
        <h2 style="color: {color_red_text}; font-family: Arial, sans-serif; font-size: 20px; margin-top: 0; text-align: center;">Urgent Ranking Notice</h2>
        <p style="font-family: Arial, sans-serif; font-size: 14px; color: {color_text}; line-height: 1.7; text-align: center;">{greeting}, I am reaching out regarding the missing website link on your Google Maps profile because the rules of local SEO are officially changing.</p>
        
        <div style="background-color: {color_red_bg}; border: 1px solid {color_red_border}; padding: 20px; margin: 25px 0; border-radius: 6px; text-align: center;">
            <strong style="color: #9f1239; font-family: Arial, sans-serif; font-size: 16px;">The 2026 AI Algorithm Shift:</strong>
            <p style="color: {color_red_text}; font-family: Arial, sans-serif; font-size: 14px; line-height: 1.6; margin: 10px 0 0 0;">Google’s AI search now significantly increases the weight of <i>linked, fast-loading</i> websites. Profiles without them are actively being suppressed and hidden from patients in the Map Pack.</p>
        </div>

        <p style="text-align: center; font-family: Arial, sans-serif; font-size: 15px; font-weight: bold; color: {color_dark}; margin-bottom: 25px;">Our architecture achieves a 100/100 Google PageSpeed score, ensuring you stay at the top.</p>
        <a href="https://wa.me/966572562151?text=YES" style="display: block; background-color: {color_red_text}; color: #ffffff; text-align: center; padding: 18px 0; font-family: Arial, sans-serif; font-size: 16px; font-weight: 900; text-decoration: none; border-radius: 6px;">SECURE YOUR RANKING TODAY</a>
        """
        html = wrap_html(body)

    elif phase == 6:
        subject = "am I off base here?"
        body = f"""
        <p style="font-family: Arial, sans-serif; font-size: 15px; color: {color_text}; line-height: 1.7;">{greeting},</p>
        <p style="font-family: Arial, sans-serif; font-size: 15px; color: {color_text}; line-height: 1.7;">I've reached out a few times about getting a high-speed, $0 monthly fee website set up for {name}.</p>
        <p style="font-family: Arial, sans-serif; font-size: 15px; color: {color_text}; line-height: 1.7;">Am I totally off base here, or is this just a really busy month for the clinic? Just let me know so I can update my notes.</p>
        
        <a href="https://wa.me/966572562151" style="display: block; margin-top: 30px; background-color: {color_dark}; color: #ffffff; text-align: center; padding: 15px 0; font-family: Arial, sans-serif; font-size: 15px; font-weight: bold; text-decoration: none; border-radius: 6px;">Message Kiran Directly</a>
        """
        html = wrap_html(body)

    elif phase == 7:
        subject = parse_spintax("{Closing my file|Last email} regarding [Name]").replace("[Name]", name)
        body = f"""
        <div style="text-align: center; margin-bottom: 25px;">
            <span style="background-color: #f1f5f9; color: #475569; padding: 6px 16px; border-radius: 20px; font-family: Arial, sans-serif; font-size: 12px; font-weight: bold; letter-spacing: 1px; text-transform: uppercase;">File Closed</span>
        </div>
        <p style="font-family: Arial, sans-serif; font-size: 15px; color: {color_text}; line-height: 1.7;">{greeting},</p>
        <p style="font-family: Arial, sans-serif; font-size: 15px; color: {color_text}; line-height: 1.7;">Since I haven't heard back, I'll assume that fixing the missing website on your Google profile isn't a priority right now. This will be my last email.</p>
        <p style="font-family: Arial, sans-serif; font-size: 15px; color: {color_text}; line-height: 1.7;">If you ever get tired of losing map traffic to competitors, or if you just want to stop paying "Web Rent" to Wix or Shopify, you know where to find me. Wishing {name} a highly successful year.</p>
        
        <div style="margin-top: 35px; padding-top: 25px; border-top: 1px solid #e2e8f0; text-align: center;">
            <p style="font-family: Arial, sans-serif; font-size: 14px; font-weight: bold; color: {color_dark}; margin-bottom: 15px;">Ready to bypass the demo and deploy instantly?</p>
            <a href="https://kiranmondal.gumroad.com/l/titanv50" style="display: block; background-color: {color_teal}; color: #ffffff; text-align: center; padding: 18px 0; font-family: Arial, sans-serif; font-size: 15px; font-weight: 900; text-decoration: none; border-radius: 6px;">PURCHASE DIRECT VIA GUMROAD</a>
        </div>
        """
        html = wrap_html(body)
        
    return subject, html
# --- 4. STREAMLIT UI SIDEBAR ---
with st.sidebar:
    st.title("⚙️ Credentials")
    user_email = st.text_input("Sender Email", value=st.secrets.get("EMAIL_USER", "kiran@kaydiemscriptlab.com"))
    app_pass = st.text_input("App Password", value=st.secrets.get("EMAIL_PASS", ""), type="password")
    sheet_url = st.text_input("Google Sheet URL", value=st.secrets.get("SHEET_URL", ""))
    if app_pass and sheet_url:
        st.success("✅ Credentials Ready")

# --- 5. MAIN LOGIC & SMTP FIX ---
st.title("🛡️ 7-Phase Master Engine")

if sheet_url:
    try:
        sh = gc.open_by_url(sheet_url)
        worksheet = sh.sheet1
        
        raw_data = worksheet.get_all_values()
        if not raw_data: st.stop()
            
        clean_headers = [str(h).strip() if str(h).strip() else f"Empty_{i}" for i, h in enumerate(raw_data[0])]
        df = pd.DataFrame(raw_data[1:], columns=clean_headers)
        
        limit = st.number_input("Batch Send Limit", value=40, max_value=200)

        if st.button("🚀 IGNITE CAMPAIGN", type="primary", use_container_width=True):
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

                if "@" not in email or status.lower() in ["replied", "bounced", "unsubscribed"]: continue
                if current_step >= 7: continue

                wait_days_map = {0: 0, 1: 3, 2: 4, 3: 4, 4: 6, 5: 6, 6: 6}
                required_wait = wait_days_map.get(current_step, 999)
                
                send_now = False
                if current_step == 0: send_now = True
                elif last_date_str:
                    try:
                        days_elapsed = (datetime.now() - datetime.strptime(last_date_str, "%Y-%m-%d")).days
                        if days_elapsed >= required_wait: send_now = True
                    except: send_now = True 

                if send_now:
                    new_step = current_step + 1
                    subject, html_body = get_campaign_content(new_step, name, category, address)

                    msg = MIMEMultipart()
                    msg['From'] = f"Kiran Deb Mondal <{user_email}>"
                    msg['To'] = email
                    msg['Subject'] = subject
                    msg.attach(MIMEText(html_body, 'html'))

                    try:
                        # THE CRITICAL FIX: OPENING AND CLOSING CONNECTION INSIDE THE LOOP
                        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                            server.login(user_email, app_pass)
                            server.send_message(msg)
                        
                        worksheet.update_cell(index + 2, col_status_idx, f"Phase {new_step} Sent")
                        worksheet.update_cell(index + 2, col_date_idx, datetime.now().strftime("%Y-%m-%d"))
                        worksheet.update_cell(index + 2, col_step_idx, new_step)
                        
                        sent_count += 1
                        st_progress.progress(sent_count / limit)
                        st_status.success(f"✅ [{sent_count}] Sent Phase {new_step} to {name}")
                        
                        if sent_count < limit:
                            time.sleep(random.randint(45, 90))
                            
                    except Exception as e:
                        st_status.error(f"❌ Failed for {email}: {e}")

            st.success("🎉 Campaign Session Finished!")
            st.balloons()
            
    except Exception as e:
        st.error(f"System Error: {e}")
