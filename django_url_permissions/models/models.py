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

