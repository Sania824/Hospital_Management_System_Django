from django.http import Http404
from django.test import TestCase
import pytest
from django.contrib.auth.models import User
from django.test import RequestFactory
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
# from hospital.models import Patient
from hospital.models import Patient

# Create your tests here.

# Test login_view
@pytest.mark.django_db
def test_login_view_get(client):
    response = client.get(reverse('login'))
    assert response.status_code == 200
    assert 'login.html' in [t.name for t in response.templates]

@pytest.mark.django_db
def test_login_view_post_success(client):
    User.objects.create_user(username='sania', password='admin123', is_staff=True)
    response = client.post(reverse('login'), {
        'uname': 'sania',
        'pwd': 'admin123'
    })
    assert response.status_code == 302
    assert response.url == reverse('index')

@pytest.mark.django_db
def test_login_view_post_failure(client):
    response = client.post(reverse('login'), {
        'uname': 'wrong',
        'pwd': 'wrong'
    })
    assert response.status_code == 200
    assert 'login.html' in [t.name for t in response.templates]
    assert 'error' in response.context

# Test logout_view
@pytest.mark.django_db
def test_logout_view_authenticated(client):
    user = User.objects.create_user(username='testuser', password='12345')
    client.force_login(user)
    response = client.get(reverse('logout'))
    assert response.status_code == 302
    assert response.url == reverse('login')

@pytest.mark.django_db
def test_logout_view_unauthenticated(client):
    response = client.get(reverse('logout'))
    assert response.status_code == 302
    assert response.url == reverse('login')

# Test add_patient
@pytest.mark.django_db
def test_add_patient_get(client):
    response = client.get(reverse('add_patient'))
    assert response.status_code == 200
    assert 'add_patient.html' in [t.name for t in response.templates]

@pytest.mark.django_db
def test_add_patient_post_success(client):
    response = client.post(reverse('add_patient'), {
        'name': 'Ayesha Khan',
        'gender': 'Female',
        'mobile': '1234567890',
        'address': 'Main St'
    })
    assert response.status_code == 302
    assert response.url == reverse('patient_page')
    assert Patient.objects.count() == 1

@pytest.mark.django_db
def test_add_patient_post_missing_fields(client):
    response = client.post(reverse('add_patient'), {
        'name': '',
        'gender': 'Female',
        'mobile': '1234567890',
        'address': 'Main St'
    })
    assert response.status_code == 200
    assert 'error' in response.context
    assert Patient.objects.count() == 0

@pytest.mark.django_db
def test_add_patient_post_invalid_mobile(client):
    response = client.post(reverse('add_patient'), {
        'name': 'Ayesha Khan',
        'gender': 'Female',
        'mobile': 'invalid',
        'address': ' Main St'
    })
    assert response.status_code == 200
    assert 'error' in response.context
    assert Patient.objects.count() == 0

# Test view_patients
@pytest.mark.django_db
def test_view_patients_empty(client):
    response = client.get(reverse('view_patients'))
    assert response.status_code == 200
    assert 'view_patients.html' in [t.name for t in response.templates]
    assert len(response.context['data']) == 0

@pytest.mark.django_db
def test_view_patients_with_data(client):
    Patient.objects.create(
        name='Ayesha Khan',
        gender='Female',
        mobile='1234567890',
        address=' Main St'
    )
    response = client.get(reverse('view_patients'))
    assert response.status_code == 200
    assert len(response.context['data']) == 1

# Test del_patient
@pytest.mark.django_db
def test_del_patient(client):
    patient = Patient.objects.create(
        name='Ayesha Khan',
        gender='Female',
        mobile='1234567890',
        address=' Main St'
    )
    response = client.get(reverse('del_patient', args=[patient.id]))
    assert response.status_code == 302
    assert response.url == reverse('view_patients')
    with pytest.raises(Patient.DoesNotExist):
        Patient.objects.get(id=patient.id)

@pytest.mark.django_db
def test_del_nonexistent_patient(client):
        response = client.get(reverse('del_patient', args=[999]))  # ID doesn't exist
        assert response.status_code == 404

# Test update_patients
@pytest.mark.django_db
def test_update_patients_get(client):
    patient = Patient.objects.create(
        name='Ayesha Khan',
        gender='Female',
        mobile='1234567890',
        address=' Main St'
    )
    response = client.get(reverse('update_patients', args=[patient.id]))
    assert response.status_code == 200
    assert 'update_patients.html' in [t.name for t in response.templates]
    assert response.context['patient'] == patient

@pytest.mark.django_db
def test_update_patients_post(client):
    patient = Patient.objects.create(
        name='Ayesha Khan',
        gender='Female',
        mobile='1234567890',
        address=' Main St'
    )
    response = client.post(reverse('update_patients', args=[patient.id]), {
        'name': 'Jane Doe',
        'gender': 'Female',
        'mobile': '0987654321',
        'address': '456 Oak St'
    })
    assert response.status_code == 302
    assert response.url == reverse('view_patients')
    updated_patient = Patient.objects.get(id=patient.id)
    assert updated_patient.name == 'Jane Doe'
    assert updated_patient.gender == 'Female'
    assert updated_patient.mobile == '0987654321'
    assert updated_patient.address == '456 Oak St'
#
# @pytest.mark.django_db
# def test_add_patient_post_success(client):
#     response = client.post(reverse('add_patient'), {
#         'name': 'John Doe',
#         'gender': 'Male',
#         'mobile': '1234567890',
#         'address': '123 Main St'
#     })
#     assert response.status_code == 302
#     assert response.url == reverse('patient_page')
#     assert Patient.objects.count() == 1