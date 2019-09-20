import time

from models import Model
from utils import log

class Todo(Model):
    """
    C create 创建数据
    R read 读取数据
    U update 更新数据
    D delete 删除数据
    """

    def __init__(self, form):
        super().__init__(form)
        self.title = form.get('title', '')
        # 和别的数据关联的方式, 用 user_id 表明拥有它的 user 实例
        self.user_id = form.get('user_id', -1)
        self.created_time = form.get('created_time', 0)
        self.updated_time = form.get('updated_time', 0)
        self.completed = form.get('completed', 0)

    @classmethod
    def add(cls, form, user_id):
        form['user_id'] = user_id
        current_time = int(time.time())
        form['created_time'] = current_time
        form['updated_time'] = current_time
        todo = cls.new(form)
        return todo

    @classmethod
    def update(cls, id, form):
        item = Todo.find_by(id=id)
        editable_fields = [
            'title',
            'completed',
        ]
        for key in form:
            if key in editable_fields:
                setattr(item, key, form[key])

        item.updated_time = time.time()
        item.save()
        return item
