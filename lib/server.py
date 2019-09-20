import _thread
import socket

from utils import log
from lib.request import Request
from lib.response import Response
from routes.index import (
    error,
)
import routes.index
import routes.passport
import routes.todo

from routes import routes

class Server:
    def __init__(self):
        self.middlewares = []

    def handle_path(self, req: Request, res: Response):
        """
        根据 path 调用相应的处理函数
        没有处理的 path 会返回 404
        """
        # 获取路由
        m_routes = routes.get(req.method, None)
        if m_routes is None or req.path not in m_routes:
            error(req, res)
        else:
            m_routes[req.path](req, res)


    def use(self, middleware):
        self.middlewares.append(middleware)


    def process_connection(self, connection):
        with connection:
            r = b''
            while True:
                content = connection.recv(1024)
                r += content
                if len(content) != 1024:
                    break
            log('request log:\n <{}>'.format(r))
            r = r.decode()
            if r:
                request = Request(r)
                response = Response()

                m_num = len(self.middlewares)
                if m_num > 0:
                    # 下一个中间件的 index
                    next_i = 0
                    def next():
                        nonlocal next_i
                        if next_i == m_num:
                            self.handle_path(request, response)
                        else:
                            m = self.middlewares[next_i]
                            next_i += 1
                            m(request, response, next)
                    next()
                else:
                    self.handle_path(request, response)

                # 把响应发送给客户端
                connection.sendall(response.toHttp())


    def run(self, host, port):
        """
        启动服务器
        """
        # 使用 with 可以保证程序中断的时候正确关闭 socket 释放占用的端口
        log('启动:', 'http://{}:{}'.format(host, port))
        with socket.socket() as s:
            # 使用 下面这句 可以保证程序重启后使用原有端口
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((host, port))
            # 无限循环来处理请求
            # 监听 -> 接收 -> 读取请求数据 -> 解码成字符串 -> 处理请求 -> 生成响应
            s.listen()
            while True:
                connection, address = s.accept()
                log('ip <{}>\n'.format(address))
                _thread.start_new_thread(self.process_connection, (connection,))

