
from models.session import Session
from models.user import User

routes = {}

def route(methods: list, path: str):
    def wrapper(fn):
        for m in methods:
            routes.setdefault(m, {})
            routes[m][path] = fn
        return fn
    return wrapper


def current_user(request):
    if 'session_id' in request.cookies:
        session_id = request.cookies['session_id']
        s = Session.find_by(session_id=session_id)
        if s is None or s.expired():
            return None
        else:
            user_id = s.user_id
            u = User.find_by(id=user_id)
            return u
    else:
        return None

def login_required(route_function):

    def f(request, response):
        u = current_user(request)
        if u is None:
            return response.redirect('/login')
        else:
            return route_function(request)

    return f
