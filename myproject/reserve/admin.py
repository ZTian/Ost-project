from .models import Resource, Reservation, Tag
from django.contrib import admin

admin.site.register(Resource)
admin.site.register(Reservation)
admin.site.register(Tag)