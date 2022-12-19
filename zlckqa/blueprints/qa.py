from flask import Blueprint, render_template, request, g, redirect, url_for, flash
from zlckqa.decorators import login_required
from .forms import QuestionForm, AnswerForm
from zlckqa.models import QuestionModel, AnswerModel
from zlckqa.exts import db
from sqlalchemy import or_

bp = Blueprint("qa", __name__, url_prefix="/")


@bp.route("/")
def index():
    questions = QuestionModel.query.order_by(db.text("-create_time")).all()
    return render_template("index.html", questions=questions)


@bp.route("/question/public", methods=["GET", "POST"])
@login_required  # 装饰器,用于把识图函数传递给定义的装饰函数
def public_question():
    # 判断是否登录, 如果没有登录, 跳转到登录界面
    if request.method == "GET":
        return render_template("public_question.html")
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = QuestionModel(title=title, content=content, author=g.user)
            db.session.add(question)
            db.session.commit()
            return redirect("/")
        else:
            flash("标题或内容格式错误!")
            return redirect(url_for("qa.public_question"))


@bp.route("/question/<int:question_id>")
def question_detail(question_id):
    question = QuestionModel.query.get(question_id)
    return render_template("detail.html", question=question)


@bp.route("/answer/<int:question_id>", methods=["POST"])
@login_required
def answer(question_id):
    form = AnswerForm(request.form)
    if form.validate():
        content = form.content.data
        answer_model = AnswerModel(content=content, author=g.user, question_id=question_id)
        db.session.add(answer_model)
        db.session.commit()
        return redirect(url_for("qa.question_detail", question_id=question_id))
    else:
        flash("验证失败!")
        return redirect(url_for("qa.question_detail", question_id=question_id))


@bp.route("/search")
def search():
    # 使用request.args.get('query')可以得到get请求中url的query的值
    query = request.args.get("query")
    # filter_by：直接使用字段的名称
    # filter：使用模型.字段名称
    # 查找标题或者内容中包含query的问答
    questions = QuestionModel.query.filter(
        or_(QuestionModel.title.contains(query),
            QuestionModel.content.contains(query))
    ).order_by(db.text("-create_time"))
    return render_template("index.html", questions=questions)
