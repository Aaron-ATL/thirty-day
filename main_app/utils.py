import hashlib
import base64
import hmac
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.http import HttpRequest

def send_activation_email(user):
    form = PasswordResetForm({'email': user.username})
    if form.is_valid():
        request = HttpRequest()
        request.META['SERVER_NAME'] = settings.DOMAIN
        request.META['SERVER_PORT'] = '443'
        form.save(
            request=request,
            use_https=True,
            subject_template_name='registration/activation_subject.txt',
            email_template_name='registration/account_activation_email.html',
            from_email="support@30daybassist.com",
            html_email_template_name='registration/account_activation_email.html'
        )

def webhook_is_verified(data, request_hmac):
    digest = hmac.new(settings.SHOPIFY_WEBHOOK_SECRET.encode('utf-8'), data, hashlib.sha256).digest()
    computed_hmac = base64.b64encode(digest)
    return hmac.compare_digest(computed_hmac, request_hmac.encode('utf-8'))

def has_purchased_course(request_body):
    return settings.SHOPIFY_PRODUCT_ID in request_body

def create_user(email):
    new_user = User(
        username=email,
        email=email,
        password=settings.DEFAULT_PW
    )
    new_user.save()