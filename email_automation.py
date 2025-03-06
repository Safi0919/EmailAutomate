import imaplib
import email
import smtplib
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email credentials
EMAIL_USER = "your email address"
EMAIL_PASS = "your Google apps password"

# IMAP and SMTP settings for Gmail
IMAP_SERVER = "imap.gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def extract_details(email_body):
    """Extract appointment details from email body."""
    date_time_match = re.search(r"An appointment has been scheduled for (.+?) PT", email_body)
    modality_match = re.search(r"This is a .*? (in-person|Zoom) appointment", email_body, re.IGNORECASE)
    location_match = re.search(r"Location:\s+(.+)", email_body)
    topic_match = re.search(r"Topic\s+([\s\S]+?)\n\n", email_body)
    attendee_match = re.search(r"Attendees\s+(.+)", email_body)
    comments_match = re.search(r"Comments([\s\S]+)", email_body)

    date_time = date_time_match.group(1) if date_time_match else "N/A"
    modality = modality_match.group(1) if modality_match else "N/A"
    location = location_match.group(1) if location_match else "N/A"
    topic = topic_match.group(1).strip() if topic_match else "N/A"
    attendee = attendee_match.group(1).strip() if attendee_match else "N/A"
    comments = comments_match.group(1).strip() if comments_match else "N/A"

    return date_time, modality, location, topic, attendee, comments

def fetch_unread_emails():
    """Fetch all unread emails."""
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_USER, EMAIL_PASS)
    mail.select("inbox")

    result, data = mail.search(None, 'UNSEEN')
    email_ids = data[0].split()

    emails = []
    for email_id in email_ids:
        result, data = mail.fetch(email_id, "(RFC822)")
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)

        sender = msg["From"]
        email_body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    email_body = part.get_payload(decode=True).decode()
                    break
        else:
            email_body = msg.get_payload(decode=True).decode()

        emails.append((email_id, sender, email_body))

    mail.logout()
    return emails

def send_confirmation_email(to_email, details):
    """Send confirmation email with extracted details."""
    date_time, modality, location, topic, attendee, comments = details

    confirmation_body = f"""
    Hi {attendee},

    Your tutoring appointment is confirmed!

    📅 Date & Time: {date_time} PT
    📍 Modality: {modality}
    {'📌 Location: ' + location if modality.lower() == 'in-person' else ''}
    {'🔗 Zoom Link: ' + location if modality.lower() == 'zoom' else ''}

    📚 Topic: {topic}

    📝 Comments:
    {comments}

    Looking forward to our session!

    Best,
    Safiullah Saif
    """

    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = to_email
    msg["Cc"] = "safiullah.saif@sjsu.edu"
    msg["Subject"] = "Tutoring Appointment Confirmation"

    msg.attach(MIMEText(confirmation_body, "plain"))

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL_USER, EMAIL_PASS)
    server.sendmail(EMAIL_USER, [to_email, "safiullah.saif@sjsu.edu"], msg.as_string())
    server.quit()

    print("Confirmation email sent to:", to_email)

def main():
    emails = fetch_unread_emails()

    if not emails:
        print("No new appointment emails found.")
        return

    for email_id, sender_email, email_body in emails:
        details = extract_details(email_body)
        date_time, modality, location, topic, attendee, comments = details

        print("\n===============================")
        print(f"📩 New Tutoring Request from {attendee}")
        print(f"📅 Date & Time: {date_time} PT")
        print(f"📍 Modality: {modality}")
        if modality.lower() == "in-person":
            print(f"📌 Location: {location}")
        elif modality.lower() == "zoom":
            print(f"🔗 Zoom Link: {location}")
        print(f"📚 Topic: {topic}")
        print("📝 Comments:", comments)
        print("===============================")

        confirm = input("Do you want to send a confirmation email? (yes/no): ").strip().lower()
        if confirm == "yes":
            send_confirmation_email(sender_email, details)
        else:
            print("Skipping this email.")

if __name__ == "__main__":
    main()
