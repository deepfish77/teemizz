from django.conf.urls import url

from .views import (
    TeamCreateView,
    TeamDetailView,
    TeamListView,
  
)

app_name="teammates"

urlpatterns = [
    url(r'^create-team/$',  TeamCreateView.as_view(), name='create-team'),
    #url(r'^(?P<pk>\d+)/edit/$', ProjectUpdateView.as_view(), name='update-team'),
    url(r'^(?P<pk>\d+)/$', TeamDetailView.as_view(), name='team-detail'),
    url(r'^$', TeamListView.as_view(), name='team-list'),
]