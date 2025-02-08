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

from django.contrib import admin
from django.urls import get_resolver
from django.utils.translation import gettext_lazy as _
from .models import *
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group
from django.contrib import admin
from .models import GroupUrlPermissions


class CustomGroupAdmin(GroupAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        
        # Get current group
        group = self.get_object(request, object_id)
        
        if group:
            # Get chosen URL permissions
            chosen_url_permissions = GroupUrlPermissions.objects.filter(group=group)
            
            # Get all URL patterns from Django resolver
            resolver = get_resolver()
            available_urls = []
            
            # Get HTTP methods from model
            http_methods = [method[0] for method in GroupUrlPermissions.HTTP_METHODS]
            
            for pattern in resolver.url_patterns:
                if hasattr(pattern, 'pattern'):
                    url_path = str(pattern.pattern)
                    # Create entries for each HTTP method
                    for method in http_methods:
                        available_urls.append({
                            'id': f"{url_path}|{method}",
                            'url': url_path,
                            'http_method': method,
                        })
            
            # Filter out URLs that are already chosen
            chosen_url_methods = []
            for perm in chosen_url_permissions:
                chosen_url_methods.append({
                    'id': f"{perm.url}|{perm.http_method}",
                    'url': perm.url,
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
                    GroupUrlPermissions.objects.create(
                        group=obj,
                        url=url,
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













