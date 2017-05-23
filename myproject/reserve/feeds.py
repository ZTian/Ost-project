from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.utils.feedgenerator import Rss201rev2Feed

from .models import Reservation, Resource

class ExtenedRssFeed(Rss201rev2Feed):
    mime_type = ''

class ResourcesFeed(Feed):
    title = "Resources Information"
    link = "/rss/"
    description = "Updates on new resources"

    def get_object(self, request, resource_id):
        return Resource.objects.get(pk=resource_id)

    def title(self, obj):
        return obj.title

    def description(self, obj):
        return str(obj.start_time) + str(obj.end_time)

    def items(self, obj):
        return Reservation.objects.filter(resource=obj)

    def item_title(self, item):
        return item.resource


    def item_link(self, item):
        return reverse('reserve:rss', kwargs={'resource_id': item.id})




