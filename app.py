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
# --- 3. THE "FOUNDER AESTHETIC" 7-PHASE ENGINE ---
def get_campaign_content(phase, name, category, address):
    greeting = random.choice(["Hi", "Hello", "Greetings", "Dear"])
    
    display_address = "your city" if ("(" in str(address) or str(address).lower() == "n/a" or not address) else address
    display_cat = "Dental" if (str(category).lower() == "n/a" or not category) else category

    # Ultra-clean email typography (Google/Apple standard)
    font = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
    text_color = "#202124" # Google's specific dark gray (easier on eyes than pure black)
    brand_color = "#000000" # Pitch black for high-end contrast
    accent_color = "#0d9488" # Teal for links/highlights

    # Executive Signature
    footer = f"""
    <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #e5e7eb;">
        <p style="margin: 0; font-family: {font}; font-size: 15px; font-weight: 600; color: #111827;">Kiran Deb Mondal</p>
        <p style="margin: 2px 0 10px 0; font-family: {font}; font-size: 13px; color: #6b7280;">Principal Technologist | Stop Web Rent</p>
        <p style="margin: 0; font-family: {font}; font-size: 13px;">
            <a href="https://wa.me/966572562151" style="color: {accent_color}; text-decoration: none; font-weight: 500;">WhatsApp Support</a> &nbsp;|&nbsp; 
            <a href="https://www.stopwebrent.com" style="color: {accent_color}; text-decoration: none; font-weight: 500;">www.StopWebRent.com</a>
        </p>
    </div>
    """

    # Global Wrapper
    html_top = f"""
    <html><body style="margin: 0; padding: 0; background-color: #ffffff;">
    <div style="max-width: 600px; margin: 0 auto; padding: 30px 20px;">
    """
    html_bottom = f"{footer}</div></body></html>"

    # Bulletproof Button Generator (Renders perfectly in Gmail/Outlook)
    def make_button(text, url, bg_color="#000000", text_color="#ffffff"):
        return f"""
        <table width="100%" border="0" cellspacing="0" cellpadding="0" style="margin: 25px 0;">
          <tr>
            <td>
              <table border="0" cellspacing="0" cellpadding="0">
                <tr>
                  <td align="center" style="border-radius: 6px;" bgcolor="{bg_color}">
                    <a href="{url}" target="_blank" style="font-size: 15px; font-family: {font}; color: {text_color}; text-decoration: none; border-radius: 6px; padding: 14px 28px; border: 1px solid {bg_color}; display: inline-block; font-weight: bold;">{text}</a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
        </table>
        """

    if phase == 1:
        subject = parse_spintax("{Action Required|Google Maps alert|Missing link} for [Name]").replace("[Name]", name)
        html = html_top + f"""
        <p style="font-family: {font}; font-size: 16px; color: {text_color}; margin: 0 0 20px 0; line-height: 1.6;">{greeting} {name} team,</p>
        <p style="font-family: {font}; font-size: 16px; color: {text_color}; margin: 0 0 20px 0; line-height: 1.6;">I was researching <strong>{display_cat}</strong> clinics in <strong>{display_address}</strong>. Your practice has a phenomenal reputation, but you are currently missing a critical digital asset:</p>
        
        <p style="font-family: {font}; font-size: 16px; color: {text_color}; margin: 0 0 20px 0; line-height: 1.6;">
            <strong style="color: #dc2626;">⚠️ You do not have a "Website" link on your Google Maps profile.</strong><br>
            Google's current algorithm actively pushes profiles without websites down the rankings, handing your high-value patients to competitors.
        </p>

        <p style="font-family: {font}; font-size: 16px; color: {text_color}; margin: 0 0 20px 0; line-height: 1.6;">I engineer <strong>0.1s High-Velocity</strong> websites specifically for healthcare clinics. Unlike Wix or Shopify, my Titan Architecture requires <strong>$0 in monthly hosting fees.</strong></p>
        
        <p style="font-family: {font}; font-size: 16px; color: {text_color}; margin: 0 0 10px 0; line-height: 1.6;"><strong>My Offer: A Free 24-Hour Preview</strong><br>I will use your current logo and photos to build a live demo. If you don't love the performance, you pay nothing.</p>

        {make_button("Reply 'YES' via WhatsApp for Free Demo \u2192", "https://wa.me/966572562151?text=YES", accent_color)}
        """ + html_bottom

    elif phase == 2:
        subject = f"Re: {name} digital preview"
        html = html_top + f"""
        <p style="font-family: {font}; font-size: 16px; color: {text_color}; margin: 0 0 20px 0; line-height: 1.6;">{greeting} again,</p>
        <p style="font-family: {font}; font-size: 16px; color: {text_color}; margin: 0 0 25px 0; line-height: 1.6;">I wanted to follow up on my last email. When I build a Titan Engine site for a clinic like <strong>{name}</strong>, it's not a brochure—it's a lead generation machine.</p>
        
        <div style="border-left: 3px solid #e5e7eb; padding-left: 15px; margin: 25px 0;">
            <p style="font-family: {font}; font-size: 15px; color: #111827; margin: 0 0 10px 0; font-weight: 600;">Technical Specifications:</p>
            <ul style="font-family: {font}; font-size: 15px; color: {text_color}; line-height: 1.8; margin: 0; padding-left: 20px;">
                <li><strong>WhatsApp Routing:</strong> Patients book in one tap.</li>
                <li><strong>Zero-DB Architecture:</strong> 100% unhackable infrastructure.</li>
                <li><strong>Mobile-Native:</strong> Installs directly to patient's phones.</li>
            </ul>
        </div>

        {make_button("View Live Demo Environment", "https://hv-furniture-bit.github.io/dental-junction-behala/index.html", brand_color)}

        <p style="font-family: {font}; font-size: 16px; color: {text_color}; margin: 25px 0 0 0; line-height: 1.6;">Reply <strong>"YES"</strong> to this email and I will build a prototype for {name} today.</p>
        """ + html_bottom

    elif phase == 3:
        subject = parse_spintax("{Stop paying|How to save $1,800 on} website rent")
        html = html_top + f"""
        <p style="font-family: {font}; font-size: 16px; color: {text_color}; margin: 0 0 20px 0; line-height: 1.6;">{greeting},</p>
        <p style="font-family: {font}; font-size: 16px; color: {text_color}; margin: 0 0 25px 0; line-height: 1.6;">Most clinics are trapped paying $30-$50 every month to Wix or Shopify. The Titan Engine changes that. <strong>Pay a one-time setup fee, and own it forever.</strong></p>
        
        <table width="100%" border="0" cellspacing="0" cellpadding="0" style="border: 1px solid #e5e7eb; border-radius: 8px; margin-bottom: 25px; max-width: 500px;">
            <tr>
                <td style="padding: 12px 15px; border-bottom: 1px solid #e5e7eb; font-family: {font}; font-size: 14px; color: #6b7280;">5-Year Projection</td>
                <td align="right" style="padding: 12px 15px; border-bottom: 1px solid #e5e7eb; font-family: {font}; font-size: 14px; font-weight: bold; color: #111827;">Titan Engine</td>
                <td align="right" style="padding: 12px 15px; border-bottom: 1px solid #e5e7eb; font-family: {font}; font-size: 14px; color: #6b7280;">Wix / Shopify</td>
            </tr>
            <tr>
                <td style="padding: 12px 15px; border-bottom: 1px solid #e5e7eb; font-family: {font}; font-size: 15px; color: {text_color};">Setup Fee</td>
                <td align="right" style="padding: 12px 15px; border-bottom: 1px solid #e5e7eb; font-family: {font}; font-size: 15px; font-weight: bold; color: #111827;">$199</td>
                <td align="right" style="padding: 12px 15px; border-bottom: 1px solid #e5e7eb; font-family: {font}; font-size: 15px; color: #6b7280;">$0</td>
            </tr>
            <tr>
                <td style="padding: 12px 15px; border-bottom: 1px solid #e5e7eb; font-family: {font}; font-size: 15px; color: {text_color};">Monthly Rent</td>
                <td align="right" style="padding: 12px 15px; border-bottom: 1px solid #e5e7eb; font-family: {font}; font-size: 15px; font-weight: bold; color: {accent_color};">$0</td>
                <td align="right" style="padding: 12px 15px; border-bottom: 1px solid #e5e7eb; font-family: {font}; font-size: 15px; color: #6b7280;">$1,740</td>
            </tr>
            <tr style="background-color: #f9fafb;">
                <td style="padding: 15px; font-family: {font}; font-size: 15px; font-weight: bold; color: #111827; border-radius: 0 0 0 8px;">Total Cost</td>
                <td align="right" style="padding: 15px; font-family: {font}; font-size: 15px; font-weight: bold; color: {accent_color};">$274</td>
                <td align="right" style="padding: 15px; font-family: {font}; font-size: 15px; font-weight: bold; color: #dc2626; border-radius: 0 0 8px 0;">$2,115</td>
            </tr>
        </table>

        <p style="font-family: {font}; font-size: 16px; color: {text_color}; margin: 0 0 10px 0; line-height: 1.6;"><strong>That is $1,841 in direct savings.</strong></p>

        {make_button("Claim Your $1,841 Savings", "https://wa.me/966572562151", brand_color)}
        """ + html_bottom

    elif phase == 4:
        subject = parse_spintax("Update {name} website using Excel?")
        html = html_top + f"""
        <p style="font-family: {font}; font-size: 16px; color: {text_color}; margin: 0 0 20px 0; line-height: 1.6;">{greeting},</p>
        <p style="font-family: {font}; font-size: 16px; color: {text_color}; margin: 0 0 20px 0; line-height: 1.6;">Clinics avoid building websites because they hate complex dashboards and paying web developers.</p>
        
        <p style="font-family: {font}; font-size: 16px; color: {text_color}; margin: 0 0 20px 0; line-height: 1.6;"><strong>📊 The Spreadsheet CMS</strong><br>
        Your website is hard-wired directly to a private Google Sheet. If your receptionist can type into Excel, they can manage your entire website. Change a price, and it updates globally in 1 second.</p>

        <p style="font-family: {font}; font-size: 16px; color: {text_color}; margin: 0; line-height: 1.6;">Should I build a quick prototype so you can see how easy this is?</p>
        """ + html_bottom

    elif phase == 5:
        subject = parse_spintax("The 2026 Google algorithm & [Name]").replace("[Name]", name)
        html = html_top + f"""
        <p style="font-family: {font}; font-size: 16px; color: {text_color}; margin: 0 0 20px 0; line-height: 1.6;">{greeting},</p>
        <p style="font-family: {font}; font-size: 16px; color: {text_color}; margin: 0 0 25px 0; line-height: 1.6;">I am reaching out regarding the missing website link on your Google Maps profile because the rules of local SEO are officially changing.</p>
        
        <div style="background-color: #fef2f2; border: 1px solid #fecaca; padding: 20px; border-radius: 8px; margin: 25px 0;">
            <strong style="color: #991b1b; font-family: {font}; font-size: 16px;">The 2026 AI Algorithm Shift:</strong>
            <p style="color: #b91c1c; font-family: {font}; font-size: 15px; line-height: 1.6; margin: 8px 0 0 0;">Google’s AI search now significantly increases the weight of <i>linked, fast-loading</i> websites. Profiles without them are actively being suppressed and hidden from patients in the Map Pack.</p>
        </div>

        <p style="font-family: {font}; font-size: 16px; color: {text_color}; margin: 0 0 25px 0; line-height: 1.6;">Our architecture achieves a <strong>100/100 Google PageSpeed score</strong>, ensuring you stay at the top.</p>
        
        {make_button("Secure Your Ranking Today", "https://wa.me/966572562151?text=YES", "#dc2626")}
        """ + html_bottom

    elif phase == 6:
        subject = "am I off base here?"
        html = html_top + f"""
        <p style="font-family: {font}; font-size: 16px; color: {text_color}; margin: 0 0 20px 0; line-height: 1.6;">{greeting},</p>
        <p style="font-family: {font}; font-size: 16px; color: {text_color}; margin: 0 0 20px 0; line-height: 1.6;">I've reached out a few times about getting a high-speed, $0 monthly fee website set up for {name}.</p>
        <p style="font-family: {font}; font-size: 16px; color: {text_color}; margin: 0; line-height: 1.6;">Am I totally off base here, or is this just a really busy month for the clinic? Just let me know so I can update my notes.</p>
        """ + html_bottom

    elif phase == 7:
        subject = parse_spintax("{Closing my file|Last email} regarding [Name]").replace("[Name]", name)
        html = html_top + f"""
        <p style="font-family: {font}; font-size: 16px; color: {text_color}; margin: 0 0 20px 0; line-height: 1.6;">{greeting},</p>
        <p style="font-family: {font}; font-size: 16px; color: {text_color}; margin: 0 0 20px 0; line-height: 1.6;">Since I haven't heard back, I'll assume that fixing the missing website on your Google profile isn't a priority right now. This will be my last email.</p>
        <p style="font-family: {font}; font-size: 16px; color: {text_color}; margin: 0 0 30px 0; line-height: 1.6;">If you ever get tired of losing map traffic to competitors, or if you just want to stop paying "Web Rent" to Wix or Shopify, you know where to find me. Wishing {name} a highly successful year.</p>
        
        <div style="margin-top: 35px; padding-top: 25px; border-top: 1px solid #e5e7eb;">
            <p style="font-family: {font}; font-size: 15px; color: #111827; font-weight: 600; margin: 0 0 15px 0;">Ready to bypass the demo and deploy instantly?</p>
            {make_button("Purchase Direct via Gumroad", "https://kiranmondal.gumroad.com/l/titanv50", brand_color)}
        </div>
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
