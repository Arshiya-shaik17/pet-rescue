from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

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