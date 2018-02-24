
from teemizone.views import (profesion_list_view , ProfessionListVIew  , ProfessionDetailView  , ProfessionCreateView)
from django.conf.urls import url 
app_name="teemizone"

urlpatterns = [
    
    url(r'^list/(?P<slug>[\w-]+)/$', ProfessionListVIew.as_view()),
    url(r'^detail/(?P<slug>[\w-]+)/$', ProfessionDetailView.as_view()),
    url(r'^$', profesion_list_view),
    url(r'^create/$', ProfessionCreateView.as_view()),
    
    ]

# url(r'^teammateslist/(?P<slug>[\w-]+)/$', ProfessionListVIew.as_view()),        
# url(r'^create/$', profession_create_view),
# url(r'^teammates/python$', PythonProfessionListVIew.as_view()),
