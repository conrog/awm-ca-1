from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from world.models import Pub

@admin.register(Pub)
class PubAdmin(OSMGeoAdmin):
    list_display = ('name','location')