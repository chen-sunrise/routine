# -*- coding:utf-8 -*-

from rent_house import get_app, db, models
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

# 创建app
app = get_app('development')

# 让app和db在迁移时建立关联
manager = Manager(app)

# 让app和db在迁移时建立关联
Migrate(app, db)

# 将数据库迁移脚本添加到脚本管理器
manager.add_command('db', MigrateCommand)


#
# @app.route('/', methods=['GET', 'POST'])
# def index():
#     # 测试redis数据库
#     # from iHome import redis_store
#     # redis_store.set('name', 'heheheehehehehhe')
#
#     # 测试session:flask自带的session模块，用于存储session
#     # from flask import session
#     # session['name'] = 'sz07sz07'
#
#     return 'index'

if __name__ == '__main__':
    # app.run()
    print app.url_map
    manager.run()