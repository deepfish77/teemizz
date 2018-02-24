from django.db import models
from django.conf import settings
from teemizone.models import Profession, Tool, TechSkill
from django.template.defaultfilters import default
from django.urls import reverse
from django.conf.locale import tr
from django.db.models import Q
from teammates.models import Team ,TeamPositions


User = settings.AUTH_USER_MODEL 


class ProjectManager(models.Manager):

    def get_queryset(self):
        return ProjectQuerySet(self.model, using=self._db)

    def search(self, query):  # RestaurantLocation.objects.search()
        return self.get_queryset().search(query)
    
    def add_team_candidate(self, request_team, project_to_join):
        project_ = Project.objects.get(project_to_join)
        team = request_team
        if team in project_.team_candidates.all() :
            return team
        else:
            project_.team_candidates.add(team)
            
        return team
    def remove_team_candidate(self, request_team, project_to_join):
        project_ = Project.objects.get(project_to_join)
        team = request_team
        if team in project_.team_candidates.all() :
            project_.team_candidates.remove(team)
        else:
            return team
            
        return team
    
    
    
class ProjectQuerySet(models.query.QuerySet):

    def search(self, query):  # RestaurantLocation.objects.all().search(query) #RestaurantLocation.objects.filter(something).search()
        if query:
            query = query.strip()
            return self.filter(
                Q(name__icontains=query) | 
                Q(name__iexact=query) | 
                Q(desired_tech__icontains=query) | 
                Q(desired_tech__iexact=query) | 
                Q(tools__icontains=query) | 
                Q(tools__iexact=query)
                ).distinct()
            
        return self


class Project(models.Model):
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    desired_tech = models.ManyToManyField(TechSkill, blank=True)
    name = models.CharField(max_length=120)
    public = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    requrements = models.ManyToManyField(Profession , help_text='Select the Desired Pofession', blank=True)
    tools = models.ManyToManyField(Tool, blank=True)
    slug = models.SlugField(null=True, blank=True)
    team_candidates = models.ManyToManyField(Team, blank=True, related_name='team_candidates')
    selected_team = models.OneToOneField(Team, blank=True, on_delete=models.CASCADE, related_name='selected_team',default=None)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('projects:detail' , kwargs={'slug':self.pk})
    
    class Meta:
        ordering = ['-updated', '-timestamp']
        
    def get_desired_tech(self):
        return self.desired_tech.all()
    
    objects = ProjectManager()

#     def get_excludes(self):
#         return self.excludes.split(",")
