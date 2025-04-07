import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Mailtrap SMTP credentials (from your screenshot)
SMTP_SERVER = "sandbox.smtp.mailtrap.io"
SMTP_PORT = 2525
USERNAME = "28606c657e7c5a"
PASSWORD = "e188fd757ecf11"  # replace with full password

# Sample candidate list
candidates = [
    {
        "name": "Candidate One",
        "email": "candidate1@example.com",
        "job_title": "Backend Developer",
        "interview_time": "2025-04-10 10:00 AM"
    },
    {
        "name": "Candidate Two",
        "email": "candidate2@example.com",
        "job_title": "Backend Developer",
        "interview_time": "2025-04-10 11:00 AM"
    }
]

# Send emails
for candidate in candidates:
    try:
        msg = MIMEMultipart()
        msg["From"] = "noreply@example.com"
        msg["To"] = candidate["email"]
        msg["Subject"] = f"Interview Scheduled for {candidate['job_title']}"

        body = f"""
        Hi {candidate['name']},

        You have been shortlisted for the position of {candidate['job_title']}.
        Your interview is scheduled on {candidate['interview_time']}.

        Please be available 5 minutes before your slot.

        Best regards,
        HR Team
        """

        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(USERNAME, PASSWORD)
            server.sendmail(msg["From"], msg["To"], msg.as_string())

        print(f"✅ Email sent to {candidate['email']}")
    
    except Exception as e:
        print(f"❌ Failed to send email to {candidate['email']}: {e}")
