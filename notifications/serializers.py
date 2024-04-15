import random

import jwt
from django.contrib.auth import get_user_model
from rest_framework import serializers

from notifications.models import PasswordRestore
from todo import settings


class RestoreEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields = ('email',)

    def validate_email(self, value):
        normalized_email = value.lower()
        return normalized_email

    def generate_code(self):
        code = random.randrange(1000000, 10000000)
        email = self.validated_data.get("email")
        user = get_user_model().objects.filter(email=email).first()
        if user:
            pr_instance = PasswordRestore.objects.filter(user__email=email).first()
            if not pr_instance:
                pr_instance = PasswordRestore(user=user)
            pr_instance.restoreCode = code
            pr_instance.save()

            return user, code
        return None, None


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        fields = ('token', "password")

    def get_payload(self):
        if self.is_valid():
            """May throw an ExpiredSignatureError if token is expired"""
            token = self.data.get("token")
            payload = jwt.decode(token, settings.SECRET_KEY, settings.TOKEN_ALGORITHM)
            return dict(payload)
