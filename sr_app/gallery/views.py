import base64
import io
import json
import math
import os
import uuid
from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404, HttpResponse
from django.http import JsonResponse
from django.core.files.base import ContentFile

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
import requests
from gallery.forms import PhotoForm

from accounts.decorators import allowed_users, unauthenticated_user, admin_only
from accounts.models import Customer
from gallery.models import Category, Photo, SRPhoto, get_user_directory_path
from PIL import Image

# Create your views here.
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer', 'employee', 'admin'])
def galleryPage(request, pk):
    user = request.user
    context = {'user': user}
    if request.user.is_authenticated and not request.user.is_staff:
        customer = request.user.customer

        user_media_path = settings.USER_MEDIA_STORAGE.path('')
        customer_uuid_path = get_user_directory_path(instance=user, filename='')
        customer_media_path = os.path.join(user_media_path, customer_uuid_path)
        
        category = request.GET.get('category')
        if category == "All":
            photos = SRPhoto.objects.filter(user=user)
        else:
            photos = SRPhoto.objects.filter(category__name=category, user=user) 
        
        if 'category' not in request.GET:
            # Build the redirect URL with 'category=All'
            redirect_url = reverse('gallery', kwargs={'pk': request.user.pk}) + '?category=All'
            return redirect(redirect_url)
        
        categories = Category.objects.all()
        context = {'categories': categories, 'customer': customer, 'customer_media_path': customer_media_path, 'photos': photos}
    elif request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        category = request.GET.get('category')
        if category == "All":
            photos = Photo.objects.filter(user=user) # Only retrieve photos for the current user
        else:
            photos = Photo.objects.filter(category__name=category, user=user)

        if 'category' not in request.GET:
            # Build the redirect URL with 'category=All'
            redirect_url = reverse('gallery', kwargs={'pk': request.user.pk}) + '?category=All'
            return redirect(redirect_url)

        categories = Category.objects.all()
        context = {'categories': categories, 'photos': photos}
        
    return render(request, 'gallery.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer', 'employee', 'admin'])
def uploadPage(request, pk):
    categories = Category.objects.all()
    context = {'categories': categories}
    
    user = request.user
    if request.user.is_authenticated and not request.user.is_staff:
        customer = request.user.customer
        context = {'categories': categories, 'user': user, 'customer': customer}
    
    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')

        model_chosen = data.get('model-chosen', '')
        print(model_chosen)
        
        if model_chosen == '':
            messages.info(request, 'Please select model before uploading!')
            return render(request, 'upload.html', context)
        
        if data['category'] != "":
            category = Category.objects.get(id=data['category'])
        elif data['category_custom'] != "":
            category, created = Category.objects.get_or_create(name=data['category_custom'], user=user)
        else:
            category = None
        
        for image in images:
            print(image)
            # Make API request to TorchServe model based on model_chosen value
            if model_chosen == 'realesrgan':
                model_name = 'realESRGAN'
            elif model_chosen == 'swinir':
                model_name = 'swinIR'
            else:
                messages.info(request, 'Invalid model selected!')
                return render(request, 'upload.html', context)

            # Construct the inference API request
            url = f'http://host.docker.internal:8080/predictions/{model_name}'
            files = {'data': image.read()}

            # Send the inference API request and get the response
            response = requests.post(url, files=files)

            # Deserialize the JSON response
            response_data = response.json()

            # Retrieve the result and score fields from the response data
            img = response_data.get('result')
            niqe_old = response_data.get('niqe_old')
            niqe_new = response_data.get('niqe_new')
            brisque_old = response_data.get('brisque_old')
            brisque_new = response_data.get('brisque_new')

            if response.status_code == 200:
                img_bytes = base64.b64decode(img)

                # Create Photo Object with the corresponding field values
                photo = Photo.objects.create(
                    user=user,
                    image=image,
                    category=category,
                    description=data['description'],
                    niqe=niqe_old,
                    brisque=brisque_old,
                )
                photo.save()

                # Create SRPhoto Object after inference on uploaded image
                sr_photo = SRPhoto.objects.create(
                    user=user,
                    original_photo=photo,
                    image= ContentFile(img_bytes),
                    model_chosen=data.get('model-chosen'),
                    niqe=niqe_new,
                    brisque=brisque_new,
                )
                sr_photo.save()
            else:
                messages.error(request, 'Error making API request to TorchServe model!')

        messages.success(request, 'Upload successful!')
        return redirect(reverse('gallery', kwargs={'pk': request.user.pk}) + '?category=All')
        
    context = {'categories': categories, 'user': user}
    return render(request, 'upload.html', context)

