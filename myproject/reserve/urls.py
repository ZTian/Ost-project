from django.conf.urls import url
from reserve.feeds import ResourcesFeed

from . import views

app_name = 'reserve'

urlpatterns = [
    #/reserve/
    url(r'^$', views.index, name='index'),

    #/reserve/<reservation_id>
    url(r'^(?P<reservation_id>[0-9]+)/$', views.detail, name='detail'),

    url(r'^resource/(?P<resource_id>[0-9]+)/$', views.resource_detail, name='resource'),
    url(r'^resource/reserve/(?P<pk>[0-9]+)/$', views.ReserveResourceCreate.as_view(), name='reserve-resource'),

    url(r'^reserve/addReserve/$', views.ReserveCreate.as_view(), name='reserve-add'),
    url(r'^reserve/addResource/$', views.ResourceCreate.as_view(), name='resource-add'),
    url(r'^reserve/addTag/$', views.TagCreate.as_view(), name='tag-add'),
    #url(r'^resource/addResource/$', views.resource_create, name='resource-add'),
    url(r'^(?P<reservation_id>[0-9]+)/delete$', views.reserve_delete, name='reserve_delete'),
    url(r'^resource/update/(?P<pk>[0-9]+)/$', views.ResourceUpdate.as_view(), name='resource-update'),
    url(r'^user/(?P<username>\w+)/$', views.user_detail, name='user-detail'),
    url(r'^tag/(?P<tag_id>[0-9]+)/$', views.tag_info, name='tag-detail'),
    url(r'^rss/(?P<resource_id>[0-9]+)/$', ResourcesFeed(), name='rss'),
    #url(r'^reserve/(?P<reservation_id>[0-9]+)/delete/$', views.ReserveDelete.as_view(), name='resource-delete'),
]