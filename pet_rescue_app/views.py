from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status as drf_status

from .models import User, PetRequest
from .serializers import UserSerializer, PetRequestSerializer, AdminPetRequestSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PetRequestViewSet(viewsets.ModelViewSet):
    queryset = PetRequest.objects.all()
    serializer_class = PetRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # automatically attach logged-in user
        serializer.save(user=self.request.user)

    def get_queryset(self):
        # regular users only see their own requests
        if self.request.user.is_staff:
            return PetRequest.objects.all()
        return PetRequest.objects.filter(user=self.request.user)


class AdminApprovalView(APIView):
    """Only admin can access this view to accept/reject requests"""
    permission_classes = [IsAdminUser]

    def patch(self, request, pk):
        try:
            pet_request = PetRequest.objects.get(pk=pk)
        except PetRequest.DoesNotExist:
            return Response(
                {"error": "Pet request not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        new_status = request.data.get('status')

        if new_status not in ['Accepted', 'Rejected']:
            return Response(
                {"error": "Status must be 'Accepted' or 'Rejected'"},
                status=status.HTTP_400_BAD_REQUEST
            )

        pet_request.status = new_status
        pet_request.save()

        return Response({
            "message": f"Pet request {new_status} successfully",
            "id": pet_request.id,
            "status": pet_request.status
        }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get("email")
    password = request.data.get("password")

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"message": "Invalid email"}, status=401)

    if not user.check_password(password):
        return Response({"message": "Invalid password"}, status=401)

    refresh = RefreshToken.for_user(user)

    return Response({
        "access": str(refresh.access_token),
        "refresh": str(refresh)
    })





@api_view(['GET'])
@permission_classes([AllowAny])
def search_pets(request):
    queryset = PetRequest.objects.filter(status='Accepted')

    pet_type = request.query_params.get('pet_type', None)
    breed = request.query_params.get('breed', None)
    color = request.query_params.get('color', None)
    location = request.query_params.get('location', None)
    request_type = request.query_params.get('request_type', None)

    if pet_type:
        queryset = queryset.filter(pet_type__icontains=pet_type)
    if breed:
        queryset = queryset.filter(breed__icontains=breed)
    if color:
        queryset = queryset.filter(color__icontains=color)
    if location:
        queryset = queryset.filter(location__icontains=location)
    if request_type:
        queryset = queryset.filter(request_type__icontains=request_type)

    serializer = PetRequestSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def public_pets(request):
    accepted_pets = PetRequest.objects.filter(status='Accepted')
    serializer = PetRequestSerializer(accepted_pets, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    return Response({
        "id": request.user.id,
        "email": request.user.email,
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "is_staff": request.user.is_staff,
    })