from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, PetRequestViewSet, login_view,
    AdminApprovalView, search_pets, public_pets, me  # ✅ added me
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'pet-requests', PetRequestViewSet)

urlpatterns = [
    path('login/', login_view),
    path('me/', me),                                       # ✅ added
    path('admin/approve/<int:pk>/', AdminApprovalView.as_view()),
    path('search/', search_pets),
    path('public-pets/', public_pets),
    path('', include(router.urls)),
]