from django.conf.urls import url
from films import views as films_views


urlpatterns = [
    url(r'^$', films_views.list, name='film_list'),
    url(r'^(?P<pk>[0-9]+)/$', films_views.detail, name='film_detail'),
    url(r'^top/$', films_views.top_rated, name='film_top_rated'),
]
