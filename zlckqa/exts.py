from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

# 建立数据库映射对象
db = SQLAlchemy()
mail = Mail()