@login_required(login_url='login')
def viewImg(request, pk):
    photo = Photo.objects.get(id=pk)
    srphoto = SRPhoto.objects.get(original_photo=photo)
    try:
        img_path = os.path.join(settings.MEDIA_ROOT, str(photo.image))
        img = Image.open(img_path)
        img_path_sr = os.path.join(settings.MEDIA_ROOT, str(srphoto.image))
        img_sr = Image.open(img_path_sr)
    except IOError:
        raise Http404("Image does not exist")
    
    width, height = img.size
    color_mode = img.mode
    file_format = img.format
    file_size = math.ceil(os.path.getsize(img_path) / 1000)

    sr_file_format = img_sr.format
    sr_file_size = math.ceil(os.path.getsize(img_path_sr) / 1000)
    img.close()
    img_sr.close()

    context = {'photo': photo, 'srphoto': srphoto, 'color_mode': color_mode, 'file_format': file_format, 'file_size': file_size, 'sr_file_format': sr_file_format, 'sr_file_size': sr_file_size, 'height': height, 'width': width}
    return render(request, 'viewPhoto.html', context)

@login_required(login_url='login')
def deleteImg(request, pk):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        photo_ids = request.POST.get('photo_ids').split(',')
        for photo_id in photo_ids:
            try:
                photo = Photo.objects.get(id=photo_id)
                sr_photo = SRPhoto.objects.get(original_photo=photo)
                if photo.user == request.user and sr_photo.user == request.user:
                    photo.delete()
                    sr_photo.delete()
                else:
                    return JsonResponse({'success': False, 'message': 'You do not have permission to delete this photo.'})
            except Photo.DoesNotExist:
                pass
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@login_required(login_url='login')
def updateImg(request, pk):
    context = {}
    if request.user.is_authenticated:
        user = request.user
        photo = Photo.objects.get(id=pk, user=user)
        form = PhotoForm(instance=photo, user=user)
        if request.method == 'POST':
            form = PhotoForm(request.POST, instance=photo, user=user)
            if form.is_valid():
                form.save()
                return redirect('photo', pk=pk)
        context = {'photo': photo, 'form': form}
    return render(request, 'update.html', context)

@login_required(login_url='login')
def handle_category(request, pk):
    user = request.user
    categories = Category.objects.filter(user=user)
    if request.user.is_authenticated and not request.user.is_staff:
        customer = request.user.customer
        context = {'categories': categories, 'customer': customer}
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            category_name = request.POST['category_name']
            category, created = Category.objects.get_or_create(name=category_name, user=user)
            if not created:
                messages.info(request, "Category already exists!")
                return redirect('handle_category', category.id)
            
            messages.success(request, "Category added successfully!")
            return redirect('handle_category', category.id)
        elif action == 'update':
            data = request.POST
            if data['category'] != "" and data['category_name_new'] != "":
                category, created = Category.objects.get_or_create(id=data['category'], user=user)
                if category.name == data['category_name_new']:
                    messages.info(request, "Category already exists!")
                    return redirect('handle_category', data['category'])

                category.name = data['category_name_new']
                category.save()
                messages.success(request, "Category updated successfully!")
                return redirect('handle_category', category.id)
            else:
                messages.info(request, "Please provide both the category and new name!")
                return redirect('handle_category', data['category'])
        elif action == 'delete':
            category = Category.objects.get(pk=pk)
            category.delete()

    context = {'categories': categories, 'user': user}
    return render(request, 'settings.html', context)


        
