from datetime import datetime
from uuid import uuid1

from flask import Blueprint, render_template, flash, request, url_for, session
from flask_login import current_user
from werkzeug.utils import redirect

from app.orm.db import db
from app.orm.models import Paper, ConferenceDict, Role, Label, User

bp = Blueprint('bp', __name__)


@bp.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('main.html')
    return render_template('index.html')


@bp.route('/createDB')
def create_db():
    db.create_all()
    confer_name_list = [
        "会议一",
        "会议二",
        "会议三",
        "会议四",
        "会议五",
        "会议六",
        "其他"
    ]

    role_name_list = [
        "USER",
        "ADMIN"
    ]

    for confer_name in confer_name_list:
        c = ConferenceDict()
        c.name = confer_name
        c.id = uuid1().__str__()
        db.session.add(c)

    for role_name in role_name_list:
        r = Role()
        r.rid = uuid1().__str__()
        r.rolename = role_name
        db.session.add(r)

    db.session.commit()
    return "create success"


@bp.route('/dropDB')
def drop_db():
    db.drop_all()
    return "drop success"


@bp.route('/user_main')
def user_main():
    uid = current_user.uid
    paper_list = Paper.query.all()

    papers = [{
        "pid": p.pid,
        "uid": p.uid,
        "name": p.title,
        "year": p.year,
        "conference": p.conference
    } for p in paper_list]
    return render_template('user_main.html', papers=papers)


@bp.route('/my_papers')
def my_papers():
    uid = current_user.uid
    paper_list = Paper.query.filter_by(uid=uid).all()

    papers = [{
        "pid": p.pid,
        "uid": p.uid,
        "name": p.title,
        "year": p.year,
        "conference": p.conference
    } for p in paper_list]
    return render_template('my_papers.html', papers=papers)


def check_paper_form(req):
    error_code = 0
    if req.form.get('title') == "":
        flash("论文标题不能为空", "error")
        error_code += 1
    if req.form.get('summary') == "":
        flash("摘要不能为空", "error")
        error_code += 1
    if req.form.get('conference') == "":
        flash("会议名称不能为空", "error")
        error_code += 1
    if req.form.get('url') == "":
        flash("文章链接不能为空", "error")
        error_code += 1
    return error_code


@bp.route('/paper_add', methods=['GET', 'POST'])
def add_paper():
    conferences = ConferenceDict.query.order_by(ConferenceDict.id)
    conference_list = [c.name for c in conferences]

    if request.method == 'GET':
        return render_template('paper_add.html', paper=None, conference_list=conference_list)

    if request.method == 'POST':
        error_code = check_paper_form(request)
        if error_code > 0:
            return render_template('paper_add.html', paper=None, conference_list=conference_list)

        new_paper = Paper()
        new_paper.uid = current_user.uid
        new_paper.pid = uuid1().__str__()
        new_paper.time = datetime.now()
        new_paper.conference = request.form.get('conference')
        new_paper.year = request.form.get('year')
        new_paper.title = request.form.get('title')
        new_paper.summary = request.form.get('summary')
        new_paper.url = request.form.get('url')
        db.session.add(new_paper)
        db.session.commit()
        flash("论文添加成功！", "success")
        return redirect(url_for("bp.my_papers"))


@bp.route('/paper_edit', methods=['GET', 'POST'])
def edit_paper():
    conferences = ConferenceDict.query.order_by(ConferenceDict.id)
    conference_list = [c.name for c in conferences]

    if request.method == 'GET':
        pid = request.args.get('pid')
        paper = Paper.query.filter_by(pid=pid).first()
        # 意外错误, 更新的 paper 不存在
        if paper is None:
            flash("论文不存在！", "error")
            return redirect(url_for("bp.my_papers"))

        paper_html = {
            "pid": paper.pid,
            "title": paper.title,
            "summary": paper.summary,
            "year": paper.year,
            "conference": paper.conference,
            "url": paper.url
        }
        return render_template('paper_edit.html', paper=paper_html, conference_list=conference_list)

    if request.method == 'POST':
        pid = request.form.get('pid')
        update_paper = Paper.query.filter_by(pid=pid).first()
        # 意外错误, 更新的 paper 不存在
        if update_paper is None:
            flash("未知错误, 更新的论文不存在, 保存失败!", "error")
            return redirect(url_for("bp.my_papers"))
        paper_html = {
            "pid": update_paper.pid,
            "title": update_paper.title,
            "summary": update_paper.summary,
            "year": update_paper.year,
            "conference": update_paper.conference,
            "url": update_paper.url
        }
        error_code = check_paper_form(request)
        if error_code > 0:
            return render_template('paper_edit.html', paper=paper_html, conference_list=conference_list)

        update_paper.conference = request.form.get('conference')
        update_paper.year = request.form.get('year')
        update_paper.title = request.form.get('title')
        update_paper.summary = request.form.get('summary')
        update_paper.url = request.form.get('url')
        update_paper.time = datetime.now()

        db.session.commit()

        flash("保存成功！", "success")
        return redirect(url_for("bp.my_papers"))


