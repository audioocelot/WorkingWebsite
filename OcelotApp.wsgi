import logging, sys
sys.path.insert(0, '/var/www/ocelot.audio/public_html/OcelotApp')
logging.basicConfig(stream=sys.stderr)

from OcelotApp import app as application
