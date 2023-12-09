from django import forms
from .models import TaApplicant

class TaApplicantForm(forms.ModelForm):
    class Meta:
        model = TaApplicant
        fields = ['name', 'email', 'z_number', 'phn_number', 'dept', 'level', 'password']



from django import forms
from .models import TaApplicant

class LoginForm(forms.ModelForm):
    class Meta:
        model = TaApplicant
        fields = ['email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
