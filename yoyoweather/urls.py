from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'yoyoweather.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^api/', include('api.urls')),
    url(r'^', include('api.urls')),
    url(r'^admin/', admin.site.urls),
]
