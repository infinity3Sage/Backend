import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

django.setup()


from apps.empresa.models import Empresa

def create_empresa():
    Empresa.objects.create(
        nombre='NUNSYS',
        api_endpoint='https://sagex3.nunsys.com:7777/soap-generic/syracuse/collaboration/syracuse/CAdxWebServiceXmlCC',
        suscripcion='FREE'
    )

if __name__ == '__main__':
    create_empresa()