import time

from utils import log
from routes import route, current_user
from models.todo import Todo
from lib.request import Request
from lib.response import Response

def formatted_time(unix_time):
    t = time.localtime(unix_time)
    ft = time.strftime('%Y-%m-%d %H:%M:%S', t)
    return ft


@route(['GET'], '/api/todo')
def index(req: Request, res: Response):
    """
    todo 首页的路由函数
    """
    try:
        user_id = int(req.query['userId'])
    except:
        return res.json({
            'code': 400,
            'msg': '参数错误',
        })
    todos = Todo.find_all(user_id=user_id)
    res.json({
        'code': 0,
        'msg': '',
        'data': [t.json() for t in todos],
    })


@route(['POST'], '/api/todo/add')
def add(req: Request, res: Response):
    """
    用于增加新 todo 的路由函数
    """
    u = current_user(req)
    if u is None:
        return res.json({
            'code': 401,
            'msg': 'Unauthorized',
        })
    form = req.body
    t = Todo.add(form, u.id)
    res.json({
        'code': 0,
        'msg': '添加 todo 成功',
        'data': t.json(),
    })


@route(['POST'], '/api/todo/delete')
def delete(req: Request, res: Response):
    todo_id = req.body['id']
    Todo.delete(todo_id)
    res.json({
        'code': 0,
        'msg': '删除成功',
    })


@route(['POST'], '/api/todo/update')
def update(req: Request, res: Response):
    form = req.body
    todo_id = form['id']
    t = Todo.find_by(id=todo_id)
    u = current_user(req)

    if t is None:
        return res.json({
            'code': 400,
            'msg': 'todo {} 不存在'.format(todo_id),
        })

    # todo 项的 id 与当前用户的 id 一样（有权限更新）
    # 才能编辑
    if (u is None and t.user_id > 0) or u.id != t.user_id:
        res.json({
            'code': 401,
            'msg': 'Unauthorized',
        })
    else:
        form.pop('id')
        new_t = Todo.update(todo_id, form)
        log(form)
        res.json({
            'code': 0,
            'msg': '',
            'data': new_t.json(),
        })
