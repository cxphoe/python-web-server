from lib.request import Request
from lib.response import Response
import os
import mimetypes

from utils import log

def static(options):
    """
    静态文件获取
    """
    public_path = options['public_path']
    def fn(req: Request, res: Response, next):
        if not req.path.startswith(public_path):
            return next()

        filepath = req.path[len(public_path) + 1:]
        realpath = os.path.join(os.getcwd(), 'public/static', filepath)
        if os.path.isfile(realpath):
            _, extname = os.path.splitext(filepath)
            res.headers['Content-type'] = mimetypes.types_map[extname]
            with open(realpath, 'rb') as f:
                res.body = f.read()
        else:
            res.headers['Content-type'] = 'text/html'
            res.body = '<h1>NOT FOUND</h1>'
    return fn
