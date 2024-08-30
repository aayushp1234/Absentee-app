# absentee_app/models.py

from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=100)
    twilio_account_sid  = models.CharField(max_length=100)
    twilio_auth_token   = models.CharField(max_length=100)
    twilio_phone_number = models.CharField(max_length=20)
    local_phone_number  = models.CharField(max_length=20, default = "+910000000000")

    class Meta:
        app_label = 'absentee_app'
