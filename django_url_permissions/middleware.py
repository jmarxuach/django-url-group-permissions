# Copyright (c) 2025 IT ELAZOS SL
# Intellectual property of IT ELAZOS SL. All rights reserved.
#
# This source code is part of the "django_url_permissions" project.
# Unauthorized use, reproduction, distribution, modification, or transmission
# of this code, in whole or in part, is strictly prohibited without the express
# written consent of IT ELAZOS SL.
#
# Unauthorized use of this code will be considered an infringement of
# intellectual property rights and may result in legal action.

from django.http import HttpResponseForbidden
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from .models.models import GroupUrlPermissions
from django.urls import get_resolver


class UrlPermissionMiddleware(MiddlewareMixin):
    """
    Middleware to check if the user's groups have permission to access the current URL.
    """
    
    def __init__(self, get_response):
        super().__init__(get_response)
        self.exempt_urls = getattr(settings, 'URL_PERMISSION_EXEMPT_URLS', [])
        self.permission_required = getattr(settings, 'URL_PERMISSION_REQUIRED', True)

    def is_exempt_url(self, path):
        """Check if the URL is exempt from permission checks."""
        return any(path.startswith(exempt_url) for exempt_url in self.exempt_urls)

    def process_request(self, request):
        # Skip permission check for exempt URLs        
        if self.is_exempt_url(request.path):
            return None
    
        # Skip permission check if URL_PERMISSION_REQUIRED is False
        if not self.permission_required:
            return None

        # Always allow authentication-related URLs
        if not request.user.is_authenticated:
            return None
        
        # Skip permission check for superusers
        if request.user.is_superuser:
            return None

        # Get the view function
        resolver = get_resolver()
        resolver_match = resolver.resolve(request.path)
        view_func = resolver_match.func

        # Check if view requires URL permission        
        check_permissions = getattr(view_func, 'requires_url_permission', False)
        if not check_permissions:
            return None

        # Get the current HTTP method
        method = request.method

        # Check if user has permission for this URL
        has_permission = GroupUrlPermissions.has_url_permission(
            user=request.user,
            url=request.path,
            method=method
        )

        if not has_permission:
            return HttpResponseForbidden("You don't have permission to access this URL.")

        return None
