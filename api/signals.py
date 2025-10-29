import threading
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from api.models import Advisor, Delegate, Executive, Staff, StudentOfficer, MUNDirector, School
import logging

registration_logger = logging.getLogger("registration_log")

_user = threading.local()

# Middleware to store the current user
class CurrentUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _user.value = getattr(request, "user", None)
        response = self.get_response(request)
        _user.value = None
        return response

def get_current_user():
    return getattr(_user, "value", None)

# Signal handlers
@receiver(post_save, sender=Advisor)
@receiver(post_save, sender=Delegate)
@receiver(post_save, sender=Executive)
@receiver(post_save, sender=Staff)
@receiver(post_save, sender=StudentOfficer)
@receiver(post_save, sender=MUNDirector)
def log_participant_save(sender, instance, created, **kwargs):
    user = get_current_user()
    action = "CREATED" if created else "UPDATED"
    registration_logger.info(f"User {user} {action} {instance.__class__.__name__} {instance.id}")

@receiver(post_delete, sender=Advisor)
@receiver(post_delete, sender=Delegate)
@receiver(post_delete, sender=Executive)
@receiver(post_delete, sender=Staff)
@receiver(post_delete, sender=StudentOfficer)
@receiver(post_delete, sender=MUNDirector)
def log_participant_delete(sender, instance, **kwargs):
    user = get_current_user()
    registration_logger.warning(f"User {user} DELETED {instance.__class__.__name__} {instance.id}")

@receiver(post_save, sender=School)
def log_school_save(sender, instance, created, **kwargs):
    user = get_current_user()
    action = "CREATED" if created else "UPDATED"
    if created:
        registration_logger.debug(f"User {user} CREATED School {instance.id} ({instance.name})")
    else:
        registration_logger.info(f"User {user} UPDATED School {instance.id} ({instance.name})")

@receiver(post_delete, sender=School)
def log_school_delete(sender, instance, **kwargs):
    user = get_current_user()
    registration_logger.warning(f"User {user} DELETED School {instance.id} ({instance.name})")