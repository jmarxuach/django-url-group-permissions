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
# This source code is part of the "django_url_group_permissions" project.
# Intellectual property of IT ELAZOS SL.

from django.contrib import admin
from django.urls import URLPattern, URLResolver
from django.conf import settings
from .models import *
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group
from django.contrib import admin
from .models import GroupUrlPermissions
from django.utils.translation import gettext_lazy as _


class CustomGroupAdmin(GroupAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form

    def get_clean_url(self, url_path):
        """Remove language prefix if present and clean the URL path."""
        if hasattr(settings, 'LANGUAGES'):
            for lang_code, _ in settings.LANGUAGES:
                prefix = f'{lang_code}/'
                if url_path.startswith(prefix):
                    return url_path[len(prefix):]
        return url_path

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        
        # Get current group
        group = self.get_object(request, object_id)
        
        if group:
            # Get chosen URL permissions
            chosen_url_permissions = GroupUrlPermissions.objects.filter(group=group)
            
            # Get HTTP methods from model
            http_methods = [method[0] for method in GroupUrlPermissions.HTTP_METHODS]
            
            # Get all URLs using the recursive method
            available_urls = set()
            urlconf = __import__(settings.ROOT_URLCONF, {}, {}, [''])
            
            def list_urls(patterns, acc=None):
                if acc is None:
                    acc = []
                if not patterns:
                    return
                pattern = patterns[0]
                if isinstance(pattern, URLPattern):
                    url_path = ''.join(acc + [str(pattern.pattern)])
                    # Clean URL path
                    clean_url = self.get_clean_url(url_path)
                    # Add all HTTP methods for user-defined URLs
                    for method in http_methods:
                        available_urls.add((clean_url, method))
                            
                elif isinstance(pattern, URLResolver):
                    yield from list_urls(pattern.url_patterns, acc + [str(pattern.pattern)])
                yield from list_urls(patterns[1:], acc)
            
            # Process all URL patterns
            for _ in list_urls(urlconf.urlpatterns):
                pass
            
            # Convert set to list of dictionaries
            available_urls = [
                {
                    'id': f"{url}|{method}",
                    'url': url,
                    'http_method': method,
                }
                for url, method in available_urls
            ]
            
            # Filter out URLs that are already chosen
            chosen_url_methods = []
            for perm in chosen_url_permissions:
                clean_url = self.get_clean_url(perm.url)
                chosen_url_methods.append({
                    'id': f"{clean_url}|{perm.http_method}",
                    'url': clean_url,
                    'http_method': perm.http_method,
                })       

            # Create a set of chosen IDs for efficient lookup
            chosen_ids = {item['id'] for item in chosen_url_methods}

            available_url_permissions = [
                url for url in available_urls 
                if f"{url['url']}|{url['http_method']}" not in chosen_ids
            ]
            
            extra_context.update({
                'available_url_permissions': available_url_permissions,
                'chosen_url_permissions': chosen_url_methods
            })
        
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        
        # Clear all existing URL permissions for this group
        GroupUrlPermissions.objects.filter(group=obj).delete()
        
        # get the list of url and method from the form
        chosen_permissions = request.POST.getlist('url_permissions')

        if chosen_permissions:
            for perm_id in chosen_permissions:
                if perm_id:  # Only process non-empty values
                    url, method = perm_id.split('|')
                    # Store URL without language prefix
                    clean_url = self.get_clean_url(url)
                    GroupUrlPermissions.objects.create(
                        group=obj,
                        url=clean_url,
                        http_method=method
                    )
                

# Unregister the default GroupAdmin
admin.site.unregister(Group)
# Register the custom GroupAdmin
admin.site.register(Group, CustomGroupAdmin) 


@admin.register(GroupUrlPermissions)
class GroupUrlPermissionsAdmin(admin.ModelAdmin):
    list_display = ('group', 'url', 'http_method', 'is_active', 'created_at')
    list_filter = ('group', 'http_method', 'is_active')
    search_fields = ('group__name', 'url', 'description')
    ordering = ('group__name', 'url')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('group', 'url', 'http_method')
        }),
        (_('Options'), {
            'fields': ('is_active', 'description')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )













