import pymysql

import config

from models import SQLModel
from models.session import Session
from models.todo import Todo
from models.user import User
from models.user_role import UserRole

def recreate_table(cursor):
    for model in [Session, Todo, User]:
        cursor.execute(model.sql_create)

def recreate_database():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password=config.db_password,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    with connection.cursor() as cursor:
        cursor.execute(
            'DROP DATABASE IF EXISTS `{}`'.format(
                config.db_name
            )
        )
        cursor.execute(
            'CREATE DATABASE `{}` DEFAULT CHARACTER SET utf8mb4'.format(
                config.db_name
            )
        )
        cursor.execute('USE `{}`'.format(config.db_name))

        recreate_table(cursor)

    connection.commit()
    connection.close()

def test_data():
    form = dict(
        username='phoe',
        password='123',
        role=UserRole.admin
    )
    User.register(form)

if __name__ == '__main__':
    recreate_database()
    SQLModel.init_db()
    test_data()
