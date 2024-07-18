from smtplib import SMTPConnectError, SMTPServerDisconnected

from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import status


def send_email_to_attendee(subject, body,
                           from_email, recipient_list):
    
    try:
        send_mail(
            subject,
            body,
            from_email,
            recipient_list
        )
    except SMTPConnectError:
        return Response(
            {
                "error":"Server Connection Error"
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
    except SMTPServerDisconnected:
        return Response(

            {
                "error":"Server Connection Error"        
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
