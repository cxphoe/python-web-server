import json
from utils import log
from lib.cookies import Cookies

# 定义一个 class 用于保存请求的数据
class Response(object):
    def __init__(self, code: int=200, headers=None, body=''):
        self.code = code
        self.headers = headers or {}
        self.body = body
        self.cookies = Cookies()

    def toHttp(self):
        """
        Content-Type: text/html
        Set-Cookie: user=phoe
        """
        packet = 'HTTP/1.x {} VERY OK\r\n'.format(self.code)
        headers = self.headers
        if headers is not None:
            packet += ''.join([
                '{}: {}\r\n'.format(k, v) for k, v in headers.items()
            ])
        packet += str(self.cookies)
        packet += '\r\n'
        packet = packet.encode()
        if type(self.body) != bytes:
            self.body = self.body.encode()
        return packet + self.body

    def redirect(self, url):
        """
        浏览器在收到 302 响应的时候
        会自动在 HTTP header 里面找 Location 字段并获取一个 url
        然后自动请求新的 url
        """
        # 增加 Location 字段并生成 HTTP 响应返回
        # 注意, 没有 HTTP body 部分
        self.code = 302
        self.body = ''
        self.headers['Location'] = url

    def render(self, filename, payload={}):
        """
        根据文件名字读取模板文件路径中的文件
        """
        path = 'public/view/' + filename
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            for key in payload:
                content = content.replace('{{' + key + '}}', payload[key])
            self.body = content
            self.headers['Content-type'] = 'text/html'

    def json(self, data):
        """
        设置 json 数据
        """
        self.headers['Content-type'] = 'application/json'
        self.body = json.dumps(data)
