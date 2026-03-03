import jwt
from django.conf import settings
from datetime import datetime, timedelta
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from .models import User,  PetRequest
from .serializers import UserSerializer,PetRequestSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminUserRole
import uuid


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PetRequestViewSet(viewsets.ModelViewSet):
    serializer_class = PetRequestSerializer

    def get_queryset(self):
        user = self.request.user

        # Admin sees all
        if user.is_authenticated and user.role == "Admin":
            return PetRequest.objects.all()

        # Public sees only accepted
        return PetRequest.objects.filter(status="Accepted")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAdminUserRole()]
        elif self.action == 'create':
            return [IsAuthenticated()]
        return []


@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {"success": False, "message": "Invalid email"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if check_password(password, user.password):

        payload = {
            "user_id": user.id,
            "email": user.email,
            "role": user.role,
            "exp": datetime.utcnow() + timedelta(hours=1),
            "iat": datetime.utcnow()
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

        return Response({
            "success": True,
            "message": "Login successful",
            "access_token": token
        })

    return Response(
        {"success": False, "message": "Invalid password"},
        status=status.HTTP_400_BAD_REQUEST
    )