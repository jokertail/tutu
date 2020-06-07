from uuid import uuid1

from flask import Blueprint, render_template, request, session, url_for
from werkzeug.utils import redirect

from app.orm.models import User

test_bp = Blueprint('test_bp', __name__)


@test_bp.route('/test/session1')
def test_session():
    session['test'] = request.args.get('aaa')
    return "1 finished!"


@test_bp.route('/test/session2')
def test_session2():
    return session['test']


@test_bp.route('/test/url_for_1')
def test_url_for_1():
    return request.args.get("hehe")


@test_bp.route('/test/url_for_2')
def test_url_for_2():
    return redirect(url_for("test_bp.test_url_for_1", hehe="ssssssss"))


@test_bp.route('/test/testList')
def test_list():
    tem_list = [i for i in range(10)]
    return render_template('test.html', test_list=tem_list)


@test_bp.route('/test/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        telephone = request.form.get('telephone')
        print(request.form)

        user = User()
        user.username = username
        user.password = password
        user.email = email
        user.telephone = telephone
        user.uid = uuid1().__str__()

        print(user.uid)
        print(type(user.uid))
        print(username, password)
        return "hahahha"



@test_bp.route('/test/labels')
def test_labels():
    return render_template('labels.html')