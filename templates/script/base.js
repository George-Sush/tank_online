alert("js агружен");
var ship_size = 1;
var flag = false;
const board = [];
function repeat_stuff()
{
    for (var y = 0; y < 10; y++) {
        for (var x = 0; x < 10; x++){
            document.write('<button onclick="put('+x+','+y+')", id="'+x+'_'+y+'";">🟦</button>');
        }
        document.write('<br/>');
    }
    document.write('<br/>');
    document.write('<button onclick="rotate_ship()", id="rotate";">🢂</button>');
    document.write('<button onclick="set_ship_size(4);">⬛⬛⬛⬛</button>');
    document.write('<button onclick="set_ship_size(3);">⬛⬛⬛</button>');
    document.write('<button onclick="set_ship_size(2);">⬛⬛</button>');
    document.write('<button onclick="set_ship_size(1);">⬛</button>');
    document.write('<button onclick="complete();">complete</button>');
}
function put(x, y)
{
    board.push([x, y]);
    alert(x + ', ' + y);
}
function rotate_ship()
{
    if (flag==false) {
    flag = true;
    alert("Повернули корабль, теперь он вертикальный");
    document.getElementById("rotate").innerHTML='🢃';
    } else {
    flag = false;
    alert("Повернули корабль, теперь он горизонтальный");
    document.getElementById("rotate").innerHTML='🢂';
    }
}
function set_ship_size(size) {
    ship_size = size;
    alert("Корабль длины " + size);
}
function complete() {
    alert(board);
}
repeat_stuff();