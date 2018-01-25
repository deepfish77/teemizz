from django.db import models
from django.conf import settings
from teemizone.models import Profession, Tool, TechSkill
from django.template.defaultfilters import default
from django.urls import reverse
from django.conf.locale import tr
from django.db.models import Q


User = settings.AUTH_USER_MODEL 

class ProjectManager(models.Manager):
    def get_queryset(self):
        return ProjectQuerySet(self.model, using=self._db)

    def search(self, query): #RestaurantLocation.objects.search()
        return self.get_queryset().search(query)
    
    
    
class ProjectQuerySet(models.query.QuerySet):
    def search(self, query): #RestaurantLocation.objects.all().search(query) #RestaurantLocation.objects.filter(something).search()
        if query:
            query = query.strip()
            return self.filter(
                Q(name__icontains=query)|
                Q(name__iexact=query)|
                Q(desired_tech__icontains=query)|
                Q(desired_tech__iexact=query)|
                Q(tools__icontains=query)|
                Q(tools__iexact=query)
                ).distinct()
        return self




class Project(models.Model):
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    desired_tech = models.ManyToManyField(TechSkill, blank=True)
    name = models.CharField(max_length=120)
    #excludes = models.TextField(blank=True, null=True, help_text='seperate each item with comma')
    public = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    requrements = models.ManyToManyField(Profession ,help_text='Select the Desired Pofession', blank=True)
    tools = models.ManyToManyField(Tool, blank=True)
    slug = models.SlugField(null=True, blank=True)
    
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
