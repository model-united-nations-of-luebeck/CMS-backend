import logging
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template import loader
from drfpasswordless.settings import api_settings
from email.utils import formataddr
import os


logger = logging.getLogger(__name__)
User = get_user_model()

def inject_template_context(context):
    """
    Injects additional context into email template.
    """
    for processor in api_settings.PASSWORDLESS_CONTEXT_PROCESSORS:
        context.update(processor())
    return context

def send_passwordless_email(user, email_token, **kwargs):
    """
    Sends a Email to user.email.

    Passes silently without sending in test environment
    """

    try:
        if api_settings.PASSWORDLESS_EMAIL_NOREPLY_ADDRESS:
            # Make sure we have a sending address before sending.

            # Get email subject and message
            email_subject = kwargs.get('email_subject',
                                       api_settings.PASSWORDLESS_EMAIL_SUBJECT)
            email_plaintext = kwargs.get('email_plaintext',
                                         api_settings.PASSWORDLESS_EMAIL_PLAINTEXT_MESSAGE)
            email_html = kwargs.get('email_html',
                                    api_settings.PASSWORDLESS_EMAIL_TOKEN_HTML_TEMPLATE_NAME)

            # Inject context if user specifies.
            context = inject_template_context({'callback_token': email_token.key, })
            html_message = loader.render_to_string(email_html, context,)
            send_mail(
                email_subject,
                email_plaintext % email_token.key,
                formataddr((os.getenv('EMAIL_FROM_NAME', 'CMS Registration'), api_settings.PASSWORDLESS_EMAIL_NOREPLY_ADDRESS)),
                [getattr(user, api_settings.PASSWORDLESS_USER_EMAIL_FIELD_NAME)],
                fail_silently=False,
                html_message=html_message,)

        else:
            logger.debug("Failed to send token email. Missing PASSWORDLESS_EMAIL_NOREPLY_ADDRESS.")
            return False
        return True

    except Exception as e:
        logger.debug("Failed to send token email to user: %d."
                  "Possibly no email on user object. Email entered was %s" %
                  (user.id, getattr(user, api_settings.PASSWORDLESS_USER_EMAIL_FIELD_NAME)))
        logger.debug(e)
        return False
