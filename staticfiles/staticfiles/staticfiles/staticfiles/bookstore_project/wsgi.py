"""
WSGI config for bookstore_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

# The path to your project directory
project_home = '/home/puff/puff.pythonanywhere.com'
if project_home not in sys.path:
    sys.path.append(project_home)


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookstore_project.settings')

# Activate the virtual environment
activate_this = '/home/puff/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

application = get_wsgi_application()
