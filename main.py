from flask import Flask, render_template, redirect
from flask_login import LoginManager
import sqlite3
import json

from werkzeug.security import generate_password_hash, check_password_hash

from data import db_session
from data.RegisterForm import RegisterForm
from data.user import User
from data.Login_Form import LoginForm
from data.db_session import global_init, create_session
from flask_login import login_user, login_required, logout_user
app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)


url = input("input server adres:")
board = ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O',
         'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O',
         'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O',
         'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O',
         'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O',
         'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O',
         'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O',
         'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O',
         'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O',
         'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/base")


@app.route('/base')
def base():
    return render_template("/base.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.hashed_password == form.password.data:
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
@login_required
def point():
    name = "George"
    return render_template("menu.html", title="str(coord)", user_name=name)


@app.route("/start_game")
@login_required
def start_game():
    global board, url
    return render_template("game_on_ready_first_step.html", url=url, help_list=board, need_to_reload="False")


@app.route("/start_game/change/<int:position>")
@login_required
def change(position):
    global board, url
    board[position] = "█"
    print(position)
    app.route("../start_game")
    return render_template("game_on_ready_first_step.html", url=url, help_list=board, need_to_reload="True")


# def add_new_user(name="test_user", email="test@test.test", hashed_password="test123"):
#     user = User()
#     session = create_session()
#
#     user.name = name
#     user.email = email
#     user.hashed_password = hashed_password
#
#     try:
#         session.add(user)
#         session.commit()
#     except sqlite3.IntegrityError:
#         return render_template("register.html", message="Неправильный логин или пароль")
#
#
#     con = sqlite3.connect("db/users.db")
#     cur = con.cursor()
#     result = cur.execute(f"""SELECT id FROM users WHERE name == '{name}'""").fetchall()
#     with open("db/boards.json", "r") as read_file:
#         file = json.load(read_file)
#         read_file.close()
#     with open("db/boards.json", "w") as write_file:
#         board_copy = board.copy()
#         file[str(result[0][0])] = [board_copy, None]
#         json.dump(file, write_file)
#         write_file.close()


def set_password(self, password):
    self.hashed_password = generate_password_hash(password)


def check_password(self, password):
    return check_password_hash(self.hashed_password, password)

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
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


if __name__ == '__main__':
    global_init("db/users.db")
    # add_new_user() обавление пользователя со значением имя(уникальное), почта(уникальное), пароль.
    # В базе данных есть тестовый пользователь
    app.run('127.0.0.1', 80)
