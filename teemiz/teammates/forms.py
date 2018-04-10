from django import forms
from .models import Team




class TeamCreateForm(forms.ModelForm):
    class Meta:
        model = Team
        
        fields = [
           
            'name',  
            'summary', 
            'owner',        
            'type',
            'objective',
            'industry',
          
            
        ]
        
        
    def __init__(self, user=None, **kwargs):
        print(user)
        super(TeamCreateForm, self).__init__(**kwargs)
        # Filtering kwargs for limiting the objects to the ones that belong to the user 
        #self.fields['Team'].queryset = Profession.objects.filter(owner=user)
        
        # Same filter with exclude
        #self.fields['Team'].queryset = Profession.objects.filter(owner=user).exclude(project__isnull=False)
        
        