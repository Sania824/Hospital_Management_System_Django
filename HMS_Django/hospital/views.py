from logging import error
from traceback import print_tb

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout

from .models import Patient, Doctor, Appointment


def about(request):
    return render(request, 'About.html')

def home(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'index.html')

def index(request):
    if not request.user.is_staff:
        return redirect('login')
    else:
        return render(request, 'index.html')

def login_view(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(request, username = u, password = p)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('index')
        else:
            error = "yes"
    return render(request, 'login.html', {error: 'error'})

def logout_view(request):
   if request.user.is_authenticated:
       logout(request)
   return redirect('login')

def patient_page(request):
    return render(request, 'patient_page.html')

def doctor_page(request):
    return render(request, 'doctor_page.html')

def apt_page(request):
    return render(request, 'apt_page.html')
#
# def add_patient(request):
#     return render(request, 'add_patient.html')


def add_patient(request):
    if request.method == 'POST':
        print("Form Submitted")
        name = request.POST.get('name')
        gender = request.POST.get('gender')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')

        print("Received data:", name, gender, mobile, address)

        if name and gender and mobile and address:
            try:
                Patient.objects.create(
                    name = name,
                    gender = gender,
                    mobile = mobile,
                    address = address
                )
                print("Patient Added")
                return redirect('patient_page')
            except ValueError:
                error = "The number should be integers"
        else:
            error = "All fields are required!"

        return render(request, 'add_patient.html', {'error':error})
    return render(request, 'add_patient.html')

def view_patients(request):
    all_data = Patient.objects.all()
    return render(request, 'view_patients.html', {'data':all_data})

def del_patient(request, patient_id):
    patient = get_object_or_404(Patient, id = patient_id)
    patient.delete()
    print("Patient Deleted Successfully")
    return redirect('view_patients')
    # return render(request, 'del_patient.html')

def update_patients(request, patient_id):
    patient = get_object_or_404(Patient, id = patient_id)
    if request.method == 'POST':
        patient.name = request.POST.get('name')
        patient.gender = request.POST.get('gender')
        patient.mobile = request.POST.get('mobile')
        patient.address = request.POST.get('address')
        patient.save()
        return redirect('view_patients')
    return render(request, 'update_patients.html', {'patient':patient})

def add_doctor(request):
    if request.method == 'POST':
        print("Form Submitted")
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        specialization = request.POST.get('specialization')

        print("Received data:", name, mobile, specialization)

        if name and mobile and specialization:
            try:
                Doctor.objects.create(
                    name = name,
                    mobile = mobile,
                    specialization = specialization
                )
                print("Doctor Added")
                return redirect('doctor_page')
            except ValueError:
                error = "The number should be integers"
        else:
            error = "All fields are required!"

        return render(request, 'add_doctor.html', {'error':error})
    return render(request, 'add_doctor.html')

def view_doctor(request):
    all_data = Doctor.objects.all()
    return render(request, 'view_doctor.html', {'data':all_data})

def del_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id = doctor_id)
    doctor.delete()
    print("Doctor Deleted Successfully")
    return redirect('view_doctor')
    # return render(request, 'del_patient.html')

def update_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id = doctor_id)
    if request.method == 'POST':
        doctor.name = request.POST.get('name')
        doctor.mobile = request.POST.get('mobile')
        doctor.specialization = request.POST.get('specialization')
        doctor.save()
        return redirect('view_doctor')
    return render(request, 'update_doctor.html', {'doctor':doctor})

# def add_apt(request):
#     doctor = Doctor.objects.all()
#     patient = Patient.objects.all()
#     error = None
#     if request.method == 'POST':
#         print("Form Submitted")
#         dname = request.POST.get('dname') # Getting the values that were submitted with the POST request
#         pname = request.POST.get('pname')
#         date = request.POST.get('date')
#         time = request.POST.get('time')
#
#         if dname and pname and date and time:
#             try:
#                 doctor = Doctor.objects.get(id=dname)
#                 patient = Patient.objects.get(id=pname)
#                 Appointment.objects.create(
#                     doctor = dname,
#                     patient = pname,
#                     date = date,
#                     time = time
#                 )
#                 print("Data Saved")
#                 return redirect('apt_page')
#             except Doctor.DoesNotExist:
#                 error = "Doctor not found!"
#             except Patient.DoesNotExist:
#                 error = "Patient not found!"
#             except ValueError:
#                 error = "Invalid Data Provided"
#         else:
#             error = "All fields are required!"
#     return render(request, 'add_apt.html', {'doctor': doctor, 'patient': patient})

def add_apt(request):
    error = None

    if request.method == 'POST':
        print("Form Submitted")
        dname = request.POST.get('dname')  # Doctor name as string
        pname = request.POST.get('pname')  # Patient name as string
        date = request.POST.get('date')
        time = request.POST.get('time')

        if dname and pname and date and time:
            try:
                doctor = Doctor.objects.get(name__iexact=dname)
                patient = Patient.objects.get(name__iexact=pname)
                Appointment.objects.create(
                    doctor=doctor,
                    patient=patient,
                    date=date,
                    time=time
                )
                print("Data Saved")
                return redirect('apt_page')
            except Doctor.DoesNotExist:
                error = f"No doctor found with name '{dname}'"
            except Patient.DoesNotExist:
                error = f"No patient found with name '{pname}'"
            except ValueError:
                error = "Invalid data provided"
        else:
            error = "All fields are required!"

    return render(request, 'add_apt.html', {'error': error})


def view_apt(request):
    all_data = Appointment.objects.all()
    return render(request, 'view_apt.html', {'data':all_data})

def del_apt(request, apt_id):
    apt = get_object_or_404(Appointment, id = apt_id)
    apt.delete()
    print("Appointment Deleted Successfully")
    return redirect('view_apt')

# def update_apt(request, apt_id):
#     apt = get_object_or_404(Appointment, id = apt_id)
#     if request.method == 'POST':
#         apt.dname = request.POST.get('dname')
#         apt.pname = request.POST.get('pname')
#         apt.date = request.POST.get('date')
#         apt.time = request.POST.get('time')
#         apt.save()
#         return redirect('view_apt')
#     return render(request, 'update_apt.html', {'apt': apt})

def update_apt(request, apt_id):
    apt = get_object_or_404(Appointment, id=apt_id)

    if request.method == 'POST':
        # Get doctor/patient by ID from form
        doctor_id = request.POST.get('doctor')
        patient_id = request.POST.get('patient')

        # Update relationship fields using IDs
        apt.doctor = Doctor.objects.get(id=doctor_id)
        apt.patient = Patient.objects.get(id=patient_id)

        # Update date/time
        apt.date = request.POST.get('date')
        apt.time = request.POST.get('time')

        apt.save()
        return redirect('view_apt')

    return render(request, 'update_apt.html', {
        'apt': apt,
        'doctors': Doctor.objects.all(),
        'patients': Patient.objects.all()
    })