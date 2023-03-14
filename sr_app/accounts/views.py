import uuid
from django.shortcuts import redirect, render
from django.http import HttpResponse

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import UserCreationForm

from accounts.models import *
from .decorators import allowed_users, unauthenticated_user, admin_only
from .forms import CreateUserForm, CustomerForm

# Create your views here.

def homePage(request):
    if request.user.is_authenticated and not request.user.is_staff:
        customer = request.user.customer
        context = {'customer': customer}
    elif request.user.is_authenticated and request.user.is_superuser:
        user = request.user
        context = {'user': user}
    else:
        context = {}
    return render(request, 'home.html', context)

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = request.POST.get('role')            
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was create for ' + username)
            return redirect('login')
        
    context = {'form': form}
    return render(request, 'register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'Username and/or Password is incorrect')

    context = {}
    return render(request, 'login.html', context)

@allowed_users(allowed_roles=['employee', 'admin'])
@admin_only
def empRegisterPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            employee = Employee.objects.create(
                user=user, 
                uuid=uuid.uuid4(),
                is_staff=True,
            )
            employee.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was create for ' + username)
            return redirect('login_emp')
        
    context = {'form': form}
    return render(request, 'register_emp.html', context)

@allowed_users(allowed_roles=['employee', 'admin'])
@admin_only
def empLoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'Username and/or Password is incorrect')

    context = {}
    return render(request, 'login_emp.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer', 'employee', 'admin'])
def profilePage(request, pk):
    user = request.user
    form = CustomerForm()
    if request.user.is_authenticated and not request.user.is_staff:
        customer = request.user.customer

        form = CustomerForm(instance=customer)
        if request.method == 'POST':
            form = CustomerForm(request.POST, instance=customer)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile Settings updated successfully!')
                return redirect('profile', pk=request.user.customer.pk)

    context = {'user': user, 'form': form}
    return render(request, 'profile.html', context)

@login_required(login_url='login')
@admin_only
def metrics_dashboard(request):
    context = {}
    return render(request, 'dashboard.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

