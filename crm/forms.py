from django import forms
from django.forms import ModelForm, inlineformset_factory
from .models import Applicant, FamilyMember, Order


class ApplicantForm(ModelForm):
    class Meta:
        model = Applicant
        exclude = ()

class FamilyMemberForm(ModelForm):
    class Meta:
        model = FamilyMember
        exclude = ()

FamilyMemberFormSet = inlineformset_factory(Applicant, FamilyMember,
form=FamilyMemberForm, extra=1)

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'


