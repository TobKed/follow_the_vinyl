from django.contrib import admin

from follow_the_vinyl.raports.models import (
    DiscogsUser,
    OnlyDayAndHourSchedule,
    Raport,
    SnapShot,
)


@admin.register(DiscogsUser)
class DiscogsUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Raport)
class RaportAdmin(admin.ModelAdmin):
    pass


@admin.register(SnapShot)
class SnapShotAdmin(admin.ModelAdmin):
    pass


@admin.register(OnlyDayAndHourSchedule)
class OnlyDayAndHourScheduleAdmin(admin.ModelAdmin):
    pass
