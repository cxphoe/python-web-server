import time

from models.todo import Todo
from routes import (
    redirect,
    template,
    current_user,
    response_with_headers,
    login_required
)
from utils import log


def formatted_time(unix_time):
    t = time.localtime(unix_time)
    ft = time.strftime('%Y-%m-%d %H:%M:%S', t)
    return ft


def index(request):
    """
    todo 首页的路由函数
    """
    todos = Todo.all()
    # todos = Todo.all()

    # 下面这行生成一个 html 字符串
    todo_html = """
    <tr>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
        <td>
            <a href="/todo/edit?id={}">编辑</a>
            <a href="/todo/delete?id={}">删除</a>
        </td>
    </tr>
    """
    todo_html = ''.join([
        todo_html.format(
            t.id,
            t.title,
            formatted_time(t.created_time),
            formatted_time(t.updated_time),
            t.id,
            t.id
        ) for t in todos
    ])
    # 添加表头
    todo_html = """
    <table border=1>
        <tr>
            <th>id</th>
            <th>title</th>
            <th>创建时间</th>
            <th>更新时间</th>
            <th>操作</th>
        </tr>
        {}
    </table>
    """.format(todo_html)

    # 替换模板文件中的标记字符串
    body = template('todo_index.html')
    body = body.replace('{{todos}}', todo_html)

    headers = {
        'Content-Type': 'text/html',
    }
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    return r.encode()


def add(request):
    """
    用于增加新 todo 的路由函数
    """
    form = request.form()
    u = current_user(request)
    Todo.add(form, u.id or -1)

    # 浏览器发送数据过来被处理后, 重定向到首页
    # 浏览器在请求新首页的时候, 就能看到新增的数据了
    return redirect('/todo')


def delete(request):
    todo_id = int(request.query['id'])
    Todo.delete(todo_id)
    return redirect('/todo')


def edit(request):
    todo_id = int(request.query['id'])
    t = Todo.one(id=todo_id)

    u = current_user(request)
    # 只有在当前用户不是游客，且
    # form 里面的 id 有对应的 todo 项，且
    # todo 项的 id 与当前用户的 id 一样（有权限更新）
    # 才能编辑
    log('<edit> 当前用户:', u)
    if not u.is_guest() and t is not None and u.id == t.user_id:
        body = template('todo_edit.html')
        body = body.replace('{{todo_id}}', str(todo_id))
        body = body.replace('{{todo_title}}', t.title)

        headers = {
            'Content-Type': 'text/html',
        }
        header = response_with_headers(headers)
        r = header + '\r\n' + body
        return r.encode()

    else:
        log('<edit> 重定向到主页面')
        return redirect('/todo')


def update(request):
    """
    用于增加新 todo 的路由函数
    /todo/update?id={{todo_id}}
    /todo/update/1
    """
    form = request.form()
    u = current_user(request)
    t = Todo.one(id=int(form['id']))
    # 只有在当前用户不是游客，且
    # form 里面的 id 有对应的 todo 项，且
    # todo 项的 id 与当前用户的 id 一样（有权限更新）
    # 才能修改
    if not u.is_guest() and t is not None and u.id == t.user_id:
        Todo.update(form)

    return redirect('/todo')


def same_owner_required(route_function):
    pass


def route_dict():
    """
    路由字典
    key 是路由(路由就是 path)
    value 是路由处理函数(就是响应)
    """
    d = {
        '/todo': index,
        '/todo/add': add,
        '/todo/edit': edit,
        '/todo/update': update,
        '/todo/delete': delete,
    }
    return d
