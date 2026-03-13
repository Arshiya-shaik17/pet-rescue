from rest_framework import serializers
from .models import User, PetRequest


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class PetRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetRequest
        fields = '__all__'
        read_only_fields = ['user', 'status', 'created_at']  # ✅ user & status are auto-set


class AdminPetRequestSerializer(serializers.ModelSerializer):
    """Only admin can update status using this serializer"""
    class Meta:
        model = PetRequest
        fields = ['id', 'status']  # admin can only change status