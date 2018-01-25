
from django.contrib import admin
from django.conf.urls import url , include
from teemizone.views import (teammate_list_view , ProfessionListVIew  , ProfessionDetailView , team_create_view , ProfessionCreateView)
from django.contrib.auth.views import LoginView , TemplateView 
from profiles.views import ProfileFollowToggle ,RegisterView
# urlpatterns = [
#     url(r'^admin/', admin.site.urls),
#     url(r'^$', HomeView.as_view(), name='home'),
#     url(r'^register/$', RegisterView.as_view(), name='register'),
#     url(r'^activate/(?P<code>[a-z0-9].*)/$', activate_user_view, name='activate'),
#     url(r'^login/$', LoginView.as_view(), name='login'),
#     url(r'^logout/$', LogoutView.as_view(), name='logout'),
#     url(r'^profile-follow/$', ProfileFollowToggle.as_view(), name='follow'),
#     url(r'^u/', include('profiles.urls', namespace='profiles')),
#     url(r'^items/', include('menus.urls', namespace='menus')),
#     url(r'^restaurants/', include('restaurants.urls', namespace='restaurants')),
#     url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),
#     url(r'^contact/$', TemplateView.as_view(template_name='contact.html'), name='contact'),
# ]

urlpatterns = [
        url(r'^admin/', admin.site.urls),
        url(r'^teammates/$', teammate_list_view),
        url(r'^login/$', LoginView.as_view(), name='login'),
    # url(r'^logout/$', LogoutView.as_view(), name='logout'),
        url(r'^register/$', RegisterView.as_view(), name='register'),
    # url(r'^teammateslist/(?P<slug>[\w-]+)/$', ProfessionListVIew.as_view()),
        url(r'^teammates/(?P<slug>[\w-]+)/$', ProfessionListVIew.as_view()),
        url(r'^teammates-detail/(?P<slug>[\w-]+)/$', ProfessionDetailView.as_view()),
    # url(r'^create/$', team_create_view),
        url(r'^create/$', ProfessionCreateView.as_view()),
    # url(r'^teammates/python$', PythonProfessionListVIew.as_view()),
        url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),
        url(r'^contact/$', TemplateView.as_view(template_name='contact.html'), name='contact'),
        url(r'^projects/', include('projects.urls' , namespace='projects')),
        url(r'^u/', include('profiles.urls', namespace='profiles')),
       url(r'^profile-follow/$', ProfileFollowToggle.as_view(), name='follow'),

             ]
    
