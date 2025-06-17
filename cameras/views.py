from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Camera
from .forms import CameraForm
from .serializers import CameraSerializer

@login_required
def add_camera(request):
    if request.method == 'POST':
        form = CameraForm(request.POST)
        if form.is_valid():
            camera = form.save(commit=False)
            camera.user = request.user
            camera.save()
            return redirect('dashboard')
    else:
        form = CameraForm()
    return render(request, 'add_camera.html', {'form': form})

class CameraViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CameraSerializer

    def get_queryset(self):
        return Camera.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)