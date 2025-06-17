from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FaceViewSet

router = DefaultRouter()
router.register(r'', FaceViewSet, basename='face')

urlpatterns = [
    path('', include(router.urls)),
]