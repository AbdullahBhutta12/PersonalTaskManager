import smtplib
from email.mime.text import MIMEText
from argon2 import PasswordHasher

ph = PasswordHasher()


def bcrypt(password: str) -> str:
    return ph.hash(password)


def verify(hashed_password, plain_password) -> bool:
    try:
        return ph.verify(hashed_password, plain_password)
    except:
        return False


def send_verification_email(to_email: str, code: str):
    sender_email = "116abdullahbhutta@gmail.com"
    sender_password = "xqvghmmgfetesmnx"
    subject = "Verify your email - Personal Task Manager"
    body = f"Your verification code is: {code}"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print(f"✅ Verification email sent to {to_email}")
    except Exception as e:
        print("❌ Email send error:", e)
