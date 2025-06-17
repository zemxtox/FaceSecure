from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from accounts import views as accounts_views
from django.contrib.auth import views as auth_views
from detection.views import start_streams
from cameras.views import add_camera
from rest_framework.routers import DefaultRouter
from cameras.views import CameraViewSet

router = DefaultRouter()
router.register(r'cameras', CameraViewSet, basename='camera')

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('signup/', accounts_views.signup_view, name='signup'),
    path('dashboard/', start_streams, name='dashboard'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/cameras/', include('cameras.urls')),
    path('api/faces/', include('faces.urls')),
    path('api/detection/', include('detection.urls')),
    path('cameras/add/', add_camera, name='add_camera'),
    path('api/', include(router.urls)),
    path('faces/', include('faces.urls')),  # Add this if not present
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)