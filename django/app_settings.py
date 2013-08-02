
from django.conf import settings


HUB = getattr(settings, 'SIMPLESYNC_HUB', 'Threaded')
