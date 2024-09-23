from django.urls import path
from .views import EmpresaListAPIView, EmpresaDetailAPIView, update_empresa_modulo, update_empresa_submodulo, update_empresa_submodulo2

urlpatterns = [
    path('', EmpresaListAPIView.as_view(), name='empresa-list'),
    path('<int:pk>/', EmpresaDetailAPIView.as_view(), name='empresa-detail'),
    path('<int:empresa_id>/modulo/<int:modulo_id>/update/', update_empresa_modulo, name='update-empresa-modulo'),
    path('<int:empresa_id>/submodulo/<int:submodulo_id>/update/', update_empresa_submodulo, name='update-empresa-submodulo'),
    path('<int:empresa_id>/submodulo2/<int:submodulo2_id>/update/', update_empresa_submodulo2, name='update-empresa-submodulo2'),
]
