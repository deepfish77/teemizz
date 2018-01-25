from django import forms
from teemizone.models import Profession


from .models import Project
#Model form, a form that is based on the model 
class ProjectCreateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            
            'name',         
            'requrements',
            'desired_tech',
            'public',
            'tools'
        ]
        
        
    def __init__(self, user=None, **kwargs):
        print(user)
        super(ProjectCreateForm, self).__init__(**kwargs)
        # Filtering kwargs for limiting the objects to the ones that belong to the user 
        #self.fields['Project'].queryset = Profession.objects.filter(owner=user)
        
        # Same filter with exclude
        #self.fields['Profession'].queryset = Profession.objects.filter(owner=user).exclude(project__isnull=False)
        
        