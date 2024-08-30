from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'twilio_account_sid', 'twilio_auth_token', 'twilio_phone_number','local_phone_number']
