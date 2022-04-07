from flask import Flask, render_template
app = Flask(__name__)

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


@app.route("/")
def point():
    name = "George"
    return render_template("menu.html", title="str(coord)", user_name=name)


@app.route("/start_game")
def start_game():
    global board, url
    return render_template("game_on_ready_first_step.html", url=url, help_list=board, need_to_reload="False")


@app.route("/start_game/change/<int:position>")
def change(position):
    global board, url
    board[position] = "█"
    print(position)
    app.route("../start_game")
    return render_template("game_on_ready_first_step.html", url=url, help_list=board, need_to_reload="True")


if __name__ == '__main__':
    app.run('127.0.0.1', 80)
