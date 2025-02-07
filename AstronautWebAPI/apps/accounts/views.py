from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login
from .serializers import RegisterationSerializer, LoginSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework_simplejwt.views import TokenRefreshView

#Register View
@extend_schema(
    request=RegisterationSerializer,
    responses={201: {"message": "User created successfully"}},
    summary="Registration",
    description="Endpoint for user registration.",
    tags=["SignIn/SignUp"]
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = RegisterationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login View
@extend_schema(
    request=LoginSerializer,
    responses={
        200: {"message": "Logged in successfully"},
        401: {"error": "Invalid credentials"}
    },
    summary="Login",
    description="Endpoint for user signin.",
    tags=["SignIn/SignUp"]
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    # Validate request data using the serializer
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return Response({"message": "Logged in successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        # Return validation errors if the request data is not valid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims if needed
        token['email'] = user.email
        return token

    def validate(self, attrs):
        # 'username' here expects the USERNAME_FIELD, so pass 'email' from request
        # if you want to rename it, you can override more extensively.
        return super().validate(attrs)


@extend_schema_view(
    post=extend_schema(
        tags=["Authentication"],
        summary="Obtain JWT Token",
        description="Endpoint to obtain a access token by providing valid credentials."
    )
)
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@extend_schema_view(
    post=extend_schema(
        tags=["Authentication"],
        summary="Refresh Jwt Token",
        description="Endpoint to refresh jwt token using a referesh token."
    )
)
class MyTokenRefreshView(TokenRefreshView):
    pass

