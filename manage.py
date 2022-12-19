# 导入app工程
from app import app
# 导入数据库
from exts import db
# 导入Manager用来设置应用程序可通过指令操作
from flask_migrate import Migrate

# 构建数据库迁移操作，将数据库迁移指令绑定给指定的app和数据库
migrate = Migrate(app,db)
# 添加数据库迁移指令，该操作保证数据库的迁移可以使用指令操作

#以下为当指令操作runserver时，开启服务。
if __name__ == '__main__':
    app.run()
