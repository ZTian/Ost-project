from django.conf.urls import include, url
from django.contrib import admin
from reserve.views import login_view, register_view, logout_view


urlpatterns = [
    url(r'^reserve/', include('reserve.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^login/', login_view, name="login"),
    url(r'^logout/', logout_view, name="logout"),
    url(r'^register/', register_view, name="register"),
]
