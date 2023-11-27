from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib.sessions.models import Session
from django.conf import settings


class Category(models.Model):
    """
    Model to represent a news category.
    """
    CATEGORY_CHOICES = [
        ('SP', 'Sports'),
        ('WR', 'World'),
        ('FN', 'Finance'),
    ]

    code = models.CharField(max_length=2, choices=CATEGORY_CHOICES, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    favorite_categories = models.ManyToManyField(Category)  # Allows multiple categories to be chosen

class News(models.Model):
    CATEGORY_CHOICES = [
        ('SP', 'Sports'),
        ('WR', 'World'),
        ('FN', 'Finance'),
    ]

    title = models.CharField(max_length=255, default='Default Title')
    text = models.TextField()  # Long news text
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)

    # Optional: timestamp fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title  # Return the title in the admin or when the model is printed

    class Meta:
        verbose_name_plural = "news"

class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.news}"


@receiver(pre_delete, sender=CustomUser)
def delete_user_sessions(sender, instance, **kwargs):
    # This function will run before a CustomUser is deleted
    # It will find and delete any sessions associated with the user
    sessions = Session.objects.filter(session_data__contains=str(instance.id))
    sessions.delete()