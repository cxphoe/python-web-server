from models import Model
from utils import log
import hashlib

class User(Model):
    """
    User 是一个保存用户数据的 model
    现在只有两个属性 username 和 password
    """

    def __init__(self, form):
        super().__init__(form)
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    @staticmethod
    def salted_password(password, salt=')(*&^%'):
        """
        密码加盐
        """
        salted = password + salt
        hash = hashlib.sha256(salted.encode('ascii')).hexdigest()
        return hash

    @classmethod
    def login(cls, form):
        u = User.find_by(username=form['username'], password=cls.salted_password(form['password']))
        if u is not None:
            return u
        else:
            return None

    @classmethod
    def register(cls, form):
        valid = len(form['username']) > 2 and len(form['password']) > 2
        if valid:
            form['password'] = cls.salted_password(form['password'])
            u = User.new(form)
            result = '注册成功'
            return u, result
        else:
            result = '用户名或者密码长度必须大于2'
            return None, result