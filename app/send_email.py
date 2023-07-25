from fastapi import BackgroundTasks
<<<<<<< HEAD:app/send_email.py
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
=======
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig,MessageType
>>>>>>> main:send_email.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from app.setting import Settings


class Settings(BaseSettings):
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    MAIL_FROM: str
    MAIL_FROM_NAME: str | None = None
    SQLALCHEMY_DATABASE_URL: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=587,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)
email_file = """
<html>
<body style="margin: 0; padding: 0; box-sizing: border-box; font-family: Arial, Helvetica, sans-serif;">
<div style="width: 100%; background: #efefef; border-radius: 10px; padding: 10px;">
  <div style="margin: 0 auto; width: 90%; text-align: center;">
    <h1 style="background-color: rgba(0, 53, 102, 1); padding: 5px 10px; border-radius: 5px; color: white;">Codavatar</h1>
    <div style="margin: 30px auto; background: white; width: 40%; border-radius: 10px; padding: 50px; text-align: center;">
      <h3 style="margin-bottom: 100px; font-size: 24px;">Aayush Dip Giri</h3>
      <p style="margin-bottom: 30px;">Lorem ipsum dolor sit amet consectetur adipisicing elit. Eligendi, doloremque.</p>
      <a style="display: block; margin: 0 auto; border: none; background-color: rgba(255, 214, 10, 1); color: white; width: 200px; line-height: 24px; padding: 10px; font-size: 24px; border-radius: 10px; cursor: pointer; text-decoration: none;"
        href="https://fastapi.tiangolo.com/"
        target="_blank"
      >
      </a>
    </div>
  </div>
</div>
</body>
</html>
"""


def send_email_background(
    background_tasks: BackgroundTasks, subject: str, email_to: str
) -> None:
    message = MessageSchema(
        subject=subject,
        body=email_file,
        recipients=email_to,
        subtype=MessageType.html,
    )
    f_m = FastMail(conf)
    background_tasks.add_task(f_m.send_message, message)
