import os
import django

# Configura las variables de entorno para Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Inicializa Django
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def change_password(email, new_password):
    try:
        # Obtener la instancia del usuario
        user = User.objects.get(email=email)
        # Establecer la nueva contraseña
        user.set_password(new_password)
        # Guardar el usuario con la nueva contraseña
        user.save()
        print(f"La contraseña para {email} ha sido cambiada exitosamente.")
    except User.DoesNotExist:
        print(f"El usuario con el email {email} no existe.")

if __name__ == '__main__':
    # Cambiar la contraseña del usuario especificado
    change_password('infinity3-sage@nunsys.com', '123456789.')
