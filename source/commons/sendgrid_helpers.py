import sendgrid
from django.conf import settings
from sendgrid.helpers.mail import Email, To, HtmlContent, Mail

from commons.exceptions import SendEmailError


def send_email(to, subject, content):
    try:
        sg = sendgrid.SendGridAPIClient(
            api_key=settings.get('SENDGRID_API_KEY'))
        from_email = Email(settings.get('DEFAULT_FROM_EMAIL'))
        to_email = To(to)
        html_content = HtmlContent(content)
        mail = Mail(from_email, to_email, subject, html_content)
        response = sg.client.mail.send.post(request_body=mail.get())

        if response.status_code == 200:
            return True

        return False
    except Exception as e:
        raise SendEmailError(e)
