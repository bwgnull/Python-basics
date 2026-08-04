import smtplib

sender = "PLACEHOLDER@gmail.com"
receiver = "PLACEHOLDER@gmail.com"
app_password = "PLACEHOLDER"

subject = "Script Test Email"
body = "This is a test email sent via Python SMTP client."

message = f"""From: {sender}
To: {receiver}
Subject: {subject}

{body}
"""

with smtplib.SMTP("smtp.gmail.com", 587) as smtp:

    smtp.set_debuglevel(1)

    # Handshake
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()

    # Auth
    smtp.login(sender, app_password)

    print("\nLogin successful!")

    # Send message
    smtp.sendmail(sender, receiver, message)

    print("\nTest email sent successfully!")