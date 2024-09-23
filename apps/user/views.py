# apps/user/views.py
from rest_framework import generics, permissions
from .models import UserAccount
from .serializers import UserSerializer, UserCreateSerializer

class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]  # Solo usuarios autenticados pueden acceder

    def get_queryset(self):
        # Filtra los usuarios por la empresa del usuario actualmente autenticado
        user_company = self.request.user.empresa
        if user_company:
            return UserAccount.objects.filter(empresa=user_company)
        return UserAccount.objects.none()  # Retorna vacío si el usuario no tiene una empresa

class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.IsAuthenticated]  # Solo usuarios autenticados pueden crear nuevos usuarios

    def perform_create(self, serializer):
        # Establece la empresa del nuevo usuario como la del usuario que realiza la solicitud
        serializer.save(empresa=self.request.user.empresa)

class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserAccount.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]  # Solo usuarios autenticados pueden acceder

    def get_object(self):
        # Permite solo al usuario autenticado acceder y actualizar sus propios datos
        obj = super().get_object()
        if self.request.user.is_staff or self.request.user == obj:
            return obj
        raise permissions.PermissionDenied("You do not have permission to access this resource.")
