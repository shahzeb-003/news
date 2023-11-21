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
from django.contrib.auth.decorators import login_required

@csrf_exempt
def get_user_details(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        user = request.user
        data = {
            'email': user.email,
            'date_of_birth': user.date_of_birth.strftime('%Y-%m-%d') if user.date_of_birth else None,
            'profile_image': user.profile_image.url if user.profile_image else None,
            'favorite_category' : user.favorite_category
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
    
from django.http import JsonResponse
from .models import News

@csrf_exempt
@login_required
def get_news_by_category(request, category):
    news_items = News.objects.filter(category=category)
    data = [{"id": item.id, "title": item.title, "text": item.text} for item in news_items]
    return JsonResponse(data, safe=False)

@csrf_exempt
def get_favorite_category(request):

    if request.user.is_authenticated:
        user = request.user
        data = {
            'favorite_category' : user.favorite_category
        }
        return JsonResponse(data)
    else:
        # If user is not authenticated, return an appropriate response
        return JsonResponse({'error': 'User is not authenticated'})
    
from django.http import JsonResponse
from .models import News, Comment


@csrf_exempt
def get_comments(request, news_id):
    try:
        news = News.objects.get(id=news_id)
        comments = Comment.objects.filter(news=news, parent=None).order_by('-created_at')  # Fetch top-level comments

        def get_replies(comment):
            replies = comment.replies.order_by('-created_at')
            return [{'id': reply.id, 'author_email': reply.author.email, 'text': reply.text, 'created_at': reply.created_at, 'replies': get_replies(reply)} for reply in replies]

        data = [{'id': comment.id, 'author_email': comment.author.email, 'text': comment.text, 'created_at': comment.created_at, 'replies': get_replies(comment)} for comment in comments]
        return JsonResponse(data, safe=False)
    except News.DoesNotExist:
        return JsonResponse({'error': 'News item not found'}, status=404)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
import json


@login_required
@csrf_exempt
def submit_comment(request, news_id):
    try:
        news = News.objects.get(id=news_id)
        data = json.loads(request.body)
        comment_text = data.get('text')
        parent_id = data.get('parent_id')  # ID of the parent comment, if replying to a comment

        if not comment_text:
            return JsonResponse({'error': 'No text provided'}, status=400)

        parent_comment = None
        if parent_id:
            try:
                parent_comment = Comment.objects.get(id=parent_id, news=news)  # Ensure the parent comment belongs to the same news item
            except Comment.DoesNotExist:
                return JsonResponse({'error': 'Parent comment not found'}, status=404)

        Comment.objects.create(news=news, author=request.user, text=comment_text, parent=parent_comment)
        return JsonResponse({'status': 'Comment added successfully'})
    except News.DoesNotExist:
        return JsonResponse({'error': 'News item not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
