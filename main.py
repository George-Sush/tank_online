from flask import Flask, render_template, redirect, make_response, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
import sqlite3
from data.RegisterForm import RegisterForm
from requests import request
import os
from data.users import *
# from data.games import Game
from data.Login_Form import LoginForm
from data.db_session import global_init, create_session
import datetime
users_game = []
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=30
)
login_manager = LoginManager()
login_manager.init_app(app)


url = input("input server adres: ")  # "https://batle-ships-online.herokuapp.com/"  # input()


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/base")


@app.route('/base')
def base():
    print(current_user)
    return render_template("/base.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and check_password_hash(user.hashed_password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/base")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def point():
    # name = "George"
    return redirect("/base")  # render_template("menu.html", title="str(coord)", user_name=name)


@app.route("/start_game")
@login_required
def start_game():
    global url
    return render_template("game_on_ready_first_step.html", url=url)


# @app.route("/start_game/change/<int:position>")
# @login_required
# def change(position):
#     global url
#     # board[position] = "█"
#     app.route("../start_game")
#     return render_template("game_on_ready_first_step.html", url=url, need_to_reload="True")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route("/cookie_test")
def cookie_test():
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count:
        res = make_response(
            f"Вы пришли на эту страницу {visits_count + 1} раз")
        res.set_cookie("visits_count", str(visits_count + 1),
                       max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response(
            "Вы пришли на эту страницу в первый раз за последние 2 года")
        res.set_cookie("visits_count", '1',
                       max_age=60 * 60 * 24 * 365 * 2)
    return res


@app.route("/session_test")
def session_test():
    visits_count = session.get('visits_count', 0)
    session['visits_count'] = visits_count + 1
    return make_response(
        f"Вы пришли на эту страницу {visits_count + 1} раз")


# @app.route("/search_game")
# def new_game(user1):
#     con = sqlite3.connect("db/users.db")
#     cur = con.cursor()
#     result = cur.execute(f"""SELECT id FROM users
#                 WHERE game_status == True AND id != {user1}""").fetchall()
#     if len(result) == 0:
#         print("Игроков нет, ждите")
#     else:
#         user2
#     session = create_session()
#     game = Game(
#         users=f"{user1},{user2}"
#     )


@app.route("/search")
@login_required
def what_to_do():
    return render_template("search.html")


@app.route("/new_game")
@login_required
def new_game():
    if len(users_game) == 0:
        users_game.append(current_user.id)
        return render_template("wait.html")
    else:
        user2 = users_game.pop(0)
        res = create_game(current_user.id, user2)
        return render_template("game_on_ready_second_step.html", message=res) # сразу активная игра


def create_game(user1, user2):
    return f"{user1},{user2}"


if __name__ == '__main__':
    global_init("db/users.db")
    # add_new_user() обавление пользователя со значением имя(уникальное), почта(уникальное), пароль.
    # В базе данных есть тестовый пользователь
    # port = int(os.environ.get("PORT", 80))
    # app.run(host='0.0.0.0', port=port)
    app.run('127.0.0.1', 80)
