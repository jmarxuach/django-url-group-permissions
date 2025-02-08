# Copyright (c) 2024 IT ELAZOS SL
# All rights reserved.
#
# MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# This source code is part of the "django_url_permissions" project.
# Intellectual property of IT ELAZOS SL.

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
        self.check_all_views = getattr(settings, 'URL_PERMISSION_CHECK_ALL_VIEWS', False)

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

        # Check if permissions should be checked
        check_permissions = (
            self.check_all_views or 
            getattr(view_func, 'requires_url_permission', False)
        )
        
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
