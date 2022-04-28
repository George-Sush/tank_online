import json
from flask import Flask, render_template, redirect, make_response, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from itertools import zip_longest
import sqlite3
from data.RegisterForm import RegisterForm
from requests import request
import os
from data.users import *
from data.games import Game
from data.Login_Form import LoginForm
from data.db_session import global_init, create_session
import datetime
users_game = []
users_b = {}
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
    # print(current_user)
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


@app.route("/new_game/<board>")
@login_required
def new_game(board):
    json_obj = {}
    board = board.split(",")
    # print(len(board))
    i_ = iter(board)
    board = list(zip_longest(i_, i_))
    # print(board)
    result = []
    for y in range(10):
        res = []
        for x in range(10):
            if tuple([str(x), str(y)]) in board:
                res.append("⬛")  # ⬛ это корабль
            else:
                res.append("🟦")  # 🟦 это вода
        result.append(res)
    # print(result)
    json_obj["data"] = result
    if len(users_game) == 0:
        users_game.append(current_user.id)
        # print(current_user.id)
        users_b[str(current_user.id)] = json_obj  # result
        return redirect("/wait")  # "wait.html")
    else:
        user2 = users_game.pop(0)
        if user2 == current_user.id:
            print("id Совпадают")
            return "id Совпадают"
        # print(user2, current_user.id)
        create_game(current_user.id, user2, json_obj)  # result
        return redirect("/battle")  # сразу активная игра


@app.route("/check")
@login_required
def need():
    return redirect("/wait")


@app.route("/wait")
@login_required
def need_wait_or_not():
    con = sqlite3.connect("db/users.db")
    cur = con.cursor()
    result = cur.execute(f"""SELECT * FROM games WHERE user_2 = {current_user.id}""").fetchall()
    if len(result) > 0:
        # print(str(users_b[str(current_user.id)]))
        board = str(users_b[str(current_user.id)])
        # print(board)
        cur.execute(f"""UPDATE games SET field_2 = "{str(board)}" WHERE user_2 = {current_user.id}""")
        con.commit()
        # res = cur.execute(f"""SELECT field_1 FROM games WHERE user_2 = {current_user.id}""").fetchall()
        # print(res[0][0])
        # result = eval(res[0][0])
        # print(result)
        cur.close()
        return redirect("/start")

    cur.close()
    return render_template("wait.html", url=url)


@app.route("/fire/<coord>")
@login_required
def fire_on_coord(coord):
    x = int(coord.split("_")[0])
    y = int(coord.split("_")[1])
    con = sqlite3.connect("db/users.db")
    cur = con.cursor()
    res = cur.execute(f"""SELECT * 
                         FROM games 
                         WHERE user_1 = {current_user.id} 
                         OR user_2 = {current_user.id}""").fetchall()
    res = res[0]
    if res[1] == current_user.id:
        board = eval(res[4])
        new_board = board["data"]
        if new_board[y][x] == "⬛":
            new_board[y][x] = "🟥"
        elif new_board[y][x] == "🟦":
            new_board[y][x] = "⚪"
        else:
            return "Ошибка"
        board["data"] = new_board
        cur.execute(f"""UPDATE games SET field_2 = "{str(board)}" WHERE user_1 = {current_user.id}""")
        con.commit()
    else:
        board = eval(res[3])
        new_board = board["data"]
        if new_board[y][x] == "⬛":
            new_board[y][x] = "🟥"
        elif new_board[y][x] == "🟦":
            new_board[y][x] = "⚪"
        else:
            return "Ошибка"
        board["data"] = new_board
        cur.execute(f"""UPDATE games SET field_1 = "{str(board)}" WHERE user_2 = {current_user.id}""")
        con.commit()
    if res[-1]:
        cur.execute(f"""UPDATE games SET flag = {False} WHERE id = {res[0]}""")
    else:
        cur.execute(f"""UPDATE games SET flag = {True} WHERE id = {res[0]}""")
    cur.close()
    return redirect("/battle")


@app.route("/battle")
@login_required
def battle_now():
    alarm = False
    con = sqlite3.connect("db/users.db")
    cur = con.cursor()
    res = cur.execute(f"""SELECT * 
                      FROM games 
                      WHERE user_1 = {current_user.id} 
                      OR user_2 = {current_user.id}""").fetchall()
    res = res[0]
    print(res)
    if res[4] is None:
        return render_template("another_wait.html")
    if res[1] == current_user.id:
        if res[-1]:
            flag = True
        else:
            flag = False
        board = eval(res[3])
        board_another = eval(res[4])
    else:
        if res[-1]:
            flag = False
        else:
            flag = True
        board = eval(res[4])
        board_another = eval(res[3])
    if board is None or board_another is None:
        alarm = True
    else:
        board = board["data"]
        board_another = board_another["data"]
    print("Тут пользователь не ждал")
    print(type(board), board)
    print(type(board_another), board_another)
    return render_template("active_game.html", user_board=board, another_user_board=board_another, flag=flag,
                           alarm=alarm)


@app.route("/alarm")
@login_required
def alarm_try():
    return redirect("/battle")


@app.route("/start")
@login_required
def go():
    con = sqlite3.connect("db/users.db")
    cur = con.cursor()
    res = cur.execute(f"""SELECT field_1 FROM games WHERE user_2 = {current_user.id}""").fetchall()
    result = eval(res[0][0])
    board = users_b[str(current_user.id)]
    cur.close()
    print("Тут старт пользователя, который ждал")
    result = result["data"]
    board = board["data"]
    print(type(result), result)
    print(type(board), board)

    return render_template("active_game.html", user_board=board, another_user_board=result, flag=False,
                           alarm=False)


def create_game(user1, user2, board_1):
    db_sess = create_session()
    game = Game(
        user_1=int(user1),
        user_2=int(user2),
        field_1=str(board_1),
    )
    db_sess.add(game)
    db_sess.commit()


def end_game(id):
    con = sqlite3.connect("db/users.db")
    cur = con.cursor()
    try:
        cur.execute(f"""DELETE FROM games WHERE id == {id}""")
        con.commit()
    except Exception:
        print(f"Нет игры с id {id}")
    cur.close()


def clear_games_table():
    con = sqlite3.connect("db/users.db")
    cur = con.cursor()
    cur.execute("""DELETE FROM games""")
    con.commit()
    cur.close()


if __name__ == '__main__':
    global_init("db/users.db")
    clear_games_table()  # могут возникать ошибки, если не почистить таблицу
    # port = int(os.environ.get("PORT", 80))
    # app.run(host='0.0.0.0', port=port)
    app.run('127.0.0.1', 80)
