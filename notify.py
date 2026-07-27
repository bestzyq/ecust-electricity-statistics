from contextlib import suppress
import json
import os
import smtplib
from email.mime.text import MIMEText

# Read latest kWh from data.js
originstring = "[]"
with suppress(FileNotFoundError):
    with open("data.js", "r", encoding="utf-8") as f:
        originstring = f.read().lstrip("data=")

data = json.loads(originstring)
if not data:
    print("No data found, skipping notification.")
    exit(0)

remain = data[-1]["kWh"]
print(f"Current remaining: {remain} kWh")

# Only send email if remaining is below 20 kWh
if remain >= 20:
    print(f"Remaining >= 20 kWh, no need to notify.")
    exit(0)

sender_email = os.environ.get("SENDER_EMAIL")
receiver_emails = os.environ.get("RECEIVER_EMAILS", "").split(",")
smtp_username = os.environ.get("SMTP_USERNAME")
smtp_password = os.environ.get("SMTP_PASSWORD")

if not all([smtp_username, smtp_password, sender_email, receiver_emails]):
    print("Missing email configuration, skipping notification.")
    exit(0)

subject = "低电量提醒"
message = f"剩余电量不足20度，请及时充电。剩余电量：{remain} kWh."

email = MIMEText(message)
email["Subject"] = subject
email["From"] = sender_email
email["To"] = ", ".join(receiver_emails)

smtp_server = "smtphz.qiye.163.com"
smtp_port = 25

with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls()
    server.login(smtp_username, smtp_password)
    server.send_message(email)

print(f"Low battery notification sent. Remaining: {remain} kWh")
