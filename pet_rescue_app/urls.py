from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, PetRequestViewSet, login_view,
    AdminApprovalView, search_pets, public_pets, me,
    my_notifications, mark_notification_read,
    profile, change_password, delete_account
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'pet-requests', PetRequestViewSet)

urlpatterns = [
    path('login/', login_view),
    path('me/', me),
    path('profile/', profile),                                    # 👤
    path('change-password/', change_password),                    # 🔑
    path('delete-account/', delete_account),                      # ❌
    path('admin/approve/<int:pk>/', AdminApprovalView.as_view()),
    path('search/', search_pets),
    path('public-pets/', public_pets),
    path('notifications/', my_notifications),
    path('notifications/<int:pk>/read/', mark_notification_read),
    path('', include(router.urls)),
]