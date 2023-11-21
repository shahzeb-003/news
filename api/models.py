from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib.sessions.models import Session

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

@receiver(pre_delete, sender=CustomUser)
def delete_user_sessions(sender, instance, **kwargs):
    # This function will run before a CustomUser is deleted
    # It will find and delete any sessions associated with the user
    sessions = Session.objects.filter(session_data__contains=str(instance.id))
    sessions.delete()