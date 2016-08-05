from django.conf.urls import patterns, url, include
from . import views

urlpatterns = [
    #'api.views',
    #url(r'^weatherapi$',views.index, name = 'index')
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #url(r'^weatherapi/get/$', views.CustomGet.as_view()),
    url(r'^weatherapi/', views.CustomGet.as_view()),
]
