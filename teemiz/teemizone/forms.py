from django import forms
from .models import Profession
from teemizone.validators import validate_category
from teemizone.models import Industry ,Profession









class ProfessionRegistration(forms.Form):
    name = forms.CharField(required=False)
    category = forms.CharField(required=False)
    experience = forms.CharField(required=False)
    industry = forms.CharField(required=False)
    skills = forms.CharField(required=False)
    
    def clean_name(self):
        name = self.cleaned_data.get("name")
        if(name == "Hello"):
            raise forms.ValidationError("Occupation Name is not valid")
        
        
class ProfessionCreateForm(forms.ModelForm):
   # email = forms.EmailField()
   
   # occupation_category = forms.CharField(required=False , validators=[validate_category])

    class Meta:
        model = Profession
        fields = [
            'name',
            'skills',
            'category',
            'industry',
           
        ]
    
    def clean_name(self):
        name = self.cleaned_data.get("name")
        if name == "Hello":
            raise forms.ValidationError("Not a valid name")
        return name
    
#     def clean_email(self):
#         email = self.cleaned_data.get("email")
#         if (".edu" in email): 
#             raise forms.ValidationError("We don't accept emails from .edu domain")
#         return email
