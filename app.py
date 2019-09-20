from lib.server import Server
from middleware.csrf import csrf
from middleware.static import static

if __name__ == '__main__':
    # 生成配置并且运行程序
    config = dict(
        host='localhost',
        port=3000,
    )
    app = Server()

    app.use(csrf(dict(
        header_name='x_csrf_token',
        cookie_name='csrf_token',
    )))

    app.use(static(dict(
        public_path='/static'
    )))

    app.run(**config)
