from django.conf.urls import url

from .views import (
    TeamCreateView,
    TeamDetailView,
    TeamFullView,
    TeamListView,
    team_api_list,
    team_api_detail,
    TeamApiDetail,
    TeamAPI

)

app_name = "teammates"

urlpatterns = [
    url(r'^create/$',  TeamCreateView.as_view(), name='create-team'),
    url(r'^list/(?P<slug>[\w-]+)/$', TeamListView.as_view()),
    url(r'^detail/(?P<slug>[\w-]+)/$', TeamFullView.as_view()),


    url(r'^api/$',TeamAPI.as_view()),
    url(r'^api/(?P<pk>[0-9]+)/$', team_api_detail),
    url(r'^api/teamdetail/(?P<pk>[0-9]+)/$', TeamApiDetail.as_view()),

]
