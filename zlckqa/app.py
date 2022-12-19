from flask import Flask, session, g
import config
from exts import db, mail
from blueprints import qa_bp, user_bp
from flask_migrate import Migrate
from models import UserModel

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
mail.init_app(app)

migrate = Migrate(app, db)

# 在主程序中，通过app.register_blueprint()方法将这个蓝图注册进url映射中
app.register_blueprint(qa_bp)
app.register_blueprint(user_bp)


@app.before_request
def before_request():
    user_id = session.get("user_id")
    if user_id:
        try:
            user = UserModel.query.get(user_id)
            # 给全局变量g绑定值为user的user变量
            setattr(g, "user", user)
        except:
            # 也可以这样给全局变量g绑定为None
            g.user = None


# 请求 -> before_request -> 视图函数 -> 视图函数中返回模板 -> context_processor上下文处理器
@app.context_processor
def context_processor():
    if hasattr(g, "user"):
        return {"user": g.user}
    else:
        return {}


if __name__ == '__main__':
    app.run()
