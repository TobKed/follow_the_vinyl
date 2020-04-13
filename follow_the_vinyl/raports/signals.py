from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask

from follow_the_vinyl.raports.models import Raport

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()


@receiver(post_save, sender=Raport)
def save_raport_periodic_task(sender, instance, **kwargs):
    if instance.periodic_task:
        instance.periodic_task.crontab = instance.crontab_schedule
        instance.periodic_task.save()
    else:
        instance.periodic_task = PeriodicTask.objects.create(
            crontab=instance.crontab_schedule,
            name=f"Raport(id={instance.id}).periodic_task",
            task="follow_the_vinyl.raports.tasks.send_raport",
            kwargs={"raport_id": instance.id},
        )
        instance.save()


@receiver(post_delete, sender=Raport)
def delete_raport_periodic_task_and_schedule(sender, instance, **kwargs):
    if instance.periodic_task:
        instance.periodic_task.delete()
    # if instance.crontab_schedule:
    #     instance.crontab_schedule.delete()
    if instance.schedule:
        instance.schedule.delete()
