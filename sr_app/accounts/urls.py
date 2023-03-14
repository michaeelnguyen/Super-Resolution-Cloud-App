from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePage, name="home"),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('register/employee/', views.empRegisterPage, name='register_emp'),
    path('login/employee/', views.empLoginPage, name='login_emp'),
    path('profile/<str:pk>/', views.profilePage, name="profile"),
    path('dashboard/', views.metrics_dashboard, name="dashboard"),
    path('logout/', views.logoutUser, name="logout"),
]
