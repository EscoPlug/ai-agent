import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from colorama import Fore

def send_email(to_email: str, subject: str, html_content: str):
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port_env = os.getenv("SMTP_PORT", "587")
    try:
        smtp_port = int(smtp_port_env)
    except ValueError:
        smtp_port = 587
        
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")

    if not sender_email or not sender_password:
        print(Fore.RED + "Error: Sender email or password not configured in environment variables.")
        return False

    msg = MIMEMultipart()
    # High-end touch: allow setting a custom display name
    display_name = os.getenv("SENDER_DISPLAY_NAME", "AI Outreach Agent")
    msg['From'] = f"{display_name} <{sender_email}>"
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(html_content, 'html'))

    try:
        # Determine whether to use SSL or STARTTLS based on port
        if smtp_port == 465:
            server = smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=15)
        else:
            server = smtplib.SMTP(smtp_server, smtp_port, timeout=15)
            server.starttls()
        
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print(Fore.GREEN + f"Successfully sent email to {to_email}")
        return True
    except smtplib.SMTPAuthenticationError:
        print(Fore.RED + f"Authentication failed for {sender_email}. Check App Password.")
        return False
    except smtplib.SMTPConnectError:
        print(Fore.RED + f"Connection failed to {smtp_server}:{smtp_port}. Check network/firewall.")
        return False
    except Exception as e:
        print(Fore.RED + f"Unexpected error sending to {to_email}: {type(e).__name__}: {e}")
        return False
