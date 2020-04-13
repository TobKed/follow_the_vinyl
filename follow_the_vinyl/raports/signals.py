from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from raports.models import Raport




@receiver(post_save, sender=User)
def create_raport_periodic_task(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=Raport)
def save_raport_periodic_task(sender, instance, **kwargs):
    instance.profile.save()
