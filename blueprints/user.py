from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session, flash
from exts import mail, db
from flask_mail import Message
from models import EmailCaptchaModel, UserModel
import string
import random
from datetime import datetime
from .forms import RegisterFrom, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash

# url_prefix是用于蓝图中的视图url前缀
bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                session["user_id"] = user.id
                return redirect("/")
            else:
                flash("邮箱与密码不匹配！")
                return redirect(url_for("user.login"))
        else:
            flash("邮箱或密码格式有误！")
            return redirect(url_for("user.login"))


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        form = RegisterFrom(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data

            # 使用generate_password_hash生成password的哈希后的密码
            hash_password = generate_password_hash(password)
            user = UserModel(email=email, username=username, password=hash_password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("user.login"))
        else:
            return redirect(url_for("user.register"))


@bp.route("/logout")
def logout():
    # 清除session所有数据
    session.clear()
    return redirect(url_for("user.login"))


@bp.route("/captcha", methods=["POST"])
def get_captcha():
    # GET, POST
    email = request.form.get("email")
    # 建立letters列表存放string.ascii_letters小写英文字母以及大写英文字母与string.digits阿拉伯数字
    letters = string.ascii_letters + string.digits
    # 随机在letters中取样,取4个元素
    captcha = "".join(random.sample(letters, 4))
    if email:
        massage = Message(
            subject="邮箱测试",  # 邮件主题
            recipients=[email],   # 邮件接收方
            body=f"您的验证码为:{captcha}"   # 邮件内容
        )
        mail.send(massage)
        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
        if captcha_model:
            captcha_model.captcha = captcha
            captcha_model.create_time = datetime.now()
            db.session.commit()
        else:
            captcha_model = EmailCaptchaModel(email=email, captcha=captcha)
            db.session.add(captcha_model)
            db.session.commit()
        # code: 200 是正常的,成功的请求
        return jsonify({"code": 200})
    else:
        # code: 400 是客户端错误
        return jsonify({"code": 400, "message": "请先输入邮箱!"})
