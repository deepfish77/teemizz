from django.db import models
from django.conf import settings
from django.template.defaultfilters import default
from teemizone.models import Profession, Tool, Industry, Tag
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf.locale import tr
"""username/email
Name
Phone
Address (country ,zip..)
Summary
Industry
Position
Photo
LinkedIn Profile(Em)
Password
Experience(RM)
Education (RM)
Skills (RM)
Interested In (OS)
Member Of (List)
Past Experience (RM)
Interests (OS)
Reviews
Activity(RM)
"""

User = settings.AUTH_USER_MODEL


class JobReview(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE) 
    name = models.CharField(max_length=100, blank=True)
    related_job = models.ForeignKey(Industry, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
   
TEAM_TYPES = (
    ('S', 'Student'),
    ('G', 'Graduate'),
    ('J', 'Junior'),
    ('I', 'Intermediate'),
    ('P', 'Professional'),
    
)
class TeamRequiredProfession(models.Model):
    name = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=100, blank=True)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE)
    profession = models.ForeignKey(Profession, on_delete=models.CASCADE, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    candidates = models.ManyToManyField(User, blank=True, related_name='candidates')
    accepted_teammate = models.OneToOneField(User, blank=True, on_delete=models.CASCADE , related_name='accepted')


class Team(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  
    type = models.CharField(max_length=20, choices=TEAM_TYPES)
    name = models.CharField(max_length=100, blank=True)
    objective = models.CharField(max_length=100, blank=True)
    summary = models.TextField(blank=True)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE)
    team_jobs = models.ManyToManyField(TeamRequiredProfession)
    tags = models.ManyToManyField(Tag)
    members = models.ManyToManyField(User, blank=True, related_name='members')
     
    def __str__(self):
       return self.name
  
  




    
 
    
  



