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

from django.db import models
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _


class GroupUrlPermissions(models.Model):
    HTTP_METHODS = (
        ('GET', 'GET'),
        ('POST', 'POST'),
        ('PUT', 'PUT'),
        ('PATCH', 'PATCH'),
        ('DELETE', 'DELETE'),
        ('HEAD', 'HEAD'),
        ('OPTIONS', 'OPTIONS'),
        ('ALL', 'ALL'),
    )

    id = models.AutoField(primary_key=True)
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='url_permissions'
    )
    url = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        help_text=_('URL pattern (can include wildcards like /api/*/users/)')
    )
    http_method = models.CharField(
        max_length=10,
        choices=HTTP_METHODS,
        default='GET',
        help_text=_('HTTP method this permission applies to')
    )
    is_active = models.BooleanField(
        default=True,
        help_text=_('Whether this permission is currently active')
    )
    description = models.TextField(
        null=True,
        blank=True,
        help_text=_('Optional description of what this permission does')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('group__name', 'url')
        verbose_name_plural = _('URL Permissions')
        verbose_name = _('URL Permission')
        unique_together = ('group', 'url', 'http_method')
        indexes = [
            models.Index(fields=['url']),
            models.Index(fields=['http_method']),
        ]

    def __str__(self):
        return f"{self.group.name} - {self.http_method} {self.url}"

    @classmethod
    def has_url_permission(cls, user, url, method='GET'):
        """
        Check if a user has permission to access a specific URL with given method.
        """        

        if url.startswith('/'):
            url = url[1:]

        if user.is_superuser:
            return True
            
        user_groups = user.groups.all()
        return cls.objects.filter(
            group__in=user_groups,
            url=url,
            is_active=True,
        ).filter(
            models.Q(http_method=method.upper()) | 
            models.Q(http_method='ALL')
        ).exists()

