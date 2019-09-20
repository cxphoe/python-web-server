import json
import urllib
from utils import log

# 定义一个 class 用于保存请求的数据
class Request(object):
    def __init__(self, raw_data):
        # 只能 split 一次，因为 body 中可能有换行
        header, self.body = raw_data.split('\r\n\r\n', 1)
        h = header.split('\r\n')

        parts = h[0].split()
        self.method = parts[0]
        path = parts[1]
        self.path = ""
        self.query = {}
        self.parse_path(path)

        self.headers = {}
        self.cookies = {}
        self.add_headers(h[1:])
        self.parse_body()

    def add_headers(self, header):
        """
        Cookie: user=phoe
        """
        lines = header
        for line in lines:
            k, v = line.split(': ', 1)
            self.headers[k] = v

        if 'Cookie' in self.headers:
            cookies = self.headers['Cookie']
            for item in cookies.split('; '):
                k, v = item.split('=', 1)
                self.cookies[k] = v

    def parse_body(self):
        content_type = self.headers.get('content-type', None)
        if content_type is None:
            content_type = self.headers.get('Content-type', None)
        if content_type is None:
            return
        try:
            self.body = json.loads(self.body)
        except:
            pass

    def form(self):
        if len(self.body) == 0:
            return {}
        body = urllib.parse.unquote_plus(self.body)
        args = body.split('&')
        f = {}
        for arg in args:
            k, v = arg.split('=')
            f[k] = v
        return f

    def parse_path(self, path):
        """
        输入: /post?message=hello&author=phoe
        返回
        (post, {
            'message': 'hello',
            'author': 'phoe',
        })
        """
        index = path.find('?')
        if index == -1:
            self.path = path
            self.query = {}
        else:
            path, query_string = path.split('?', 1)
            args = query_string.split('&')
            query = {}
            for arg in args:
                k, v = arg.split('=')
                query[k] = v
            self.path = path
            self.query = query
