from django.contrib import admin

from missions.models import Target, Mission

admin.site.register(Mission)
admin.site.register(Target)
