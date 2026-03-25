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

# --- 3. ULTRA-MODERN APPLE/STRIPE STYLE HTML ENGINE ---
def get_campaign_content(phase, name, category, address):
    greeting = random.choice(["Hi", "Hello", "Greetings", "Dear"])
    
    display_address = "your city" if ("(" in str(address) or str(address).lower() == "n/a" or not address) else address
    display_cat = "Dental" if (str(category).lower() == "n/a" or not category) else category

    # Global Aesthetic Variables
    font = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
    color_bg = "#f4f4f5"          # Soft light gray
    color_card = "#ffffff"        # Pure white
    color_text = "#27272a"        # Deep gray/black
    color_muted = "#71717a"       # Muted gray
    color_black = "#09090b"       # Vercel/Apple Black
    color_emerald = "#10b981"     # Success Green
    color_crimson = "#ef4444"     # Warning Red

    # Dynamic Modern Footer
    footer = f"""
    <tr><td style="padding: 30px 40px; background-color: #fafafa; border-top: 1px solid #e4e4e7; text-align: center; border-radius: 0 0 16px 16px;">
        <p style="margin: 0; font-family: {font}; font-size: 14px; font-weight: 600; color: {color_black};">Kiran Deb Mondal</p>
        <p style="margin: 4px 0 16px 0; font-family: {font}; font-size: 13px; color: {color_muted};">Principal Technologist | Stop Web Rent</p>
        <a href="https://wa.me/966572562151" style="color: {color_black}; text-decoration: none; font-family: {font}; font-size: 13px; font-weight: 500; border: 1px solid #e4e4e7; padding: 6px 12px; border-radius: 6px; background: #fff;">WhatsApp Support</a>
        &nbsp;&nbsp;
        <a href="https://www.stopwebrent.com" style="color: {color_black}; text-decoration: none; font-family: {font}; font-size: 13px; font-weight: 500; border: 1px solid #e4e4e7; padding: 6px 12px; border-radius: 6px; background: #fff;">StopWebRent.com</a>
    </td></tr>
    """

    # Wrapper top
    html_top = f"""
    <html><body style="margin: 0; padding: 40px 20px; background-color: {color_bg};">
    <table width="100%" border="0" cellspacing="0" cellpadding="0"><tr><td align="center">
    <table width="600" border="0" cellspacing="0" cellpadding="0" style="background-color: {color_card}; border-radius: 16px; border: 1px solid #e4e4e7; box-shadow: 0 4px 20px rgba(0,0,0,0.04);">
    """
    # Wrapper bottom
    html_bottom = f"{footer}</table></td></tr></table></body></html>"

    if phase == 1:
        subject = parse_spintax("{Action Required|Google Maps alert|Missing link} for [Name]").replace("[Name]", name)
        html = html_top + f"""
        <tr><td style="background-color: {color_black}; padding: 35px 40px; border-radius: 16px 16px 0 0; text-align: left;">
            <span style="background-color: rgba(255,255,255,0.1); color: #fff; font-family: {font}; font-size: 11px; font-weight: bold; padding: 4px 10px; border-radius: 20px; letter-spacing: 1px; text-transform: uppercase;">System Audit</span>
            <h1 style="color: #ffffff; font-family: {font}; font-size: 24px; margin: 15px 0 0 0; font-weight: 700;">Digital Asset Report</h1>
        </td></tr>
        <tr><td style="padding: 40px;">
            <p style="font-family: {font}; font-size: 16px; color: {color_text}; margin: 0 0 20px 0; line-height: 1.6;">{greeting} {name} team,</p>
            <p style="font-family: {font}; font-size: 16px; color: {color_text}; margin: 0 0 20px 0; line-height: 1.6;">I was researching <strong>{display_cat}</strong> clinics in <strong>{display_address}</strong>. Your practice has a phenomenal reputation, but you are currently missing a critical digital asset:</p>
            
            <table width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color: #fef2f2; border-left: 4px solid {color_crimson}; margin: 25px 0;">
                <tr><td style="padding: 16px 20px; font-family: {font};">
                    <strong style="color: #991b1b; font-size: 15px;">⚠️ Missing Element:</strong><br>
                    <span style="color: {color_crimson}; font-size: 15px; line-height: 1.5; display: inline-block; margin-top: 5px;">You do not have a <strong>"Website"</strong> link on your Google Maps profile. Google's algorithm actively pushes profiles without websites down the rankings.</span>
                </td></tr>
            </table>

            <p style="font-family: {font}; font-size: 16px; color: {color_text}; margin: 0 0 25px 0; line-height: 1.6;">I engineer <strong>0.1s High-Velocity</strong> websites specifically for healthcare clinics. Unlike Wix or Shopify, my Titan Architecture requires <strong>$0 in monthly hosting fees.</strong></p>
            
            <table width="100%" border="0" cellspacing="0" cellpadding="0"><tr><td align="center">
                <a href="https://wa.me/966572562151?text=YES" style="display: inline-block; background-color: {color_black}; color: #ffffff; font-family: {font}; font-size: 15px; font-weight: 600; text-decoration: none; padding: 16px 32px; border-radius: 8px;">Request Free 24-Hour Preview</a>
            </td></tr></table>
            <p style="font-family: {font}; font-size: 13px; color: {color_muted}; text-align: center; margin: 15px 0 0 0;">(I'll use your current logo/photos. If you don't love it, you pay nothing.)</p>
        </td></tr>
        """ + html_bottom

    elif phase == 2:
        subject = f"Re: {name} digital preview"
        html = html_top + f"""
        <tr><td style="padding: 40px;">
            <p style="font-family: {font}; font-size: 16px; color: {color_text}; margin: 0 0 20px 0; line-height: 1.6;">{greeting} again,</p>
            <p style="font-family: {font}; font-size: 16px; color: {color_text}; margin: 0 0 25px 0; line-height: 1.6;">I wanted to follow up on my last email. When I build a Titan Engine site for a clinic like <strong>{name}</strong>, it's not a brochure—it's a lead generation machine.</p>
            
            <table width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color: #fafafa; border: 1px solid #e4e4e7; border-radius: 12px; margin-bottom: 25px;">
                <tr><td style="padding: 24px; font-family: {font};">
                    <strong style="color: {color_black}; font-size: 16px;">Technical Specifications:</strong>
                    <ul style="color: {color_text}; font-size: 15px; line-height: 1.8; margin: 10px 0 0 0; padding-left: 20px;">
                        <li><strong>WhatsApp Routing:</strong> Patients book in one tap.</li>
                        <li><strong>Zero-DB Architecture:</strong> 100% unhackable.</li>
                        <li><strong>Mobile-Native:</strong> Installs directly to patient's phones.</li>
                    </ul>
                </td></tr>
            </table>

            <table width="100%" border="0" cellspacing="0" cellpadding="0"><tr><td align="center">
                <a href="https://hv-furniture-bit.github.io/dental-junction-behala/index.html" style="color: #2563eb; font-family: {font}; font-size: 16px; font-weight: 600; text-decoration: underline;">View the Live Demo Environment &rarr;</a>
            </td></tr></table>
            <p style="font-family: {font}; font-size: 15px; color: {color_text}; text-align: center; margin: 25px 0 0 0;">Reply <strong>"YES"</strong> and I will build a prototype for {name} today.</p>
        </td></tr>
        """ + html_bottom

    elif phase == 3:
        subject = parse_spintax("{Stop paying|How to save $1,800 on} website rent")
        html = html_top + f"""
        <tr><td style="background-color: {color_black}; padding: 35px 40px; border-radius: 16px 16px 0 0; text-align: center;">
            <h1 style="color: #ffffff; font-family: {font}; font-size: 22px; margin: 0; font-weight: 700;">Stop Renting. Start Owning.</h1>
        </td></tr>
        <tr><td style="padding: 40px;">
            <p style="font-family: {font}; font-size: 16px; color: {color_text}; margin: 0 0 25px 0; line-height: 1.6; text-align: center;">Most clinics are trapped paying $30-$50 every month to Wix or Shopify. The Titan Engine changes that. <strong>Pay a one-time setup fee, and own it forever.</strong></p>
            
            <!-- Beautiful Invoice Table -->
            <table width="100%" border="0" cellspacing="0" cellpadding="0" style="border: 1px solid #e4e4e7; border-radius: 8px; overflow: hidden; margin-bottom: 30px;">
                <tr>
                    <td style="background-color: #fafafa; padding: 15px; border-bottom: 1px solid #e4e4e7; font-family: {font}; font-size: 14px; color: {color_muted};">5-Year Projection</td>
                    <td align="right" style="background-color: #fafafa; padding: 15px; border-bottom: 1px solid #e4e4e7; font-family: {font}; font-size: 14px; font-weight: bold; color: {color_black};">Titan Engine</td>
                    <td align="right" style="background-color: #fafafa; padding: 15px; border-bottom: 1px solid #e4e4e7; font-family: {font}; font-size: 14px; color: {color_muted};">Wix/Shopify</td>
                </tr>
                <tr>
                    <td style="padding: 15px; border-bottom: 1px solid #e4e4e7; font-family: {font}; font-size: 15px; color: {color_text};">Setup / Build Fee</td>
                    <td align="right" style="padding: 15px; border-bottom: 1px solid #e4e4e7; font-family: {font}; font-size: 15px; font-weight: bold; color: {color_black};">$199</td>
                    <td align="right" style="padding: 15px; border-bottom: 1px solid #e4e4e7; font-family: {font}; font-size: 15px; color: {color_muted};">$0</td>
                </tr>
                <tr>
                    <td style="padding: 15px; border-bottom: 1px solid #e4e4e7; font-family: {font}; font-size: 15px; color: {color_text};">Monthly Hosting Rent</td>
                    <td align="right" style="padding: 15px; border-bottom: 1px solid #e4e4e7; font-family: {font}; font-size: 15px; font-weight: bold; color: {color_emerald};">$0</td>
                    <td align="right" style="padding: 15px; border-bottom: 1px solid #e4e4e7; font-family: {font}; font-size: 15px; color: {color_muted};">$1,740</td>
                </tr>
                <tr>
                    <td style="background-color: #09090b; padding: 15px; font-family: {font}; font-size: 15px; font-weight: bold; color: #ffffff;">Total Cost</td>
                    <td align="right" style="background-color: #09090b; padding: 15px; font-family: {font}; font-size: 15px; font-weight: bold; color: {color_emerald};">$274 <span style="font-size: 11px; font-weight: normal; color: #a1a1aa;">(w/ domain)</span></td>
                    <td align="right" style="background-color: #09090b; padding: 15px; font-family: {font}; font-size: 15px; font-weight: bold; color: {color_crimson};">$2,115</td>
                </tr>
            </table>

            <table width="100%" border="0" cellspacing="0" cellpadding="0"><tr><td align="center">
                <a href="https://wa.me/966572562151" style="display: inline-block; background-color: {color_black}; color: #ffffff; font-family: {font}; font-size: 15px; font-weight: 600; text-decoration: none; padding: 16px 32px; border-radius: 8px;">Claim Your $1,841 Savings</a>
            </td></tr></table>
        </td></tr>
        """ + html_bottom

    elif phase == 4:
        subject = parse_spintax("Update {name} website using Excel?")
        html = html_top + f"""
        <tr><td style="padding: 40px;">
            <p style="font-family: {font}; font-size: 16px; color: {color_text}; margin: 0 0 20px 0; line-height: 1.6;">{greeting},</p>
            <p style="font-family: {font}; font-size: 16px; color: {color_text}; margin: 0 0 25px 0; line-height: 1.6;">Clinics avoid building websites because they hate complex dashboards and expensive web developers.</p>
            
            <table width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color: #ecfdf5; border: 1px solid #a7f3d0; border-radius: 12px; margin-bottom: 25px;">
                <tr><td style="padding: 24px; font-family: {font};">
                    <span style="font-size: 20px; display: block; margin-bottom: 8px;">📊</span>
                    <strong style="color: #065f46; font-size: 16px;">The Spreadsheet CMS</strong>
                    <p style="color: #047857; font-size: 15px; line-height: 1.6; margin: 8px 0 0 0;">Your website is hard-wired directly to a private Google Sheet. If your receptionist can type into Excel, they can manage your entire website. Change a price, and it updates globally in 1 second.</p>
                </td></tr>
            </table>

            <p style="font-family: {font}; font-size: 16px; color: {color_text}; margin: 0; line-height: 1.6; text-align: center;">Should I build a quick prototype so you can see how easy this is?</p>
        </td></tr>
        """ + html_bottom

    elif phase == 5:
        subject = parse_spintax("The 2026 Google algorithm & [Name]").replace("[Name]", name)
        html = html_top + f"""
        <tr><td style="background-color: {color_crimson}; padding: 35px 40px; border-radius: 16px 16px 0 0; text-align: left;">
            <h1 style="color: #ffffff; font-family: {font}; font-size: 22px; margin: 0; font-weight: 700;">Urgent Ranking Notice</h1>
        </td></tr>
        <tr><td style="padding: 40px;">
            <p style="font-family: {font}; font-size: 16px; color: {color_text}; margin: 0 0 25px 0; line-height: 1.6;">{greeting}, I am reaching out regarding the missing website link on your Google Maps profile because the rules of local SEO are officially changing.</p>
            
            <table width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color: #fef2f2; border: 1px solid #fecaca; border-radius: 12px; margin-bottom: 25px;">
                <tr><td style="padding: 24px; font-family: {font};">
                    <strong style="color: #991b1b; font-size: 16px;">The 2026 AI Algorithm Shift:</strong>
                    <p style="color: #b91c1c; font-size: 15px; line-height: 1.6; margin: 8px 0 0 0;">Google’s AI search now significantly increases the weight of <i>linked, fast-loading</i> websites. Profiles without them are actively being suppressed and hidden from patients in the Map Pack.</p>
                </td></tr>
            </table>

            <p style="font-family: {font}; font-size: 16px; color: {color_text}; margin: 0 0 25px 0; line-height: 1.6;">Our architecture achieves a <strong>100/100 Google PageSpeed score</strong>, ensuring you stay at the top.</p>
            
            <table width="100%" border="0" cellspacing="0" cellpadding="0"><tr><td align="center">
                <a href="https://wa.me/966572562151?text=YES" style="display: inline-block; background-color: {color_crimson}; color: #ffffff; font-family: {font}; font-size: 15px; font-weight: 600; text-decoration: none; padding: 16px 32px; border-radius: 8px;">Secure Your Ranking Today</a>
            </td></tr></table>
        </td></tr>
        """ + html_bottom

    elif phase == 6:
        subject = "am I off base here?"
        html = html_top + f"""
        <tr><td style="padding: 40px;">
            <p style="font-family: {font}; font-size: 16px; color: {color_text}; margin: 0 0 20px 0; line-height: 1.6;">{greeting},</p>
            <p style="font-family: {font}; font-size: 16px; color: {color_text}; margin: 0 0 20px 0; line-height: 1.6;">I've reached out a few times about getting a high-speed, $0 monthly fee website set up for {name}.</p>
            <p style="font-family: {font}; font-size: 16px; color: {color_text}; margin: 0; line-height: 1.6;">Am I totally off base here, or is this just a really busy month for the clinic? Just let me know so I can update my notes.</p>
        </td></tr>
        """ + html_bottom

    elif phase == 7:
        subject = parse_spintax("{Closing my file|Last email} regarding [Name]").replace("[Name]", name)
        html = html_top + f"""
        <tr><td style="padding: 40px;">
            <div style="text-align: center; margin-bottom: 25px;">
                <span style="background-color: #f4f4f5; border: 1px solid #e4e4e7; color: {color_muted}; font-family: {font}; font-size: 11px; font-weight: bold; padding: 4px 12px; border-radius: 20px; letter-spacing: 1px; text-transform: uppercase;">File Closed</span>
            </div>
            <p style="font-family: {font}; font-size: 16px; color: {color_text}; margin: 0 0 20px 0; line-height: 1.6;">{greeting},</p>
            <p style="font-family: {font}; font-size: 16px; color: {color_text}; margin: 0 0 20px 0; line-height: 1.6;">Since I haven't heard back, I'll assume that fixing the missing website on your Google profile isn't a priority right now. This will be my last email.</p>
            <p style="font-family: {font}; font-size: 16px; color: {color_text}; margin: 0 0 30px 0; line-height: 1.6;">If you ever get tired of losing map traffic to competitors, or if you just want to stop paying "Web Rent" to Wix or Shopify, you know where to find me. Wishing {name} a highly successful year.</p>
            
            <table width="100%" border="0" cellspacing="0" cellpadding="0" style="border-top: 1px solid #e4e4e7; padding-top: 30px;"><tr><td align="center">
                <p style="font-family: {font}; font-size: 14px; font-weight: 600; color: {color_black}; margin: 0 0 15px 0;">Ready to bypass the demo and deploy instantly?</p>
                <a href="https://kiranmondal.gumroad.com/l/titanv50" style="display: inline-block; background-color: #ffffff; border: 1px solid #e4e4e7; color: {color_black}; font-family: {font}; font-size: 14px; font-weight: 600; text-decoration: none; padding: 12px 24px; border-radius: 8px; box-shadow: 0 1px 2px rgba(0,0,0,0.05);">Purchase Direct via Gumroad</a>
            </td></tr></table>
        </td></tr>
        """ + html_bottom
        
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
