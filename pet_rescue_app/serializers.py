from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import User, PetRequest


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password',
            'phone',
            'address',
            'city',
            'role',
            'created_at'
        ]

    def create(self, validated_data):
        # Hash password before saving
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Hash password only if it is being updated
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)

    def validate_phone(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        if len(value) < 10:
            raise serializers.ValidationError("Phone number must be at least 10 digits.")
        return value
    
    password = serializers.CharField(
    write_only=True,
    style={'input_type': 'password'}
    )
    
class PetRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = PetRequest
        fields = '__all__'