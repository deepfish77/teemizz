from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, View
from .models import Profile
from .forms import RegisterForm
from projects.models import Project
from teammates.models import Team 


User = get_user_model()



class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = '/'

    def dispatch(self, *args, **kwargs):
        # if self.request.user.is_authenticated():
        #     return redirect("/logout")
        return super(RegisterView, self).dispatch(*args, **kwargs)



class ProfileFollowToggle(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        username_to_toggle = request.POST.get("username")
        profile_, is_following = Profile.objects.toggle_follow(request.user, username_to_toggle)
        return redirect(f"/u/{profile_.user.username}/")

 
 
 
 
class ProfileDetailView(DetailView):
    template_name = 'profiles/user.html'
    """Checkiing the user """
    def get_object(self):
        username = self.kwargs.get("username")
        if username is None:
            raise Http404
        print(User.objects.all())
        return get_object_or_404(User, username__iexact=username, is_active=True)

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(*args, **kwargs)
        user = context['user']
        is_following = False
        if user.profile in self.request.user.is_following.all():
            is_following = True
        context['is_following'] = is_following
        query = self.request.GET.get('q')
        print("the query" , query)
        
        
        # getting the projects related to the user 
        items_exists = Project.objects.filter(user=user).exists()
        project_qs = Project.objects.filter(user=user).search(query) 
        if items_exists and project_qs.exists():
            context['projects'] = project_qs
        # getting the teams related to the user    
        team_exists = Team.objects.filter(owner=user).exists()
        print ("the team:" ,team_exists)
        team_qs = Team.objects.filter(owner=user).search(query)
        if team_exists and team_qs.exists():
            context['teams'] = team_qs
            print('team context: ' , team_qs)
        
        return context 
    
    
    
    
def activate_user_view(request, code=None, *args, **kwargs):
    if code:
        qs = Profile.objects.filter(activation_key=code)
        if qs.exists() and qs.count() == 1:
            profile = qs.first()
            if not profile.activated:
                user_ = profile.user
                user_.is_active = True
                user_.save()
                profile.activated=True
                profile.activation_key=None
                profile.save()
                return redirect("/login")
    return redirect("/login")
