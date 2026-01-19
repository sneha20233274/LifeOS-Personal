from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

conf = ConnectionConfig(
    MAIL_USERNAME="devskillhub1410@gmail.com",
    MAIL_PASSWORD="lzvmmhzhuvcpplsa",
    MAIL_FROM="devskillhub1410@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,     
    MAIL_SSL_TLS=False,     
    USE_CREDENTIALS=True
)

fastmail = FastMail(conf)
