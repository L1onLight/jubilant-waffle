import os

from dotenv import load_dotenv

from todo import settings

load_dotenv()


class EmailNotificationHandler:
    pass


# Default values for email and password
EMAIL_SYSTEM_DEFAULTS = {
    'EMAIL': 'example@example.com',
    'PASSWORD': 'password123',
}

# Custom setting for email and app password from google
EMAIL_SYSTEM = getattr(settings, 'EMAIL_SYSTEM', EMAIL_SYSTEM_DEFAULTS)

# Retrieve email and password from environment variables if set
EMAIL_SYSTEM['EMAIL'] = os.getenv('EMAIL_SYSTEM_EMAIL', EMAIL_SYSTEM['EMAIL'])
EMAIL_SYSTEM['PASSWORD'] = os.getenv(
    'EMAIL_SYSTEM_PASSWORD', EMAIL_SYSTEM['PASSWORD'])

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587

EMAIL_HOST_USER = EMAIL_SYSTEM['EMAIL']
EMAIL_HOST_PASSWORD = EMAIL_SYSTEM['PASSWORD']

EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
email_system_password = os.environ.get('EMAIL_SYSTEM_PASSWORD')
