from django.urls import path
from .views import (
    EmpresaListAPIView,
    EmpresaDetailAPIView,
    ModuloListView,
    SubmoduloListView,
    Submodulo2ListView,
    update_empresa_modulo,
    update_empresa_submodulo,
    update_empresa_submodulo2,
    get_empresa_for_user  # Nueva vista para obtener la empresa del usuario
)

urlpatterns = [
    path('', EmpresaListAPIView.as_view(), name='empresa-list'),
    path('<int:pk>/', EmpresaDetailAPIView.as_view(), name='empresa-detail'),
    path('<int:empresa_id>/modulo/<int:modulo_id>/update/', update_empresa_modulo, name='update-empresa-modulo'),
    path('<int:empresa_id>/submodulo/<int:submodulo_id>/update/', update_empresa_submodulo, name='update-empresa-submodulo'),
    path('<int:empresa_id>/submodulo2/<int:submodulo2_id>/update/', update_empresa_submodulo2, name='update-empresa-submodulo2'),
    
    path('modulos/', ModuloListView.as_view(), name='modulo-list'),
    path('submodulos/', SubmoduloListView.as_view(), name='submodulo-list'),
    path('submodulos2/', Submodulo2ListView.as_view(), name='submodulo2-list'),
    path('usuario/', get_empresa_for_user, name='empresa-usuario'),
]
