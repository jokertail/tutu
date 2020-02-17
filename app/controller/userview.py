from urllib.parse import urlparse, urljoin
from uuid import uuid1

from flask import Blueprint, request, render_template, flash, url_for, redirect, abort
from flask_login import login_user

from app.orm.models import User

user_bp = Blueprint('user_bp', __name__)


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


@user_bp.route('/user/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if not user:
            flash("用户不存在，请先注册", "error")
            return redirect(url_for('user_bp.login'))

        if user.password != password:
            flash("密码错误", "error")
            return redirect(url_for('user_bp.login'))

        login_user(user)
        flash("登录成功", "success")

        next_url = request.args.get('next')
        if not is_safe_url(next_url):
            return abort(400)

        return redirect(next_url or url_for('bp.index'))


@user_bp.route('/user/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        telephone = request.form.get('telephone')

        user = User()
        user.username = username
        user.password = password
        user.email = email
        user.telephone = telephone
        user.uid = uuid1().__str__()

        # db.session.add(user)
        # db.session.commit()

        flash("photo upload error", "error")

        return redirect(url_for('bp.index'))
