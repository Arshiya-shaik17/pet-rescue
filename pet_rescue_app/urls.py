from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, PetRequestViewSet, login_view

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'pet-requests', PetRequestViewSet)

urlpatterns = router.urls + [
    path('login/', login_view),
]