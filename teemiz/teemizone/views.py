from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse , HttpResponseRedirect
from django.views import View
from django.views.generic import TemplateView , ListView , CreateView , DetailView
from .models import Profession
from django.db.models import Q
from teemizone.models import TechSkill
from .forms import ProfessionRegistration , ProfessionCreateForm
from django.template.context_processors import request
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class ProfessionCreateView(LoginRequiredMixin, CreateView):
    form_class = ProfessionCreateForm
    template_name = 'form.html'
    success_url = "/teammates/"
    # login_url = "/admin/login/"
    
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = self.request.user
        
        return super(ProfessionCreateView , self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(ProfessionCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Add Profession'
        
        return context
    
    
@login_required()
def team_create_view(request):
    form = ProfessionRegistration(request.POST or None) 
    errors = None     
    #    if request.method == "POST":
    #         name = request.POST.get("name") #request.POST["title"]
    #         experience = request.POST.get("years_of_experience")
    #         category = request.POST.get("occupation_category")
    #         seniority = request.POST.get("seniority")
    #         technical_skills= request.POST.get("technical_skills")
        
    if (form.is_valid()):
        if request.user.is_authenticated():
            
            instance = form.save(commit=False)
            instance.owner = request.user
            instance.save()
            
            # Before association to User
#             obj = Profession.objects.create(
#                     name = form.cleaned_data.get('name'),
#                     years_of_experience= form.cleaned_data.get('years_of_experience'),
#                     occupation_category = form.cleaned_data.get('occupation_category'),
#                     technical_skills = form.cleaned_data.get('technical_skills'),
#                     seniority = form.cleaned_data.get('seniority')
#  
#         )
            return HttpResponseRedirect("/teammates/")
        else:
            return HttpResponseRedirect("/login/")
    
    if (form.errors):
        print(form.errors)
      
    template_name = 'form.html'
    context = {"form": form, "errors": errors}
      
    return  render(request, template_name , context)   


def teammate_list_view(request):
    template_name = 'teamates_list.html'
    queryset = Profession.objects.all()
    print (queryset)
    context = {
        "object_list": queryset
    }
    return render(request, template_name, context)    
    
# LIST VIEWS

    
class ProfessionListVIew(ListView):
    template_name = 'teamates_list.html'

    # queryset = Profession.objects.filter(occupation_category='python')
    def get_queryset(self):
        print("kwargs" + str(self.kwargs.get))
        
        slug = self.kwargs.get("slug")
        if slug:
            queryset = Profession.objects.filter(
                
                  Q (occupation_category__icontains=slug))
            print("QUER: " + str(queryset))
        else:
            queryset = Profession.objects.all()
            print("QUERAllpy: " + str(queryset.all()))
        return queryset  # ListView.get_queryset(self)
    
    # DETAIL VIEWS 

    
class ProfessionDetailView(DetailView):
    template_name = 'teemates_detail.html'

    queryset = Profession.objects.all()
     
    def get_context_data(self, **kwargs):
        print("The args are:" + str(kwargs))
        context = super(ProfessionDetailView, self).get_context_data(**kwargs)
        print("The Context Below")
        print(context)
        return context
    
    def get_object(self, *args, **kwargs):
        
        pk = self.kwargs.get('pk')
        print("mate_id_is")
        print(pk)
        if (pk is not None):
            selected_choice = int(pk)
        else:
            selected_choice = 1
      
        obj = get_object_or_404(Profession, id=selected_choice)
        return obj
     
# class RestaurantDetailView(DetailView):
#     queryset = RestaurantLocation.objects.all()
#     
#     def get_object(self, *args, **kwargs):
#         rest_id = self.kwargs.get('rest_id')
#         obj = get_object_or_404(RestaurantLocation, id=rest_id) # pk = rest_id
#         return obj
    
# METHOD BASED VIEWS
# def home(request):
#     num = random.randint(0, 1000000)
#     some_list = [num, random.randint(0, 1000000) , random.randint(99999999, 9999999999999)]
#     context = {
#        " bool_item":False,
#        "num":num,
#        "some_list":some_list
#         
#         }
#     condition_bool_item = False
#     if (condition_bool_item):
#             num = random.randint(0, 100000000)
#     return render(request, "base.html", context)

# def about(request):
#     
#     context = {
#         }
#   
#     return render(request, "about.html", context)

# CLASS BASED VIEW
# class ContactView(View):
#     
#     def get(self , request, *args, **kwargs):
#         context = {}
#         return  render(request, "contact.html" , context)    
   
   # TEMPLATEVIEW BASED VIEW         
# class ContactView(TemplateView):
#     template_name = 'contact.html'    
#     
#     
# class AboutView(TemplateView):
#     tempalte_name = 'about.html'
#     
#     
# class HomeView(TemplateView):
#     template_name = 'home.html'
#     
#     def get_context_data(self, *args, **kwargs):
#         
#         context = super(HomeView , self).get_context_data(*args, **kwargs)
#         #print  ("the context is "  + context)
#         return context
#     

