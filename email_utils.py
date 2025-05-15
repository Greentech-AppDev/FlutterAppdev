from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

conf = ConnectionConfig(
    MAIL_USERNAME="your_email@example.com",
    MAIL_PASSWORD="your_email_password",
    MAIL_FROM="your_email@example.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.example.com",
    MAIL_TLS=True,
    MAIL_SSL=False,
)

async def send_verification_email(email_to: str, token: str):
    verification_link = f"http://your-frontend-or-backend-url/verify-email?token={token}"
    message = MessageSchema(
        subject="Verify your email",
        recipients=[email_to],
        body=f"Please verify your email by clicking on this link: {verification_link}",
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message)
