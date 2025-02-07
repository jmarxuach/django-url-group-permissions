# Django URL Permissions

A Django package that provides a flexible and efficient way to manage URL-based permissions through Django's user groups. This package allows you to control access to specific URLs based on user group membership and HTTP methods.

## Features

- 🔒 Control access to URLs based on user groups
- 🌐 Support for all HTTP methods (GET, POST, PUT, PATCH, DELETE, etc.)
- ⚡ Option to grant all-method access with a single permission
- 🔌 Easy integration through middleware
- ⚙️ Configurable exempt URLs
- 🐍 Support for Django 3.2+ and Python 3.7+
- 👨‍💼 Built-in admin interface integration
- 🚀 Efficient database querying with proper indexing

## Installation

Install the package using pip:

```bash
pip install django-url-permissions
```

## Quick Start

1. Add 'django_url_permissions' to your INSTALLED_APPS:

```python
INSTALLED_APPS = [
    ...
    'django_url_permissions',
]

```

2. Add the middleware to your settings:

```python
MIDDLEWARE = [
    ...
    'django_url_permissions.middleware.UrlPermissionMiddleware',
]
```

3. Configure optional settings:

```python
# URLs that don't require permission checks
URL_PERMISSION_EXEMPT_URLS = [
    '/admin/',
    '/login/',
    '/static/',
    '/media/',
]

# Global switch to enable/disable permission checks
URL_PERMISSION_REQUIRED = True
```

4. Run migrations:

```bash
python manage.py migrate
```

## Usage

### Decorator

```python
from django_url_permissions import url_permission_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@url_permission_required
@login_required
def my_view(request):
    return render(request, 'my_template.html')
```

Note: The order of decorators matters. `@url_permission_required` should be placed before `@login_required` to ensure the user is authenticated before checking URL permissions.

## Managing URL Permissions

URL permissions are managed through the Django admin interface, similar to model permissions:

1. Go to Django admin (`/admin/`)
2. Navigate to "Groups"
3. Create or edit a group
4. In the group edit page, you'll find a "URL Permissions" section below the standard model permissions
5. Use the interface to:
   - View available URL permissions
   - Add/remove URL permissions for different HTTP methods
   - Filter URLs using the search box
   - Choose multiple permissions at once

Users will only be able to access URLs that their groups have been granted permission to access.


### Supported HTTP Methods

- GET
- POST
- PUT
- PATCH
- DELETE
- HEAD
- OPTIONS
- ALL (special permission that grants access to all methods)

## Configuration Options

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| URL_PERMISSION_REQUIRED | bool | True | Global switch to enable/disable permission checks |
| URL_PERMISSION_EXEMPT_URLS | list | [] | List of URL prefixes that bypass permission checks |

## Model Fields

| Field | Type | Description |
|-------|------|-------------|
| group | ForeignKey | The Django group this permission applies to |
| url | CharField | The URL pattern this permission controls |
| http_method | CharField | The HTTP method or 'ALL' |
| is_active | BooleanField | Whether this permission is currently active |
| description | TextField | Optional description of the permission |
| created_at | DateTimeField | When the permission was created |
| updated_at | DateTimeField | When the permission was last updated |

## Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone the repository
git clone https://github.com/jmarxuach/django-url-permissions.git
cd django-url-permissions

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any problems or have questions, please:

1. Check the [GitHub Issues](https://github.com/jmarxuach/django-url-permissions/issues) for existing problems or solutions
2. Create a new issue if your problem is not yet reported

## Changelog

### 0.1.0 (Initial Release)
- Basic URL permission functionality
- Group-based permission management
- HTTP method support
- Middleware implementation
- Admin interface integration

## Authors

- Joan Marxuach - Initial work - [jmarxuach](https://github.com/jmarxuach)

## Acknowledgments

- Thanks to the Django community for the amazing framework
- Inspired by the need for flexible URL-based permissions in Django applications