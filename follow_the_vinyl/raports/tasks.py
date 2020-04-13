from celery import Celery
from django_celery_beat.models import CrontabSchedule, PeriodicTask

from .models import Raport

app = Celery()


@app.task
def send_raport(raport_pk: int) -> None:
    raport = Raport.objects.get(pk=raport_pk)
    raport.send_raport()


@app.task
def clean_orphan_raport_tasks() -> None:
    print("clean_orphan_raport_tasks()")
    session = app.backend.ResultSession()
    with app.backend.session_cleanup(session):
        # session.query(PeriodicTask).filter(raport=None).delete()
        # session.commit()
        print(session.query(PeriodicTask).filter(raport=None).all())



@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    schedule, _ = CrontabSchedule.objects.get_or_create(
        minute="*/3", hour="*", day_of_week="*", day_of_month="*", month_of_year="*",
    )
    kwargs = dict(
        crontab=schedule,
        name=clean_orphan_raport_tasks.name,
        task=clean_orphan_raport_tasks.name,
    )
    periodic_task = PeriodicTask.objects.filter(
        name=clean_orphan_raport_tasks.name
    ).first()
    if periodic_task and periodic_task.crontab != schedule:
        periodic_task.crontab = schedule
        periodic_task.save()
    else:
        PeriodicTask.objects.create(**kwargs)
