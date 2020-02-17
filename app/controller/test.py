from uuid import uuid1

from flask import Blueprint, render_template, request

from app.orm.models import User

test_bp = Blueprint('test_bp', __name__)


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