def load_paper(pid):
    if pid is None:
        flash("请求错误, 缺少论文 id", "error")
        return None

    paper = Paper.query.filter_by(pid=pid).first()
    if paper is None:
        flash("未知错误, 论文不存在!", "error")
        return None
    return paper


@bp.route('/label_list')
def label_list():
    pid = request.args.get('pid')

    paper = load_paper(pid)
    if paper is None:
        return redirect(url_for("bp.user_main"))

    session['pid'] = pid
    user = User.query.filter_by(uid=paper.uid).first()
    paper_html = {
        "pid": paper.pid,
        "title": paper.title,
        "conference": paper.conference,
        "summary": paper.summary,
        "time": paper.time.strftime('%Y-%m-%d'),
        "year": paper.year,
        "url": paper.url,
        "uploader_name": user.name,
        "uploader_tele": user.telephone,
        "uploader_email": user.email
    }

    label_all = Label.query.filter_by(pid=pid).all()
    labels = []

    for l in label_all:
        name = User.query.filter_by(uid=l.uid).first().name
        time = l.time.strftime('%Y-%m-%d')
        info = l.info
        labels.append({
            "lid": l.lid,
            "uid": l.uid,
            "pid": pid,
            "name": name,
            "time": time,
            "info": info
        })

    return render_template("labels.html", labels=labels, paper=paper_html)


@bp.route('/my_labels')
def my_labels():
    uid = current_user.uid
    pid = request.args.get('pid')

    paper = load_paper(pid)
    if paper is None:
        return redirect(url_for("bp.user_main"))

    session['pid'] = pid
    user = User.query.filter_by(uid=paper.uid).first()
    paper_html = {
        "pid": paper.pid,
        "title": paper.title,
        "conference": paper.conference,
        "summary": paper.summary,
        "time": paper.time.strftime('%Y-%m-%d'),
        "year": paper.year,
        "url": paper.url,
        "uploader_name": user.name,
        "uploader_tele": user.telephone,
        "uploader_email": user.email
    }

    label_all = Label.query.filter_by(pid=pid, uid=uid).all()
    labels = []

    for l in label_all:
        name = User.query.filter_by(uid=l.uid).first().name
        time = l.time.strftime('%Y-%m-%d')
        info = l.info
        labels.append({
            "lid": l.lid,
            "uid": l.uid,
            "pid": pid,
            "name": name,
            "time": time,
            "info": info
        })

    return render_template("labels.html", labels=labels, paper=paper_html)


def check_label_form(req):
    error_code = 0
    if req.form.get('info') == "":
        flash("标注信息不能为空！", "error")
        error_code += 1
    return error_code


@bp.route('/label_add', methods=['GET', 'POST'])
def label_add():
    if request.method == 'GET':
        pid = request.args.get('pid')
        paper = load_paper(pid)
        if paper is None:
            return redirect(url_for("bp.user_main"))

        label_html = {
            "pid": pid,
            "paper_title": paper.title,
            "paper_url": paper.url
        }

        session['pid'] = pid

        return render_template("label_add.html", label=label_html)

    if request.method == 'POST':
        pid = session['pid']
        paper = load_paper(pid)
        if paper is None:
            return redirect(url_for("bp.user_main"))

        label_html = {
            "pid": pid,
            "paper_title": paper.title,
            "paper_url": paper.url
        }
        error_code = check_label_form(request)
        if error_code > 0:
            return render_template("label_add.html", label=label_html)

        new_label = Label()
        new_label.lid = uuid1().__str__()
        new_label.pid = pid
        new_label.uid = current_user.uid
        new_label.time = datetime.now()
        new_label.info = request.form.get('info')
        db.session.add(new_label)
        db.session.commit()
        flash("标注添加成功!", "success")
        return redirect(url_for("bp.my_labels", pid=pid))


def load_label(lid):
    if lid is None:
        flash("请求错误, 缺少标注 id", "error")
        return None
    label = Label.query.filter_by(lid=lid).first()
    if label is None:
        flash("未知错误, 标注不存在!", "error")
        return None
    return label


@bp.route('/label_edit', methods=['GET', 'POSt'])
def label_edit():
    if request.method == 'GET':
        lid = request.args.get('lid')
        label = load_label(lid)
        if label is None:
            return redirect(url_for("bp.my_labels", pid=session['pid']))

        paper = load_paper(label.pid)
        session['pid'] = label.pid
        session['lid'] = lid
        label_html = {
            "pid": label.pid,
            "info": label.info,
            "paper_title": paper.title,
            "paper_url": paper.url
        }
        return render_template("label_edit.html", label=label_html)

    if request.method == 'POST':
        pid = session['pid']
        lid = session['lid']
        paper = load_paper(pid)
        if paper is None:
            return redirect(url_for("bp.user_main"))

        label = load_label(lid)
        if label is None:
            return redirect(url_for("bp.my_labels", pid=pid))

        label_html = {
            "pid": label.pid,
            "info": label.info,
            "paper_title": paper.title,
            "paper_url": paper.url
        }
        error_code = check_label_form(request)
        if error_code > 0:
            return render_template("label_edit.html", label=label_html)

        label.info = request.form.get('info')
        label.time = datetime.now()
        db.session.commit()
        return redirect(url_for("bp.my_labels", pid=pid))
