from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserProfileSerializer, UserSerializer
from .models import CustomUser

# Allow anyone to register
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {'message': 'User registered successfully.', 'data': serializer.data},
            status=status.HTTP_201_CREATED
        )
    return Response(
        {'error': 'Invalid data.', 'details': serializer.errors},
        status=status.HTTP_400_BAD_REQUEST
    )

# Allow anyone to login
@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    username_or_email = request.data.get('username')
    password = request.data.get('password')

    if not username_or_email or not password:
        return Response(
            {'error': 'Username/email and password are required.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = None
    if '@' in username_or_email:
        # Try to find user by email
        try:
            user_obj = CustomUser.objects.get(email=username_or_email)
            user = authenticate(username=user_obj.username, password=password)
        except CustomUser.DoesNotExist:
            user = None
    else:
        # Try to authenticate by username
        user = authenticate(username=username_or_email, password=password)

    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {'token': token.key, 'message': 'Login successful.'},
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            {'error': 'Invalid credentials. Please check your username/email and password.'},
            status=status.HTTP_401_UNAUTHORIZED
        )

# Logout requires authentication
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    try:
        if hasattr(request.user, 'auth_token'):
            request.user.auth_token.delete()
            return Response(
                {'message': 'Successfully logged out.'},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': 'No token found for this user.'},
                status=status.HTTP_400_BAD_REQUEST
            )
    except Exception as e:
        return Response(
            {'error': 'An error occurred during logout.', 'details': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# Profile - get and update
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user

    if request.method == 'GET':
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile updated successfully.', 'data': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
