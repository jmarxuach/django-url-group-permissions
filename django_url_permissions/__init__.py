default_app_config = 'django_url_permissions.apps.DjangoUrlPermissionsConfig'

from .decorators import url_permission_required

__all__ = ['url_permission_required']

