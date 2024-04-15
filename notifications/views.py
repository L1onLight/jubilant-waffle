import datetime
import smtplib
import threading
import time

import jwt
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags
from drf_spectacular.utils import extend_schema
from jwt import ExpiredSignatureError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from notifications.models import PasswordRestore
from notifications.serializers import RestoreEmailSerializer, TokenSerializer


class PasswordRestoreHandler(threading.Thread):
    def __init__(self, receiver_email, code, url):
        payload = {"email": receiver_email, "code": code,
                   "exp": (timezone.now() + datetime.timedelta(minutes=10)).timestamp()}
        jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.TOKEN_ALGORITHM)
        url = url + f"?token={jwt_token}"
        self.context = {"url": url, "code": code}
        self.html_message = render_to_string(
            'notifications/password_restore_HTML.html', self.context)
        self.subject = 'Password Restore'
        self.message = strip_tags(self.html_message)
        self.recipient_list = [receiver_email]
        threading.Thread.__init__(self)

    def run(self):
        try:
            send_mail(
                subject=self.subject,
                message=self.message,
                html_message=self.html_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=self.recipient_list
            )
        except smtplib.SMTPDataError:
            time.sleep(1)
            send_mail(
                subject=self.subject,
                message=self.message,
                html_message=self.html_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=self.recipient_list
            )


def send_password_restore_mail(receiver_email, code, url):
    PasswordRestoreHandler(receiver_email, code, url).start()


@extend_schema(
    tags=["Notifications"],
    request=RestoreEmailSerializer,
    responses={200: {}},
    methods=["POST"]
)
@api_view(['POST'])
def restore_mail(request: Request):
    """Requires email. Generates code and sends restore mail to user with JWT token in link query.
    Token expire time set to 10 minutes."""
    # Todo change url to frontend url
    serializer = RestoreEmailSerializer(data=request.data)
    if serializer.is_valid():
        user, code = serializer.generate_code()
        if user and code:
            send_password_restore_mail(user.email, code=code, url=request.build_absolute_uri())
        return Response({"message": "Check your email"})
    return Response({"detail": "Email should be provided"}, status=400)


@extend_schema(
    tags=["Notifications"],
    request=TokenSerializer,
    responses={200: {}},
    methods=["POST"]
)
@api_view(['POST'])
def check_code(request: Request):
    """Requires JWT token from /restore/ endpoint and new password to set"""
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        try:
            payload = serializer.get_payload()
            pr_instance = PasswordRestore.objects.filter(user__email=payload.get("email")).first()
            if pr_instance and pr_instance.is_valid(payload.get("code")):
                pr_instance.user.set_password(serializer.validated_data.get("password"))
                pr_instance.user.save()
                return Response({"detail": "New password set"})
        except ExpiredSignatureError:
            return Response({"detail": "Expired token"}, status.HTTP_410_GONE)
    return Response({"detail": "Bad request"}, status.HTTP_404_NOT_FOUND)
