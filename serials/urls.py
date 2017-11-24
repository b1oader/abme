from django.conf.urls import include, url
from serials import views as serials_views

#from .views import SignUpView

urlpatterns = [
    url(r'^$', serials_views.list, name='serial_list'),
    url(r'^(?P<pk>[0-9]+)/$', serials_views.detail, name='serial_detail'),
]