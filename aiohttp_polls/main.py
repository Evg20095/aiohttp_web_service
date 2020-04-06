from aiohttp import web
import aiohttp_jinja2
import jinja2
import aiohttp_security
from aiohttp_session import SimpleCookieStorage, session_middleware

from routes import setup_routes
from settings import config
from db import close_pg, init_pg
from secure import identity_policy, autz_policy


middleware = session_middleware(SimpleCookieStorage())
app = web.Application(middlewares=[middleware])
app['config'] = config
setup_routes(app)
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(r'D:\Programming\Aiohttp\Web-server\aiohttp_polls\templates'))
app.on_startup.append(init_pg)
app.on_cleanup.append(close_pg)
aiohttp_security.setup(app, identity_policy, autz_policy)
web.run_app(app)

