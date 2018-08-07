import time

from models import Model


class Todo(Model):
    """
    针对我们的数据 TODO
    我们要做 4 件事情
    C create 创建数据
    R read 读取数据
    U update 更新数据
    D delete 删除数据

    Todo.new() 来创建一个 todo
    """

    def __init__(self, form):
        super().__init__(form)
        self.title = form.get('title', '')
        # 和别的数据关联的方式, 用 user_id 表明拥有它的 user 实例
        self.user_id = form.get('user_id', -1)
        # 创建的时候，初始化创建时间和更新时间
        self.created_time = form.get('created_time', 0)
        self.updated_time = form.get('updated_time', 0)

    @classmethod
    def update(cls, form):
        todo_id = int(form['id'])
        t = Todo.find_by(id=todo_id)
        t.title = form['title']
        # 在 save 之前更新 updated_time
        t.updated_time = int(time.time())
        t.save()
