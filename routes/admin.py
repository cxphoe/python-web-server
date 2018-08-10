from models.todo import Todo
from routes import (
    redirect,
    template,
    current_user,
    response_with_headers,
    login_required
)
from utils import log
from models.user import User


def users(request):
    u = current_user(request)
    # if not u.is_admin():
    #     log('<admin:users> 重定向到登陆页面')
    #     return redirect('/login')
    # 得到所有用户
    users = User.all()
    # 先写好单个用户数据展示的 html
    users_html = """
    <tr>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
    </tr>
    """

    # 生成所有用户数据的 html 内容
    users_html = ''.join(
        users_html.format(
            u.id, u.username, u.password
        ) for u in users
    )

    # 替换模板文件中的标记字符串
    body = template('admin_users.html')
    body = body.replace('{{users}}', users_html)

    header = response_with_headers({
        'Content-Type': 'text/html',
    })
    r = header + '\r\n' + body
    return r.encode()


def users_update(request):
    u = current_user(request)
    if not u.is_admin():
        log('<admin:users_update> 重定向到登陆页面')
        return redirect('/login')
    else:
        form = request.form()
        target_id = int(form.get('id', -1))
        target = User.one(id=target_id)
        if target is not None:
            password = form.get('password', '')
            if len(password) > 2:
                target.password = password
            target.update(target_id, password=password)
        else:
            log('<admin:users_update> 没有找到id:{}的用户'.format(form['id']))
        return redirect('/admin/users')


def route_dict():
    """
    路由字典
    key 是路由(路由就是 path)
    value 是路由处理函数(就是响应)
    """
    d = {
        '/admin/users': users,
        '/admin/users/update': users_update,
    }
    return d
