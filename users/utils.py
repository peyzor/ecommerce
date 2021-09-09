from django.core.mail import EmailMessage


class Util:
    @staticmethod
    def send_email(data):
        subject = data['subject']
        body = data['body']
        to = data['to']
        email = EmailMessage(subject=subject, body=body, to=[to])
        email.send()
