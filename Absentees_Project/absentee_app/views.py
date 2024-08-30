from django.shortcuts import render, redirect, get_object_or_404
from .forms import StudentForm
from django.http import HttpResponse
from .models import Student
from twilio.rest import Client
from django.conf import settings
import datetime
import pandas as pd
from django.http import HttpResponse
from django.utils.encoding import escape_uri_path
import os


def student_form(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('success')
    else:
        form = StudentForm()
    return render(request, 'student_form.html', {'form': form})

def submit_student_form(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('Form submitted successfully!')
    else:
        form = StudentForm()
    return render(request, 'student_form.html', {'form': form})

def display_names(request):
    students = Student.objects.all()
    return render(request, 'display_names.html', {'students': students})
    

def send_sms_to_selected_students(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_students')  # Get the IDs of selected students
        selected_students = Student.objects.filter(pk__in=selected_ids)  # Retrieve selected students from the database 
        for student in selected_students:
            send_sms(student)
        timestamp = datetime.datetime.now().strftime("%H-%M-%S")  # Generate timestamp
        date = datetime.datetime.now().strftime("%Y-%m-%d")  # Generate date

        # Check if Excel file exists
        file_path = f'selected_students.xlsx'
        if os.path.exists(file_path):
            # If the file exists, read the existing data
            existing_df = pd.read_excel(file_path)
            # Create a DataFrame for new data
            new_data = {'Student Name': [student.name for student in selected_students],
                        'Timestamp': [timestamp] * len(selected_students),
                        'Date': [date] * len(selected_students)}
            new_df = pd.DataFrame(new_data)
            # Append new data to existing DataFrame
            updated_df = pd.concat([existing_df, new_df], ignore_index=True)
            # Write updated DataFrame to Excel file
            updated_df.to_excel(file_path, index=False)
        else:
            # If the file doesn't exist, create a new Excel file
            data = {'Student Name': [student.name for student in selected_students],
                    'Timestamp': [timestamp] * len(selected_students),
                    'Date': [date] * len(selected_students)}
            df = pd.DataFrame(data)
            df.to_excel(file_path, index=False)

        # Twilio API setup and sending SMS messages to selected students (same as before)
        # ...
        return HttpResponse('SMS sent successfully to selected students and Excel file updated!')
    else:
        return HttpResponse('Invalid request method!')


def send_sms(student):
    # Twilio API setup
    account_sid = student.twilio_account_sid
    auth_token = student.twilio_auth_token
    twilio_phone_number = student.twilio_phone_number

    try:
        # Initialize Twilio client
        client = Client(account_sid, auth_token)
        # Send SMS message
        message = client.messages.create(
            body='You were absent for today\'s lecture.',
            from_=twilio_phone_number,
            to=student.local_phone_number
        )
        return f'SMS sent to {student.name} successfully! SID: {message.sid}'
    except Exception as e:
        return f'Error sending SMS to {student.name}: {e}'

def landing_page(request):
    return render(request, 'landing_page.html')

def success(request):
    return render(request,'success.html')
