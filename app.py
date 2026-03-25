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
    display_address = "your area" if ("(" in str(address) or str(address).lower() == "n/a" or not address) else address
    display_cat = "Dental" if (str(category).lower() == "n/a" or not category) else category

    # Global UI Typography & Colors (Premium SaaS Aesthetic)
    font = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
    color_bg = "#F8FAFC"          # Light Slate Background
    color_card = "#FFFFFF"        # Pure White Card
    color_text = "#334155"        # Slate Text (Highly readable)
    color_heading = "#0F172A"     # Midnight Slate (Premium look)
    color_teal = "#0D9488"        # Subtle Link Highlights

    # --- MASTER UI WRAPPER ENGINE ---
    def build_premium_html(body_content, badge_text="Titan Engine | Digital Audit", right_text="CONFIDENTIAL"):
        return f"""
        <html>
        <body style="margin: 0; padding: 40px 15px; background-color: {color_bg};">
            <table width="100%" border="0" cellspacing="0" cellpadding="0">
                <tr>
                    <td align="center">
                        <table width="600" border="0" cellspacing="0" cellpadding="0" style="background-color: {color_card}; border: 1px solid #E2E8F0; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.03);">
                            
                            <!-- MINIMALIST BRANDING BAR -->
                            <tr>
                                <td style="padding: 25px 40px 15px 40px; border-bottom: 1px solid #F1F5F9;">
                                    <table width="100%" border="0" cellspacing="0" cellpadding="0">
                                        <tr>
                                            <td style="font-family: {font}; font-size: 11px; font-weight: 700; color: {color_teal}; text-transform: uppercase; letter-spacing: 1.5px;">
                                                {badge_text}
                                            </td>
                                            <td align="right" style="font-family: {font}; font-size: 11px; color: #94A3B8; font-weight: 600; letter-spacing: 1px;">
                                                {right_text}
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>

                            <!-- BODY CONTENT -->
                            <tr>
                                <td style="padding: 35px 40px;">
                                    {body_content}
                                </td>
                            </tr>
                            
                            <!-- EXECUTIVE FOOTER -->
                            <tr>
                                <td style="padding: 25px 40px; background-color: #F8FAFC; border-top: 1px solid #E2E8F0; border-radius: 0 0 12px 12px;">
                                    <p style="margin: 0; font-family: {font}; font-size: 14px; font-weight: 700; color: {color_heading};">
                                        Kiran Deb Mondal
                                    </p>
                                    <p style="margin: 2px 0 0 0; font-family: {font}; font-size: 13px; color: #64748B;">
                                        Principal Technologist | Stop Web Rent
                                    </p>
                                    <p style="margin: 12px 0 0 0; font-family: {font}; font-size: 12px;">
                                        <a href="https://www.StopWebRent.com" style="color: #64748B; text-decoration: none; font-weight: 600;">StopWebRent.com</a>
                                        &nbsp;&nbsp;|&nbsp;&nbsp;
                                        <a href="https://wa.me/966572562151" style="color: #64748B; text-decoration: none; font-weight: 600;">WhatsApp Support</a>
                                    </p>
                                </td>
                            </tr>

                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """

    # --- REUSABLE COMPONENTS ---
    def button(text, url, bg_color=color_heading):
        return f"""
        <table width="100%" border="0" cellspacing="0" cellpadding="0" style="margin: 25px 0;">
            <tr>
                <td align="center">
                    <a href="{url}" style="display: inline-block; padding: 16px 36px; background-color: {bg_color}; color: #FFFFFF; font-family: {font}; font-size: 15px; font-weight: 600; text-decoration: none; border-radius: 8px; box-shadow: 0 4px 6px rgba(15, 23, 42, 0.15);">
                        {text}
                    </a>
                </td>
            </tr>
        </table>
        """

    # ==========================================
    # PHASE 1: THE CORE PROBLEM & PROTOTYPE OFFER
    # ==========================================
    if phase == 1:
        subject = parse_spintax("{Patient inquiry|Google Maps analysis|Missing asset} for [Name]").replace("[Name]", name)
        body = f"""
        <h2 style="margin: 0 0 20px 0; font-family: {font}; font-size: 20px; font-weight: 700; color: {color_heading};">{greeting} {name} team,</h2>
        
        <p style="margin: 0 0 20px 0; font-family: {font}; font-size: 15px; line-height: 1.7; color: {color_text};">
            I was analyzing top-rated <strong>{display_cat}</strong> clinics in {display_address}. Your practice has an incredible reputation, but you are currently dealing with a massive leak in your patient acquisition funnel.
        </p>

        <!-- PREMIUM AMBER ALERT BOX -->
        <table width="100%" border="0" cellspacing="0" cellpadding="0" style="margin: 25px 0; background-color: #FFFBEB; border-left: 4px solid #F59E0B; border-radius: 0 8px 8px 0;">
            <tr>
                <td style="padding: 18px 20px;">
                    <p style="margin: 0 0 5px 0; font-family: {font}; font-size: 14px; font-weight: 700; color: #B45309;">Status: Missing Google Maps Asset</p>
                    <p style="margin: 0; font-family: {font}; font-size: 14px; line-height: 1.6; color: #92400E;">You do not have a "Website" button linked to your Google profile. Google's algorithm actively suppresses clinics without high-speed websites, handing your high-value patients directly to competitors.</p>
                </td>
            </tr>
        </table>

        <h3 style="margin: 30px 0 15px 0; font-family: {font}; font-size: 16px; font-weight: 700; color: {color_heading};">The Fix: Titan Engine Architecture</h3>

        <p style="margin: 0 0 20px 0; font-family: {font}; font-size: 15px; line-height: 1.7; color: {color_text};">
            I engineer <strong>0.1s High-Velocity</strong> web frameworks specifically for healthcare providers. Because I use static-site architecture, it is 100% unhackable. Best of all? <strong>I charge $0 in monthly hosting fees.</strong>
        </p>

        <div style="background-color: #F8FAFC; border: 1px dashed #CBD5E1; padding: 20px; text-align: center; border-radius: 8px; margin-bottom: 20px;">
            <p style="margin: 0; font-family: {font}; font-size: 15px; font-weight: 700; color: {color_heading};">My Offer: A Free 24-Hour Prototype</p>
            <p style="margin: 5px 0 0 0; font-family: {font}; font-size: 13px; color: #64748B;">I will use your existing logo and photos. If you don't love it, you pay nothing.</p>
        </div>

        {button("Review Your Free Prototype &rarr;", "https://wa.me/966572562151?text=YES")}
        
        <p align="center" style="margin: 0; font-family: {font}; font-size: 13px;">
            <a href="https://hv-furniture-bit.github.io/dental-junction-behala/index.html" style="color: {color_teal}; font-weight: 600; text-decoration: underline;">Or click here to view a live tech demo</a>
        </p>
        """
        html = build_premium_html(body)

    # ==========================================
    # PHASE 2: VISUAL PROOF & TECHNICAL VALUE
    # ==========================================
    elif phase == 2:
        subject = f"Re: {name} digital prototype"
        body = f"""
        <h2 style="margin: 0 0 20px 0; font-family: {font}; font-size: 18px; font-weight: 700; color: {color_heading};">{greeting} again,</h2>
        
        <p style="margin: 0 0 20px 0; font-family: {font}; font-size: 15px; line-height: 1.7; color: {color_text};">
            I wanted to follow up on my last note. When I deploy a Titan Engine site for a practice like <strong>{name}</strong>, it is not just a digital brochure—it is an automated lead generation machine.
        </p>

        <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 20px; border-radius: 8px; margin: 25px 0;">
            <p style="margin: 0 0 10px 0; font-family: {font}; font-size: 14px; font-weight: 700; color: {color_heading};">⚡ Core Specifications Included:</p>
            <ul style="margin: 0; padding-left: 20px; font-family: {font}; font-size: 14px; line-height: 1.8; color: {color_text};">
                <li><strong>WhatsApp Routing:</strong> Patients book consultations in one tap.</li>
                <li><strong>Multilingual Engine:</strong> Instantly translates to local dialects.</li>
                <li><strong>Mobile-Native PWA:</strong> Installs directly onto your patient's smartphone screen like an app.</li>
            </ul>
        </div>

        <p style="margin: 0 0 20px 0; font-family: {font}; font-size: 15px; line-height: 1.7; color: {color_text}; text-align: center;">
            Would you like me to build a custom risk-free prototype for {name} today?
        </p>

        {button("Yes, Build My Prototype", "https://wa.me/966572562151?text=YES")}
        """
        html = build_premium_html(body, "Titan Engine | Spec Sheet", "FOLLOW UP")

    # ==========================================
    # PHASE 3: THE FINANCIAL SHIFT
    # ==========================================
    elif phase == 3:
        subject = parse_spintax("{Financial analysis|Stop paying web rent} for [Name]").replace("[Name]", name)
        body = f"""
        <h2 style="margin: 0 0 20px 0; font-family: {font}; font-size: 20px; font-weight: 700; color: {color_heading}; text-align: center;">Stop Renting. Start Owning.</h2>
        
        <p style="margin: 0 0 25px 0; font-family: {font}; font-size: 15px; line-height: 1.7; color: {color_text}; text-align: center;">
            Most {display_cat} clinics are trapped paying $30-$50 every single month to Wix or Shopify just to keep their site online. The Titan Engine changes that. <strong>Pay a one-time setup fee, and own it forever.</strong>
        </p>

        <!-- CLEAN SAAS PRICING TABLE -->
        <table width="100%" border="0" cellspacing="0" cellpadding="0" style="border: 1px solid #E2E8F0; border-radius: 8px; margin-bottom: 25px;">
            <tr>
                <td style="padding: 15px; border-bottom: 1px solid #E2E8F0; font-family: {font}; font-size: 13px; color: #64748B; font-weight: 600;">5-YEAR COST PROJECTION</td>
                <td align="right" style="padding: 15px; border-bottom: 1px solid #E2E8F0; font-family: {font}; font-size: 13px; color: {color_heading}; font-weight: 700;">TITAN ENGINE</td>
                <td align="right" style="padding: 15px; border-bottom: 1px solid #E2E8F0; font-family: {font}; font-size: 13px; color: #64748B; font-weight: 600;">WIX / SHOPIFY</td>
            </tr>
            <tr>
                <td style="padding: 15px; border-bottom: 1px solid #E2E8F0; font-family: {font}; font-size: 15px; color: {color_text};">Setup Fee</td>
                <td align="right" style="padding: 15px; border-bottom: 1px solid #E2E8F0; font-family: {font}; font-size: 15px; font-weight: 700; color: {color_heading};">$199</td>
                <td align="right" style="padding: 15px; border-bottom: 1px solid #E2E8F0; font-family: {font}; font-size: 15px; color: #64748B;">$0</td>
            </tr>
            <tr>
                <td style="padding: 15px; border-bottom: 1px solid #E2E8F0; font-family: {font}; font-size: 15px; color: {color_text};">Monthly Web Rent</td>
                <td align="right" style="padding: 15px; border-bottom: 1px solid #E2E8F0; font-family: {font}; font-size: 15px; font-weight: 700; color: {color_teal};">$0</td>
                <td align="right" style="padding: 15px; border-bottom: 1px solid #E2E8F0; font-family: {font}; font-size: 15px; color: #64748B;">$1,740</td>
            </tr>
            <tr style="background-color: #F8FAFC;">
                <td style="padding: 15px; font-family: {font}; font-size: 15px; font-weight: 700; color: {color_heading}; border-radius: 0 0 0 8px;">Total Cost</td>
                <td align="right" style="padding: 15px; font-family: {font}; font-size: 16px; font-weight: 800; color: {color_teal};">$274</td>
                <td align="right" style="padding: 15px; font-family: {font}; font-size: 15px; font-weight: 700; color: #EF4444; border-radius: 0 0 8px 0;">$2,115</td>
            </tr>
        </table>

        <p style="margin: 0; font-family: {font}; font-size: 16px; line-height: 1.7; color: {color_heading}; text-align: center; font-weight: 700;">
            That is $1,841 in direct savings.
        </p>

        {button("Claim Your $1,841 Savings", "https://wa.me/966572562151")}
        """
        html = build_premium_html(body, "Titan Engine | ROI Analysis", "FINANCIALS")

    # ==========================================
    # PHASE 4: THE EASE OF USE (Spreadsheet CMS)
    # ==========================================
    elif phase == 4:
        subject = parse_spintax("Update {name} website using Excel?")
        body = f"""
        <h2 style="margin: 0 0 20px 0; font-family: {font}; font-size: 18px; font-weight: 700; color: {color_heading};">{greeting},</h2>
        
        <p style="margin: 0 0 20px 0; font-family: {font}; font-size: 15px; line-height: 1.7; color: {color_text};">
            The #1 reason clinics avoid building professional websites is because they hate learning complex WordPress dashboards and paying developers $100 just to change a service price.
        </p>

        <!-- GREEN INFO BOX -->
        <table width="100%" border="0" cellspacing="0" cellpadding="0" style="margin: 25px 0; background-color: #F0FDF4; border-left: 4px solid #16A34A; border-radius: 0 8px 8px 0;">
            <tr>
                <td style="padding: 18px 20px;">
                    <p style="margin: 0 0 5px 0; font-family: {font}; font-size: 14px; font-weight: 700; color: #166534;">📊 The Spreadsheet CMS</p>
                    <p style="margin: 0; font-family: {font}; font-size: 14px; line-height: 1.6; color: #15803D;">Your entire website is hard-wired directly to a private Google Sheet. If your receptionist can type into an Excel file, they can manage your entire digital presence. Change a price in the sheet, and your live website updates globally in 1 second.</p>
                </td>
            </tr>
        </table>

        <p style="margin: 0 0 20px 0; font-family: {font}; font-size: 15px; line-height: 1.7; color: {color_text}; text-align: center;">
            Should I build a quick prototype so you can see exactly how easy this is?
        </p>

        {button("Yes, Build The Prototype", "https://wa.me/966572562151?text=YES")}
        """
        html = build_premium_html(body, "Titan Engine | Infrastructure", "TECH UPDATE")

    # ==========================================
    # PHASE 5: THE FEAR / FOMO (2026 Shift)
    # ==========================================
    elif phase == 5:
        subject = parse_spintax("The 2026 Google algorithm & [Name]").replace("[Name]", name)
        body = f"""
        <h2 style="margin: 0 0 20px 0; font-family: {font}; font-size: 20px; font-weight: 700; color: #B91C1C; text-align: center;">Urgent Ranking Notice</h2>
        
        <p style="margin: 0 0 20px 0; font-family: {font}; font-size: 15px; line-height: 1.7; color: {color_text}; text-align: center;">
            {greeting}, I am reaching out regarding the missing website link on your Google Maps profile because the rules of local SEO are officially changing.
        </p>

        <!-- RED MUTED ALERT BOX -->
        <table width="100%" border="0" cellspacing="0" cellpadding="0" style="margin: 25px 0; background-color: #FEF2F2; border: 1px solid #FECACA; border-radius: 8px;">
            <tr>
                <td style="padding: 20px; text-align: center;">
                    <p style="margin: 0 0 10px 0; font-family: {font}; font-size: 15px; font-weight: 700; color: #991B1B;">The 2026 AI Algorithm Shift</p>
                    <p style="margin: 0; font-family: {font}; font-size: 14px; line-height: 1.6; color: #B91C1C;">Google’s AI search now significantly increases the weight of <i>linked, fast-loading</i> websites. Profiles without them are actively being suppressed and hidden from patients in the Map Pack.</p>
                </td>
            </tr>
        </table>

        <p style="margin: 0 0 20px 0; font-family: {font}; font-size: 15px; line-height: 1.7; color: {color_heading}; font-weight: 600; text-align: center;">
            Our architecture achieves a 100/100 Google PageSpeed score, ensuring you stay at the top.
        </p>

        {button("Secure Your Ranking Today", "https://wa.me/966572562151?text=YES", "#B91C1C")}
        """
        html = build_premium_html(body, "Titan Engine | SEO Alert", "ALGORITHM SHIFT")

    # ==========================================
    # PHASE 6: THE HUMAN CHECK-IN
    # ==========================================
    elif phase == 6:
        # Intentionally stripped down to look like a direct, personal follow-up
        subject = "am I off base here?"
        body = f"""
        <p style="margin: 0 0 15px 0; font-family: {font}; font-size: 15px; line-height: 1.7; color: {color_text};">{greeting},</p>
        
        <p style="margin: 0 0 15px 0; font-family: {font}; font-size: 15px; line-height: 1.7; color: {color_text};">
            I've reached out a few times about getting a high-speed, $0 monthly fee website set up for {name}.
        </p>
        
        <p style="margin: 0 0 25px 0; font-family: {font}; font-size: 15px; line-height: 1.7; color: {color_text};">
            Am I totally off base here, or is this just a really busy month for the clinic? Just let me know so I can update my notes.
        </p>

        {button("Message Kiran Directly", "https://wa.me/966572562151")}
        """
        html = build_premium_html(body, "Titan Engine | Client Relations", "CHECK IN")

    # ==========================================
    # PHASE 7: THE BREAKUP / DIRECT PURCHASE
    # ==========================================
    elif phase == 7:
        subject = parse_spintax("{Closing my file|Last email} regarding [Name]").replace("[Name]", name)
        body = f"""
        <div style="text-align: center; margin-bottom: 25px;">
            <span style="background-color: #F1F5F9; color: #475569; padding: 6px 16px; border-radius: 20px; font-family: {font}; font-size: 11px; font-weight: 800; letter-spacing: 1px; text-transform: uppercase;">File Closed</span>
        </div>
        
        <p style="margin: 0 0 15px 0; font-family: {font}; font-size: 15px; line-height: 1.7; color: {color_text};">{greeting},</p>
        
        <p style="margin: 0 0 15px 0; font-family: {font}; font-size: 15px; line-height: 1.7; color: {color_text};">
            Since I haven't heard back, I'll assume that fixing the missing website on your Google profile isn't a priority right now. This will be my last email.
        </p>
        
        <p style="margin: 0 0 30px 0; font-family: {font}; font-size: 15px; line-height: 1.7; color: {color_text};">
            If you ever get tired of losing map traffic to competitors, or if you just want to stop paying "Web Rent" to Wix or Shopify, you know where to find me. Wishing {name} a highly successful year.
        </p>
        
        <div style="margin-top: 35px; padding-top: 30px; border-top: 1px solid #E2E8F0; text-align: center;">
            <p style="margin: 0 0 15px 0; font-family: {font}; font-size: 14px; font-weight: 700; color: {color_heading};">
                Ready to bypass the demo and deploy instantly?
            </p>
            {button("Purchase Direct via Gumroad", "https://kiranmondal.gumroad.com/l/titanv50", color_teal)}
        </div>
        """
        html = build_premium_html(body, "Titan Engine | File Closed", "FINAL NOTICE")
        
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
