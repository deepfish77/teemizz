from django.contrib import admin
from teammates.models import Team, WhatWeNeed, TeamPositions, JobReview,\
    Responsibilities

# Register your models here.
admin.site.register(WhatWeNeed)
admin.site.register(Team)
admin.site.register(TeamPositions)
admin.site.register(JobReview)
admin.site.register(Responsibilities)

