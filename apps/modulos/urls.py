from django.urls import path
from .views import ModuloListView, SubmoduloListView, Submodulo2ListView

urlpatterns = [
    path('modulos/', ModuloListView.as_view(), name='modulo-list'),

    path('submodulos/', SubmoduloListView.as_view(), name='submodulo-list'),

    path('submodulos2/', Submodulo2ListView.as_view(), name='submodulo2-list'),
]
