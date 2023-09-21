# accounts/urls.py
from django.urls import path
from accounts.views import UserRegistrationView, UserLoginView, UserProfileView, VerifyEmailView, UserLogoutView, UserDeleteView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('delete/', UserDeleteView.as_view(), name='user-delete'),

]
