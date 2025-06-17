from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import FaceForm
from .models import Face
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import FaceSerializer

@login_required
def add_face(request):
    if request.method == 'POST':
        form = FaceForm(request.POST, request.FILES)
        if form.is_valid():
            face = form.save(commit=False)
            face.user = request.user
            face.save()
            return redirect('dashboard')
    else:
        form = FaceForm()
    return render(request, 'add_face.html', {'form': form})

class FaceViewSet(viewsets.ModelViewSet):
    serializer_class = FaceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name']
    ordering_fields = ['name', 'created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return Face.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        face = self.get_object()
        face.is_active = not face.is_active
        face.save()
        return Response({'status': 'face status toggled'})
