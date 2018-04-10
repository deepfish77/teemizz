
from django.contrib import admin
from django.conf.urls import url , include
from django.contrib.auth.views import LoginView , TemplateView 
from profiles.views import ProfileFollowToggle , RegisterView
from teammates.views import HomeView
from django.conf import settings
from django.conf.urls.static import static
from django.views import generic
from rest_framework.schemas import get_schema_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import views, serializers, status
from rest_framework.response import Response




urlpatterns = [
        url(r'^$', HomeView.as_view(), name='home'),
        url(r'^admin/', admin.site.urls),
        url(r'^login/$', LoginView.as_view(), name='login'),
        url(r'^register/$', RegisterView.as_view(), name='register'),
        url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),
        url(r'^contact/$', TemplateView.as_view(template_name='contact.html'), name='contact'),
        url(r'^projects/', include('projects.urls' , namespace='projects')),
        url(r'^teammates/', include('teammates.urls' , namespace='teammates')),
        url(r'^professions/', include('teemizone.urls' , namespace='teemizone')),
        url(r'^u/', include('profiles.urls', namespace='profiles')),
        url(r'^profile-follow/$', ProfileFollowToggle.as_view(), name='follow'),
        url(r'^$', generic.RedirectView.as_view( url='/api/', permanent=False)),
        url(r'^api/$', get_schema_view()),
        url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),
        url(r'^api/auth/token/obtain/$', TokenObtainPairView.as_view()),
        url(r'^api/auth/token/refresh/$', TokenRefreshView.as_view()),
      

             ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 
    



