from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, PetRequestViewSet, login_view, AdminApprovalView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'pet-requests', PetRequestViewSet)

urlpatterns = [
    path('login/', login_view),
    path('admin/approve/<int:pk>/', AdminApprovalView.as_view()),  # ✅ admin approval
    path('', include(router.urls)),
]