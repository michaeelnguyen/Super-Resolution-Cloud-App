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
    # View to display the application homepage
    # If the user has an account, retrieve the respective user's information
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
    # View to register an account for the customer
    # After the POST method, obtain the user account information using CreateUserForm()
    # to create an customer user account.
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            #role = request.POST.get('role')            
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was create for ' + username)
            return redirect('login')
        
    context = {'form': form}
    return render(request, 'register.html', context)

@unauthenticated_user
def loginPage(request):
    # After POST method, retrieve user credentials and authenticate login
    # On successful login, redirect to the dashboard page
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
    # Admin permission to register an employee using the employee registration page.
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
    # Admin permission to allow employee to login with their user credentials
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

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer', 'employee', 'admin'])
def profilePage(request, pk):
    # Retrieve and display a certain customer's profile using CustomerForm
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
    # View to display embedded metrics from grafana dashboard
    context = {}
    return render(request, 'dashboard.html', context)

def logoutUser(request):
    # View to allow the user to logout of the application
    logout(request)
    return redirect('home')

