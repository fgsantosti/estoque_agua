import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'estoque_agua.settings')
application = get_wsgi_application()
