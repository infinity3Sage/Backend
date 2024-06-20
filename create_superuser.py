import os
import django

# Configura las variables de entorno para Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Inicializa Django
django.setup()

from django.contrib.auth import get_user_model
from apps.empresa.models import Empresa

User = get_user_model()

def create_superuser():
    # Obtener la instancia de la empresa
    empresa = Empresa.objects.get(nombre='NUNSYS')
    
    # Crear el superusuario
    User.objects.create_superuser(
        email='infinity3-sage@nunsys.com',
        password='passWordAquÍ!',
        first_name='Infinity',
        last_name='By_Sage',
        cliente_sage='admin',
        empresa=empresa
    )

if __name__ == '__main__':
    create_superuser()
