from django.urls import path
from . import views
from . views import display_names, send_sms


urlpatterns = [
    path('student-form/', views.student_form, name='student_form'),
    path('success/', views.success, name='success'),
    path('display-names/', display_names, name='display_names'),
    path('send-sms/<int:student_id>/', send_sms, name='send_sms'),
    path('submit_student_form/', views.submit_student_form, name='submit_student_form'),
    path('', views.landing_page, name='landing_page'),
    path('send-sms/', views.send_sms_to_selected_students, name='send_sms_to_selected_students')
]
