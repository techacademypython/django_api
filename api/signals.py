from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
User = get_user_model()


@receiver(post_save, sender=User, dispatch_uid="created_token")
def created_token(sender, **kwargs):
    instance = kwargs.get('instance')
    created = kwargs.get('created')

    if created:
        Token.objects.create(
            user=instance
        )
