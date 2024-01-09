from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Protocol


@receiver(post_save, sender=Protocol)
def set_protocol_name(sender, instance, created, **kwargs):
    if created:
        instance.name = f"protocol_{instance.id}"
        instance.save()
