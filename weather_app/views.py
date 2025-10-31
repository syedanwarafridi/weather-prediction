from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from .models import CustomUser, PredictionRequest
from .serializers import UserRegistrationSerializer
import requests
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.permissions import AllowAny


def home_view(request):
    """Render the main HTML page with all forms"""
    return render(request, 'weather_app/home.html')

class RegisterView(APIView):
    """Handle user registration"""
    permission_classes = [AllowAny] 
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        """Handle GET request for registration form"""
        return Response({
            "message": "Send POST request with email, username, and password for registration"
        })
@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    """Handle user login"""
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)  # Create session for the user
            return Response({
                "message": "Login successful",
                "user": {
                    "email": user.email,
                    "username": user.username
                }
            })
        else:
            return Response({"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
    def get(self, request):
        """Handle GET request for login form"""
        return Response({
            "message": "Send POST request with email and password for login"
        })
        
@method_decorator(csrf_exempt, name='dispatch')
class WeatherPredictionView(APIView):
    """Handle weather prediction requests"""
    permission_classes = [IsAuthenticated]  # Ensure user is logged in

    def post(self, request):
        location = request.data.get('location')
        
        if not location:
            return Response({"error": "Location is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Simple geocoding - in production, use a proper geocoding service
        location_coordinates = {
            "london,uk": {"lat": 51.5074, "lon": -0.1278},
            "new york,us": {"lat": 40.7128, "lon": -74.0060},
            "tokyo,jp": {"lat": 35.6762, "lon": 139.6503},
            "paris,fr": {"lat": 48.8566, "lon": 2.3522},
            "delhi,in": {"lat": 28.6139, "lon": 77.2090},
            "mumbai,in": {"lat": 19.0760, "lon": 72.8777},
            "sydney,au": {"lat": -33.8688, "lon": 151.2093},
        }

        # Get coordinates for the location (default to London if not found)
        location_lower = location.lower()
        if location_lower in location_coordinates:
            latitude = location_coordinates[location_lower]["lat"]
            longitude = location_coordinates[location_lower]["lon"]
        else:
            # Default to London if location not in our simple database
            latitude = 51.5074
            longitude = -0.1278

        # Build the API URL for Open-Meteo
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'hourly': 'precipitation_probability,temperature_2m,relative_humidity_2m',
            'daily': 'precipitation_probability_max',
            'timezone': 'auto',
            'forecast_days': 1
        }

        # Make the request to the weather API
        try:
            api_response = requests.get(url, params=params)
            weather_data = api_response.json()
            
            # Check if API returned an error
            if 'error' in weather_data:
                return Response({
                    "error": f"Weather API error: {weather_data['error']}"
                }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
                
        except requests.exceptions.RequestException as e:
            return Response({
                "error": f"Failed to fetch weather data: {str(e)}"
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        # Save the prediction request to the database
        PredictionRequest.objects.create(
            user=request.user,
            location=location
        )

        if 'hourly' in weather_data and 'time' in weather_data['hourly']:
            current_time = weather_data['hourly']['time'][0]
            current_temp = weather_data['hourly']['temperature_2m'][0]
            current_humidity = weather_data['hourly']['relative_humidity_2m'][0]
            current_precipitation = weather_data['hourly']['precipitation_probability'][0]
            
            formatted_response = {
                "location": location,
                "coordinates": f"{latitude}, {longitude}",
                "current_weather": {
                    "time": current_time,
                    "temperature": f"{current_temp}°C",
                    "humidity": f"{current_humidity}%",
                    "precipitation_probability": f"{current_precipitation}%"
                },
                "today_max_precipitation": f"{weather_data['daily']['precipitation_probability_max'][0]}%",
                "raw_data": weather_data  # Include full data for debugging
            }
        else:
            formatted_response = {
                "location": location,
                "message": "Weather data available but in different format",
                "raw_data": weather_data
            }

        return Response(formatted_response)
    
    def get(self, request):
        """Handle GET request - show user's prediction history"""
        user_predictions = PredictionRequest.objects.filter(user=request.user).order_by('-date_requested')[:10]
        
        prediction_history = []
        for prediction in user_predictions:
            prediction_history.append({
                "location": prediction.location,
                "date_requested": prediction.date_requested.strftime("%Y-%m-%d %H:%M:%S")
            })
        
        return Response({
            "message": f"Welcome {request.user.username}",
            "prediction_history": prediction_history,
            "instructions": "Send POST request with 'location' parameter to get weather prediction"
        })

class UserProfileView(APIView):
    """Get current user profile"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({
            "user": {
                "email": request.user.email,
                "username": request.user.username,
                "is_active": request.user.is_active
            }
        })

class LogoutView(APIView):
    """Handle user logout"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        from django.contrib.auth import logout
        logout(request)
        return Response({"message": "Logout successful"})
    
    def get(self, request):
        return Response({
            "message": "Send POST request to logout"
        })