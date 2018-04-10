from django.db import models
from enum import unique
from django.db.models.signals import pre_save , post_save
from .utils import unique_slug_generator
from .validators import validate_category
from django.conf import settings
from django.db.models import Q
User = settings.AUTH_USER_MODEL
    
    
# Industry 
class Industry (models.Model):
    name = models.CharField(max_length=120, null=True, blank=True)
    description = models.CharField(max_length=120, null=True, blank=True)
    
    def __str__(self):
        return self.name

   
# TechSkill Model
class TechSkill(models.Model):
    name = models.CharField(max_length=120, null=True, blank=True)
    description = models.CharField(max_length=120, null=True, blank=True)
    industry = models.ManyToManyField(Industry)  
    tools = models.ManyToManyField('Tool')
    
    def __str__(self):
        return self.name
# Category Model


class Category(models.Model):
    name = models.CharField(max_length=120, null=True, blank=True)
    description = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return self.name

# Experience 


class Experience(models.Model):
    name = models.CharField(max_length=120, null=True, blank=True)
    description = models.CharField(max_length=120, null=True, blank=True)
    duration = models.CharField(max_length=12, null=True, blank=True)
    Industry = models.ForeignKey('Industry', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

 
# Tools 
class Tool (models.Model):
    name = models.CharField(max_length=120, null=True, blank=True)
    description = models.CharField(max_length=120, null=True, blank=True)
    usage = models.CharField(max_length=120, null=True, blank=True)
    
    def __str__(self):
        return self.name

    
class Tag(models.Model):
    name = models.CharField(max_length=120, null=True, blank=True)
   
    def __str__(self):
        return self.name
   

# Profession Model
class Profession(models.Model):
   # owner = models.ForeignKey(User, on_delete = models.CASCADE)  # class_instance.model_set.all() # Django Models Unleashed JOINCFE.com
    name = models.CharField(max_length=120, null=True, blank=True) 
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True) 
    skills = models.ManyToManyField(TechSkill, blank=True)
    tools = models.ManyToManyField(Tool, blank=True)
    industry = models.ManyToManyField(Industry, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    updated = models.DateTimeField(auto_now=True, blank=True)
    slug = models.SlugField(null=True, blank=True)
    
    def __str__(self):
        return self.name

    @property
    def title(self):
        return self.name
    
    
class ProfessionQuerySet(models.query.QuerySet):

    def search(self, query):  # RestaurantLocation.objects.all().search(query) #RestaurantLocation.objects.filter(something).search()
        if query:
            query = query.strip()
            return self.filter(
                Q(name__icontains=query) | 
                Q(category__icontains=query) | 
                Q(category__iexact=query) | 
                Q(skills__icontains=query) | 
                Q(skills__iexact=query) | 
                Q(tools__icontains=query) | 
                Q(tools__contents__icontains=query)
                ).distinct()
        return self
   
    
def rl_pre_save_receiver(sender, instance, *args, **kwargs):
    print('saving..')
    print(instance.timestamp)
    if not instance.slug:
        # instance.name = 'new teemate'
        instance.slug = unique_slug_generator(instance)

    
def rl_post_save_receiver(sender, instance, *args, **kwargs):
    print('saved')
    print(instance.timestamp)
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
        instance.save()


pre_save.connect(rl_pre_save_receiver, sender=Profession)

# post_save.connect(rl_post_save_receiver, sender=Profession)