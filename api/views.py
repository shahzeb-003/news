from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST

@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/login')
    else:
        form = CustomUserCreationForm()

    
    return render(request, 'register.html', {'form': form})


# This can be changed with LoginView in urls.py

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # This logs the user in and sets the session cookie
            return redirect('http://localhost:5173/')
        else:
            return JsonResponse({'error': 'Invalid login credentials'}, status=400)
    return render(request, 'login.html')


@require_POST
@csrf_exempt
def logout_view(request):
    logout(request)
    request.session.flush()
    print(f'User logged out. User is_authenticated: {request.user.is_authenticated}')
    return JsonResponse({'status': 'logged out'})


@never_cache
def check_authentication(request):
    if request.user.is_authenticated:
        return JsonResponse({'isAuthenticated': True}, status=200)
    else:
        return JsonResponse({'isAuthenticated': False}, status=401)

from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required

@csrf_exempt
def get_user_details(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        user = request.user
        data = {
            'email': user.email,
            'date_of_birth': user.date_of_birth.strftime('%Y-%m-%d') if user.date_of_birth else None,
            'profile_image': user.profile_image.url if user.profile_image else None
        }
        return JsonResponse(data)
    else:
        # If user is not authenticated, return an appropriate response
        return JsonResponse({'error': 'User is not authenticated'})


from django.views.decorators.http import require_http_methods
from .forms import CustomUserChangeForm  # You need to create this form

@login_required
@require_http_methods(["POST"])
@csrf_exempt
def update_user_details(request):
    user = request.user
    form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': 'success'}, status=200)
    else:
        return JsonResponse(form.errors, status=400)