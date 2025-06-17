from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FaceViewSet, add_face

router = DefaultRouter()
router.register(r'', FaceViewSet, basename='face')

urlpatterns = [
    path('add/', add_face, name='add_face'),
    path('', include(router.urls)),
]