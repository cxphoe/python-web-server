from lib.request import Request
from lib.response import Response
from utils import log

simple_methods = set(['GET', 'OPTIONS', 'HEAD', 'TRACE'])
# 暂时用固定的字符代替
csrf_token = 'ai258gj2jk2kdc'

def csrf(options):
    """
    csrf 验证
    """
    def fn(req: Request, res: Response, next):
        # 如果在 cookie 中检查不到 cookie，就进行设置
        if req.cookies.get(options['cookie_name'], None) is None:
            res.cookies.set(options['cookie_name'], csrf_token)

        # 简单请求不需要检查 csrf_token
        if req.method in simple_methods:
            return next()

        log(req.method, req.headers, options['header_name'])
        if req.headers.get(options['header_name'], None) != csrf_token:
            res.code = 403
            res.body = ''
        else:
            next()
    return fn
