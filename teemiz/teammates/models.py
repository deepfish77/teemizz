from django.db import models
from django.conf import settings
from django.template.defaultfilters import default
from teemizone.models import Profession, Tool, Industry, Tag
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf.locale import tr
from django.db.models import Q
from django.urls import reverse
from teemizone.utils import unique_slug_generator
from django.db.models.signals import pre_save


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


class Member(models.Model):
    # name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='member', blank=True)
    related_profession = models.OneToOneField(
        Profession, on_delete=models.CASCADE, blank=True)


POSITION_TYPES = (
    ('F', 'Full Time'),
    ('P', 'Part Time'),
    ('J', 'Hours'),

)


class Responsibilities(models.Model):
    name = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)


EXPERIENCE = (
    ('0', 'No Experience'),
    ('1', '0-1 Years'),
    ('2', '1-3 Years'),
    ('3', '3-5 Years'),
    ('4', 'More THan 5 Years'),

)


class WhatWeNeed(models.Model):
    name = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    technologies = models.ManyToManyField(Tool, blank=True)
    experience = models.CharField(
        max_length=100, choices=EXPERIENCE, blank=True)


class TeamPositionsManager(models.Manager):
    def apply_to_position(self, request_user, position_to_add):
        position_ = TeamPositions.objects.get(
            position__name__iexact=position_to_add)
        user = request_user
        is_applied = False
        if user in position_.candidates.all():
            position_.candidates.remove(user)
        else:
            position_.candidatess.add(user)
            is_applied = True
        return position_, is_applied


TEAM_TYPES = (
    ('S', 'Student'),
    ('G', 'Graduate'),
    ('J', 'Junior'),
    ('I', 'Intermediate'),
    ('P', 'Professional'),
    ('M', 'Mixed'),

)


class TeamManager(models.Manager):
    def get_queryset(self):
        return TeamQuerySet(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query)

    def toggle_follow(self, request_team, username_to_toggle):
        team_ = Team.objects.get(user__username__iexact=username_to_toggle)
        team = request_team
        is_following = False
        if team in team_.followers.all():
            team_.followers.remove(team)
        else:
            team_.followers.add(team)
            is_following = True
        return team_, is_following


class TeamQuerySet(models.query.QuerySet):
    def search(self, query):  # RestaurantLocation.objects.all().search(query) #RestaurantLocation.objects.filter(something).search()
        if query:
            query = query.strip()
            return self.filter(
                Q(name__icontains=query) |
                Q(name__iexact=query) |
                Q(objective__icontains=query) |
                Q(objective__iexact=query) |
                Q(team_positions__icontains=query) |
                Q(team_positions__iexact=query)

            ).distinct()
        return self


class Team(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    type = models.CharField(
        max_length=20, choices=TEAM_TYPES, blank=True, default=None)
    name = models.CharField(max_length=100, blank=True)
    objective = models.CharField(max_length=100, blank=True)
    summary = models.TextField(blank=True, default=None)
    industry = models.ForeignKey(
        Industry, on_delete=models.CASCADE, blank=True, default=None)
    tags = models.ManyToManyField(Tag, blank=True, default=None)
    docfile = models.FileField(
        upload_to='documents/%Y/%m/%d', blank=True, default=None)
    slug = models.SlugField(null=True, blank=True, default=None)

    objects = TeamManager()

    def __str__(self):
        return self.name

    @property
    def industry_name(self):
        return self.industry.name


#     def get_absolute_url(self):  # get_absolute_url
#         # return f"/teams/{self.slug}"
#         return reverse('team-detail', kwargs={'slug': self.slug})

    @property
    def title(self):
        return self.name


class TeamPositions(models.Model):
    name = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=100, blank=True)
    industry = models.ForeignKey(
        Industry, on_delete=models.CASCADE, blank=True, related_name='position_industry')
    profession = models.ForeignKey(
        Profession, on_delete=models.CASCADE, blank=True, related_name='position_profession')
    tags = models.ManyToManyField(Tag, blank=True, related_name='position_tags')
    candidates = models.ManyToManyField(
        User, blank=True, related_name='position_candidates')
    responsibilities = models.ManyToManyField(Responsibilities, blank=True, related_name='position_responsibilities')
    what_we_need = models.ManyToManyField(WhatWeNeed, blank=True , related_name='position_requirements')
    accepted_teammate = models.OneToOneField(
        User, blank=True, null=True, on_delete=models.CASCADE, related_name='accepted')
    related_team = models.ForeignKey(
        Team, on_delete=models.CASCADE, blank=True, related_name='related_positions')

    def __str__(self):
        return self.name

    objects = TeamPositionsManager()


class JobReview(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    related_job = models.ForeignKey(TeamPositions, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)])


def rl_pre_save_receiver(sender, instance, *args, **kwargs):
    instance.category = instance.name.capitalize()
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(rl_pre_save_receiver, sender=Team)
