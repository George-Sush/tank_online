from flask import Flask, render_template
app = Flask(__name__)

coord = (0, 0)


@app.route("/")
def point():
    return render_template("base.html", title=str(coord))


@app.route("/up")
def up_go():
    global coord
    coord = (coord[0], coord[1] + 1)
    res = str(coord)
    return render_template("base.html", title=res)


@app.route("/down")
def down_go():
    global coord
    coord = (coord[0], coord[1] - 1)
    res = str(coord)
    return render_template("base.html", title=res)


@app.route("/right")
def right_go():
    global coord
    coord = (coord[0] + 1, coord[1])
    res = str(coord)
    return render_template("base.html", title=res)


@app.route("/left")
def left_go():
    global coord
    coord = (coord[0] - 1, coord[1])
    res = str(coord)
    return render_template("base.html", title=res)


if __name__ == '__main__':
    app.run('127.0.0.1', 80)
