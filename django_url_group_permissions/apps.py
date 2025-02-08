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

from django.apps import AppConfig


class DjangoUrlPermissionsConfig(AppConfig):
    name = 'django_url_permissions'
    verbose_name = "Django URL Permissions"

    def ready(self):
        #add here setup for entire app. Executes only once in runserver
        pass      
        


