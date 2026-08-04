import smtplib

with smtplib.SMTP('smtp.gmail.com', 587) as smtp:

    # Log protocol messages to the console
    smtp.set_debuglevel(1)

    def log_status(step, response):
        if response is None:
            print(f"\n[{step}] No response received")
            return

        code, message = response
        print(f"\n[{step}] Status Code: {code}")
        print(message.decode().strip())
        print("-" * 50)

    # Identify to the server
    log_status("EHLO", smtp.ehlo())

    # Start encrypted TLS session
    log_status("START TLS", smtp.starttls())

    # Identify again after TLS
    log_status("EHLO POST TLS", smtp.ehlo())

    # Login using credentials, do not use spaces in app password
    try:
        smtp.login("PLACEHOLDER@gmail.com", "PLACEHOLDER PASSWORD")
        print("\nLogin successful!")
    except smtplib.SMTPAuthenticationError as e:
        print("\nLogin failed")
        print("SMTP Code:", e.smtp_code)
        print("SMTP Error:", e.smtp_error.decode())

    smtp.quit()