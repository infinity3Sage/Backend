from django.urls import path
from .views import get_modulos

urlpatterns = [
    path('modulos/', get_modulos, name='get_modulos'),
]
