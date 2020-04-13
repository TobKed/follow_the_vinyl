from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RaportsConfig(AppConfig):
    name = "follow_the_vinyl.raports"
    verbose_name = _("Raports")

    def ready(self):
        import follow_the_vinyl.raports.signals  # noqa
