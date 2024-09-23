import os
import django

# Configura las variables de entorno para Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Inicializa Django
django.setup()

from django.contrib.auth import get_user_model
from apps.empresa.models import Empresa

User = get_user_model()

def create_user():
    # Obtener la instancia de la empresa (esto es un ejemplo, ajusta según tu lógica)
    empresa = Empresa.objects.get(nombre='SANYCESS')
    
    # Crear un nuevo usuario
    new_user = User.objects.create_user(
        username='Sanycess',  # Aquí debe ser un valor de tipo str para el username
        email=' sanycessadmin@gmail.com',
        password='12345678.',
        first_name='Marcos',
        last_name='Romero',
        cliente_sage='admin',
        empresa=empresa
    )

    # Imprimir el usuario creado para verificar
    print(f'Usuario creado: {new_user}')

if __name__ == '__main__':
    create_user()
