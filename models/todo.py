import time

from models import SQLModel
from utils import log

class Todo(SQLModel):
    """
    C create 创建数据
    R read 读取数据
    U update 更新数据
    D delete 删除数据
    """

    sql_create = '''
        CREATE TABLE `todo` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `title` VARCHAR(64) NOT NULL,
        `user_id` INT NOT NULL,
        `created_time` INT NOT NULL,
        `updated_time` INT NOT NULL,
        PRIMARY KEY (`id`)
    )'''

    def __init__(self, form):
        super().__init__(form)
        self.title = form.get('title', '')
        # 和别的数据关联的方式, 用 user_id 表明拥有它的 user 实例
        self.user_id = form.get('user_id', -1)
        self.created_time = form.get('created_time', 0)
        self.updated_time = form.get('updated_time', 0)

    @classmethod
    def add(cls, form, user_id):
        form['user_id'] = user_id
        current_time = int(time.time())
        form['created_time'] = current_time
        form['updated_time'] = current_time
        log('add todo:', form)
        todo = cls.new(form)
        return todo

    @classmethod
    def update(cls, id, **kwargs):
        super().update(
            id=id,
            title=kwargs['title'],
            updated_time=int(time.time())
        )

        t = Todo.one(id=id)
        return t
