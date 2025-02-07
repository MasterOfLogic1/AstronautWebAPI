from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView  # <-- Add this import
from .views import login_view,register_view,MyTokenObtainPairView,MyTokenRefreshView

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
]

