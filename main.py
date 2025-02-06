import json
from flask import Flask, render_template, redirect, make_response, session
from flask import request as new_request
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from data import db_session

# from itertools import zip_longest
import sqlite3
from data.RegisterForm import RegisterForm
from requests import request
from data.users import *
from data.games import Game
from data.Login_Form import LoginForm
from data.db_session import global_init, create_session
import datetime

winner_list = []
users_game = []
users_b = {}
another_user_b = {}
app = Flask(__name__)
app.config["SECRET_KEY"] = "yandexlyceum_secret_key"
app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(days=30)
login_manager = LoginManager()
login_manager.init_app(app)


url = input(
    "input server adres, if you use ngrok: "
)  # "https://batle-ships-online.herokuapp.com/"  # input()


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/base")


@app.route("/base")
def base():
    check = check_process(2)
    if check == 0:
        pass
    else:
        return check
    return render_template("/base.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and check_password_hash(user.hashed_password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/base")
        return render_template(
            "login.html", message="Неправильный логин или пароль", form=form
        )
    return render_template("login.html", title="Авторизация", form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def point():
    return redirect("/base")


@app.route("/start_game")
@login_required
def start_game():
    check = check_process(1)
    if check == 0:
        pass
    else:
        return check
    return render_template("game_on_ready_first_step.html")


@app.route("/register", methods=["GET", "POST"])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template(
                "register.html",
                title="Регистрация",
                form=form,
                message="Пароли не совпадают",
            )
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template(
                "register.html",
                title="Регистрация",
                form=form,
                message="Такой пользователь уже есть",
            )
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect("/login")
    return render_template("register.html", title="Регистрация", form=form)


@app.route("/postmethod", methods=["POST"])
@login_required
def get_post_javascript_data():
    jsdata = json.loads(new_request.form.to_dict().popitem()[0])
    another_user_b[str(current_user.id)] = jsdata
    print(jsdata)
    print(len(jsdata))
    return f"<HTML><BODY>{type(jsdata)}: {jsdata}</BODY><HTML>"


@app.route("/new_game")
@login_required
def new_game():
    check = check_process(7)
    if check == 0:
        pass
    else:
        return check
    if str(current_user.id) in another_user_b:
        board = another_user_b[str(current_user.id)]
        del another_user_b[str(current_user.id)]
    else:
        return redirect("/")
    if len(board) != 20:
        return redirect("/")
    json_obj = {}
    # board = board.split(",")
    # i_ = iter(board)
    # board = list(zip_longest(i_, i_))
    result = []
    for y in range(10):
        res = []
        for x in range(10):
            if [x, y] in board:
                res.append("⬛")  # ⬛ это корабль
            else:
                res.append("🟦")  # 🟦 это вода
        result.append(res)
    json_obj["data"] = result
    if len(users_game) == 0:
        users_game.append(current_user.id)
        users_b[str(current_user.id)] = json_obj
        return redirect("/wait")
    else:
        user2 = users_game.pop(0)
        if user2 == current_user.id:
            print("id Совпадают")
            return "id Совпадают"
        create_game(current_user.id, user2, json_obj)
        return redirect("/battle")  # сразу активная игра


@app.route("/check")
@login_required
def need():
    return redirect("/wait")


@app.route("/wait")
@login_required
def need_wait_or_not():
    check = check_process(0)
    if check == 0:
        pass
    else:
        return check
    con = sqlite3.connect("db/users.db")
    cur = con.cursor()
    result = cur.execute(
        f"""SELECT * FROM games WHERE user_2 = {current_user.id}"""
    ).fetchall()
    if len(result) > 0:
        board = str(users_b[str(current_user.id)])
        cur.execute(
            f"""UPDATE games SET field_2 = "{str(board)}" WHERE user_2 = {current_user.id}"""
        )
        con.commit()
        cur.close()
        return redirect("/start")
    cur.close()
    return render_template("wait.html", url=url)


@app.route("/fire/<coord>")
@login_required
def fire_on_coord(coord):
    check = check_process(3)
    if check == 0:
        pass
    else:
        return check
    try:
        if len(coord.split("_")) != 2:
            return redirect("/battle")
        x = int(coord.split("_")[0])
        y = int(coord.split("_")[1])
        if x < 0 or x > 9 or y < 0 or y > 9:
            return redirect("/battle")
    except ValueError:
        return redirect("/battle")
    con = sqlite3.connect("db/users.db")
    cur = con.cursor()
    res = cur.execute(
        f"""SELECT * 
                         FROM games 
                         WHERE user_1 = {current_user.id} 
                         OR user_2 = {current_user.id}"""
    ).fetchall()
    res = res[0]
    if (current_user.id == res[1] and not res[-2]) or (
        current_user.id == res[2] and res[-2]
    ):
        return redirect("/battle")
    if res[1] == current_user.id:
        board = eval(res[4])
        new_board = board["data"]
        if new_board[y][x] == "⬛":
            new_board[y][x] = "🟥"
            need_change = False
        elif new_board[y][x] == "🟦":
            need_change = True
            new_board[y][x] = "⚪"
        else:
            return redirect("/battle")
    else:
        board = eval(res[3])
        new_board = board["data"]
        if new_board[y][x] == "⬛":
            new_board[y][x] = "🟥"
            need_change = False
        elif new_board[y][x] == "🟦":
            need_change = True
            new_board[y][x] = "⚪"
        else:
            return redirect("/battle")
    ship = list()
    min_x = 99
    max_x = -99
    min_y = 99
    max_y = -99
    ship_bloks = list()
    ship.append(new_board[y][x])
    new_x = x
    while True:
        new_x += 1
        if new_x > 9:
            max_x = 9
            break
        if new_board[y][new_x] == "⬛" or new_board[y][new_x] == "🟥":
            ship.append(tuple([y, new_x]))
            ship_bloks.append(new_board[y][new_x])
            if max_x < new_x:
                max_x = new_x
        else:
            max_x = new_x
            break
    new_x = x
    while True:
        new_x -= 1
        if new_x < 0:
            min_x = 0
            break
        if new_board[y][new_x] == "⬛" or new_board[y][new_x] == "🟥":
            ship.append(tuple([y, new_x]))
            ship_bloks.append(new_board[y][new_x])
            if min_x > new_x:
                min_x = new_x
        else:
            min_x = new_x
            break
    new_y = y
    while True:
        new_y += 1
        if new_y > 9:
            max_y = 9
            break
        if new_board[new_y][x] == "⬛" or new_board[new_y][x] == "🟥":
            ship.append(tuple([new_y, x]))
            ship_bloks.append(new_board[new_y][x])
            if max_y < new_y:
                max_y = new_y
        else:
            max_y = new_y
            break
    new_y = y
    while True:
        new_y -= 1
        if new_y < 0:
            min_y = 0
            break
        if new_board[new_y][x] == "⬛" or new_board[new_y][x] == "🟥":
            ship.append(tuple([new_y, x]))
            ship_bloks.append(new_board[new_y][x])
            if min_y > new_y:
                min_y = new_y
        else:
            min_y = new_y
            break
    if "⬛" not in ship_bloks and new_board[y][x] != "⚪":
        for i in range(max([max_y - min_y + 1, 1])):
            for e in range(max([max_x - min_x + 1, 1])):
                if new_board[min_y + i][min_x + e] == "🟦":
                    new_board[min_y + i][min_x + e] = "⚪"
    if res[1] == current_user.id:
        board["data"] = new_board
        cur.execute(
            f"""UPDATE games SET field_2 = "{str(board)}" WHERE user_1 = {current_user.id}"""
        )
        con.commit()
    else:
        board["data"] = new_board
        cur.execute(
            f"""UPDATE games SET field_1 = "{str(board)}" WHERE user_2 = {current_user.id}"""
        )
        con.commit()
    if need_change:
        if res[-2]:
            cur.execute(f"""UPDATE games SET flag = {False} WHERE id = {res[0]}""")
        else:
            cur.execute(f"""UPDATE games SET flag = {True} WHERE id = {res[0]}""")
        con.commit()
    cur.close()
    return redirect("/battle")


@app.route("/battle")
@login_required
def battle_now():
    check = check_process(4)
    if check == 0:
        pass
    else:
        return check
    someone_win = True
    alarm = False
    con = sqlite3.connect("db/users.db")
    cur = con.cursor()
    res = cur.execute(
        f"""SELECT * 
                      FROM games 
                      WHERE user_1 = {current_user.id} 
                      OR user_2 = {current_user.id}"""
    ).fetchall()
    res = res[0]
    if res[4] is None:
        return render_template("another_wait.html")
    if res[1] == current_user.id:
        if res[-2]:
            flag = 1
        else:
            flag = 0
        board = eval(res[3])
        board_another = eval(res[4])
    else:
        if res[-2]:
            flag = 0
        else:
            flag = 1
        board = eval(res[4])
        board_another = eval(res[3])
    if board is None or board_another is None:
        alarm = True
    else:
        board = board["data"]
        board_another = board_another["data"]
    board_another_for_send = []
    for i in board_another:
        help_list = []
        for e in i:
            if e == "⬛":
                someone_win = False
                help_list.append("🟦")
            else:
                help_list.append(e)
        board_another_for_send.append(help_list)
    if someone_win:
        if current_user.id == res[1]:  # добавить победу
            cur.execute(f"""UPDATE games SET flag_win = {1} WHERE id = {res[0]}""")
        else:
            cur.execute(f"""UPDATE games SET flag_win = {2} WHERE id = {res[0]}""")
        con.commit()
        cur.close()
        return redirect("/win")
    cur.close()
    return render_template(
        "active_game.html",
        user_board=board,
        another_user_board=board_another_for_send,
        flag=flag,
        alarm=alarm,
    )


@app.route("/win")
@login_required
def win_check():
    con = sqlite3.connect("db/users.db")
    cur = con.cursor()
    res = cur.execute(
        f"""SELECT * 
                          FROM games 
                          WHERE user_1 = {current_user.id} 
                          OR user_2 = {current_user.id}"""
    ).fetchall()
    if len(res) == 0:
        return redirect("/base")
    res = res[0]
    if res[-1] == 0:
        return redirect("/battle")
    else:
        if (current_user.id == res[1] and res[-1] == 1) or (
            current_user.id == res[2] and res[-1] == 2
        ):
            user_id_who_win = current_user.id
        else:
            return redirect("/lose")
    cur.execute(
        f"""UPDATE users SET game_wins = {current_user.game_wins + 1} WHERE id = {user_id_who_win}"""
    )
    con.commit()
    con.close()
    return render_template("win.html")


@app.route("/lose")
@login_required
def lose_check():
    con = sqlite3.connect("db/users.db")
    cur = con.cursor()
    res = cur.execute(
        f"""SELECT * 
                          FROM games 
                          WHERE user_1 = {current_user.id} 
                          OR user_2 = {current_user.id}"""
    ).fetchall()
    if len(res) == 0:
        return redirect("/base")
    res = res[0]
    if res[-1] == 0:
        return redirect("/battle")
    else:
        if (current_user.id == res[1] and res[-1] == 2) or (
            current_user.id == res[2] and res[-1] == 1
        ):
            user_id_who_lose = current_user.id
        else:
            return redirect("/win")
    cur.execute(
        f"""UPDATE users SET game_loses = {current_user.game_loses + 1} WHERE id = {user_id_who_lose}"""
    )
    con.commit()
    end_game(res[0])
    con.close()
    return render_template("lose.html")


@app.route("/check_new")
@login_required
def check_try():
    check = check_process(6)
    if check == 0:
        pass
    else:
        return check
    con = sqlite3.connect("db/users.db")
    cur = con.cursor()
    res = cur.execute(
        f"""SELECT * 
                          FROM games 
                          WHERE user_1 = {current_user.id} 
                          OR user_2 = {current_user.id}"""
    ).fetchall()
    res = res[0]
    if res[-1] != 0:  # добавить поражение
        return redirect("/lose")
    return redirect("/battle")


@app.route("/afk_alarm")
@login_required
def afk():
    check = check_process(8)
    if check == 0:
        pass
    else:
        return check
    con = sqlite3.connect("db/users.db")
    cur = con.cursor()
    res = cur.execute(
        f"""SELECT * 
                      FROM games 
                      WHERE user_1 = {current_user.id} 
                      OR user_2 = {current_user.id}"""
    ).fetchall()
    res = res[0]
    if current_user.id == res[1]:
        cur.execute(
            f"""UPDATE games
                    SET flag_win = {2} WHERE id = {res[0]}"""
        )
        winner_list.append(res[2])
    else:
        cur.execute(
            f"""UPDATE games
                    SET flag_win = {1} WHERE id = {res[0]}"""
        )
        winner_list.append(res[1])
    cur.execute(
        f"""UPDATE users SET game_loses = {current_user.game_loses + 1} WHERE id = {current_user.id}"""
    )
    con.commit()
    end_game(res[0])
    con.close()
    return render_template("afk_info.html")


@app.route("/start")
@login_required
def go():
    check = check_process(5)
    if check == 0:
        pass
    else:
        return check
    con = sqlite3.connect("db/users.db")
    cur = con.cursor()
    res = cur.execute(
        f"""SELECT field_1 FROM games WHERE user_2 = {current_user.id}"""
    ).fetchall()
    result = eval(res[0][0])
    board = users_b[str(current_user.id)]
    del users_b[str(current_user.id)]
    cur.close()
    result = result["data"]
    board = board["data"]
    board_another_for_send = []
    for i in result:
        help_list = []
        for e in i:
            if e == "⬛":
                help_list.append("🟦")
            else:
                help_list.append(e)
        board_another_for_send.append(help_list)
    return render_template(
        "active_game.html",
        user_board=board,
        another_user_board=board_another_for_send,
        flag=0,
        alarm=False,
    )


def create_game(user1, user2, board_1):
    db_sess = create_session()
    game = Game(
        user_1=int(user1),
        user_2=int(user2),
        field_1=str(board_1),
    )
    db_sess.add(game)
    db_sess.commit()


def end_game(id_game):
    con = sqlite3.connect("db/users.db")
    cur = con.cursor()
    try:
        cur.execute(f"""DELETE FROM games WHERE id == {id_game}""")
        con.commit()
    except sqlite3.OperationalError:
        print(f"Нет игры с id {id_game}")
    cur.close()


def check_process(type_of_key):
    con = sqlite3.connect("db/users.db")
    cur = con.cursor()
    try:
        res = cur.execute(
            f"""SELECT * 
                          FROM games WHERE user_1 = {current_user.id} OR user_2 = {current_user.id}"""
        ).fetchall()
        if len(res) == 0:
            res = []
        else:
            res = res[0]
    except AttributeError:
        res = []
    if type_of_key == 0:
        if str(current_user.id) in users_b and len(res) == 0:
            return 0
        elif str(current_user.id) not in users_b and len(res) == 0:
            return redirect("/")
        else:
            if res[4] is None:
                return 0
            return redirect("/battle")
    elif type_of_key == 1:
        if str(current_user.id) in users_b:
            return redirect("/wait")
        if len(res) != 0 and res[4] is not None:
            return redirect("/battle")
        return 0
    elif type_of_key == 2:
        try:
            if len(res) == 0 and str(current_user.id) not in users_b:
                return 0
            elif str(current_user.id) in users_b:
                return redirect("/wait")
            else:
                return redirect("/battle")
        except AttributeError:
            return 0
    elif type_of_key == 3:
        if current_user.id in winner_list:
            winner_list.remove(current_user.id)
            cur.execute(
                f"""UPDATE users SET game_wins = {current_user.game_wins + 1} WHERE id = {current_user.id}"""
            )
            con.commit()
            con.close()
            return render_template("win.html")
        if len(res) == 0 or str(current_user.id) in users_b:
            if str(current_user.id) in users_b:
                return redirect("/wait")
            return redirect("/")
        if (current_user.id == res[1] and res[-2]) or (
            current_user.id == res[2] and not res[-2]
        ):
            return 0
        else:
            return redirect("/battle")
    elif type_of_key == 4:
        if len(res) == 0:
            if str(current_user.id) in users_b:
                return redirect("/wait")
            return redirect("/")
        return 0
    elif type_of_key == 5:
        if len(res) == 0:
            return redirect("/")
        if str(current_user.id) not in users_b:
            return redirect("/battle")
        return 0
    elif type_of_key == 6:
        if current_user.id in winner_list:
            winner_list.remove(current_user.id)
            cur.execute(
                f"""UPDATE users SET game_wins = {current_user.game_wins + 1} WHERE id = {current_user.id}"""
            )
            con.commit()
            con.close()
            return render_template("win.html")
        if len(res) == 0:
            return redirect("/")
        return 0
    elif type_of_key == 7:
        if str(current_user.id) in users_b:
            return redirect("/wait")
        if len(res) != 0:
            return redirect("/battle")
        return 0
    elif type_of_key == 8:
        if len(res) == 0:
            return redirect("/")
        if str(current_user.id) in users_b:
            return redirect("/wait")
        return 0


def clear_games_table():
    con = sqlite3.connect("db/users.db")
    cur = con.cursor()
    cur.execute("""DELETE FROM games""")
    con.commit()
    cur.close()


if __name__ == "__main__":
    global_init("db/users.db")
    clear_games_table()  # могут возникать ошибки, если не почистить таблицу
    # port = int(os.environ.get("PORT", 80))
    # app.run(host='0.0.0.0', port=port)
    app.run("127.0.0.1", 80)
