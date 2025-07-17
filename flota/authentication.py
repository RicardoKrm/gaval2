from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from tenants.models import Empresa

class APIKeyAuthentication(BaseAuthentication):
    """
    Autenticación personalizada para validar peticiones de webhooks de GPS
    usando una clave de API secreta por tenant.
    """
    def authenticate(self, request):
        # La clave de API se espera en la cabecera 'X-API-Key'
        api_key = request.headers.get('X-API-Key')
        if not api_key:
            return None

        try:
            # El schema_name del tenant se espera en la cabecera 'X-Tenant-Schema'
            schema_name = request.headers.get('X-Tenant-Schema')
            if not schema_name:
                raise AuthenticationFailed('La cabecera X-Tenant-Schema es requerida.')

            # Busca la empresa (tenant) que coincida con la clave de API y el schema_name
            empresa = Empresa.objects.get(api_key=api_key, schema_name=schema_name)

            # La autenticación es exitosa, pero no hay un "usuario" asociado a la petición del webhook.
            # Devolvemos la empresa como 'user' para que la vista pueda acceder a ella.
            # El segundo valor del tuple (auth) puede ser None.
            return (empresa, None)

        except Empresa.DoesNotExist:
            raise AuthenticationFailed('Clave de API o Schema de Tenant inválido.')
        except Exception as e:
            # Para otros posibles errores, como un UUID mal formado.
            raise AuthenticationFailed(f'Error de autenticación: {e}')
