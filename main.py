import streamlit as st
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd

# === CONFIGURATION ===
DB_PATH = "agents.db"
SMTP_SERVER = "sandbox.smtp.mailtrap.io"
SMTP_PORT = 2525
USERNAME = "28606c657e7c5a"
PASSWORD = "e188fd757ecf11"

# === FETCH FROM DATABASE ===
def fetch_shortlisted_candidates():
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
            SELECT c.id, c.resume_text, j.description, s.score, s.reasons
            FROM shortlisted s
            JOIN candidates c ON s.candidate_id = c.id
            JOIN jobs j ON s.job_id = j.id
        """)
        results = cur.fetchall()
        return results
    except Exception as e:
        st.error(f"Database error: {e}")
        return []
    finally:
        conn.close()

# === MOCK NAME/EMAIL FOR DISPLAY PURPOSES ===
def get_dummy_email(candidate_id):
    return f"candidate{candidate_id}@example.com"

def get_dummy_name(candidate_id):
    return f"Candidate {candidate_id}"

# === EMAIL SENDER ===
def send_email(name, email, job_title, interview_time, score, reasons):
    try:
        msg = MIMEMultipart()
        msg["From"] = "noreply@example.com"
        msg["To"] = email
        msg["Subject"] = f"Interview Scheduled for {job_title}"

        body = f"""
Hi {name},

You have been shortlisted for the position of {job_title}.
Your interview is scheduled on {interview_time}.

Score: {score}
Reasons: {reasons}

Please be available 5 minutes before your slot.

Best regards,
HR Team
"""
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(USERNAME, PASSWORD)
            server.sendmail(msg["From"], msg["To"], msg.as_string())

        return True
    except Exception as e:
        st.error(f"❌ Failed to send to {email}: {e}")
        return False

# === STREAMLIT UI ===
st.set_page_config(page_title="📋 AI Shortlisting", page_icon="📧")
st.title("📋 Shortlisted Candidates")
st.write("Candidates who matched your JD will be shown below. Click to notify them via email.")

# Notify button
if st.button("📤 Notify All Candidates via Email"):
    data = fetch_shortlisted_candidates()
    if data:
        for candidate_id, resume_text, job_desc, score, reasons in data:
            name = get_dummy_name(candidate_id)
            email = get_dummy_email(candidate_id)
            interview_time = "2025-04-10 10:00 AM"  # You can update logic here to fetch or allow input
            job_title = "Backend Developer"         # Static or derived from job description

            if send_email(name, email, job_title, interview_time, score, reasons):
                st.success(f"✅ Email sent to {name} ({email})")
    else:
        st.warning("⚠️ No shortlisted candidates found in DB.")

# Display the table
st.subheader("👥 Shortlisted Candidate Summary")
data = fetch_shortlisted_candidates()
if data:
    formatted = []
    for candidate_id, resume_text, job_desc, score, reasons in data:
        formatted.append({
            "ID": candidate_id,
            "Name": get_dummy_name(candidate_id),
            "Email": get_dummy_email(candidate_id),
            "Job Description": job_desc[:60] + "...",
            "Score": score,
            "Reasons": reasons
        })

    st.dataframe(pd.DataFrame(formatted))
else:
    st.info("ℹ️ No shortlisted candidates to display.")
