from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'booking/home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'booking/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'booking/login.html', {'error': 'Invalid username or password'})
    return render(request, 'booking/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')
from .models import Service, Appointment
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def service_list(request):
    services = Service.objects.all()
    return render(request, 'booking/service_list.html', {'services': services})

@login_required
def book_appointment(request, service_id):
    service = Service.objects.get(id=service_id)

    if request.method == 'POST':
        date = request.POST['date']
        time = request.POST['time']

        conflict = Appointment.objects.filter(date=date, time=time).exists()
        if conflict:
            messages.error(request, 'That time slot is already booked. Please choose another time.')
        else:
            Appointment.objects.create(
                customer=request.user,
                service=service,
                date=date,
                time=time
            )
            messages.success(request, 'Appointment booked successfully!')
            return redirect('my_appointments')

    return render(request, 'booking/book_appointment.html', {'service': service})

@login_required
def my_appointments(request):
    appointments = Appointment.objects.filter(customer=request.user).order_by('date', 'time')
    return render(request, 'booking/my_appointments.html', {'appointments': appointments})
from django.shortcuts import get_object_or_404

@login_required
def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, customer=request.user)

    if request.method == 'POST':
        date = request.POST['date']
        time = request.POST['time']

        conflict = Appointment.objects.filter(date=date, time=time).exclude(id=appointment.id).exists()
        if conflict:
            messages.error(request, 'That time slot is already booked. Please choose another time.')
        else:
            appointment.date = date
            appointment.time = time
            appointment.save()
            messages.success(request, 'Appointment updated successfully!')
            return redirect('my_appointments')

    return render(request, 'booking/edit_appointment.html', {'appointment': appointment})

@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, customer=request.user)
    appointment.status = 'cancelled'
    appointment.save()
    messages.success(request, 'Appointment cancelled.')
    return redirect('my_appointments')

