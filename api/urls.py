from django.urls import path
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

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)