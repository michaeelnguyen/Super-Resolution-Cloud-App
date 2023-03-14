from django.urls import path
from . import views

urlpatterns = [
    path('gallery/<str:pk>/', views.galleryPage, name="gallery"),
    path('upload/<str:pk>/', views.uploadPage, name="upload"),
    path('view/<str:pk>/', views.viewImg, name='photo'),
    path('remove/<str:pk>/', views.deleteImg, name='remove'),
    path('update/<str:pk>/', views.updateImg, name='update'),
    path('settings/<str:pk>/', views.handle_category, name='handle_category'),
]

