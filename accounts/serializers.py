from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import CustomUser
import re
from favorite.serializers import FavoriteSerializer


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    full_name = serializers.CharField(write_only=True)
    profile_picture = serializers.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ['profile_picture', 'username', 'email', 'phone_number', 'full_name', 'password', 'confirm_password', 'street', 'barangay', 'bio']
        extra_kwargs = {'password': {'write_only': True}}


    def validate_username(self, value):
        # Check if the username is already taken
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken. Please choose a different one.")
        return value


    def validate_email(self, value):
        # Check if the email is already registered
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered. Please use a different email.")
        return value

    def validate_phone_number(self, value):
        if value:  # Only validate if phone is given
            # Accept either 0917... or +63917...
            pattern = r'^(09\d{9}|\+639\d{9})$'
            if not re.match(pattern, value):
                raise serializers.ValidationError(
                    "Phone number must start with '09' or '+639' and be 11 or 13 digits long."
                )
        return value

    def validate_password(self, value):
        # Validate password strength
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value

    def validate(self, data):
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Passwords do not match.")
        return data
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')

        # Handle full_name splitting
        full_name = validated_data.pop('full_name')
        names = full_name.strip().split(' ', 1)
        first_name = names[0]
        last_name = names[1] if len(names) > 1 else ''

        # Normalize Philippine phone number if needed
        phone = validated_data.get('phone_number')
        if phone and phone.startswith('09'):
            validated_data['phone_number'] = '+63' + phone[1:]

        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=first_name,
            last_name=last_name,
            phone_number=validated_data.get('phone_number', ''),
            street=validated_data.get('street', ''),
            barangay=validated_data.get('barangay', ''),
            bio=validated_data.get('bio', '')
        )
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    favorites = FavoriteSerializer(many=True, read_only=True, source='favorites')
    class Meta:
        model = CustomUser
        fields = ['profile_picture', 'first_name', 'last_name', 'email', 'phone_number', 'bio', 'favorites']




