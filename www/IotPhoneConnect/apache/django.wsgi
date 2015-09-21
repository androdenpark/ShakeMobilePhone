import os
import sys


path = "/var/www/IotPhoneConnect"


if path not in sys.path:
	sys.path.append(path)

os.environ["DJANGO_SETTINGS_MODULE"]= "IotPhoneConnect.settings"


from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


