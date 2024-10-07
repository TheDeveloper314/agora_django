from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings

def send_email(request, email_type, user):
	from_email = settings.DEFAULT_FROM_EMAIL
	current_site = get_current_site(request)
	if email_type == "verification_email":
		subject = "FoodOnline Account Verification"
		template = "accounts/emails/verification_email.html"
	elif email_type == "password_reset_email":
		subject = "FoodOnline Account Password Reset"
		template = "accounts/emails/password_reset_email.html"

	context = {"user": user, "domain": current_site,
				"uid": urlsafe_base64_encode(force_bytes(user.pk)),
				"token": default_token_generator.make_token(user),
				}

	message = render_to_string(template, context)
	to_email = user.email

	mail = EmailMessage(subject, message, from_email, to=[to_email])
	mail.send()