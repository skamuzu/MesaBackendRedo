from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import User
from actstream import action
from django.contrib.auth.models import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def log_user_creation(sender, instance, created, **kwargs):
    if created:
        action.send(instance, verb='created an account')
        
@receiver(post_save, sender=User)
def log_user_update(sender, instance, created, **kwargs):
    if not created:
        action.send(instance, verb='updated their account')     
    
@receiver(post_delete, sender=User)
def log_user_deletion(sender, instance, **kwargs):
    action.send(instance, verb='deleted their account')