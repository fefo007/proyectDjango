from django import forms
from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .models import Avatar,Travel,Messages,Order
from betterforms.multiform import MultiModelForm

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['wayToPay','departure','arrival']

class SendMessage(forms.ModelForm):
    class Meta:
        model = Messages
        widgets = {
            'message':forms.Textarea()
        }
        fields = ['addressee','subject','message']

class ChangeTravelForm(forms.ModelForm):
    class Meta:
        model = Travel
        widgets = {
            'description': forms.Textarea()
        }
        fields = '__all__'

class ChangeToursForm(forms.ModelForm):
    class Meta:
        model = Travel
        widgets = {
            'text': forms.Textarea()
        }
        fields = '__all__'

class ChangeTravelAdmin(admin.ModelAdmin):
    form = ChangeTravelForm
    
class ChangeToursAdmin(admin.ModelAdmin):
    form = ChangeToursForm

class UserEditForm(UserChangeForm):

    password = forms.CharField(help_text='',widget=forms.HiddenInput,required=False)

    # password1 = forms.CharField(label='password')
    # password2 = forms.CharField(label='repetir password')

    class Meta:
        model = User
        fields = ['first_name','last_name','email']

    # def clean_password(self):
    #     password1 = self.cleaned_data['password1']
    #     password2 = self.cleaned_data['password2']
    #     if password1 != password2:
    #         raise forms.ValidationError('las contraseñas no coinciden')
    #     return password2
    

class AvatarEditForm(forms.ModelForm):
    class Meta:
        model = Avatar
        fields = ('image',)

class UserEdit(MultiModelForm):
    form_classes = {
        'avatar':AvatarEditForm,
        'user':UserEditForm
        }

