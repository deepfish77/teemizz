from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .project_forms import ProjectCreateForm
from .models import Project


class ProjectListView(ListView):
    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)


class ProjectDetailView(DetailView):
    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)


class ProjectCreateView(CreateView):
    template_name = 'form.html'
    form_class = ProjectCreateForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        return super(ProjectCreateView, self).form_valid(form)

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Create Project'
        return context
    
    def get_form_kwargs(self):
        kwargs = super(ProjectCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    


class ProjectUpdateView(UpdateView):
    template_name = 'form.html'
    form_class = ProjectCreateForm

    def get_queryset(self):
        return Project.objects.filter(creator=self.request.creator)

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Update Item'
        return context