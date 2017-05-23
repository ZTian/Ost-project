from django.db import models
from datetime import date
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class Resource(models.Model):
    title = models.CharField(max_length=50)
    tag = models.ManyToManyField('Tag', blank=True)
    start_time = models.TimeField(null=False, default=timezone.localtime(timezone.now()))
    end_time = models.TimeField(null=False, default=timezone.localtime(timezone.now()))
    resource_owner = models.ForeignKey(User, related_name='User')
    resource_logo = models.CharField(max_length=1000, blank=True)
    resource_description = models.CharField(max_length=1000, blank=True)
    def get_absolute_url(self):
        return reverse('reserve:index')

    def __str__(self):
        return self.title

class Reservation(models.Model):
    owner = models.ForeignKey(User)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    date_time = models.DateField(default=date.today)
    start_time = models.TimeField(null=False, default=timezone.localtime(timezone.now()))
    end_time = models.TimeField(null=False, default=timezone.localtime(timezone.now()))
    def get_absolute_url(self):
        return reverse('reserve:index')

    def __str__(self):
        return self.resource.title + ' reserved by ' + self.owner.username


class Tag(models.Model):
    title = models.CharField(max_length=20)
    def __str__(self):
        return self.title
