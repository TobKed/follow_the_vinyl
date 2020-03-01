from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _


class DiscogsUser(models.Model):
    name = models.CharField(_("Name of Discogs User"), blank=True, max_length=255)
    exists = models.BooleanField(_("is Discogs User exists"), default=False)


class SnapShot(models.Model):
    user = models.ForeignKey(DiscogsUser, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    collection = JSONField()


class Raport(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    users = models.ManyToManyField(DiscogsUser)
