from django.urls import path, re_path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static

#LoginView.as_view(redirect_authenticated_user = True)

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', LoginView.as_view(redirect_authenticated_user = True), name='login'),
    path('api/logout/', views.logout_view, name='logout'),
    path('api/check-authentication/', views.check_authentication, name='check-authentication'),
    path('api/user-details/', views.get_user_details, name='user-details'),
    path('api/update-user-details/', views.update_user_details, name='update_user_details'),
    path('api/news/<str:category>/', views.get_news_by_category, name='get_news_by_category'),
    path('api/news/<int:news_id>/comments/', views.get_comments, name='get_comments'),
    path('api/news/<int:news_id>/submit-comment/', views.submit_comment, name='submit_comment'),
    path('api/edit-comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('api/delete-comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('', views.main_spa, name='spa'),
    path('profile/', views.main_spa, name='spa profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)