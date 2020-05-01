import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional

import emails
from betfund_solicitor import Message
from jinja2 import Template
from jose import jwt
from sendgrid import SendGridAPIClient

from app.core.config import settings


def send_email(
    reason: str,
    email_to: str,
    subject_template: str = "",
    html_template: str = "",
    environment: Dict[str, Any] = {},
) -> None:
    """Sends an email to user.

    Params
    ------
    email_to : str
        Email address of user.
    subject_template : str
        Email subject line template for Jinja population.
    html_template : str
        Email body template for Jinja population.
    environment : dict
        Handling Jinja environment.

    Returns
    -------
    None
    """
    # Ensure SendGrid API key is set and available
    assert settings.SENDGRID_API_KEY, "No SendGrid API key provided"

    # Render the body of email
    template = Template(html_template)
    body_mjml = template.render(**environment)

    # Initialize the `betfund_solicitor.Message` object
    message = Message(
        reason=reason,
        sender="admin@streetcred.com",
        to=email_to,
        subject=subject_template,
        body_html=body_mjml
    )

    # Initialize the `sendgrid.SendGridAPIClient` object and send email
    client = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
    response = client.client.mail.send.post(
        request_body=message.sendgrid_send_payload
    )

    logging.info(f"Send email status: {response.status_code}")


def send_test_email(email_to: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Test email"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "test_email.html") as f:
        template_str = f.read()
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={"project_name": settings.PROJECT_NAME, "email": email_to},
    )


def send_reset_password_email(email_to: str, email: str, token: str) -> None:
    """Sends email to reset password.

    Params
    ------
    email_to : str
        Email of user to send email to.
    email : str
        User's account email to validate existence.
    token : str
        Token generated for password reset.

    Returns
    -------
    None
    """
    subject = f"StreetCred - Password reset request for {email}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "reset_password.html") as f:
        template_str = f.read()
    server_frontend = settings.SERVER_FRONTEND
    link = f"{server_frontend}/?#/reset/{token}"
    send_email(
        reason=f"Password reset for {email}",
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": "Betfund",
            "username": email,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )


def send_new_account_email(email_to: str, username: str, password: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New account for user {username}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "new_account.html") as f:
        template_str = f.read()
    link = settings.SERVER_HOST
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": username,
            "password": password,
            "email": email_to,
            "link": link,
        },
    )


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email}, settings.SECRET_KEY, algorithm="HS256",
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    """Verifies a password reset token.

    Params
    ------
    token : str
        JWT password reset token.

    Returns
    -------
    string
        Username of the email if successful token.

    Raises
    ------
    `jwt.JWTError`
        If the token was invalid.

    """
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return decoded_token["sub"]
    except jwt.JWTError:
        return None