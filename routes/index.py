from utils import log
from lib.response import Response
from lib.request import Request

from routes import route

def error(req: Request, res: Response):
    """
    根据 code 返回不同的错误响应
    目前只有 404
    """
    res.code = 404
    res.body = '<h1>NOT FOUND</h1>'

@route(['GET'], '/')
def route_index(req: Request, res: Response):
    """
    主页的处理函数, 返回主页的响应
    """
    res.render('index.html')

