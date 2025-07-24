from django.urls import path, include
from . import views

# app_name = 'hospital'
urlpatterns = [
    # path('', views.about, name='about'),
    path('', views.index, name='index'),
    path('about/', views.about, name = 'about'),
    path('home/', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name = 'logout'),
    path('patient_page/', views.patient_page, name = 'patient_page'),
    path('add_patient/', views.add_patient, name='add_patient'),
    path('view_patients/', views.view_patients, name='view_patients'),
    path('del_patient/<int:patient_id>/', views.del_patient, name='del_patient'),
    path('update_patients/<int:patient_id>/', views.update_patients, name='update_patients'),
    path('doctor_page/', views.doctor_page, name = 'doctor_page'),
    path('add_doctor/', views.add_doctor, name='add_doctor'),
    path('view_doctor/', views.view_doctor, name='view_doctor'),
    path('del_doctor/<int:doctor_id>/', views.del_doctor, name='del_doctor'),
    path('update_doctor/<int:doctor_id>/', views.update_doctor, name='update_doctor'),
    path('apt_page/', views.apt_page, name = 'apt_page'),
    path('add_apt/', views.add_apt, name='add_apt'),
    path('view_apt/', views.view_apt, name='view_apt'),
    path('del_apt/<int:apt_id>/', views.del_apt, name='del_apt'),
    path('update_apt/<int:apt_id>/', views.update_apt, name='update_apt'),
]