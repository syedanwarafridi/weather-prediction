from django.urls import path
from .views import RegisterView, LoginView, WeatherPredictionView, home_view, UserProfileView, LogoutView

urlpatterns = [
    path('', home_view, name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('predict/', WeatherPredictionView.as_view(), name='predict'),
    path('profile/', UserProfileView.as_view(), name='profile'),
]