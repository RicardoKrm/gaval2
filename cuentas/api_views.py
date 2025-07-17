from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.permissions import IsAdminUser

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Este ViewSet proporciona acciones de `list` y `retrieve` solamente.
    Solo los administradores pueden ver la lista de usuarios.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser] # Solo los admin pueden acceder a esta API
