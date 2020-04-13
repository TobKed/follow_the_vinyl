import timezone_field
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_celery_beat import validators as celery_beat_validators
from django_celery_beat.models import CrontabSchedule, PeriodicTask, cronexp

from . import validators


class OnlyDayAndHourSchedule(models.Model):
    DAY_OF_THE_WEEK = (
        ("0", _("Monday")),
        ("1", _("Tuesday")),
        ("2", _("Wednesday")),
        ("3", _("Thursday")),
        ("4", _("Friday")),
        ("5", _("Saturday")),
        ("6", _("Sunday")),
    )
    HOUR_OF_THE_DAY = [(f"{i}", f"{i}:00") for i in range(0, 24)]

    minute = models.CharField(
        max_length=1,
        default="0",
        editable=False,
        verbose_name=_("Minute(s)"),
        help_text=_('Cron Minutes to Run. Use "*" for "all". (Example: "0,30")'),
        validators=[validators.always_zero],
    )
    hour = models.CharField(
        max_length=24 * 4,
        default="12",
        choices=HOUR_OF_THE_DAY,
        verbose_name=_("Hour(s)"),
        help_text=_('Cron Hours to Run. Use "*" for "all". (Example: "8,20")'),
        validators=[celery_beat_validators.hour_validator],
    )
    day_of_week = models.CharField(
        max_length=64,
        default="0",
        choices=DAY_OF_THE_WEEK,
        verbose_name=_("Day(s) Of The Week"),
        help_text=_(
            'Cron Days Of The Week to Run. Use "*" for "all". ' '(Example: "0,5")'
        ),
        validators=[celery_beat_validators.day_of_week_validator],
    )
    day_of_month = models.CharField(
        max_length=1,
        default="*",
        editable=False,
        verbose_name=_("Day(s) Of The Month"),
        help_text=_('Warning: Here should be always a "*"'),
        validators=[validators.always_star],
    )
    month_of_year = models.CharField(
        max_length=1,
        default="*",
        editable=False,
        verbose_name=_("Month(s) Of The Year"),
        help_text=_('Warning: Here should be always a "*"'),
        validators=[validators.always_star],
    )

    timezone = timezone_field.TimeZoneField(
        default="UTC",
        verbose_name=_("Cron Timezone"),
        help_text=_("Timezone to Run the Cron Schedule on.  Default is UTC."),
    )

    class Meta:
        """Table information."""

        verbose_name = _("limited crontab")
        verbose_name_plural = _("limited crontabs")
        ordering = [
            "month_of_year",
            "day_of_month",
            "day_of_week",
            "hour",
            "minute",
            "timezone",
        ]

    def __str__(self):
        return "{0} {1} {2} {3} {4} (m/h/d/dM/MY) {5}".format(
            cronexp(self.minute),
            cronexp(self.hour),
            cronexp(self.day_of_week),
            cronexp(self.day_of_month),
            cronexp(self.month_of_year),
            str(self.timezone),
        )


class DiscogsUser(models.Model):
    name = models.CharField(_("Name of Discogs User"), blank=True, max_length=255)
    exists = models.BooleanField(_("is Discogs User exists"), default=False)

    def __str__(self):
        return f"DiscogsUser(name={self.name}, exists={self.exists})"


class SnapShot(models.Model):
    user = models.ForeignKey(DiscogsUser, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    collection = JSONField()

    def __str__(self):
        return f"SnapShot(user={self.user}, created={self.created}, ...)"


class Raport(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    users = models.ManyToManyField(DiscogsUser)
    schedule = models.OneToOneField(OnlyDayAndHourSchedule, on_delete=models.CASCADE)
    crontab_schedule = models.ForeignKey(
        CrontabSchedule, blank=True, null=True, on_delete=models.SET_NULL
    )
    periodic_task = models.OneToOneField(
        PeriodicTask, blank=True, null=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"Raport(owner={self.owner}, users={[u for u in self.users.all()]}, schedule={self.schedule})"

    def send_raport(self):
        return send_mail(
            subject="subject",
            message=f"{self.owner}\n{self.users}\n{self.schedule}",
            from_email="no-reply@ftw.co",
            recipient_list=[self.owner.email],
        )

    def save(self, *args, **kwargs):
        self.crontab_schedule, _ = CrontabSchedule.objects.get_or_create(
            minute=self.schedule.minute,
            hour=self.schedule.hour,
            day_of_week=self.schedule.day_of_week,
            day_of_month=self.schedule.day_of_month,
            month_of_year=self.schedule.month_of_year,
            timezone=self.schedule.timezone,
        )
        super().save(*args, **kwargs)
