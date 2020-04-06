from views import registration, authorization, userpage, addlink, deletelink, logout, resetpassword, deleteaccount, download
from aiohttp import web

# def setup_routes(app):
#     app.router.add_routes([web.get('/', index),
#                        web.post('/login', login)])
    
def setup_routes(app):
    app.router.add_route('*', '/registration', registration)
    app.router.add_route('*', '/authorization', authorization)
    app.router.add_route('*', '/user_page', userpage)
    app.router.add_route('*', '/addlink', addlink)
    app.router.add_route('*', '/deletelink', deletelink)
    app.router.add_route('*', '/logout', logout)
    app.router.add_route('*', '/resetpassword', resetpassword)
    app.router.add_route('*', '/deleteaccount', deleteaccount)
    app.router.add_route('*', '/download', download)