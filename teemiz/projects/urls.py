from django.conf.urls import url


from .views import (
    ProjectCreateView,
    ProjectDetailView,
    ProjectListView,
    ProjectUpdateView,
)
app_name="projects"
urlpatterns = [
    url(r'^create-project/$',  ProjectCreateView.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/edit/$', ProjectUpdateView.as_view(), name='update'),
    url(r'^(?P<pk>\d+)/$', ProjectDetailView.as_view(), name='detail'),
    url(r'list-project/$', ProjectListView.as_view(), name='list'),
]