from django.contrib import admin
from .models import Profession
from teemizone.models import Tool, Industry, Tag, Category, TechSkill

admin.site.register(Profession)
admin.site.register(Tag)
admin.site.register(Tool)
admin.site.register(Industry)
admin.site.register(Category)
admin.site.register(TechSkill)
