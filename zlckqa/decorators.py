from flask import g, redirect, url_for
from functools import wraps


def login_required(func):
    @wraps(func)  # 装饰器
    # *args代表任何多个无名参数，返回的是元组；**kwargs表示关键字参数，所有传入的key=value，返回字典；
    def wrapper(*args, **kwargs):
        if hasattr(g, "user"):
            return func(*args, **kwargs)
        else:
            return redirect(url_for("user.login"))

    return wrapper
