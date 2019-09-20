import time
import random

from utils import log
from models.user import User
from models.session import Session
from lib.response import Response
from lib.request import Request
from routes import current_user, route

def random_string():
    """
    生成一个随机的字符串
    """
    seed = 'sdfsdafasfsdfsdwtfgjdfghfg'
    s = ''
    l = len(seed) - 1
    for _ in range(16):
        random_index = random.randint(0, l)
        s += seed[random_index]
    return s

@route(['GET'], '/api/passport/status')
def route_passport_status(req: Request, res: Response):
    """
    登录页面的路由函数
    """
    user_current = current_user(req)
    if user_current:
        res.json({
            'code': 0,
            'msg': 'success',
            'data': {
                'username': user_current.username,
                'id': user_current.id,
            },
        })
    else:
        res.json({
            'code': 401,
            'msg': 'Unauthorized',
            'data': {},
        })

@route(['POST'], '/api/register')
def route_register(req: Request, res: Response):
    if 'username' in req.body and 'password' in req.body:
        u, result = User.register(dict(
            username=req.body['username'],
            password=req.body['password'],
        ))
        if u is None:
            res.json({
                'code': 400,
                'msg': result,
                'data': {},
            })
        else:
            res.json({
                'code': 0,
                'msg': '注册成功',
                'data': {
                    'username': u.username,
                    'id': u.id,
                }
            })
    else:
        res.json({
            'code': 400,
            'msg': '缺乏参数 username 或 password',
            'data': {},
        })


@route(['POST'], '/api/login')
def route_login(req: Request, res: Response):
    if 'username' in req.body and 'password' in req.body:
        u = User.login(dict(
            username=req.body['username'],
            password=req.body['password'],
        ))
        if u is None:
            res.json({
                'code': 400,
                'msg': '用户名或密码错误',
                'data': {},
            })
        else:
            # 下面是把用户名存入 cookie 中
            # headers['Set-Cookie'] = 'user={}'.format(u.username)
            session_id = random_string()
            form = dict(
                session_id=session_id,
                user_id=u.id,
            )
            Session.new(form)
            res.cookies.set('session_id', session_id)
            res.json({
                'code': 0,
                'msg': '登录成功',
                'data': {
                    'username': u.username,
                    'id': u.id,
                }
            })
    else:
        res.json({
            'code': 400,
            'msg': '缺乏参数 username 或 password',
            'data': {},
        })


@route(['GET'], '/api/logout')
def route_logout(req: Request, res: Response):
    res.cookies.set('session_id', '; max-age=0')
    res.json({
        'code': 0,
        'msg': '登出成功',
        'data': {},
    })
