from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "follow_the_vinyl.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import follow_the_vinyl.users.signals  # noqa F401
        except ImportError:
            pass
