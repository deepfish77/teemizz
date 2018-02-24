from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, View , ListView
from .models import Team
from teammates.forms import TeamCreateForm
from teammates.models import TeamPositions
from projects.models import Project
# from .forms import RegisterForm

User = get_user_model()

#Team Views

class TeamFollowToggle(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        username_to_toggle = request.POST.get("username")
        profile_, is_following = Team.objects.toggle_follow(request.user, username_to_toggle)
        return redirect(f"/u/{profile_.user.username}/")


class TeamListView(ListView):
    def get_queryset(self):
        return Team.objects.filter(user=self.request.user)


class TeamDetailView(DetailView):
    def get_queryset(self):
        return Team.objects.filter(user=self.request.user)


class TeamCreateView(CreateView):
    template_name = 'form.html'
    form_class = TeamCreateForm
    
   
   
# Team Position Views  
class TeamPositionView(ListView):
    def get_queryset(self):
        print("TheTeam: " ,self.request.team)
        return TeamPositions.objects.filter(team=self.requeset.team)  
    
    
    
    
    
    
    
class HomeView(View):
 
    def get(self, request, *args, **kwargs):    
        #if  request.user.is_authenticated():
            teams_list = Team.objects.all()
            projects_list = Project.objects.all()
            print("The Teams List", teams_list)
            print("The Projects List", projects_list)
            return render(request, "home.html", {"teams": teams_list , "projects": projects_list})

    """Checkiing the user """
    def get_object(self):
        username = self.kwargs.get("username")
        if username is None:
            raise Http404
        print(User.objects.all())
        return get_object_or_404(User, username__iexact=username, is_active=True)

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(*args, **kwargs)
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
    
    
#         is_following_user_ids = [x.user.id for x in user.is_following.all()]
#         qs = Team.objects.filter(user__id__in=is_following_user_ids, public=True).order_by("-updated")[:3]
#         return render(request, "menus/home-feed.html", {'object_list': qs})

